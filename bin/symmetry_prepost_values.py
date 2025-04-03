#!/usr/bin/env python

import subprocess

### import python libraries needed for the analysis ###
import numpy as N
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import sys
from random import sample
from mvpa2.datasets.mri import *
from mvpa2.mappers.detrend import *
from mvpa2.mappers.zscore import *
from mvpa2.clfs.svm import *
from mvpa2.generators.partition import *
from mvpa2.measures.base import *
from mvpa2.measures import *
from mvpa2.measures.searchlight import *
from mvpa2.misc.stats import *
from mvpa2.base.node import *
from mvpa2.clfs.meta import *
from mvpa2.clfs.stats import *
from mvpa2.featsel.base import *
from mvpa2.featsel.helpers import *
from mvpa2.generators.permutation import *
from mvpa2.generators.base import *
from mvpa2.mappers.fx import *
from mvpa2.measures.anova import *
from mvpa2.base.dataset import *
import sys
import subprocess
import numpy as np
# ignore division by zero errors for NaN values when transforming to fisher's Z
np.seterr(divide='ignore', invalid='ignore')


### import custom searchlight function ###
from symmetry_function import *
import argparse

### set up expriment info ###
if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <subject_id> <comparison> <masktype>")
    print("Example: symmetry_prepost_values.py temple016 AC b_hip_subregions")
    sys.exit(1)


### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post representational symmetry")
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("comparison", help="Comparison type (e.g., AC)")
    parser.add_argument("masktype", help="Mask type (e.g., b_hip_subregions, b_ifg_subregions)")
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()

### Main script execution ###
if __name__ == "__main__":
    args = get_args()

    ### Set up experiment info ###
    expdir = '/corral-repl/utexas/prestonlab/temple/'
    #expdir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/'
    sbj = args.subject_id
    comparison = args.comparison
    masktype = args.masktype
    drop_run = args.drop_run
    if comparison in ['BA', 'CB', 'CA', 'CBA']:
        c_fwd = comparison[::-1]
    else:
        c_fwd = comparison

    if masktype == 'whole_brain':
        masks = ['brainmask_func_dilated']
    elif masktype == 'b_hip_subregions':
        masks = ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body']
    elif masktype == 'lat_hip_subregions':
        masks = ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body',
                 'func-l_hip', 'func-l_hip_ant', 'func-l_hip_post', 'func-l_hip_body',
                 'func-r_hip', 'func-r_hip_ant', 'func-r_hip_post', 'func-r_hip_body']
    elif masktype == 'hip_subfields':
        masks = ['CA1_mask_B_func', 'CA1_mask_L_func', 'CA1_mask_R_func',
                 'CA23DG_mask_B_func', 'CA23DG_mask_L_func', 'CA23DG_mask_R_func',
                 'posthipp_mask_B_func', 'posthipp_mask_L_func', 'posthipp_mask_R_func',
                 'subiculum_mask_B_func', 'subiculum_mask_L_func', 'subiculum_mask_R_func']
    elif masktype == 'b_ifg_subregions':
        masks = ['b_ifg_full_func', 'b_pars_opercularis_func', 'b_pars_orbitalis_func', 'b_pars_triangularis_func']
    elif masktype == 'searchlight':
        cluster_dir = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/sl_clusters/040325/{c_fwd}/cluster_masks'
        masks = []
        for f in os.listdir(cluster_dir):
            if f.endswith('.nii') or f.endswith('.nii.gz'):
                name = f.replace('.nii.gz', '').replace('.nii', '')
                masks.append(name)
    elif masktype == 'searchlight_contrast':
        cluster_dir = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/sl_clusters/contrast_040325/{c_fwd}/cluster_masks'
        masks = []
        for f in os.listdir(cluster_dir):
            if f.endswith('.nii') or f.endswith('.nii.gz'):
                name = f.replace('.nii.gz', '').replace('.nii', '')
                masks.append(name)

    ### searchlight information ###


    if drop_run is not None:
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{c_fwd}_items_drop{drop_run}.txt',
            unpack=True
        )
    else:
    # Load phase, run, triad, and item data
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{c_fwd}_items.txt',
            unpack=True
    )



    ### directories ###
    subjdir = f'{expdir}/sub-{sbj}/'
    betadir = subjdir + '/betaseries'
    temp_result_dir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/'
    #resultdir = expdir + f'/integration_prepost/symmetry_{comparison}/sub-{sbj}'
    resultdir = f'{temp_result_dir}/integration_prepost/symmetry_{comparison}/sub-{sbj}'

    for mask in masks:
        print(f"running in mask {mask}")
        if masktype in ['b_hip_subregions', 'lat_hip_subregions']:
            #slmask = f'{subjdir}/transforms/{mask}.nii.gz'
            slmask = f"{subjdir}/masks/hip_masks/{mask}.nii.gz"
        elif masktype == 'hip_subfields':
            slmask = f"{expdir}/ashs/masks/sub-{sbj}/subfield_masks/func/sub-{sbj}_{mask}.nii.gz"
        elif masktype == 'b_ifg_subregions':
            #slmask = f'/corral-repl/utexas/prestonlab/temple/freesurfer/sub-{sbj}/mri/ifg_masks/{mask}.nii.gz'
            slmask = f"{subjdir}/masks/ifg_masks/{mask}.nii.gz"
        elif masktype == 'searchlight':
            slmask = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/sub-{sbj}/sl-{c_fwd}/sl-{mask}.nii.gz'
        elif masktype == 'searchlight_contrast':
            slmask = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/masks/sub-{sbj}/sl-{c_fwd}_con/sl-{mask}.nii.gz'
        # load in data - need to swap order if going backward


        if c_fwd == 'ABC':
            ds = fmri_dataset(os.path.join(betadir, f'pre_post_items.nii.gz'), mask=slmask)
        else:
            ds = fmri_dataset(os.path.join(betadir, f'pre_post_{c_fwd}_items.nii.gz'), mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]

        # similarity measure
        measure = symmetry_function('correlation', 1, comparison)

        df = measure(ds)

        os.makedirs(f'{resultdir}', exist_ok=True)

        out_file_df = os.path.join(resultdir, f"{sbj}_symmetry_{comparison}_{mask}_full.csv")
        # np.savetxt(out_file_w, within, fmt="%.8f")
        # np.savetxt(out_file_a, across, fmt="%.8f")
        df.to_csv(out_file_df)

        # out_file_w = f"{resultdir}/{sbj}_symmetry_{comparison}_within_{mask}.txt"
        # out_file_a = f"{resultdir}/{sbj}_symmetry_{comparison}_across_{mask}.txt"
        # savetxt(out_file_w, within, fmt="%.8f")
        # savetxt(out_file_a, across, fmt="%.8f")