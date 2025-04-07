#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: manual_ashs_transforms.sh subject"

    exit 1
fi

sub=$1
base_dir=$2

ash_dir=${base_dir}/sub-${sub}/

# save original output with incorrect transformation
mv ${ash_dir}/final ${ash_dir}/final_orig

mkdir ${ash_dir}/final

# create new warp/affine files for T1 to T2 transformation
ANTS 3 -m CC[${ash_dir}/coronal.nii.gz, ${ash_dir}/mprage.nii.gz,1,5] \
-t SyN[0.25] -r Gauss[3,0] -o T1_to_T2_manual_ \
-i 30x90x20 --use-Histogram-Matching \
--number-of-affine-iterations 10000x10000x10000x10000x10000 --MI-option 32x16000

# create the new manual masks from the multiatlas directory
antsApplyTransforms -d 3 -i ${ash_dir}/multiatlas/fusion/lfseg_corr_nogray_left.nii.gz \
-o ${ash_dir}/final/sub-${sub}_left_lfseg_corr_nogray.nii.gz \
-r ${ash_dir}/mprage.nii.gz \
-t ${ash_dir}/T1_to_T2_manual_InverseWarp.nii.gz \
-t [${ash_dir}/T1_to_T2_PR_manual.txt,1] \
-n NearestNeighbor

antsApplyTransforms -d 3 -i ${ash_dir}/multiatlas/fusion/lfseg_corr_nogray_right.nii.gz \
-o ${ash_dir}/final/sub-${sub}_right_lfseg_corr_nogray.nii.gz \
-r ${ash_dir}/mprage.nii.gz \
-t ${ash_dir}/T1_to_T2_manual_InverseWarp.nii.gz \
-t [${ash_dir}/T1_to_T2_PR_manual.txt,1] \
-n NearestNeighbor


subfield_masks.sh $sub $base_dir