#!/usr/bin/env python3
"""
Fast FD (Power) + stdDVARS using AFNI for tasks: arrow(1..6) and collector(1..4)

What it runs per run:
  1) 3dTstat -mean -> mean image (fast)
  2) 3dAutomask on mean -> mask
  3) 3dvolreg -1Dfile -> motion.1D (no output dataset)
  4) 3dTto1D -dvar -> raw DVARS (masked)
Then:
  - FD (Power): sum(|Δtrans|) + R * sum(|Δrot_rad|), R=head radius (default 50 mm)
  - stdDVARS: robust z = (DVARS - median) / (MAD*1.4826)
  - Pad leading 0 so length == N_TR

Printed metrics per run, task, and overall:
  A) FD>fd_thr & stdDVARS<z_thr
  B) FD>fd_thr & stdDVARS>z_thr
  C) FD>fd_thr
  D) stdDVARS>z_thr
  E) FD>fd_thr OR stdDVARS>z_thr
"""

from __future__ import annotations
import argparse, os, sys, time
from pathlib import Path
import subprocess
import numpy as np

# ---- make prints unbuffered so SLURM .out fills during run ----
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass
print_flush = lambda *a, **k: print(*a, flush=True, **k)

# ------------------------- subprocess helper ------------------------- #
def run(cmd: list[str]) -> None:
    """Run a command; stream output to stdout/stderr (so SLURM captures it)."""
    subprocess.run(cmd, check=True)

def afni_exists() -> None:
    for tool in ("3dTstat", "3dAutomask", "3dvolreg", "3dTto1D"):
        if not shutil.which(tool):
            raise RuntimeError(f"Required AFNI tool not found in PATH: {tool}")

# ------------------------- core helpers ------------------------- #
def pad_to_ntr(x: np.ndarray, ntr: int) -> np.ndarray:
    x = np.array(x).ravel() if x is not None else np.array([])
    x = np.insert(x, 0, 0.0)
    if x.size >= ntr:
        return x[:ntr]
    return np.pad(x, (0, ntr - x.size), mode="constant")

def robust_z(x: np.ndarray) -> np.ndarray:
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    scale = mad * 1.4826 if mad > 0 else (np.std(x) if np.std(x) > 0 else 1.0)
    return (x - med) / scale

def load_1d(path: Path) -> np.ndarray:
    if path.exists() and os.path.getsize(path) > 0:
        return np.loadtxt(path)
    return np.array([])

def compute_fd_power_from_motion_1d(motion: np.ndarray, head_radius_mm: float) -> np.ndarray:
    """
    motion shape: (T,6) from AFNI 3dvolreg: [roll pitch yaw dS dL dP]
      rotations are in DEGREES; translations (mm).
    FD_power[t] = sum(|Δtrans|) + R * sum(|Δrot(rad)|)
    """
    if motion.size == 0:
        return np.array([])
    motion = np.atleast_2d(motion)
    if motion.shape[1] < 6:
        raise ValueError("motion.1D does not have 6 columns")
    # columns: roll pitch yaw (deg) then 3 translations (mm)
    rot_deg = motion[:, 0:3]
    trans_mm = motion[:, 3:6]
    # diffs (t - t-1), pad with zeros at start later
    drot_deg = np.diff(rot_deg, axis=0)
    dtrans_mm = np.diff(trans_mm, axis=0)
    # convert degrees -> radians
    drot_rad = np.deg2rad(drot_deg)
    # Power FD: L1 norm of diffs
    fd = np.sum(np.abs(dtrans_mm), axis=1) + head_radius_mm * np.sum(np.abs(drot_rad), axis=1)
    return fd

