#!/bin/env bash
#
# create ifg masks with freesurfer output

if [[ $# -lt 2 ]]; then
    echo "Usage: fs_ifg.sh freesurfer_dir sub"
    exit 1
fi

FS=$1
sub=$2
mkdir -p $FS/sub-${sub}/mri/ifg_masks

mri_binarize --i $FS/sub-$sub/mri/aparc+aseg.mgz --o $FS/sub-${sub}/mri/ifg_masks/b_pars_opercularis.nii.gz \
--match 1018 2018

mri_binarize --i $FS/sub-$sub/mri/aparc+aseg.mgz --o $FS/sub-${sub}/mri/ifg_masks/b_pars_orbitalis.nii.gz \
--match 1019 2019

mri_binarize --i $FS/sub-$sub/mri/aparc+aseg.mgz --o $FS/sub-${sub}/mri/ifg_masks/b_pars_triangularis.nii.gz \
--match 1020 2020

mri_binarize --i $FS/sub-$sub/mri/aparc+aseg.mgz --o $FS/sub-${sub}/mri/ifg_masks/b_ifg_full.nii.gz \
--match 1018 1019 1020 2018 2019 2020

for mask in $FS/sub-$sub/mri/ifg_masks/*.nii.gz; do
  antsApplyTransforms -d 3 -i $mask -n NearestNeighbor \
-o func_${mask} -t [$FM/sub-$sub/transforms/mask_to_func_ref_Affine.txt] \
-r $FS/sub-$sub/mri/out/brainmask_func_dilated.nii.gz

done