#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: move_to_corral.sh fmriprep_dir"

    exit 1
fi

fmriprep_dir=$1
sub=$2

sl_to_mni.sh ${sub} ${fmriprep_dir} AB b_hip
sl_to_mni.sh ${sub} ${fmriprep_dir} AC b_hip
sl_to_mni.sh ${sub} ${fmriprep_dir} ABC b_hip
sl_to_mni.sh ${sub} ${fmriprep_dir} AB brainmask_func_dilated
sl_to_mni.sh ${sub} ${fmriprep_dir} AC brainmask_func_dilated
sl_to_mni.sh ${sub} ${fmriprep_dir} ABC brainmask_func_dilated