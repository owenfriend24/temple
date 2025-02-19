#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: ashs_test.sh subject"

    exit 1
fi

sub=$1

export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=24
export ASHS_ROOT=/scratch/09123/ofriend/ashs

#$ASHS_ROOT/bin/ashs_main.sh -L -I sub-temple108 -a $CORR/ASHS_DG_CA23_combined/ -g $FM/sub-temple108/anat/sub-temple108_T1w_ss.nii.gz -f $FM/../../sub-temple108/anat/coronal_prep.nii.gz -w $FM/sub-temple108/left_only/


$ASHS_ROOT/bin/ashs_main.sh -I sub-${sub} -a $ASHS_ROOT/test_atlas/ -g $ASHS_ROOT/new/sub-${sub}/sub-${sub}_T1w_ss.nii.gz -f $ASHS_ROOT/sub-${sub}/new/sub-${sub}_desc-preproc_T2w.nii.gz -w $ASHS_ROOT/new/sub-${sub}/
