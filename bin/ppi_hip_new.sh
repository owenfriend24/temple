#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: ppi_hpc_mean.sh fmriprep_dir subject task corral_dir"
    exit 1
fi

output_dir=$1
subject=$2
task=$3

mkdir -p ${output_dir}/sub-${subject}/ppi
mkdir -p ${output_dir}/sub-${subject}/ppi_inverse

# mask functional data for HPC roi
for run in 1 2 3 4; do
    fslmeants -i /corral-repl/utexas/prestonlab/temple/sub-${subject}/func/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz \
    -m /corral-repl/utexas/prestonlab/temple/sub-${subject}/masks/hip_masks/func-b_hip.nii.gz --eig -o ${output_dir}/sub-${subject}/ppi/run-${run}_eigen_hip.txt;
    cp ${output_dir}/sub-${subject}/ppi/run-${run}_eigen_hip.txt ${output_dir}/sub-${subject}/ppi_inverse/run-${run}_eigen_hip.txt
done
