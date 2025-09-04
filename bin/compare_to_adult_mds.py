#!/usr/bin/env python3
"""
aggregate_group_and_alignment.py
--------------------------------
Auto-aggregates per-subject post-exposure RSM_z files into group-level RSM/RDMs and
computes per-subject alignment-to-adult plus plots.

Assumptions:
- Root directory (hard-coded below) contains:
    ROOT/sub-temple###/mds/_post_RSM_{mask_type}_z.npy
  where that .npy is a 12x12 Fisher-z correlation matrix saved by your subject script.
"""

from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.manifold import MDS
import matplotlib
matplotlib.use("Agg")  # headless HPC
import matplotlib.pyplot as plt
import re

from temple_utils.get_age_groups import get_children, get_adolescents, get_adults
from temple_utils.get_age_groups import get_age_years  # adjust if your age function is elsewhere

# ---------- Config ----------
ROOT = Path("/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/")

# ---------- Helpers ----------

def inv_fisher_z(z: np.ndarray) -> np.ndarray:
    return np.tanh(z)

def load_rsm_z(root_dir: Path, subject: str, mask_type: str) -> np.ndarray:
    subj_dir = f"/{root_dir}/sub-{subject}/mds"
    arr = np.load(f"{subj_dir}/_post_RSM_{mask_type}_z.npy")
    if arr.shape != (12, 12):
        raise ValueError(f"Bad shape for {subject}: {arr.shape} (expected 12x12)")
    return arr

def tri_offdiag_indices(n: int):
    return np.triu_indices(n, k=1)

def pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    x = x.astype(float); y = y.astype(float)
    x = x - x.mean(); y = y - y.mean()
    denom = np.sqrt((x*x).sum() * (y*y).sum())
    return float((x @ y) / denom) if denom != 0 else np.nan

def spearman_r(x: np.ndarray, y: np.ndarray) -> float:
    xr = pd.Series(x).rank(method="average").to_numpy()
    yr = pd.Series(y).rank(method="average").to_numpy()
    return pearson_r(xr, yr)

def average_group_rsm(root_dir: Path, subjects, mask_type: str) -> tuple[np.ndarray, np.ndarray]:
    """Average in z-space; return (group_RSM, group_RDM)."""
    z_mats = [load_rsm_z(root_dir, s, mask_type) for s in subjects]
    mean_z = np.mean(np.stack(z_mats, axis=0), axis=0)
    group_rsm = inv_fisher_z(mean_z)
    np.fill_diagonal(group_rsm, 1.0)
    group_rdm = 1.0 - group_rsm
    return group_rsm, group_rdm

def run_mds_precomputed(rdm: np.ndarray, random_state: int = 0) -> np.ndarray:
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=random_state)
    return mds.fit_transform(rdm)  # (12, 2)

def save_group_outputs(root_dir: Path, name: str, rsm: np.ndarray, rdm: np.ndarray, coords: np.ndarray, mask_type):
    (root_dir / "group_mds").mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rsm).to_csv(root_dir / f"group_mds/group-{name}_RSM_{mask_type}.csv", index=False, header=False)
    pd.DataFrame(rdm).to_csv(root_dir / f"group_mds/group-{name}_RDM_{mask_type}.csv", index=False, header=False)
    dfc = pd.DataFrame(coords, columns=["MDS1", "MDS2"])
    dfc["stimulus"] = np.arange(1, 13)
    dfc.to_csv(root_dir / f"group_mds/group-{name}_mds_coords_{mask_type}.csv", index=False)

def plot_adult_mds(root_dir: Path, coords: np.ndarray, mask_type):
    """Scatter the 12 adult items with labels 1..12."""
    (root_dir / "group_mds").mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 6), dpi=150)
    plt.scatter(coords[:, 0], coords[:, 1])
    for i, (x, y) in enumerate(coords, start=1):
        plt.text(x, y, str(i), fontsize=10, ha="center", va="center")
    plt.title("Adult Group: 2D MDS of 12 Items")
    plt.xlabel("MDS1")
    plt.ylabel("MDS2")
    plt.gca().set_aspect("equal", adjustable="datalim")
    plt.tight_layout()
    plt.savefig(root_dir / f"group_mds/group-ADULT_mds_plot_{mask_type}.png")
    plt.close()