# ------------------------- per-run processing ------------------------- #
def process_run(bold: Path, fd_thr: float, z_thr: float, head_radius: float, tmp_suffix: str) -> dict:
    """
    Returns: dict with ntr, mean_fd, hits/pcts for A..E
    """
    base = bold.with_suffix("").as_posix()  # strip .nii.gz -> path without suffix
    mean_nii = f"{base}_mean{tmp_suffix}.nii.gz"
    mask_nii = f"{base}_mask{tmp_suffix}.nii.gz"
    motion_1d = f"{base}_motion{tmp_suffix}.1D"
    dvars_1d = f"{base}_dvars{tmp_suffix}.1D"

    # nTR
    # Use fslnumb or nibabel? Keep it simple via AFNI: 3dinfo -nt
    ntr = int(subprocess.check_output(["3dinfo", "-nt", str(bold)], text=True).strip())

    if ntr <= 1:
        return dict(ntr=ntr, mean_fd=np.nan,
                    hits_A=0, hits_B=0, hits_C=0, hits_D=0, hits_E=0,
                    pct_A=0.0, pct_B=0.0, pct_C=0.0, pct_D=0.0, pct_E=0.0)

    # 1) mean
    run(["3dTstat", "-mean", "-prefix", mean_nii, str(bold)])
    # 2) automask on mean
    run(["3dAutomask", "-prefix", mask_nii, mean_nii])
    # 3) motion params (no output dataset)
    run(["3dvolreg", "-prefix", "NULL", "-base", "0", "-1Dfile", motion_1d, str(bold)])
    # 4) DVARS (masked)
    run(["3dTto1D", "-dvar", dvars_1d, "-mask", mask_nii, str(bold)])

    # Load series
    motion = load_1d(Path(motion_1d))       # (T x 6)
    fd = compute_fd_power_from_motion_1d(motion, head_radius)
    dvars = load_1d(Path(dvars_1d))

    fd = pad_to_ntr(fd, ntr)
    dvars = pad_to_ntr(dvars, ntr)
    z = robust_z(dvars)

    mean_fd = float(np.mean(fd)) if fd.size else float("nan")

    cond_A = (fd > fd_thr) & (z < z_thr)
    cond_B = (fd > fd_thr) & (z > z_thr)
    cond_C = (fd > fd_thr)
    cond_D = (z > z_thr)
    cond_E = cond_C | cond_D

    def pct(k, n): return round(100.0 * k / max(n, 1), 1)

    hits_A = int(cond_A.sum()); hits_B = int(cond_B.sum())
    hits_C = int(cond_C.sum()); hits_D = int(cond_D.sum()); hits_E = int(cond_E.sum())

    # clean temp files (comment out if you’d like to inspect)
    for p in (mean_nii, mask_nii, motion_1d, dvars_1d):
        try: os.remove(p)
        except Exception: pass

    return dict(
        ntr=ntr, mean_fd=mean_fd,
        hits_A=hits_A, hits_B=hits_B, hits_C=hits_C, hits_D=hits_D, hits_E=hits_E,
        pct_A=pct(hits_A, ntr), pct_B=pct(hits_B, ntr), pct_C=pct(hits_C, ntr),
        pct_D=pct(hits_D, ntr), pct_E=pct(hits_E, ntr),
    )

# ------------------------- orchestration ------------------------- #
def find_bold(func_dir: Path, sub: str, task: str, run_num: int) -> Path | None:
    p1 = func_dir / f"{sub}_task-{task}_run-0{run_num}_bold.nii.gz"
    if p1.exists(): return p1
    p2 = func_dir / f"{sub}_task-{task}_run-{run_num}_bold.nii.gz"
    if p2.exists(): return p2
    return None

