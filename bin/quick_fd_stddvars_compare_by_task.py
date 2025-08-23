#!/usr/bin/env python3
"""
Quick FD/stdDVARS triage (FSL-backed) for arrow (6 runs) and collector (4 runs).

- Calls FSL tools via subprocess:
    fslmaths, bet, fslval, fsl_motion_outliers
- Computes:
    * Power FD  (matches fMRIPrep definition)
    * DVARS     (from fsl_motion_outliers)
    * stdDVARS  (robust z = (DVARS - median) / (MAD*1.4826))
- Reports per-run, per-task, and overall:
    A) FD>fd_thr & stdDVARS<z_thr
    B) FD>fd_thr & stdDVARS>z_thr
    C) FD>fd_thr
    D) stdDVARS>z_thr
    E) FD>fd_thr OR stdDVARS>z_thr

Usage:
    python quick_fd_stddvars_compare_by_task.py /path/to/BIDS sub-0123 \
        --fd-thr 0.5 --z-thr 1.5 --csv /path/to/output.csv

Notes:
- We pad a leading 0 so FD/DVARS length == N_TR (like fMRIPrep’s first-volume 0).
- “stdDVARS” uses robust z (median/MAD*1.4826); switch to mean/std if you prefer.
"""

from __future__ import annotations
import argparse
import csv
import os
from pathlib import Path
import subprocess
import sys
from typing import Dict, List, Tuple

import numpy as np


