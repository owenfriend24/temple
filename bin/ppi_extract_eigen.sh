#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: ppi_hpc_mean.sh fmriprep_dir subject task corral_dir"
    exit 1
fi

output_dir=$1
subject=$2
task=$3
roi=$4

mkdir -p "${output_dir}/sub-${subject}/ppi"
mkdir -p "${output_dir}/sub-${subject}/ppi_inverse"

if [ "$roi" == "b_hip" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/hip_masks/func-${roi}.nii.gz"
elif [ "$roi" == "sl" ]; then
    mask="/corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/sl_masks/func-${roi}.nii.gz"
else
    echo "Error: Unknown ROI '$roi'"
    exit 1
fi

# mask functional data for HPC roi
for run in 1 2 3 4; do
    fslmeants -i "/corral-repl/utexas/prestonlab/temple/sub-${subject}/func/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz" \
    -m "$mask" --eig -o "${output_dir}/sub-${subject}/ppi/run-${run}_eigen_hip.txt"
done
