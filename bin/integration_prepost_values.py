#!/usr/bin/env python

### Import required Python libraries ###
import numpy as np
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import subprocess
import argparse

### Import custom searchlight function ###
from prepost_roi import *
from prepost_roi_droprun import *

### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")

    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("comparison", help="Comparison type (e.g., AC)")
    parser.add_argument("masktype", help="Mask type (e.g., b_hip_subregions)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

### Main script execution ###
if __name__ == "__main__":
    args = get_args()

    ### Set up experiment info ###
    expdir = '/corral-repl/utexas/prestonlab/temple/'
    sbj = args.subject_id
    comparison = args.comparison
    masktype = args.masktype
    drop_run = args.drop_run  # Store drop_run argument

    ### Validate masks for data analysis ###
    if masktype == 'b_hip_subregions':
        masks = ['warp-b_hip', 'warp-b_hip_ant', 'warp-b_hip_post', 'warp-b_hip_body']
    else:
        raise ValueError('Invalid mask type')

    if drop_run is not None:
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comparison}_items_drop{drop_run}.txt',
            unpack=True
        )
    else:
    # Load phase, run, triad, and item data
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comparison}_items.txt',
            unpack=True
        )

    ### Directories ###
    subjdir = os.path.join(expdir, f'sub-{sbj}')
    betadir = os.path.join(subjdir, 'betaseries')
    resultdir = os.path.join(expdir, f'integration_prepost/prepost_{comparison}')
    out_dir = os.path.join(resultdir, f'sub-{sbj}')
    os.makedirs(out_dir, exist_ok=True)

    for mask in masks:
        if masktype == 'b_hip_subregions':
            slmask = os.path.join(subjdir, 'transforms', f'{mask}.nii.gz')

        # Load fMRI data
        ds = fmri_dataset(os.path.join(betadir, f'pre_post_{comparison}_items.nii.gz'), mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]

        # Similarity measure
        if drop_run is not None:
            measure = prepost_roi_droprun('correlation', 1, comparison)
        else:
            measure = prepost_roi('correlation', 1, comparison)

        # Obtain within-pair and across-pair similarity values
        within, across = measure(ds)

        # Save results
        out_file_w = os.path.join(out_dir, f"{sbj}_prepost_{comparison}_within_{mask}.txt")
        out_file_a = os.path.join(out_dir, f"{sbj}_prepost_{comparison}_across_{mask}.txt")

        np.savetxt(out_file_w, within, fmt="%.8f")
        np.savetxt(out_file_a, across, fmt="%.8f")
