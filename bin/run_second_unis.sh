#!/bin/bash
#


if [[ $# -lt 2 ]]; then
    echo "Usage: run_first_levels.sh fmriprep_dir subject"
    exit 1
fi

fmriprep_dir=$1
subject=$2



echo "running second level analysis for sub ${subject}..."
feat "${fmriprep_dir}/sub-${subject}/univ/sub-${subject}-uni_second_level.fsf"
