#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: copy_ashs.sh ashs_dir subject"

    exit 1
fi

ashs_dir=$1
sub=$2
#mkdir ${ashs_dir}/sub-${sub}

cp /corral-repl/utexas/prestonlab/temple/sub-${sub}/anat/sub-${sub}_desc-preproc_T2w.nii.gz ${ashs_dir}/sub-${sub}/

#cp /corral-repl/utexas/prestonlab/temple/sub-${sub}/anat/sub-${sub}_T1w_ss.nii.gz ${ashs_dir}/sub-${sub}/
