#!/bin/env bash
#
# transform searchlight outputs to template space for across participant comparisons

if [[ $# -lt 1 ]]; then
    echo "Usage:  sl_to_mni.sh sub fmriprep_dir comp roi measure (e.g., sl_to_mni.sh temple024 FM AB b_gray_func prepost)"
    exit 1
fi

sub=$1
fmriprep_dir=$2
comp=$3
roi=$4
measure=$5

mkdir -p ${fmriprep_dir}/integration_prepost/mni_${comp}/

antsApplyTransforms -d 3 \
-i "${fmriprep_dir}/integration_prepost/${measure}_${comp}/${roi}/${sub}_${measure}_${comp}_${roi}_z.nii.gz" \
-o "${fmriprep_dir}/integration_prepost/mni_${comp}/${sub}_${measure}_${comp}_${roi}_mni.nii.gz" \
-r "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" \
-t "/corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" \
-t "/corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/native_to_MNI_Affine.txt"
#


# old version
#WarpImageMultiTransform 3 "${fmriprep_dir}/integration_prepost/${measure}_${comp}/sub-${sub}/${sub}_${measure}_${comp}_${roi}_z.nii.gz"\
# "${fmriprep_dir}/integration_prepost/mni_${comp}/${measure}/${sub}_${comp}_${roi}_mni.nii.gz" -R \
# "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" \
# "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" \
# "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt"

#fslmaths "${fmriprep_dir}/integration_prepost/mni_${comp}/${measure}/${sub}_${comp}_${roi}_mni.nii.gz" -mas \
#/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain_mask.nii.gz \
#"${fmriprep_dir}/integration_prepost/mni_${comp}/${measure}/${sub}_${comp}_${roi}_mni.nii.gz"




