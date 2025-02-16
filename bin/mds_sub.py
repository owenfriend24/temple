#!/usr/bin/env python
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import os
import os
import nibabel as nib
from nilearn import image
from nilearn import masking
from scipy.stats import pearsonr
from sklearn.metrics import pairwise_distances
import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
def run_com(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)

def merge_betas(sub):
    if sub in ['temple030', 'temple023']:
    	run_com(f'fslmerge -t $FM/sub-{sub}/betaseries/run4_items.nii.gz $FM/sub-{sub}/betaseries/betaOUT_run-4*')
    	run_com(f'fslmerge -t $FM/sub-{sub}/betaseries/run5_items.nii.gz $FM/sub-{sub}/betaseries/betaOUT_run-5*')
    else:
        run_com(f'fslmerge -t $FM/sub-{sub}/betaseries/run4_items.nii.gz $FM/sub-{sub}/betaseries/betaOUT_run-4*')
        run_com(f'fslmerge -t $FM/sub-{sub}/betaseries/run5_items.nii.gz $FM/sub-{sub}/betaseries/betaOUT_run-5*')
        run_com(f'fslmerge -t $FM/sub-{sub}/betaseries/run6_items.nii.gz $FM/sub-{sub}/betaseries/betaOUT_run-6*')

def sub_post(fmriprep_dir, sub, mask):
    #mask_path = os.path.join(fmriprep_dir, f'sub-{sub}', 'brainmask_func_dilated.nii.gz')
   # thresholded_mask_img = image.math_img("img > 0", img=mask_img)
    mask_path = mask
    mask_img = image.load_img(mask_path)
    thresholded_mask_img = image.math_img("img > 0", img=mask_img)
    beta_path = os.path.join(fmriprep_dir, f'sub-{sub}', 'betaseries', f'run4_items.nii.gz')
    R = masking.apply_mask(beta_path, thresholded_mask_img)
    rdm = pairwise_distances(R, metric='correlation')
    r_4 = pd.DataFrame(1 - rdm)
    
    beta_path = os.path.join(fmriprep_dir, f'sub-{sub}', 'betaseries', f'run5_items.nii.gz')
    R = masking.apply_mask(beta_path, thresholded_mask_img)
    rdm = pairwise_distances(R, metric='correlation')
    r_5 = pd.DataFrame(1 - rdm)
    
    if sub in ['temple030', 'temple023']:
        return r_4, r_5
    else:
        beta_path = os.path.join(fmriprep_dir, f'sub-{sub}', 'betaseries', f'run6_items.nii.gz')
        R = masking.apply_mask(beta_path, thresholded_mask_img)
        rdm = pairwise_distances(R, metric='correlation')
        r_6 = pd.DataFrame(1 - rdm)

        return r_4, r_5, r_6

def main(fmriprep_dir, sub, mask, mask_label):
    if sub in ['temple030', 'temple023']:
        run_com('source /home1/09123/ofriend/analysis/temple/profile')
        average_df = pd.DataFrame()
        merge_betas(sub)
        r_4, r_5 = sub_post(fmriprep_dir, sub, mask)

        dfs = [r_4, r_5]

        for df in dfs:
            if average_df.empty:
                average_df = df.copy()
            else:
                average_df += df
        average_df /= len(dfs)
        average_df.to_csv(f'{fmriprep_dir}/sub-{sub}/betaseries/avg_post_dists_{mask_label}.csv')
    else:
        run_com('source /home1/09123/ofriend/analysis/temple/profile')
        average_df = pd.DataFrame()
        merge_betas(sub)
        sub_post(fmriprep_dir, sub, mask)
        r_4, r_5, r_6 = sub_post(fmriprep_dir, sub, mask)

        dfs = [r_4, r_5, r_6]

        for df in dfs:
            if average_df.empty:
                average_df = df.copy()
            else:
                average_df += df
        average_df /= len(dfs)
        average_df.to_csv(f'{fmriprep_dir}/sub-{sub}/betaseries/avg_post_dists_{mask_label}.csv')
    

          
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fmriprep_dir", help="fmriprep derivatives directory")
    parser.add_argument("sub", help="subject number; include full templeXXX")
    parser.add_argument("mask", help="full path to mask")
    parser.add_argument("mask_label", help="mask label for output")
    args = parser.parse_args()
    main(args.fmriprep_dir, args.sub, args.mask, args.mask_label)