def process_task(func_dir: Path, sub: str, task: str, max_run: int,
                 fd_thr: float, z_thr: float, head_radius: float, tmp_suffix: str):
    task_tr=task_A=task_B=task_C=task_D=task_E=0
    for r in range(1, max_run+1):
        bold = find_bold(func_dir, sub, task, r)
        if bold is None:
            print_flush(f"  [{task}] run {r}: MISSING (skipped)")
            continue
        t0 = time.time()
        print_flush(f"  [{task}] run {r}: starting  -> {bold.name}")
        res = process_run(bold, fd_thr, z_thr, head_radius, tmp_suffix)
        print_flush(
            f"  [{task}] run {r}: N_TR={res['ntr']} | meanFD={res['mean_fd']:.3f} mm | "
            f"A(FD>{fd_thr:.2f} & z<{z_thr:.1f})={res['hits_A']}/{res['ntr']} ({res['pct_A']}%) | "
            f"B(FD>{fd_thr:.2f} & z>{z_thr:.1f})={res['hits_B']}/{res['ntr']} ({res['pct_B']}%) | "
            f"C(FD>{fd_thr:.2f})={res['hits_C']}/{res['ntr']} ({res['pct_C']}%) | "
            f"D(z>{z_thr:.1f})={res['hits_D']}/{res['ntr']} ({res['pct_D']}%) | "
            f"E(OR)={res['hits_E']}/{res['ntr']} ({res['pct_E']}%) | "
            f"elapsed={time.time()-t0:.1f}s"
        )
        task_tr+=res["ntr"]; task_A+=res["hits_A"]; task_B+=res["hits_B"]
        task_C+=res["hits_C"]; task_D+=res["hits_D"]; task_E+=res["hits_E"]

    pct = lambda k,n: round(100.0*k/max(n,1),1)
    print_flush(
        f"Task {task} summary: "
        f"A={task_A}/{task_tr} ({pct(task_A,task_tr)}%) | "
        f"B={task_B}/{task_tr} ({pct(task_B,task_tr)}%) | "
        f"C={task_C}/{task_tr} ({pct(task_C,task_tr)}%) | "
        f"D={task_D}/{task_tr} ({pct(task_D,task_tr)}%) | "
        f"E={task_E}/{task_tr} ({pct(task_E,task_tr)}%)"
    )
    return task_tr, task_A, task_B, task_C, task_D, task_E

# ------------------------- CLI ------------------------- #
def parse_args():
    ap = argparse.ArgumentParser(description="Fast FD/stdDVARS via AFNI (arrow & collector).")
    ap.add_argument("bids_root", type=Path, help="BIDS root")
    ap.add_argument("subject", type=str, help="e.g., sub-temple123")
    ap.add_argument("--fd-thr", type=float, default=0.5, help="FD threshold (mm)")
    ap.add_argument("--z-thr", type=float, default=1.5, help="stdDVARS robust-z threshold")
    ap.add_argument("--radius", type=float, default=50.0, help="Head radius (mm) for FD Power")
    ap.add_argument("--tmp-tag", type=str, default="_tmpfd", help="Suffix for transient files")
    return ap.parse_args()

def main():
    args = parse_args()
    func_dir = args.bids_root / args.subject / "func"
    if not func_dir.is_dir():
        print_flush(f"ERROR: func dir not found: {func_dir}")
        sys.exit(1)

    print_flush(f"Subject {args.subject}")
    print_flush(f"FD_THR={args.fd_thr} mm | Z_THR={args.z_thr} | Radius={args.radius} mm")

    ALL_TR=ALL_A=ALL_B=ALL_C=ALL_D=ALL_E=0
    for task, max_run in (("arrow",6), ("collector",4)):
        t_tr, t_A, t_B, t_C, t_D, t_E = process_task(
            func_dir, args.subject, task, max_run,
            fd_thr=args.fd_thr, z_thr=args.z_thr,
            head_radius=args.radius, tmp_suffix=args.tmp_tag
        )
        ALL_TR+=t_tr; ALL_A+=t_A; ALL_B+=t_B; ALL_C+=t_C; ALL_D+=t_D; ALL_E+=t_E

    pct = lambda k,n: round(100.0*k/max(n,1),1)
    print_flush(
        f"Overall summary: "
        f"A={ALL_A}/{ALL_TR} ({pct(ALL_A,ALL_TR)}%) | "
        f"B={ALL_B}/{ALL_TR} ({pct(ALL_B,ALL_TR)}%) | "
        f"C={ALL_C}/{ALL_TR} ({pct(ALL_C,ALL_TR)}%) | "
        f"D={ALL_D}/{ALL_TR} ({pct(ALL_D,ALL_TR)}%) | "
        f"E={ALL_E}/{ALL_TR} ({pct(ALL_E,ALL_TR)}%)"
    )

if __name__ == "__main__":
    import shutil
    # quick sanity: AFNI tools present?
    for tool in ("3dTstat","3dAutomask","3dvolreg","3dTto1D","3dinfo"):
        if not shutil.which(tool):
            print_flush(f"ERROR: required AFNI tool not found in PATH: {tool}")
            sys.exit(2)
    main()
