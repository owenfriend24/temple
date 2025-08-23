#!/usr/bin/env python3
"""
Fast FD (Power) + stdDVARS via AFNI for tasks: arrow(1..6) and collector(1..4)

Per run:
  1) 3dTstat -mean -> mean image
  2) 3dAutomask on mean -> mask
  3) 3dvolreg -1Dfile -> motion.1D (rot deg, trans mm)
  4) DVARS (portable):
       a) temporal diff with 3dcalc using explicit numeric selectors (no $-1)
       b) square diffs with 3dcalc
       c) spatial mean per TR with 3dmaskave
       d) sqrt in Python => DVARS
Then:
  - FD (Power): sum(|Δtrans|) + R * sum(|Δrot(rad)|), R=50 mm default
  - stdDVARS: robust z = (DVARS - median) / (MAD*1.4826)
  - Pad leading 0 so length == N_TR (like fMRIPrep first-volume 0)

Printed metrics per run, task, and overall:
  A) FD>fd_thr & stdDVARS<z_thr
  B) FD>fd_thr & stdDVARS>z_thr
  C) FD>fd_thr
  D) stdDVARS>z_thr
  E) FD>fd_thr OR stdDVARS>z_thr
"""

from __future__ import annotations
import argparse, os, sys, time, shutil, subprocess
from pathlib import Path
import numpy as np

# -------- unbuffered printing so SLURM .out updates during run --------
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass
def p(*a, **k): print(*a, flush=True, **k)

# ------------------------- subprocess helper ------------------------- #
def run(cmd: list[str]) -> None:
    """Run a command and stream output to stdout/stderr (SLURM captures it)."""
    subprocess.run(cmd, check=True)

