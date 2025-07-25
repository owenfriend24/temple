#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "batch_uni_first.sh $FM SUB"
    exit 1
fi

fmriprep_dir=$1
sub=$2
corr=$3


source $HOME/analysis/temple/profile

#mkdir -p ${fmriprep_dir}/sub-${sub}/univ

edit_first_uni.sh $HOME/analysis/temple/univ/boundary_sensitivity_template.fsf ${corr}/sub-${subject}/univ/ ${subject} ${corr}

run_first_unis_new.sh ${fmriprep_dir} ${sub} ${corr}

run_second_unis.sh ${fmriprep_dir} ${sub}
