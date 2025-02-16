#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 2 ]]; then
    echo "mni_hip_masks.sh fmriprep_dir sub"
    exit 1
fi

fmriprep_dir=$1
sub=$2

antsApplyTransforms -d 3  -i ${fmriprep_dir}/searchlight/mni_AC/brainmask_func_dilated/cluster_hip/corr_age_increasing.nii.gz -n NearestNeighbor -o ${fmriprep_dir}/sub-${sub}/transforms/hip_increasing_mask.nii.gz -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${fmriprep_dir}/searchlight/prepost_AC/${sub}_prepost_brainmask_func_dilated_z.nii.gz

#antsApplyTransforms -d 3  -i ${fmriprep_dir}/searchlight/mni_AC/brainmask_func_dilated/cluster_masks/ifg_adult_over_mask.nii.gz -n NearestNeighbor -o ${fmriprep_dir}/sub-${sub}/transforms/ifg_mask1.nii.gz -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${fmriprep_dir}/searchlight/prepost_AC/${sub}_prepost_brainmask_func_dilated_z.nii.gz

#antsApplyTransforms -d 3  -i ${fmriprep_dir}/searchlight/mni_AC/brainmask_func_dilated/cluster_masks/ifg_age_increasing.nii.gz -n NearestNeighbor -o ${fmriprep_dir}/sub-${sub}/transforms/ifg_mask2.nii.gz -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${fmriprep_dir}/searchlight/prepost_AC/${sub}_prepost_brainmask_func_dilated_z.nii.gz