def main(args):
    mask_type = args.mask_type

    children = get_children()
    adolescents = get_adolescents()
    adults = get_adults()

    # Keep only subject numbers >= 56
    children = [s for s in children if int(re.search(r'(\d+)', str(s)).group()) >= 56]
    adolescents = [s for s in adolescents if int(re.search(r'(\d+)', str(s)).group()) >= 56]
    adults = [s for s in adults if int(re.search(r'(\d+)', str(s)).group()) >= 56]

    groups = {
        "child": children,
        "adolescent": adolescents,
        "adult": adults,
    }

    # ----- Adult reference via z-stack (enables LOAO) -----
    adult_z_list = [load_rsm_z(ROOT, s, mask_type) for s in adults]
    adult_z_stack = np.stack(adult_z_list, axis=0) if len(adult_z_list) else np.empty((0,12,12))
    adult_mean_z  = adult_z_stack.mean(axis=0) if adult_z_stack.size else np.zeros((12,12))
    adult_rsm     = inv_fisher_z(adult_mean_z)
    np.fill_diagonal(adult_rsm, 1.0)
    adult_rdm     = 1.0 - adult_rsm

    # Adult MDS & outputs
    adult_coords = run_mds_precomputed(adult_rdm, random_state=0)
    save_group_outputs(ROOT, "ADULT", adult_rsm, adult_rdm, adult_coords, mask_type)
    plot_adult_mds(ROOT, adult_coords, mask_type)

    # Vectorized adult off-diagonals (in r-space) for default reference
    tri_idx = tri_offdiag_indices(12)
    adult_vec_default = adult_rsm[tri_idx].astype(float)

    # Compute & save each group’s outputs (RSM/RDM/MDS)
    for gname, subjects in groups.items():
        if not subjects:
            print(f"[WARN] No subjects found for group '{gname}'")
            continue
        grp_rsm, grp_rdm = average_group_rsm(ROOT, subjects, mask_type)
        grp_coords = run_mds_precomputed(grp_rdm, random_state=0)
        save_group_outputs(ROOT, gname, grp_rsm, grp_rdm, grp_coords, mask_type)

    # Per-subject alignment to adults (Pearson; distance = 1 - r), LOAO for adults
    rows = []
    for gname, subjects in groups.items():
        for sub in subjects:
            sub_rsm = inv_fisher_z(load_rsm_z(ROOT, sub, mask_type))
            np.fill_diagonal(sub_rsm, 1.0)
            sub_vec = sub_rsm[tri_idx].astype(float)

            # Reference vector: LOAO if subject is adult and >1 adult available
            if (sub in adults) and (adult_z_stack.shape[0] > 1):
                idx = adults.index(sub)
                loo_mean_z = (adult_z_stack.sum(axis=0) - adult_z_stack[idx]) / (adult_z_stack.shape[0] - 1)
                ref_rsm = inv_fisher_z(loo_mean_z); np.fill_diagonal(ref_rsm, 1.0)
                ref_vec = ref_rsm[tri_idx].astype(float)
            else:
                ref_vec = adult_vec_default

            align = pearson_r(sub_vec, ref_vec)   # r
            align_z = np.arctanh(np.clip(align, -0.999999, 0.999999))
            dist = 1.0 - align
            age = float(get_age_years(sub))
            rows.append({
                "subject": sub,
                "group": gname,
                "age_years": age,
                "alignment_to_adult": align,
                "alignment_to_adult_z": align_z,
                "distance_to_adult": dist,
            })

    out_csv = ROOT / f"group_mds/subject_alignment_to_adult_{mask_type}.csv"
    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    print(f"[OK] Wrote group RSM/RDMs, MDS coords, plots, and per-subject alignment scores to {ROOT}")

    # Long-format CSV for mixed model (RDM rows; later append ISC)
    long_df = df[["subject", "group", "age_years", "alignment_to_adult_z"]].copy()
    long_df["mask_type"] = mask_type
    long_df["measure"] = "RDM"
    long_df = long_df.rename(columns={"alignment_to_adult_z": "z_value"})
    long_out = ROOT / f"group_mds/representational_alignment_long_{mask_type}.csv"
    long_df.to_csv(long_out, index=False)

    # Plot distance vs. age
    plt.figure(figsize=(7, 5), dpi=150)
    plt.scatter(df["age_years"], df["distance_to_adult"])
    plt.xlabel("Age (years)")
    plt.ylabel("Distance to Adult Group (1 − Pearson r)")
    plt.title("Distance to Adult Representational Geometry vs. Age")
    plt.tight_layout()
    plt.savefig(ROOT / f"group_mds/alignment_vs_age_{mask_type}.png")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate RSMs by group and compute alignment-to-adult.")
    parser.add_argument("mask_type",  help="e.g., b_hip, b_hip_ant, b_hip_post")
    args = parser.parse_args()
    main(args)
