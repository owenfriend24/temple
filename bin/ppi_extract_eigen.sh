#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: ppi_extract_eigen.sh subject roi"
    exit 1
fi


subject=$1
roi=$2

output_dir="/corral-repl/utexas/prestonlab/temple/sub-${subject}/univ/ppi/"
mkdir -p "${output_dir}"

if [ "$roi" == "b_hip" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/hip_masks/func-${roi}.nii.gz"
elif [ "$roi" == "b_hip_ant" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/hip_masks/func-${roi}.nii.gz"
elif [ "$roi" == "l_hip" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/hip_masks/func-${roi}.nii.gz"
elif [ "$roi" == "univ_post_hip" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/sl_masks/func-${roi}.nii.gz"
elif [ "$roi" == "sl-AC_ant" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/sl_masks/sl-AC_ant.nii.gz"
elif [ "$roi" == "sl-univ_hip" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/sl_masks/sl-univ_hip.nii.gz"
elif [ "$roi" == "sl-posthip_univ" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/sl_masks/sl-posthip_univ.nii.gz"
else
    echo "Error: Unknown ROI '$roi'"
    exit 1
fi

# mask functional data for HPC roi
for run in 1 2 3 4; do
    fslmeants -i "/corral-repl/utexas/prestonlab/temple/sub-${subject}/func/sub-${subject}_task-collector_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz" \
    -m "$mask" --eig -o "${output_dir}/run-${run}_eigen_${roi}.txt"
done
