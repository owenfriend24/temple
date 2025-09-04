#!/usr/bin/env python3
"""
pull representational similarity matrices from post-exposure betaseries for MDS analyses
"""

import argparse
import os
from pathlib import Path
import numpy as np
import nibabel as nib
import pandas as pd
from scipy.stats import zscore

def fisher_z(r):
    r = np.clip(r, -0.999999, 0.999999)
    return np.arctanh(r)

def inv_fisher_z(z):
    return np.tanh(z)

def zscore_within_run(patterns):
    # avoid zero-variance cols just in case
    return np.nan_to_num(zscore(patterns, axis=0, ddof=1), nan=0.0, posinf=0.0, neginf=0.0)

def rsm_pearson(patterns):
    return np.corrcoef(patterns)

def apply_mask(data4d, mask_bool):
    # nilearn masking
    vox = data4d[mask_bool]   # (n_voxels, 12)
    return vox.T              # (12, n_voxels)

def main(subject, data_dir, mask_type):
    out_dir = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-{subject}/mds'
    os.makedirs(out_dir, exist_ok=True)
    # set paths - currently set up to assume data_dir is corral
    mask_path =  f"{data_dir}/sub-{subject}/masks/hip_masks/func-{mask_type}.nii.gz"
    post_path = f"{data_dir}/sub-{subject}/betaseries/post_items.nii.gz"

    # load mask and data
    mask = nib.load(str(mask_path)).get_fdata().astype(bool)
    data4d = nib.load(str(post_path)).get_fdata()  # (X,Y,Z,36)
    if data4d.ndim != 4 or data4d.shape[-1] != 36:
        raise ValueError(f"Expected 4D NIfTI with 36 volumes (3 runs × 12 items): got {data4d.shape}")

    # ----- split into 3 runs of 12 items -----
    # Assumes run blocks: [0..11]=run1, [12..23]=run2, [24..35]=run3
    run_slices = [slice(0, 12), slice(12, 24), slice(24, 36)]

    # Per-run RSMs (Fisher-z)
    rsms_z = []
    for k in range(3):
        print(f'pulling vals from post run {k + 4}')
        vols = data4d[..., run_slices[k]]  # <-- use this line for run-block files (default)
        if vols.shape[-1] != 12:
            raise ValueError(f"Run {k + 4} does not have 12 volumes: got {vols.shape[-1]}")

        patterns = apply_mask(vols, mask)  # (12, n_vox)
        patterns = zscore_within_run(patterns)
        rsm = rsm_pearson(patterns)  # 12×12
        rsms_z.append(fisher_z(rsm))

    # Average in z-space, then invert
    mean_z = np.mean(np.stack(rsms_z, axis=0), axis=0)  # 12×12
    mean_rsm = inv_fisher_z(mean_z)
    np.fill_diagonal(mean_rsm, 1.0)

    # Save Fisher-z RSM (preferred for later aggregation)
    out_npy = f"{out_dir}/_post_RSM_z.npy"
    out_csv = f"{out_dir}/_post_RSM_z.csv"
    np.save(out_npy, mean_z)
    pd.DataFrame(mean_z).to_csv(out_csv, index=False, header=False)

    print(f"Wahoo! Saved subject RSM_z and QC RDM for {subject}:  {out_npy}, {out_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build run-averaged 12x12 RSM (Fisher-z) for one subject.")
    parser.add_argument("subject", help="Subject ID, e.g., sub-001")
    parser.add_argument("data_dir",  help="Directory with runs & mask")
    parser.add_argument("mask_type", help="b_hip, b_hip_ant, b_hip_post")
    args = parser.parse_args()
    main(args.subject, args.data_dir, args.mask_type)
