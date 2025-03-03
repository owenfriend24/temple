#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 3 ]]; then
    echo "mni_hip_masks.sh fmriprep_dir sub corall_dir"
    exit 1
fi

fmriprep_dir=$1
sub=$2
corr=$3

mkdir -p $FS/sub-${sub}/hip_masks

for mask in b_hip b_hip_ant b_hip_body b_hip_tail b_hip_post; do

#antsApplyTransforms -d 3  -i /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz -n NearestNeighbor -o ${fmriprep_dir}/sub-${sub}/transforms/${mask}.nii.gz -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${fmriprep_dir}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${fmriprep_dir}/searchlight/prepost_AC/${sub}_prepost_brainmask_func_dilated_z.nii.gz


#WarpImageMultiTransform 3 /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz \
#${corr}/sub-${sub}/transforms/warp-${mask}.nii.gz \
#-R ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
#-i ${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt \
#${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz

WarpImageMultiTransform 3 /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz \
$FS/sub-${sub}/mri/hip_masks/warp-${mask}.nii.gz \
-R ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
-i ${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt \
${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz


#antsApplyTransforms -d 3  -i /work/09123/ofriend/ls6/wr/mni_rois/${mask}.nii.gz -n NearestNeighbor -o ${corr}/sub-${sub}/transforms/fs_func_${mask}.nii.gz -t [${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz] -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt, 1] -r ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz

done
