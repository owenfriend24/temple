#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 2 ]]; then
    echo "randomise_new.sh fmriprep_dir comp"
    exit 1
fi

roi=$1
comp=$2

if [[ $roi == 'b_hip' ]]; then
  grp_mask_path=/corral-repl/utexas/prestonlab/group_masks/hip_func/b_hip_func.nii.gz
elif [[ $roi == 'gm' ]]; then
  grp_mask_path=/corral-repl/utexas/prestonlab/group_masks/gm/group_gm_mask.nii.gz
fi

mkdir -p /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/randomise_out/

randomise -i /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/${roi}/group_z.nii.gz \
-o /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/randomise_out/${roi}_cont_acc \
-d /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/acc_cont.mat \
-t /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/acc_cont.con \
-m $grp_mask_path \
-n 5000 -x --uncorrp


randomise -i /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/b_hip/group_z.nii.gz \
-o /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/randomise_out/cont_age \
-d /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/age_cont.mat \
-t /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/age_cont.con \
-m $grp_mask_path \
-n 5000 -x --uncorrp

randomise -i /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/b_hip/group_z.nii.gz \
-o /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost/mni_${comp}/randomise_out/group_mean \
-m $grp_mask_path \
-1 \
-n 5000 -x  --uncorrp
