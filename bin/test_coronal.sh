#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: test_coronal.sh subject"

    exit 1
fi

sub=$1

N4BiasFieldCorrection -i $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w.nii.gz -o $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_corr.nii.gz

bet $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_corr.nii.gz $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_coronal.nii.gz -f 0.01
