#!/bin/env bash
#
# cluster simulations for preliminary age group RS analyses

if [[ $# -lt 1 ]]; then
    echo "Usage:  sl_to_mni.sh sub fmriprep_dir comp roi (e.g., sl_to_mni.sh temple024 FM AB brainmask_func_dilated)"
    exit 1
fi

sub=$1
fmriprep_dir=$2
comp=$3
roi=$4
mkdir -p ${fmriprep_dir}/integration_prepost/mni_${comp}
#WarpImageMultiTransform 3 "${fmriprep_dir}/searchlight/prepost_${comp}_symm/${sub}_symm_${roi}_z.nii.gz" "${fmriprep_dir}/searchlight/mni_${comp}_symm/${sub}_${comp}_symm_${roi}_mni.nii.gz" -R "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt"

WarpImageMultiTransform 3 "${fmriprep_dir}/integration_prepost/prepost_${comp}/sub-${sub}/${sub}_prepost_${roi}_z.nii.gz" "${fmriprep_dir}/integration_prepost/mni_${comp}/${sub}_${comp}_${roi}_mni.nii.gz" -R "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" "corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" "corral-repl/utexas/prestonlab/temple/sub-${sub}/transforms/native_to_MNI_Affine.txt"

#WarpImageMultiTransform 3 "${fmriprep_dir}/searchlight/mni_masks/b_hip/${sub}_bhip_mask.nii.gz" "${fmriprep_dir}/searchlight/mni_masks/b_hip/${sub}_bhip_mask_mni.nii.gz" -R "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt"

#WarpImageMultiTransform 3 "${fmriprep_dir}/searchlight/mni_masks/brainmask_func_dilated/${sub}_wb_mask.nii.gz" "${fmriprep_dir}/searchlight/mni_masks/brainmask_func_dilated/${sub}_wb_mask_mni.nii.gz" -R "/home1/09123/ofriend/analysis/temple/bin/templates/MNI152_T1_func_brain.nii.gz" "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Warp.nii.gz" "${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt"
