#!/bin/env bash
#
# create bilateral hippocampus mask with freesurfer output

if [[ $# -lt 1 ]]; then
    echo "Usage: fs_hpc.sh sub"
    exit 1
fi

sub=$1

mri_binarize --i $FS/sub-$sub/mri/aparc+aseg.mgz --o $FS/sub-$sub/mri/out/left_hip_mask.nii.gz --match 17
mri_binarize --i $FS/sub-$sub/mri/aparc+aseg.mgz --o $FS/sub-$sub/mri/out/right_hip_mask.nii.gz --match 53
fslmaths $FS/sub-$sub/mri/out/left_hip_mask.nii.gz -add $FS/sub-$sub/mri/out/right_hip_mask.nii.gz $FS/sub-$sub/mri/out/b_hip.nii.gz

antsApplyTransforms -d 3 -i $FS/sub-$sub/mri/out/b_hip.nii.gz -n NearestNeighbor -o $FS/sub-$sub/mri/out/b_hip_func.nii.gz -t [$FM/sub-$sub/transforms/mask_to_func_ref_Affine.txt] -r $FM/sub-$sub/func/sub-${sub}_task-arrow_run-01_space-T1w_desc-brain_mask.nii.gz

antsApplyTransforms -d 3 -i $FS/sub-$sub/mri/out/right_hip_mask.nii.gz -n NearestNeighbor -o $FS/sub-$sub/mri/out/right_hip_func.nii.gz -t [$FM/sub-$sub/transforms/mask_to_func_ref_Affine.txt] -r $FM/sub-$sub/func/sub-${sub}_task-arrow_run-01_space-T1w_desc-brain_mask.nii.gz

antsApplyTransforms -d 3 -i $FS/sub-$sub/mri/outfs_hpc.shleft_hip_mask.nii.gz -n NearestNeighbor -o $FS/sub-$sub/mri/out/left_hip_func.nii.gz -t [$FM/sub-$sub/transforms/mask_to_func_ref_Affine.txt] -r $FM/sub-$sub/func/sub-${sub}_task-arrow_run-01_space-T1w_desc-brain_mask.nii.gz