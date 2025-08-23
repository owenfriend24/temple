#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, os, sys
from pathlib import Path
import subprocess
import numpy as np

# ------------------------- subprocess helpers ------------------------- #
def run_com(cmd, env=None):
    """Run a command; if it fails, show stderr for fast debugging."""
    try:
        return subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, check=True, env=env
        )
    except subprocess.CalledProcessError as e:
        msg = (
            f"\n[COMMAND FAILED]\n"
            f"cmd: {' '.join(cmd)}\n"
            f"stdout:\n{e.stdout}\n"
            f"stderr:\n{e.stderr}\n"
        )
        raise RuntimeError(msg) from e

def fslval(filepath: Path, field: str) -> str:
    return run_com(["fslval", str(filepath), field]).stdout.strip()

# ------------------------- TR helpers ------------------------- #
def get_tr_seconds(bold_path: Path) -> float | None:
    """
    Try to obtain TR (sec). Order:
      1) header pixdim4 via fslval
      2) BIDS sidecar JSON RepetitionTime
    """
    # 1) header
    try:
        pixdim4 = fslval(bold_path, "pixdim4")
        tr = float(pixdim4)
        if tr > 0:
            return tr
    except Exception:
        pass
    # 2) BIDS sidecar
    sidecar = bold_path.with_suffix("").with_suffix(".json")  # handles .nii.gz
    if sidecar.exists():
        try:
            data = json.loads(sidecar.read_text())
            tr = data.get("RepetitionTime", None)
            if tr and float(tr) > 0:
                return float(tr)
        except Exception:
            pass
    return None

# ------------------------- core calculations ------------------------- #
def pad_to_ntr(x: np.ndarray, ntr: int) -> np.ndarray:
    x = np.array(x).ravel() if x is not None else np.array([])
    x = np.insert(x, 0, 0.0)
    return x[:ntr] if x.size >= ntr else np.pad(x, (0, ntr - x.size))

def robust_z(x: np.ndarray) -> np.ndarray:
    med = np.median(x); mad = np.median(np.abs(x - med))
    if mad > 0: scale = mad * 1.4826
    else:
        sd = np.std(x); scale = sd if sd > 0 else 1.0
    return (x - med) / scale

def series_mean(x: np.ndarray) -> float:
    return float(np.mean(x)) if x.size else float("nan")

def zscore(x: np.ndarray) -> np.ndarray:
    """Classic z-score (mean/std) standardization."""
    if x.size == 0:
        return np.array([])
    m = np.mean(x)
    s = np.std(x)
    if s <= 0:
        s = 1.0
    return (x - m) / s

