#!/bin/bash
#
# Smooth functional data

if [[ $# -lt 4 ]]; then
    echo "Usage: temple_smooth.sh fmriprep_dir fs_dir subject task"
    exit 1
fi

export PATH=/home1/09123/ofriend/analysis/temple/bin:$PATH
source /home1/09123/ofriend/analysis/temple/profile
fmriprep_dir=$1
fs_dir=$2
subject=$3
task=$4

if [[ "$task" == "collector" ]]; then
    num_runs=4
    tag=""
elif [[ "$task" == "arrow" ]]; then
    num_runs=6
    tag=""
elif [[ "$task" == "movie" ]]; then
  num_runs=2
  tag="_movie"
else
    echo "Error: Unknown task '$task'. Must be 'collector' or 'arrow'."
    exit 1
fi

for run in $(seq 1 $num_runs); do
    echo "Smoothing run ${run}..."

    smooth_susan \
        "${fmriprep_dir}/sub-${subject}/func/skullstripped_T1/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss${tag}.nii.gz" \
        "${fs_dir}/sub-${subject}/mri/out/brainmask_func${tag}_dilated.nii.gz" \
        4 \
        "${fmriprep_dir}/sub-${subject}/func/skullstripped_T1/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz"
    
    echo "Finished smoothing run ${run}!"
    
done
