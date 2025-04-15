#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import numpy as np
import nibabel as nib
from scipy.io import loadmat
import sklearn.linear_model as lm

def run_com(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)

    
def format_matrix(fm_dir, sub):
    for run in [1, 2, 3, 4, 5, 6]:
        run_com(f'Vest2Text {fm_dir}/sub-{sub}/betaseries/sub-{sub}_betaL1_run-{run}.mat {fm_dir}/sub-{sub}/betaseries/sub-{sub}_betaL1_run-{run}.txt')
    
def estimate_residuals(fs_dir, fm_dir, sub):
    for run in [1, 2, 3, 4, 5, 6]:
        conf = np.loadtxt(f'{fm_dir}/sub-{sub}/func/arrow_txt/sub-{sub}_task-arrow_run-0{run}_formatted_confounds.txt')
        mat = np.loadtxt(f'{fm_dir}/sub-{sub}/betaseries/sub-{sub}_betaL1_run-{run}.txt')
        design = np.hstack((mat, conf))
        
       # func = (f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/func/sub-{sub}_task-arrow_run-0{run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz')
        func = (
            f'{fm_dir}/sub-{sub}/func/skullstripped_T1/sub-{sub}_task-arrow_run-0{run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz')
        bold = nib.load(func).get_fdata()

        mask_img = nib.load(f'{fs_dir}/sub-{sub}/mri/b_gray_func.nii.gz').get_fdata() > 0
        mask_vol = nib.load(f'{fs_dir}/sub-{sub}/mri/b_gray_func.nii.gz')

        #mask_img = nib.load(f'{fs_dir}/sub-{sub}/mri/out/brainmask_func_dilated.nii.gz').get_fdata() > 0
        #mask_vol = nib.load(f'{fs_dir}/sub-{sub}/mri/out/brainmask_func_dilated.nii.gz')
        
        data = bold[mask_img].T
        model = lm.LinearRegression()
        model.fit(design, data)
        resid = data - model.predict(design)
    

        out_data = np.zeros([*mask_img.shape, resid.shape[0]])
        out_data[mask_img, :] = resid.T
        new_img = nib.Nifti1Image(out_data, mask_vol.affine, mask_vol.header)
        nib.save(new_img, f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-{sub}/betaseries/sub-{sub}_run-{run}_resid.nii.gz')
        
        
def main(fs_dir, fm_dir, sub):
    run_com('source /home1/09123/ofriend/analysis/temple/profile')
    #run_com(f'cd {fm_dir}/sub-{sub}/betaseries')
    format_matrix(fm_dir, sub)
    estimate_residuals(fs_dir, fm_dir, sub)
    #run_com(f'temple_acf.sh $FM {sub}')

          
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="freesurfer directory")
    parser.add_argument("fm_dir", help="fmriprep derivatives directory")
    parser.add_argument("sub", help="subject number; include full templeXXX")
    args = parser.parse_args()
    main(args.fs_dir, args.fm_dir, args.sub)

