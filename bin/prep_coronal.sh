#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: prep_coronal.sh subject"

    exit 1
fi

sub=$1


N4BiasFieldCorrection -i $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w.nii.gz -o $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_corr.nii.gz

bet $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_corr.nii.gz $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_coronal.nii.gz -f 0.01

mkdir -p $SCRATCH/ashs/new_test/sub-${sub}

cp $SCRATCH/temple/new_prepro/sub-${sub}/anat/sub-${sub}_T2w_coronal.nii.gz $SCRATCH/ashs/new_test/sub-${sub}/coronal.nii.gz

cp $FM/sub-${sub}/anat/sub-${sub}_T1w_ss.nii.gz $SCRATCH/ashs/new_test/sub-${sub}/highres.nii.gz
