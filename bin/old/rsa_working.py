#!/usr/bin/env python

from mvpa2.misc.fsl.base import *
from mvpa2.datasets.mri import fmri_dataset
from mvpa2.measures.rsa import PDist

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
        # create full matrix with correlation distance
        rsafx = PDist(square=True)
        runs = ['pre', 'post']
        rsamask = f'{fsdir}/sub-{sub}/mri/out/{mask}.nii.gz'
        
        
        for r in ['PRE', 'POST']:
            betadir = f'{beta_data}/sub-{sub}/func/sub-{sub}_task-arrow_space-T1w_mask-gm_func_dilated_{r}_betaseries.nii.gz'
            if not os.path.exists(betadir):
                print(f"File {betadir} does not exist. Skipping...")
                continue
            
            ds = fmri_dataset(betadir, mask=rsamask)
            rs = rsafx(ds)

            # save as text file
            subjoutfile = f'{beta_data}/sub-{sub}/rdms/sub-{sub}_arrow_{r}_{mask}.txt'
            np.savetxt(subjoutfile, 1 - rs.samples, fmt="%.8f")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sub", help="subject number e.g. temple001")
    args = parser.parse_args()
    main(args.sub)