# ------------------------- core helpers ------------------------- #
def pad_to_ntr(x: np.ndarray, ntr: int) -> np.ndarray:
    x = np.array(x).ravel() if x is not None else np.array([])
    x = np.insert(x, 0, 0.0)  # pad first sample to 0
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
    AFNI 3dvolreg motion.1D columns: [roll pitch yaw dS dL dP]
      rotations in DEGREES, translations in mm.
    FD_power[t] = sum(|Δtrans|) + R * sum(|Δrot(rad)|)
    """
    if motion.size == 0:
        return np.array([])
    motion = np.atleast_2d(motion)
    if motion.shape[1] < 6:
        raise ValueError("motion.1D does not have 6 columns")
    rot_deg = motion[:, 0:3]
    trans_mm = motion[:, 3:6]
    drot_deg = np.diff(rot_deg, axis=0)
    dtrans_mm = np.diff(trans_mm, axis=0)
    drot_rad = np.deg2rad(drot_deg)
    fd = np.sum(np.abs(dtrans_mm), axis=1) + head_radius_mm * np.sum(np.abs(drot_rad), axis=1)
    return fd

def safe_unlink(*paths: str) -> None:
    for pth in paths:
        try:
            if pth and os.path.exists(pth):
                os.remove(pth)
        except Exception:
            pass

# ------------------------- per-run processing ------------------------- #
def process_run(bold: Path, fd_thr: float, z_thr: float, head_radius: float, tmp_suffix: str) -> dict:
    base_noext = bold.with_suffix("").as_posix()  # strip .nii.gz
    mean_nii   = f"{base_noext}_mean{tmp_suffix}.nii.gz"
    mask_nii   = f"{base_noext}_mask{tmp_suffix}.nii.gz"
    motion_1d  = f"{base_noext}_motion{tmp_suffix}.1D"
    diff_nii   = f"{base_noext}_diff{tmp_suffix}.nii.gz"
    diffsq_nii = f"{base_noext}_diffsq{tmp_suffix}.nii.gz"

    # N_TR via AFNI
    ntr = int(subprocess.check_output(["3dinfo", "-nt", str(bold)], text=True).strip())
    if ntr <= 1:
        return dict(ntr=ntr, mean_fd=np.nan,
                    hits_A=0, hits_B=0, hits_C=0, hits_D=0, hits_E=0,
                    pct_A=0.0, pct_B=0.0, pct_C=0.0, pct_D=0.0, pct_E=0.0)

    # Pre-clean left-overs to avoid "conflicts with existing file"
    safe_unlink(mean_nii, mask_nii, motion_1d, diff_nii, diffsq_nii)

    # 1) mean
    run(["3dTstat", "-mean", "-prefix", mean_nii, str(bold)])
    # 2) automask on mean
    run(["3dAutomask", "-prefix", mask_nii, mean_nii])
    # 3) motion params (no output dataset)
    run(["3dvolreg", "-prefix", "NULL", "-base", "0", "-1Dfile", motion_1d, str(bold)])

    # 4) DVARS (portable): temporal diff -> square -> spatial mean -> sqrt
    # Explicit numeric selectors instead of $-1 (older AFNI compatibility)
    last = ntr - 1                      # last sub-brick index
    a_sel = f"[1..{last}]"
    b_sel = f"[0..{last-1}]"
    run(["3dcalc", "-a", str(bold) + a_sel, "-b", str(bold) + b_sel,
         "-expr", "a-b", "-prefix", diff_nii])
    run(["3dcalc", "-a", diff_nii, "-expr", "a*a", "-prefix", diffsq_nii])
    dvars_means = subprocess.check_output(
        ["3dmaskave", "-quiet", "-mask", mask_nii, diffsq_nii], text=True
    ).strip().splitlines()
    dvars = np.sqrt(np.array([float(x) for x in dvars_means], dtype=float))

    # Load motion, compute FD Power
    motion = load_1d(Path(motion_1d))
    fd = compute_fd_power_from_motion_1d(motion, head_radius)

    # pad to N_TR and standardize DVARS
    fd    = pad_to_ntr(fd, ntr)
    dvars = pad_to_ntr(dvars, ntr)
    z     = robust_z(dvars)
    mean_fd = float(np.mean(fd)) if fd.size else float("nan")

    # conditions
    cond_A = (fd > fd_thr) & (z < z_thr)
    cond_B = (fd > fd_thr) & (z > z_thr)
    cond_C = (fd > fd_thr)
    cond_D = (z > z_thr)
    cond_E = cond_C | cond_D

    hits_A = int(cond_A.sum()); hits_B = int(cond_B.sum())
    hits_C = int(cond_C.sum()); hits_D = int(cond_D.sum()); hits_E = int(cond_E.sum())
    pct = lambda k, n: round(100.0 * k / max(n, 1), 1)

    # clean temp files (comment out if you want to inspect)
    safe_unlink(mean_nii, mask_nii, motion_1d, diff_nii, diffsq_nii)

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
            p(f"  [{task}] run {r}: MISSING (skipped)")
            continue
        t0 = time.time()
        p(f"  [{task}] run {r}: starting  -> {bold.name}")
        res = process_run(bold, fd_thr, z_thr, head_radius, tmp_suffix)
        p(
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
    p(
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
        p(f"ERROR: func dir not found: {func_dir}")
        sys.exit(1)

    p(f"Subject {args.subject}")
    p(f"FD_THR={args.fd_thr} mm | Z_THR={args.z_thr} | Radius={args.radius} mm")

    ALL_TR=ALL_A=ALL_B=ALL_C=ALL_D=ALL_E=0
    # Make tmp suffix unique per run group to avoid collisions even across reruns
    base_tag = f"{args.tmp_tag}_{int(time.time())}"
    for task, max_run in (("arrow",6), ("collector",4)):
        t_tr, t_A, t_B, t_C, t_D, t_E = process_task(
            func_dir, args.subject, task, max_run,
            fd_thr=args.fd_thr, z_thr=args.z_thr,
            head_radius=args.radius, tmp_suffix=base_tag
        )
        ALL_TR+=t_tr; ALL_A+=t_A; ALL_B+=t_B; ALL_C+=t_C; ALL_D+=t_D; ALL_E+=t_E

    pct = lambda k,n: round(100.0*k/max(n,1),1)
    p(
        f"Overall summary: "
        f"A={ALL_A}/{ALL_TR} ({pct(ALL_A,ALL_TR)}%) | "
        f"B={ALL_B}/{ALL_TR} ({pct(ALL_B,ALL_TR)}%) | "
        f"C={ALL_C}/{ALL_TR} ({pct(ALL_C,ALL_TR)}%) | "
        f"D={ALL_D}/{ALL_TR} ({pct(ALL_D,ALL_TR)}%) | "
        f"E={ALL_E}/{ALL_TR} ({pct(ALL_E,ALL_TR)}%)"
    )

if __name__ == "__main__":
    # sanity: required AFNI tools present?
    for tool in ("3dTstat","3dAutomask","3dvolreg","3dinfo","3dcalc","3dmaskave"):
        if not shutil.which(tool):
            p(f"ERROR: required AFNI tool not found in PATH: {tool}")
            sys.exit(2)
    main()
