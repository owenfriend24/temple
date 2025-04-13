#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: subfield_masks.sh subject ashs_dir"

    exit 1
fi

sub=$1
a_dir=$2

sub_dir=$a_dir/sub-${sub}


mkdir -p ${sub_dir}/subfield_masks
mkdir -p ${sub_dir}/subfield_masks/func
mkdir -p ${sub_dir}/subfield_masks/anat
sf_dir=${sub_dir}/subfield_masks

#left hemisphere
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 1 -uthr 1 -bin ${sf_dir}/anat/sub-${sub}_CA1_mask_L.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 2 -uthr 2 -bin ${sf_dir}/anat/sub-${sub}_subiculum_mask_L.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 3 -uthr 3 -bin ${sf_dir}/anat/sub-${sub}_posthipp_mask_L.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz -thr 4 -uthr 4 -bin ${sf_dir}/anat/sub-${sub}_CA23DG_mask_L.nii.gz

# right hemisphere
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 1 -uthr 1 -bin ${sf_dir}/anat/sub-${sub}_CA1_mask_R.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 2 -uthr 2 -bin ${sf_dir}/anat/sub-${sub}_subiculum_mask_R.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 3 -uthr 3 -bin ${sf_dir}/anat/sub-${sub}_posthipp_mask_R.nii.gz
fslmaths ${sub_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz -thr 4 -uthr 4 -bin ${sf_dir}/anat/sub-${sub}_CA23DG_mask_R.nii.gz

# create bilateral masks
fslmaths ${sf_dir}/anat/sub-${sub}_CA1_mask_L.nii.gz -add ${sf_dir}/anat/sub-${sub}_CA1_mask_R.nii.gz ${sf_dir}/anat/sub-${sub}_CA1_mask_B.nii.gz
fslmaths ${sf_dir}/anat/sub-${sub}_subiculum_mask_L.nii.gz -add ${sf_dir}/anat/sub-${sub}_subiculum_mask_R.nii.gz ${sf_dir}/anat/sub-${sub}_subiculum_mask_B.nii.gz
fslmaths ${sf_dir}/anat/sub-${sub}_posthipp_mask_L.nii.gz -add ${sf_dir}/anat/sub-${sub}_posthipp_mask_R.nii.gz ${sf_dir}/anat/sub-${sub}_posthipp_mask_B.nii.gz
fslmaths ${sf_dir}/anat/sub-${sub}_CA23DG_mask_L.nii.gz -add ${sf_dir}/anat/sub-${sub}_CA23DG_mask_R.nii.gz ${sf_dir}/anat/sub-${sub}_CA23DG_mask_B.nii.gz

#ANTS 3 -m MI[/corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/brainmask_func_dilated.nii.gz, \
#$CORR/ashs/masks/sub-${sub}/subfield_masks/anat/sub-${sub}_CA1_mask_B.nii.gz,1,32] \
#-o $CORR/ashs/masks/sub-${sub}/subfield_masks/anat/T2_to_func_affine_ --rigid-affine true -i 0

for mask in ${sf_dir}/anat/sub-temple*; do
  mask_basename=$(basename "$mask" .nii.gz)
  output_file="${sf_dir}/func/${mask_basename}_func.nii.gz"
  antsApplyTransforms -d 3 -i $mask -n NearestNeighbor \
-o $output_file \
-r /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sourcedata/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz



#-r /corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/brainmask_func_dilated.nii.gz
##-t [$CORR/ashs/masks/sub-${sub}/subfield_masks/anat/T2_to_func_affine_Affine.txt] \


done