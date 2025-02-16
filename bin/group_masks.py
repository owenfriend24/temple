#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse

def run_com(command):
    subprocess.run(command, shell=True, check=True)

def get_child_subs():
    kids = []
    for sub in [29, 30, 32, 33, 34, 35, 36, 38, 41, 42, 45, 51, 53, 60, 63, 64, 65, 66, 68, 69, 70, 78, 79, 82, 83, 84, 85, 92, 93]:
        kids.append(f'temple0{sub}')
    return kids

def get_adult_subs():
    adults = []
    for sub in [16, 19, 20, 22, 23, 24, 25, 37, 50, 56, 57, 58, 59, 71, 72, 73, 74, 75, 76, 87, 88, 89]:
        adults.append(f'temple0{sub}')
    return adults

def get_all_subs():
    all = []
    for sub in [16, 19, 20, 22, 23, 24, 25, 37, 50, 56, 57, 58, 59, 71, 72, 73, 74, 75, 76, 87, 88, 89, 29, 30, 32, 33, 34, 35, 36, 38, 41, 42, 45, 51, 53, 60, 63, 64, 65, 66, 68, 69, 70, 78, 79, 82, 83, 84, 85, 92, 93]:
        all.append(f'temple0{sub}')
    return all

def group_masks(fs_dir, fmriprep_dir, age_group):
    if age_group == 'adult':
        subs = get_adult_subs()
    elif age_group == 'child':
        subs = get_child_subs()
    elif age_group == 'all':
        subs = get_all_subs()
    else:
        raise ValueError("age_group must be 'adult' or 'child'")

    wb_masks = []
    hip_masks = []

    # Create MNI space masks for all subs
    for sub in subs:
        # Define paths
        wb_mask_path = f'{fs_dir}/sub-{sub}/mri/out/brainmask_func_dilated.nii.gz'
        mni_mask_path = f'{fmriprep_dir}/sub-{sub}/transforms/mni_brainmask.nii.gz'
        func_mni_path = '/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz'
        func_hip_mask_path = f'{fmriprep_dir}/sub-{sub}/transforms/warp-b_hip_ant.nii.gz'
        mni_hip_mask_path = f'{fmriprep_dir}/sub-{sub}/transforms/b_hip_ant_mni_func.nii.gz'
        
        wb_masks.append(mni_mask_path)
        hip_masks.append(mni_hip_mask_path)

        # Transform whole brain mask into MNI functional space
        #run_com(f'antsApplyTransforms -d 3 -i {wb_mask_path} -n NearestNeighbor -o {mni_mask_path} '
        #        f'-t [{fmriprep_dir}/sub-{sub}/transforms/native_to_MNI_Warp.nii.gz] '
        #        f'-t [{fmriprep_dir}/sub-{sub}/transforms/native_to_MNI_Affine.txt] '
        #        f'-r {func_mni_path}')
        
        # Transform hippocampal mask into MNI functional space
        run_com(f'antsApplyTransforms -d 3 -i {func_hip_mask_path} -n NearestNeighbor -o {mni_hip_mask_path} '
                f'-t [{fmriprep_dir}/sub-{sub}/transforms/native_to_MNI_Warp.nii.gz] '
                f'-t [{fmriprep_dir}/sub-{sub}/transforms/native_to_MNI_Affine.txt] '
                f'-r {func_mni_path}')

    # Aggregate whole brain masks
   # merge_path = f'{fmriprep_dir}/group_masks/{age_group}_wb_merged.nii.gz'
   # run_com(f'fslmerge -t {merge_path} ' + ' '.join(wb_masks))

    # Take average of masks
    #ad_avg = f'{fmriprep_dir}/group_masks/{age_group}_wb_avg.nii.gz'
    #run_com(f'fslmaths {merge_path} -Tmean {ad_avg}')

    # Threshold masks
    #ad_wb_mask = f'{fmriprep_dir}/group_masks/{age_group}_wb_avg_mask.nii.gz'
    #run_com(f'fslmaths {ad_avg} -thr 0.5 -bin {ad_wb_mask}')

    # Repeat the same process for hippocampal masks
    merge_path = f'{fmriprep_dir}/group_masks/{age_group}_hip_ant_merged.nii.gz'
    run_com(f'fslmerge -t {merge_path} ' + ' '.join(hip_masks))

    ad_avg = f'{fmriprep_dir}/group_masks/{age_group}_hip_ant_avg.nii.gz'
    run_com(f'fslmaths {merge_path} -Tmean {ad_avg}')

    ad_hip_mask = f'{fmriprep_dir}/group_masks/{age_group}_hip_ant_avg_mask.nii.gz'
    run_com(f'fslmaths {ad_avg} -thr 0.5 -bin {ad_hip_mask}')

def main(fs_dir, fmriprep_dir, age_group):
    # Source the environment profile
    run_com('source /home1/09123/ofriend/analysis/temple/profile')
    
    # Generate group masks for each age group
    group_masks(fs_dir, fmriprep_dir, 'adult')
    group_masks(fs_dir, fmriprep_dir, 'child')
    group_masks(fs_dir, fmriprep_dir, 'all')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="Freesurfer directory")
    parser.add_argument("fmriprep_dir", help="fMRIPrep derivatives directory")
    parser.add_argument("age_group", help="Age group ('adult' or 'child')")
    args = parser.parse_args()
    main(args.fs_dir, args.fmriprep_dir, args.age_group)