# ------------------------- per-run processing ------------------------- #
def process_run(bold_path: Path, fd_thr: float, z_thr: float, bet_frac: float) -> dict:
    base = bold_path.with_suffix("").as_posix()

    # nTR check
    ntr = int(float(fslval(bold_path, "dim4")))
    if ntr <= 1:
        # Nothing to compute
        return dict(ntr=ntr, mean_fd=np.nan, hits_A=0, hits_B=0, hits_C=0, hits_D=0, hits_E=0,
                    pct_A=0.0, pct_B=0.0, pct_C=0.0, pct_D=0.0, pct_E=0.0)


    # Quick mask
    run_com(["fslmaths", str(bold_path), "-Tmean", f"{base}_mean"])
    run_com(["bet", f"{base}_mean", f"{base}_mean_brain", "-m", "-f", f"{bet_frac}"])
    mask_path = f"{base}_mean_brain_mask.nii.gz"

    fd_txt = f"{base}_fd.txt"
    dvars_txt = f"{base}_dvars.txt"

    # 2) FD call: remove *fmo_tr_arg
    run_com([
        "fsl_motion_outliers", "-i", str(bold_path),
        "-o", f"{base}_fd_confounds.tsv",
        "--fd", f"--thresh={fd_thr}",
        "-s", fd_txt,
        "-p", f"{base}_fd.png",
    ])

    # 3) DVARS call: remove *fmo_tr_arg
    run_com([
        "fsl_motion_outliers", "-i", str(bold_path),
        "-o", f"{base}_dvars_confounds.tsv",
        "--dvars", "--thresh=9999",
        "-s", dvars_txt,
        "-p", f"{base}_dvars.png",
        "-m", mask_path,
    ])

    # Load & pad
    fd = np.loadtxt(fd_txt) if Path(fd_txt).exists() and os.path.getsize(fd_txt) > 0 else np.array([])
    dv = np.loadtxt(dvars_txt) if Path(dvars_txt).exists() and os.path.getsize(dvars_txt) > 0 else np.array([])
    fd = pad_to_ntr(fd, ntr)
    dv = pad_to_ntr(dv, ntr)
    z = robust_z(dv)

    mean_fd = series_mean(fd)

    cond_A = (fd > fd_thr) & (z < z_thr)   # your original A
    cond_B = (fd > fd_thr) & (z > z_thr)   # spike-style
    cond_C = (fd > fd_thr)
    cond_D = (z > z_thr)
    cond_E = cond_C | cond_D

    def pct(k, n): return round(100.0 * k / max(n, 1), 1)

    hits_A = int(cond_A.sum()); hits_B = int(cond_B.sum())
    hits_C = int(cond_C.sum()); hits_D = int(cond_D.sum()); hits_E = int(cond_E.sum())

    return dict(
        ntr=ntr, mean_fd=mean_fd,
        hits_A=hits_A, hits_B=hits_B, hits_C=hits_C, hits_D=hits_D, hits_E=hits_E,
        pct_A=pct(hits_A, ntr), pct_B=pct(hits_B, ntr), pct_C=pct(hits_C, ntr),
        pct_D=pct(hits_D, ntr), pct_E=pct(hits_E, ntr),
    )

# ------------------------- task orchestration ------------------------- #
def find_bold(bids_func_dir: Path, sub: str, task: str, run: int) -> Path | None:
    p1 = bids_func_dir / f"{sub}_task-{task}_run-0{run}_bold.nii.gz"
    if p1.exists(): return p1
    p2 = bids_func_dir / f"{sub}_task-{task}_run-{run}_bold.nii.gz"
    if p2.exists(): return p2
    return None

def process_task(bids_func_dir: Path, sub: str, task: str, max_run: int,
                 fd_thr: float, z_thr: float, bet_frac: float, writer=None):
    task_tr = task_A = task_B = task_C = task_D = task_E = 0
    for run in range(1, max_run + 1):
        bold = find_bold(bids_func_dir, sub, task, run)
        if bold is None:
            print(f"  [{task}] run {run}: MISSING (skipped)")
            continue
        res = process_run(bold, fd_thr, z_thr, bet_frac)
        task_tr += res["ntr"]; task_A += res["hits_A"]; task_B += res["hits_B"]
        task_C += res["hits_C"]; task_D += res["hits_D"]; task_E += res["hits_E"]
        print(
            f"  [{task}] run {run}: N_TR={res['ntr']} | meanFD={res['mean_fd']:.3f} mm | "
            # f"A(FD>{fd_thr:.2f} & z<{z_thr:.1f})={res['hits_A']}/{res['ntr']} ({res['pct_A']}%) | "
            f"B(FD>{fd_thr:.2f} & z>{z_thr:.1f})={res['hits_B']}/{res['ntr']} ({res['pct_B']}%) | "
            f" likely within {res['hits_B'] - 2} AND {res['hits_B'] + 2} / {(res['hits_B'] - 2)/res['ntr']} - {(res['hits_B'] + 2) /res['ntr']}"
            # f"C(FD>{fd_thr:.2f})={res['hits_C']}/{res['ntr']} ({res['pct_C']}%) | "
            # f"D(z>{z_thr:.1f})={res['hits_D']}/{res['ntr']} ({res['pct_D']}%) | "
            # f"E(OR)={res['hits_E']}/{res['ntr']} ({res['pct_E']}%)"
        )
        if writer:
            writer.writerow([
                sub, task, run, res["ntr"], f"{res['mean_fd']:.6f}",
                res["hits_A"], res["pct_A"],
                res["hits_B"], res["pct_B"],
                res["hits_C"], res["pct_C"],
                res["hits_D"], res["pct_D"],
                res["hits_E"], res["pct_E"],
                fd_thr, z_thr
            ])

    def pct(k, n): return round(100.0 * k / max(n, 1), 1)
    print(
        f"Task {task} summary: A={task_A}/{task_tr} ({pct(task_A, task_tr)}%) | "
        f"B={task_B}/{task_tr} ({pct(task_B, task_tr)}%) | "
        f"C={task_C}/{task_tr} ({pct(task_C, task_tr)}%) | "
        f"D={task_D}/{task_tr} ({pct(task_D, task_tr)}%) | "
        f"E={task_E}/{task_tr} ({pct(task_E, task_tr)}%)"
    )
    return task_tr, task_A, task_B, task_C, task_D, task_E

