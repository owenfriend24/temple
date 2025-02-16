#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: temple_randomise_hip.sh fmriprep_dir"

    exit 1
fi

fmriprep_dir=$1

temple_randomise_hip.sh ${fmriprep_dir} AB
temple_randomise_hip.sh ${fmriprep_dir} AC
temple_randomise_hip.sh ${fmriprep_dir} ABC