# ------------------------- subprocess helpers ------------------------- #
def run_com(cmd: List[str], capture: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command with sensible defaults."""
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
        check=check,
    )


def fslval(filepath: Path, field: str) -> str:
    res = run_com(["fslval", str(filepath), field])
    return res.stdout.strip()


# ------------------------- core calculations ------------------------- #
def pad_to_ntr(x: np.ndarray, ntr: int) -> np.ndarray:
    """Pad a leading 0 and ensure length == ntr."""
    if x.size == 0:
        x = np.array([], dtype=float)
    x = x.ravel()
    x = np.insert(x, 0, 0.0)
    if x.size >= ntr:
        return x[:ntr]
    return np.pad(x, (0, ntr - x.size), mode="constant")


def robust_z(x: np.ndarray) -> np.ndarray:
    """Robust z-score: (x - median) / (MAD * 1.4826). Fallback to std if MAD==0."""
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    if mad > 0:
        scale = mad * 1.4826
    else:
        sd = np.std(x)
        scale = sd if sd > 0 else 1.0
    return (x - med) / scale


def series_mean(x: np.ndarray) -> float:
    return float(np.mean(x)) if x.size else float("nan")


# ------------------------- per-run processing ------------------------- #
def process_run(
    bold_path: Path,
    fd_thr: float,
    z_thr: float,
    bet_frac: float,
) -> Dict[str, float]:
    """
    Process one run:
      - quick mask (mean + bet)
      - FD & DVARS via fsl_motion_outliers
      - pad, standardize DVARS, compute counts
    Returns summary dict.
    """
    base = bold_path.with_suffix("").as_posix()

    # Quick mask
    run_com(["fslmaths", str(bold_path), "-Tmean", f"{base}_mean"], capture=False)
    run_com(["bet", f"{base}_mean", f"{base}_mean_brain", "-m", "-f", f"{bet_frac}"], capture=False)
    mask_path = f"{base}_mean_brain_mask.nii.gz"

    # FD (Power)
    fd_txt = f"{base}_fd.txt"
    run_com([
        "fsl_motion_outliers",
        "-i", str(bold_path),
        "-o", f"{base}_fd_confounds.tsv",
        "--fd", "--thresh", str(fd_thr),
        "-s", fd_txt,
        "-p", f"{base}_fd.png",
    ], capture=False)

    # DVARS (raw)
    dvars_txt = f"{base}_dvars.txt"
    run_com([
        "fsl_motion_outliers",
        "-i", str(bold_path),
        "-o", f"{base}_dvars_confounds.tsv",
        "--dvars", "--thresh", "9999",
        "-s", dvars_txt,
        "-p", f"{base}_dvars.png",
        "-m", mask_path,
    ], capture=False)

    # TR count
    ntr = int(float(fslval(bold_path, "dim4")))

    # Load & pad
    fd = np.loadtxt(fd_txt) if Path(fd_txt).exists() and os.path.getsize(fd_txt) > 0 else np.array([])
    dv = np.loadtxt(dvars_txt) if Path(dvars_txt).exists() and os.path.getsize(dvars_txt) > 0 else np.array([])

    fd = pad_to_ntr(fd, ntr)
    dv = pad_to_ntr(dv, ntr)
    z = robust_z(dv)

    # Metrics
    mean_fd = series_mean(fd)
    cond_A = (fd > fd_thr) & (z < z_thr)               # your “A” comparison
    cond_B = (fd > fd_thr) & (z > z_thr)               # “spike” style
    cond_C = (fd > fd_thr)
    cond_D = (z > z_thr)
    cond_E = cond_C | cond_D

    hits_A = int(cond_A.sum())
    hits_B = int(cond_B.sum())
    hits_C = int(cond_C.sum())
    hits_D = int(cond_D.sum())
    hits_E = int(cond_E.sum())

    def pct(k: int, n: int) -> float:
        return round(100.0 * k / max(n, 1), 1)

    return {
        "ntr": ntr,
        "mean_fd": mean_fd,
        "hits_A": hits_A,
        "hits_B": hits_B,
        "hits_C": hits_C,
        "hits_D": hits_D,
        "hits_E": hits_E,
        "pct_A": pct(hits_A, ntr),
        "pct_B": pct(hits_B, ntr),
        "pct_C": pct(hits_C, ntr),
        "pct_D": pct(hits_D, ntr),
        "pct_E": pct(hits_E, ntr),
    }


# ------------------------- task orchestration ------------------------- #
def find_bold(bids_func_dir: Path, sub: str, task: str, run: int) -> Path | None:
    """Find *_bold.nii.gz allowing 0-padded or not."""
    p1 = bids_func_dir / f"{sub}_task-{task}_run-0{run}_bold.nii.gz"
    if p1.exists():
        return p1
    p2 = bids_func_dir / f"{sub}_task-{task}_run-{run}_bold.nii.gz"
    if p2.exists():
        return p2
    return None


def process_task(
    bids_func_dir: Path,
    sub: str,
    task: str,
    max_run: int,
    fd_thr: float,
    z_thr: float,
    bet_frac: float,
    writer: csv.writer | None = None,
) -> Tuple[int, int, int, int, int, int]:
    """Process all runs in a task; print per-run and task summary; optionally write CSV."""
    task_tr = task_A = task_B = task_C = task_D = task_E = 0

    for run in range(1, max_run + 1):
        bold = find_bold(bids_func_dir, sub, task, run)
        if bold is None:
            print(f"  [{task}] run {run}: MISSING (skipped)")
            continue

        res = process_run(bold, fd_thr, z_thr, bet_frac)
        task_tr += res["ntr"]
        task_A += res["hits_A"]
        task_B += res["hits_B"]
        task_C += res["hits_C"]
        task_D += res["hits_D"]
        task_E += res["hits_E"]

        print(
            f"  [{task}] run {run}: N_TR={res['ntr']} | "
            f"meanFD={res['mean_fd']:.3f} mm | "
            f"A(FD>{fd_thr:.2f} & z<{z_thr:.1f})={res['hits_A']}/{res['ntr']} ({res['pct_A']}%) | "
            f"B(FD>{fd_thr:.2f} & z>{z_thr:.1f})={res['hits_B']}/{res['ntr']} ({res['pct_B']}%) | "
            f"C(FD>{fd_thr:.2f})={res['hits_C']}/{res['ntr']} ({res['pct_C']}%) | "
            f"D(z>{z_thr:.1f})={res['hits_D']}/{res['ntr']} ({res['pct_D']}%) | "
            f"E(OR)={res['hits_E']}/{res['ntr']} ({res['pct_E']}%)"
        )

        if writer is not None:
            writer.writerow([
                sub, task, run, res["ntr"], f"{res['mean_fd']:.6f}",
                res["hits_A"], res["pct_A"],
                res["hits_B"], res["pct_B"],
                res["hits_C"], res["pct_C"],
                res["hits_D"], res["pct_D"],
                res["hits_E"], res["pct_E"],
                fd_thr, z_thr
            ])

    # task summary
    def pct(k: int, n: int) -> float:
        return round(100.0 * k / max(n, 1), 1)

    print(
        f"Task {task} summary: "
        f"A={task_A}/{task_tr} ({pct(task_A, task_tr)}%) | "
        f"B={task_B}/{task_tr} ({pct(task_B, task_tr)}%) | "
        f"C={task_C}/{task_tr} ({pct(task_C, task_tr)}%) | "
        f"D={task_D}/{task_tr} ({pct(task_D, task_tr)}%) | "
        f"E={task_E}/{task_tr} ({pct(task_E, task_tr)}%)"
    )

    return task_tr, task_A, task_B, task_C, task_D, task_E


# ------------------------- CLI ------------------------- #
def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Fast FD/stdDVARS triage for arrow & collector.")
    ap.add_argument("bids_root", type=Path, help="BIDS root directory")
    ap.add_argument("subject", type=str, help="Subject ID (e.g., sub-0123)")
    ap.add_argument("--fd-thr", type=float, default=0.5, help="FD threshold in mm (default 0.5)")
    ap.add_argument("--z-thr", type=float, default=1.5, help="stdDVARS robust-z threshold (default 1.5)")
    ap.add_argument("--bet-frac", type=float, default=0.3, help="BET fractional intensity threshold (default 0.3)")
    ap.add_argument("--csv", type=Path, default=None, help="Optional path to write per-run CSV")
    return ap.parse_args()


def main():
    args = parse_args()
    bids_root: Path = args.bids_root
    sub: str = args.subject
    func_dir = bids_root / sub / "func"

    if not func_dir.is_dir():
        print(f"ERROR: func dir not found: {func_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Subject {sub}")
    print(f"FD_THR={args.fd_thr} mm | Z_THR={args.z_thr} | BET f={args.bet_frac}")

    writer = None
    csv_file = None
    if args.csv:
        csv_file = open(args.csv, "w", newline="")
        writer = csv.writer(csv_file)
        writer.writerow([
            "subject", "task", "run", "n_tr", "mean_fd",
            "hits_A", "pct_A",
            "hits_B", "pct_B",
            "hits_C", "pct_C",
            "hits_D", "pct_D",
            "hits_E", "pct_E",
            "fd_thr", "z_thr",
        ])

    ALL_TR = ALL_A = ALL_B = ALL_C = ALL_D = ALL_E = 0

    # Process both tasks
    for task, max_run in (("arrow", 6), ("collector", 4)):
        t_tr, t_A, t_B, t_C, t_D, t_E = process_task(
            func_dir, sub, task, max_run,
            fd_thr=args.fd_thr, z_thr=args.z_thr, bet_frac=args.bet_frac,
            writer=writer
        )
        ALL_TR += t_tr; ALL_A += t_A; ALL_B += t_B; ALL_C += t_C; ALL_D += t_D; ALL_E += t_E

    # Overall summary
    def pct(k: int, n: int) -> float:
        return round(100.0 * k / max(n, 1), 1)

    print(
        f"Overall summary: "
        f"A={ALL_A}/{ALL_TR} ({pct(ALL_A, ALL_TR)}%) | "
        f"B={ALL_B}/{ALL_TR} ({pct(ALL_B, ALL_TR)}%) | "
        f"C={ALL_C}/{ALL_TR} ({pct(ALL_C, ALL_TR)}%) | "
        f"D={ALL_D}/{ALL_TR} ({pct(ALL_D, ALL_TR)}%) | "
        f"E={ALL_E}/{ALL_TR} ({pct(ALL_E, ALL_TR)}%)"
    )

    if csv_file:
        csv_file.close()


if __name__ == "__main__":
    main()
