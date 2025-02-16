#!/bin/env bash
#
# cluster simulations for preliminary age group RS analyses

if [[ $# -lt 1 ]]; then
    echo "Usage:  sl_masks_to_func.sh temple016 $FM AC adult_IFG_AC_mask"
    exit 1
fi

sub=$1
fmriprep_dir=$2
comp=$3
maskname=$4


antsApplyTransforms -d 3  -i ${fmriprep_dir}/searchlight/mni_${comp}/brainmask_func_dilated/cluster_masks/${maskname}.nii.gz -n NearestNeighbor -o ${fmriprep_dir}/sub-${sub}/transforms/${maskname}.nii.gz -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${fmriprep_dir}/searchlight/prepost_AC/${sub}_prepost_brainmask_func_dilated_z.nii.gz
