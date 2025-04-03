#!/bin/env bash
#
# take MNI clusters from SL analyses and back project to subject functional space

if [[ $# -lt 1 ]]; then
    echo "Usage:  sl_masks_to_func.sh temple016 $FM AC $CORR"
    exit 1
fi

sub=$1
fmriprep_dir=$2
comp=$3
corr=$4

comp=AC
mask_dir=${fmriprep_dir}/masks/sub-${sub}/sl-${comp}_con/

mkdir -p ${mask_dir}

for mask in ${fmriprep_dir}/masks/sl_clusters/contrast_040325/${comp}/cluster_masks/*.nii.gz; do
  filename=$(basename "$mask")                     # e.g., "cluster1.nii.gz"
  maskname="${filename%%.*}"
  antsApplyTransforms -d 3 \
      -i ${mask} \
      -o ${mask_dir}/sl-${maskname}.nii.gz \
      -r ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
      -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
      -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
      -n NearestNeighbor

done

comp=AB
mask_dir=${fmriprep_dir}/masks/sub-${sub}/sl-${comp}_con/

mkdir -p ${mask_dir}

for mask in ${fmriprep_dir}/masks/sl_clusters/contrast_040325/${comp}/cluster_masks/*.nii.gz; do
  filename=$(basename "$mask")                     # e.g., "cluster1.nii.gz"
  maskname="${filename%%.*}"
  antsApplyTransforms -d 3 \
      -i ${mask} \
      -o ${mask_dir}/sl-${maskname}.nii.gz \
      -r ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
      -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
      -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
      -n NearestNeighbor

done


comp=ABC
mask_dir=${fmriprep_dir}/masks/sub-${sub}/sl-${comp}_con/

mkdir -p ${mask_dir}

for mask in ${fmriprep_dir}/masks/sl_clusters/contrast_040325/${comp}/cluster_masks/*.nii.gz; do
  filename=$(basename "$mask")                     # e.g., "cluster1.nii.gz"
  maskname="${filename%%.*}"
  antsApplyTransforms -d 3 \
      -i ${mask} \
      -o ${mask_dir}/sl-${maskname}.nii.gz \
      -r ${corr}/freesurfer/sub-${sub}/mri/out/brainmask_func_dilated.nii.gz \
      -t ${corr}/sub-${sub}/transforms/native_to_MNI_InverseWarp.nii.gz \
      -t [${corr}/sub-${sub}/transforms/native_to_MNI_Affine.txt,1] \
      -n NearestNeighbor

done