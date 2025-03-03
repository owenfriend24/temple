#!/bin/env bash
#
# create ifg masks with freesurfer output

if [[ $# -lt 2 ]]; then
    echo "Usage: fs_ifg.sh freesurfer_dir sub"
    exit 1
fi

fs_input_dir=$1
sub=$2
fs_output_dir=$3

mkdir -p $fs_output_dir/sub-${sub}/mri/ifg_masks

mri_binarize --i $fs_input_dir/sub-$sub/mri/aparc+aseg.mgz --o $fs_output_dir/sub-${sub}/mri/ifg_masks/b_pars_opercularis.nii.gz \
--match 1018 2018

mri_binarize --i $fs_input_dir/sub-$sub/mri/aparc+aseg.mgz --o $fs_output_dir/sub-${sub}/mri/ifg_masks/b_pars_orbitalis.nii.gz \
--match 1019 2019

mri_binarize --i $fs_input_dir/sub-$sub/mri/aparc+aseg.mgz --o $fs_output_dir/sub-${sub}/mri/ifg_masks/b_pars_triangularis.nii.gz \
--match 1020 2020

mri_binarize --i $fs_input_dir/sub-$sub/mri/aparc+aseg.mgz --o $fs_output_dir/sub-${sub}/mri/ifg_masks/b_ifg_full.nii.gz \
--match 1018 1019 1020 2018 2019 2020

for mask in $fs_output_dir/sub-$sub/mri/ifg_masks/*.nii.gz; do
  mask_basename=$(basename "$mask" .nii.gz)
  output_file="${fs_output_dir}/sub-${sub}/mri/ifg_masks/${mask_basename}_func.nii.gz"
  antsApplyTransforms -d 3 -i $mask -n NearestNeighbor \
-o $output_file -t [/corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/mask_to_func_ref_Affine.txt] \
-r $fs_input_dir/sub-$sub/mri/out/brainmask_func_dilated.nii.gz

done