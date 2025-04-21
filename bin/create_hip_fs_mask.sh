#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 2 ]]; then
    echo "create_gm_mask.sh freesurfer_dir sub"
    exit 1
fi

fs_dir=$1
sub=$2

mri_dir=${fs_dir}/sub-${sub}/mri/

mri_convert ${mri_dir}/aparc+aseg.mgz ${mri_dir}/aparcaseg.nii.gz
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 17 -uthr 17 -bin ${mri_dir}/l_hip
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 53 -uthr 54 -bin ${mri_dir}/r_hip
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 9 -uthr 13 -bin ${mri_dir}/l_subco
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 17 -uthr 17 -bin ${mri_dir}/l_hip
fslmaths  ${mri_dir}/l_hip -add ${mri_dir}/r_hip -bin ${mri_dir}/fs_hip_mask

antsApplyTransforms -d 3 \
    -i ${mri_dir}/fs_hip_mask.nii.gz \
    -o ${mri_dir}/fs_hip_mask_func.nii.gz \
    -r ${mri_dir}/out/brainmask_func_dilated.nii.gz \
    -n NearestNeighbor