# ------------------------- CLI ------------------------- #
def parse_args():
    ap = argparse.ArgumentParser(description="Fast FD/stdDVARS triage for arrow & collector.")
    ap.add_argument("bids_root", type=Path)
    ap.add_argument("subject", type=str)
    ap.add_argument("--fd-thr", type=float, default=0.5)
    ap.add_argument("--z-thr", type=float, default=1.5)
    ap.add_argument("--bet-frac", type=float, default=0.3)
    ap.add_argument("--csv", type=Path, default=None)
    return ap.parse_args()

def main():
    args = parse_args()
    func_dir = args.bids_root / args.subject / "func"
    if not func_dir.is_dir():
        print(f"ERROR: func dir not found: {func_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Subject {args.subject}")
    print(f"FD_THR={args.fd_thr} mm | Z_THR={args.z_thr} | BET f={args.bet_frac}")

    writer = None
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        f = open(args.csv, "w", newline="")
        writer = csv.writer(f)
        writer.writerow([
            "subject","task","run","n_tr","mean_fd",
            "hits_A","pct_A","hits_B","pct_B","hits_C","pct_C",
            "hits_D","pct_D","hits_E","pct_E","fd_thr","z_thr"
        ])

    ALL_TR = ALL_A = ALL_B = ALL_C = ALL_D = ALL_E = 0
    for task, max_run in (("arrow", 6), ("collector", 4)):
        t_tr, t_A, t_B, t_C, t_D, t_E = process_task(
            func_dir, args.subject, task, max_run,
            fd_thr=args.fd_thr, z_thr=args.z_thr, bet_frac=args.bet_frac, writer=writer
        )
        ALL_TR += t_tr; ALL_A += t_A; ALL_B += t_B; ALL_C += t_C; ALL_D += t_D; ALL_E += t_E

    def pct(k, n): return round(100.0 * k / max(n, 1), 1)
    print(
        f"RUN SUMMARY: "
        # f"A={ALL_A}/{ALL_TR} ({pct(ALL_A, ALL_TR)}%) | "
        f"B={ALL_B}/{ALL_TR} ({pct(ALL_B, ALL_TR)}%) | "
        f" likely within {ALL_B - 2} AND {ALL_B + 2} / {pct(ALL_B -2, ALL_TR)} - {pct(ALL_B + 2, ALL_TR)}"
        # f"C={ALL_C}/{ALL_TR} ({pct(ALL_C, ALL_TR)}%) | "
        # f"D={ALL_D}/{ALL_TR} ({pct(ALL_D, ALL_TR)}%) | "
        # f"E={ALL_E}/{ALL_TR} ({pct(ALL_E, ALL_TR)}%)"
    )

if __name__ == "__main__":
    main()
