#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: move_to_corral.sh fmriprep_dir"

    exit 1
fi

fmriprep_dir=$1

temple_randomise.sh ${fmriprep_dir} AB brainmask_func_dilated
temple_randomise.sh ${fmriprep_dir} AC brainmask_func_dilated
temple_randomise.sh ${fmriprep_dir} ABC brainmask_func_dilated
