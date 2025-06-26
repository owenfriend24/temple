#!/bin/bash
#


if [[ $# -lt 2 ]]; then
    echo "Usage: run_first_levels.sh fmriprep_dir subject"
    exit 1
fi

fmriprep_dir=$1
subject=$2
analysis_type=$3

echo "running second level analysis for sub ${subject}..."

if [ "$analysis_type" == "inverse" ]; then
    feat "${fmriprep_dir}/sub-${subject}/ppi_inverse/sub-${subject}-ppi_second_level.fsf"
else
    feat "${fmriprep_dir}/sub-${subject}/ppi/sub-${subject}-ppi_inverse_second_level.fsf"
fi

