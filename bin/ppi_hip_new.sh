#!/bin/bash

if [[ $# -lt 4 ]]; then
    echo "Usage: ppi_hpc_mean.sh fmriprep_dir subject task corral_dir"
    exit 1
fi

fmdir=$1
subject=$2
task=$3
corr=$4


mkdir -p ${fmdir}/sub-${subject}/univ/ppi




# mask functional data for HPC roii
for run in 1 2 3 4; do
    
    fslmeants -i ${corr}/sub-${subject}/func/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz -m ${corr}/sub-${subject}/transforms/warp-b_hip.nii.gz --eig -o ${fmdir}/sub-${subject}/univ/ppi/run-${run}_eigen_hip.txt
    
done
