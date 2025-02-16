#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: ppi_hpc_mean.sh freesurfer_dir fmriprep_dir subject task"
    exit 1
fi

fsdir=$1
fmdir=$2
subject=$3
task=$4

# left hippocampus 17, right 53

mkdir ${fmdir}/sub-${subject}/univ/ppi

# create bilateral hippocampal mask
mri_binarize --i ${fsdir}/sub-${subject}/mri/aparc+aseg.mgz --o $FSDIR/sub-${subject}/mri/left_hip_mask_tmp.nii.gz --match 17

mri_binarize --i $FSDIR/sub-${subject}/mri/aparc+aseg.mgz --o $FSDIR/sub-${subject}/mri/right_hip_mask_tmp.nii.gz --match 53

fslmaths $FSDIR/sub-${subject}/mri/left_hip_mask_tmp.nii.gz -add $FSDIR/sub-${subject}/mri/right_hip_mask_tmp.nii.gz $FSDIR/sub-${subject}/mri/b_hip.nii.gz

rm $FSDIR/sub-${subject}/mri/left_hip_mask_tmp.nii.gz

rm $FSDIR/sub-${subject}/mri/right_hip_mask_tmp.nii.gz

# transform mask from anatomical to functional space
antsApplyTransforms -d 3 -i $FSDIR/sub-${subject}/mri/b_hip.nii.gz -o $FSDIR/sub-${subject}/mri/b_hip_func.nii.gz -r ${fmdir}/sub-${subject}/func/sub-${subject}_task-${task}_run-01_space-T1w_boldref.nii.gz -t ${fmdir}/sub-${subject}/transforms/mask_to_func_ref_Affine.txt


# mask functional data for HPC roi
for run in 1 2 3 4; do
    
    fslmeants -i ${fmdir}/sub-${subject}/func/skullstripped_T1/sub-${subject}_task-${task}_run-0${run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz -m ${fsdir}/sub-${subject}/mri/b_hip_func.nii.gz --eig -o ${fmdir}/sub-${subject}/univ/ppi/run-${run}_eigen_hip.txt
    
done