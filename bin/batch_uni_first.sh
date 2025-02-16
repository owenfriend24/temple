#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "batch_uni_first.sh $FM SUB"
    exit 1
fi

fmriprep_dir=$1
sub=$2


source $HOME/analysis/temple/profile

#mkdir -p ${fmriprep_dir}/sub-${sub}/univ

rm -R ${fmriprep_dir}/sub-${sub}/univ/2nd_level_out.gfeat
rm -R ${fmriprep_dir}/sub-${sub}/univ/out_run1.feat
rm -R ${fmriprep_dir}/sub-${sub}/univ/out_run2.feat
rm -R ${fmriprep_dir}/sub-${sub}/univ/out_run3.feat
rm -R ${fmriprep_dir}/sub-${sub}/univ/out_run4.feat

run_first_unis_new.sh ${fmriprep_dir} ${sub}

run_second_unis.sh ${fmriprep_dir} ${sub}
