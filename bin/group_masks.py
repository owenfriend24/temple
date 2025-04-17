#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
from temple_utils import get_age_groups

def run_com(command):
    subprocess.run(command, shell=True, check=True)


def group_masks(fs_dir, fmriprep_dir, age_group):
    if age_group == 'adult':
        subs = get_age_groups.get_all_subjects()
    elif age_group == 'child':
        subs = get_age_groups.get_children()
    elif age_group == 'all':
        subs = get_age_groups.get_all_subjects()
    else:
        raise ValueError("age_group must be adult, child, all")

    wb_masks = []
    hip_masks = []

    # Create MNI space masks for all subs
    for sub in subs:
        # Define paths
        wb_mask_path = f'/corral-repl/utexas/prestonlab/temple/freesurfer/sub-{sub}/mri/b_gray_func.nii.gz'
        mni_mask_path = f'{fmriprep_dir}/sub-{sub}/masks/gm_mni.nii.gz'
        func_mni_path = '/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz'
        func_hip_mask_path = f'{fmriprep_dir}/sub-{sub}/masks/func-b_hip.nii.gz'
        mni_hip_mask_path = f'{fmriprep_dir}/sub-{sub}/masks/func-b_hip_mni.nii.gz'
        
        wb_masks.append(mni_mask_path)
        hip_masks.append(mni_hip_mask_path)

        # Transform whole brain mask into MNI functional space
        run_com(f'antsApplyTransforms -d 3 -i {wb_mask_path} -n NearestNeighbor -o {mni_mask_path} '
               f'-t [/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/native_to_MNI_Warp.nii.gz] '
               f'-t [/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/native_to_MNI_Affine.txt] '
               f'-r {func_mni_path}')
        
        # Transform hippocampal mask into MNI functional space
        run_com(f'antsApplyTransforms -d 3 -i {func_hip_mask_path} -n NearestNeighbor -o {mni_hip_mask_path} '
                f'-t [/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/native_to_MNI_Warp.nii.gz] '
                f'-t [/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/native_to_MNI_Affine.txt] '
                f'-r {func_mni_path}')

    # Aggregate whole brain masks
    merge_path = f'{fmriprep_dir}/group_masks/{age_group}_wb_merged.nii.gz'
    run_com(f'fslmerge -t {merge_path} ' + ' '.join(wb_masks))

    # Take average of masks
    ad_avg = f'{fmriprep_dir}/group_masks/{age_group}_wb_avg.nii.gz'
    run_com(f'fslmaths {merge_path} -Tmean {ad_avg}')

    # Threshold masks
    ad_wb_mask = f'{fmriprep_dir}/group_masks/{age_group}_wb_avg_mask.nii.gz'
    run_com(f'fslmaths {ad_avg} -thr 0.75 -bin {ad_wb_mask}')

    # Repeat the same process for hippocampal masks
    merge_path = f'{fmriprep_dir}/group_masks/{age_group}_hip_ant_merged.nii.gz'
    run_com(f'fslmerge -t {merge_path} ' + ' '.join(hip_masks))

    ad_avg = f'{fmriprep_dir}/group_masks/{age_group}_hip_ant_avg.nii.gz'
    run_com(f'fslmaths {merge_path} -Tmean {ad_avg}')

    ad_hip_mask = f'{fmriprep_dir}/group_masks/{age_group}_hip_ant_avg_mask.nii.gz'
    run_com(f'fslmaths {ad_avg} -thr 0.75 -bin {ad_hip_mask}')

def main(fs_dir, fmriprep_dir, age_group):
    # Source the environment profile
    run_com('source /home1/09123/ofriend/analysis/temple/profile')
    group_masks(fs_dir, fmriprep_dir, age_group)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="Freesurfer directory")
    parser.add_argument("fmriprep_dir", help="fMRIPrep derivatives directory")
    parser.add_argument("age_group", help="Age group ('adult' or 'child')")
    args = parser.parse_args()
    main(args.fs_dir, args.fmriprep_dir, args.age_group)
