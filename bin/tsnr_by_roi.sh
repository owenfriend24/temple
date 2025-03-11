#!/bin/env bash

if [[ $# -lt 2 ]]; then
    echo "Usage: tsnr_by_roi data_dir subject"
    exit 1
fi

fmdir=$1
subject=$2

mkdir ${fmdir}/sub-${subject}/func/tsnr/
func_dir=${fmdir}/sub-${subject}/func

for run in 1 2 3 4 5 6; do
  fslmaths ${func_dir}/sub-${subject}_task-arrow_run-0${run}_space-T1w_desc-preproc_bold.nii.gz -mas \
  ${fmdir}/freesurfer/sub-${subject}/mri/out/brainmask_func_dilated.nii.gz \
  ${func_dir}/tsnr/arrow_run_${run}_stripped.nii.gz

  fslmaths ${func_dir}/tsnr/arrow_run_${run}_stripped.nii.gz -Tmean ${func_dir}/tsnr/arrow_run_${run}_meanfunc.nii.gz
  fslmaths ${func_dir}/tsnr/arrow_run_${run}_stripped.nii.gz -Tstd ${func_dir}/tsnr/arrow_run_${run}_stdfunc.nii.gz
  fslmaths ${func_dir}/tsnr/arrow_run_${run}_meanfunc.nii.gz -div ${func_dir}/tsnr/arrow_run_${run}_stdfunc.nii.gz \
  ${func_dir}/tsnr/arrow_run_${run}_tsnr_map.nii.gz

  fslstats ${func_dir}/tsnr/arrow_run_${run}_tsnr_map.nii.gz -M >> ${func_dir}/tsnr/tsnr_values.txt

done