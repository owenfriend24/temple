#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 3 ]]; then
    echo "create_hip_masks.sh fmriprep_dir sub corall_dir"
    exit 1
fi

fmriprep_dir=$1
sub=$2
corr=$3

mkdir -p ${corr}/sub-${sub}/masks/qa_masks/

for mask in 11m 14c 14r 25 32pl b_erc b_phc b_prc; do

  antsApplyTransforms -d 3 \
    -i /scratch/09123/ofriend/qa_masks/${mask}.nii.gz \
    -o ${corr}/sub-${sub}/masks/qa_masks/func-${mask}.nii.gz \
    -r ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
    -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
    -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
    -n NearestNeighbor

done

#mkdir -p ${fmriprep_dir}/masks/hip_masks/sub-${sub}/

#l_hip l_hip_ant l_hip_body l_hip_tail l_hip_post \
#r_hip r_hip_ant r_hip_body r_hip_tail r_hip_post; do

#for mask in b_hip b_hip_ant b_hip_body b_hip_tail b_hip_post; do
#
#
#  antsApplyTransforms -d 3 \
#    -i /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz \
#    -o ${fmriprep_dir}/masks/hip_masks/sub-${sub}/func-${mask}.nii.gz \
#    -r ${corr}/sourcedata/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
#    -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
#    -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
#    -n NearestNeighbor
#
#
#done


#mkdir -p ${corr}/sub-${sub}/masks/sl_masks/

#l_hip l_hip_ant l_hip_body l_hip_tail l_hip_post \
#r_hip r_hip_ant r_hip_body r_hip_tail r_hip_post; do

#for mask in abc_interaction_hip ac_dlpfc_interaction ac_dmpfc_age_inc \
#ac_hip_age_dec ac_hip_age_inc ac_ifg_age_inc; do

#for mask in AB_mpfc_mask AB_precuneus_mask AC_dlpfc_mask AC_l_hip_ant_mask AC_parietal_mask AC_r_hip_ant_mask AC_r_hip_body_mask; do
#
#  antsApplyTransforms -d 3 \
#    -i /work/09123/ofriend/ls6/temple/backups/integration_prepost/sl_masks/${mask}.nii.gz \
#    -o ${corr}/sub-${sub}/masks/sl_masks/func-${mask}.nii.gz \
#    -r ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
#    -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
#    -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
#    -n NearestNeighbor
#
#done
#

#antsApplyTransforms -d 3  -i /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz -n NearestNeighbor -o ${fmriprep_dir}/sub-${sub}/transforms/${mask}.nii.gz -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${fmriprep_dir}/searchlight/prepost_AC/${sub}_prepost_brainmask_func_dilated_z.nii.gz

# normal
#WarpImageMultiTransform 3 /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz \
#${corr}/sub-${sub}/transforms/warp-${mask}.nii.gz \
#-R ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
#-i ${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt \
#${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz

#WarpImageMultiTransform 3 /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz \
#${corr}/sub-${sub}/masks/hip_masks/warp-${mask}.nii.gz \
#-R ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
#-i ${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt \
#${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz --use-NN



