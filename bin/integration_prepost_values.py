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
import pandas as pd

# ignore division by zero errors for NaN values when transforming to fisher's Z
np.seterr(divide='ignore', invalid='ignore')

### Import custom searchlight function ###
from prepost_roi import *
from prepost_roi_droprun import *
from prepost_roi_shuffle import *
from prepost_roi_shuffle_droprun import *

### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")

    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("comparison", help="Comparison type (e.g., AC)")
    parser.add_argument("masktype", help="Mask type (e.g., b_hip_subregions, b_ifg_subregions)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

### Main script execution ###
if __name__ == "__main__":
    args = get_args()

    ### Set up experiment info ###

    sbj = args.subject_id

    if sbj in ['temple117', 'temple121', 'temple125']:
        expdir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/'
    else:
        expdir = '/corral-repl/utexas/prestonlab/temple/'

    comparison = args.comparison
    masktype = args.masktype
    drop_run = args.drop_run

    ### Validate masks for data analysis ###
    if masktype == 'b_hip_subregions':
        masks = ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body']
    elif masktype == 'lat_hip_subregions':
        masks = ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body',
                 'func-l_hip', 'func-l_hip_ant', 'func-l_hip_post', 'func-l_hip_body',
                 'func-r_hip', 'func-r_hip_ant', 'func-r_hip_post', 'func-r_hip_body']
    elif masktype == 'hip_subfields':
        masks = ['CA1_mask_B_func', 'CA23DG_mask_B_func', 'posthipp_mask_B_func', 'subiculum_mask_B_func']
        # masks = ['CA1_mask_B_func', 'CA1_mask_L_func', 'CA1_mask_R_func',
        #          'CA23DG_mask_B_func', 'CA23DG_mask_L_func', 'CA23DG_mask_R_func',
        #          'posthipp_mask_B_func', 'posthipp_mask_L_func', 'posthipp_mask_R_func',
        #          'subiculum_mask_B_func', 'subiculum_mask_L_func', 'subiculum_mask_R_func']
    elif masktype == 'b_ifg_subregions':
        masks = ['b_ifg_full_func', 'b_pars_opercularis_func', 'b_pars_orbitalis_func', 'b_pars_triangularis_func']
    elif masktype == 'searchlight':
        cluster_dir = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/sl_masks/'
        masks = []
        for f in os.listdir(cluster_dir):
            if f.endswith('.nii') or f.endswith('.nii.gz'):
                name = f.replace('.nii.gz', '').replace('.nii', '')
                masks.append(name)

    else:
        raise ValueError('Invalid mask type')

    comp_file = comparison
    if comparison == 'AC':
        comp_file = 'ABC'

    if drop_run is not None:
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comp_file}_items_drop{drop_run}.txt',
            unpack=True
        )
    else:
    # Load phase, run, triad, and item data
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comp_file}_items.txt',
            unpack=True
    )

    ### Directories ###
    subjdir = os.path.join(expdir, f'sub-{sbj}')
    betadir = os.path.join(subjdir, 'betaseries')
    #resultdir = os.path.join(expdir, f'integration_prepost/prepost_{comparison}')
    temp_result_dir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/'
    resultdir = os.path.join(temp_result_dir, f'integration_prepost/prepost_{comparison}')
    out_dir = os.path.join(resultdir, f'sub-{sbj}')
    os.makedirs(out_dir, exist_ok=True)

    for mask in masks:
        print(f"running in mask {mask}")
        if masktype in ['b_hip_subregions', 'lat_hip_subregions']:
            #slmask = os.path.join(subjdir, 'transforms', f'{mask}.nii.gz')
            slmask = f"/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/hip_masks/sub-{sbj}/{mask}.nii.gz"
        elif masktype == 'hip_subfields':
            slmask = f"/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/subfield_masks/sub-{sbj}/subfield_masks/func/sub-{sbj}_{mask}.nii.gz"
        elif masktype == 'b_ifg_subregions':
            #slmask = f'/corral-repl/utexas/prestonlab/temple/freesurfer/sub-{sbj}/mri/ifg_masks/{mask}.nii.gz'
            slmask = f"{subjdir}/masks/ifg_masks/{mask}.nii.gz"
        elif masktype == 'searchlight':
            slmask = f"/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/sl_masks/sub-{sbj}/sl-{mask}.nii.gz"

        # Load fMRI data
        if comparison in ['ABC', 'AC']:
            ds = fmri_dataset(os.path.join(betadir, f'pre_post_items.nii.gz'), mask=slmask)
        else:
            ds = fmri_dataset(os.path.join(betadir, f'pre_post_{comparison}_items.nii.gz'), mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]

        # Similarity measure
        if comparison == 'AC':
            if drop_run is not None:
                measure = prepost_roi_shuffle_droprun('correlation', 1, comparison)
            else:
                measure = prepost_roi_shuffle('correlation', 1, comparison)
        else:
            if drop_run is not None:
                measure = prepost_roi_droprun('correlation', 1, comparison)
            else:
                measure = prepost_roi('correlation', 1, comparison)

        # Obtain within-pair and across-pair similarity values
        df = measure(ds)

        # Save results
        # out_file_w = os.path.join(out_dir, f"{sbj}_prepost_{comparison}_within_{mask}.txt")
        # out_file_a = os.path.join(out_dir, f"{sbj}_prepost_{comparison}_across_{mask}.txt")

        out_file_df = os.path.join(out_dir, f"{sbj}_prepost_{comparison}_{mask}_full.csv")

        # np.savetxt(out_file_w, within, fmt="%.8f")
        # np.savetxt(out_file_a, across, fmt="%.8f")
        print(f"saving file to {out_file_df}")
        df.to_csv(out_file_df)

