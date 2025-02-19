#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: subfield_masks.sh subject ashs_dir"

    exit 1
fi

sub=$1
a_dir=$2

sub_dir=$a_dir/sub-${sub}


mkdir -p ${sub_dir}/subfield_masks
sf_dir=${sub_dir}/subfield_masks

#left hemisphere
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 1 -uthr 1 -bin ${sf_dir}/sub-${sub}_CA1_mask_L.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 2 -uthr 2 -bin ${sf_dir}/sub-${sub}_subiculum_mask_L.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 3 -uthr 3 -bin ${sf_dir}/sub-${sub}_posthipp_mask_L.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 4 -uthr 4 -bin ${sf_dir}/sub-${sub}_CA23DG_mask_L.nii.gz

# right hemisphere
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 1 -uthr 1 -bin ${sf_dir}/sub-${sub}_CA1_mask_R.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 2 -uthr 2 -bin ${sf_dir}/sub-${sub}_subiculum_mask_R.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 3 -uthr 3 -bin ${sf_dir}/sub-${sub}_posthipp_mask_R.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 4 -uthr 4 -bin ${sf_dir}/sub-${sub}_CA23DG_mask_R.nii.gz

# create bilateral masks
fslmaths ${sf_dir}/sub-${sub}_CA1_mask_L.nii.gz -add ${sf_dir}/sub-${sub}_CA1_mask_R.nii.gz ${sf_dir}/sub-${sub}_CA1_mask_B.nii.gz
fslmaths ${sf_dir}/sub-${sub}_subiculum_mask_L.nii.gz -add ${sf_dir}/sub-${sub}_subiculum_mask_R.nii.gz ${sf_dir}/sub-${sub}_subiculum_mask_B.nii.gz
fslmaths ${sf_dir}/sub-${sub}_posthipp_mask_L.nii.gz -add ${sf_dir}/sub-${sub}_posthipp_mask_R.nii.gz ${sf_dir}/sub-${sub}_posthipp_mask_B.nii.gz
fslmaths ${sf_dir}/sub-${sub}_CA23DG_mask_L.nii.gz -add ${sf_dir}/sub-${sub}_CA23DG_mask_R.nii.gz ${sf_dir}/sub-${sub}_CA23DG_mask_B.nii.gz

