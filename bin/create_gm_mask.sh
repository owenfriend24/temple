#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 3 ]]; then
    echo "create_gm_mask.sh freesurfer_dir sub"
    exit 1
fi

fs_dir=$1
sub=$2

mri_dir=${fs_dir}/sub-${sub}/mri/

mri_convert ${mri_dir}/aparc+aseg.mgz ${mri_dir}/aparcaseg.nii.gz
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 1000 -uthr 1035 -bin ${mri_dir}/l_ctx
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 2000 -uthr 2035 -bin ${mri_dir}/r_ctx
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 9 -uthr 13 -bin ${mri_dir}/l_subco
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 17 -uthr 17 -bin ${mri_dir}/l_hip
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 18 -uthr 18 -add ${mri_dir}/l_subco -add ${mri_dir}/l_hip -bin ${mri_dir}/l_subco
fslmaths ${mri_dir}/aparcaseg.nii.gz -thr 48 -uthr 54 -bin ${mri_dir}/r_subco
fslmaths ${mri_dir}/l_subco -add ${mri_dir}/r_subco -add ${mri_dir}/l_ctx -add ${mri_dir}/r_ctx -bin ${mri_dir}/b_gray

antsApplyTransforms -d 3 \
    -i ${mri_dir}/b_gray.nii.gz \
    -o ${mri_dir}/b_gray_func.nii.gz \
    -r ${mri_dir}/out/brainmask_func_dilated.nii.gz \
    -n NearestNeighbor