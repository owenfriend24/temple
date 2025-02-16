#!/usr/bin/env python

from mvpa2.misc.fsl.base import *
from mvpa2.datasets.mri import fmri_dataset
from mvpa2.measures.rsa import PDist
from scipy.spatial.distance import pdist, squareform
import argparse
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import sys
from copy import copy
import subprocess
import numpy as np

masks = ['brainmask_func_dilated']
fsdir = '/scratch/09123/ofriend/temple/skyra_prepro/derivatives/fmriprep/sourcedata/freesurfer'
beta_data = '/corral-repl/utexas/prestonlab/temple/beta'

def main(sub):
    subprocess.run(f'mkdir {beta_data}/sub-{sub}/rdms', shell=True)
    for mask in masks:
        
        
        runs = ['pre', 'post']
        rsamask = f'{fsdir}/sub-{sub}/mri/out/{mask}.nii.gz'

        pre_beta =  f'{beta_data}/sub-{sub}/func/sub-{sub}_task-arrow_space-T1w_mask-gm_func_dilated_PRE_betaseries.nii.gz'
        post_beta =  f'{beta_data}/sub-{sub}/func/sub-{sub}_task-arrow_space-T1w_mask-gm_func_dilated_POST_betaseries.nii.gz'
    
        if not os.path.exists(pre_beta):
            print(f"Pre file does not exist. Skipping...")
            continue
        
        if not os.path.exists(post_beta):
            print(f"Post file does not exist. Skipping...")
            continue

        pre_ds = fmri_dataset(pre_beta, mask=rsamask)
        post_ds  = fmri_dataset(post_beta, mask=rsamask)

        rs = pdist(np.vstack([pre_ds.samples, post_ds.samples]), metric='correlation')

        # save as text file
        subjoutfile = f'{beta_data}/sub-{sub}/rdms/sub-{sub}_arrow_PREPOST_{mask}.txt'
        np.savetxt(subjoutfile,squareform(1-rs), fmt="%.8f")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sub", help="subject number e.g. temple001")
    args = parser.parse_args()
    main(args.sub)
