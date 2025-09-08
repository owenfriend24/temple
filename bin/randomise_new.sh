#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 2 ]]; then
    echo "randomise_new.sh roi comp"
    exit 1
fi

roi=$1
comp=$2

if [[ $roi == 'b_hip' ]]; then
  grp_mask_path=/corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_func.nii.gz
elif [[ $roi == 'b_gray_func' ]]; then
  grp_mask_path=/corral-repl/utexas/prestonlab/temple/group_masks/gm/gm_binary/prob_mask.nii.gz
fi

mkdir -p /corral-repl/utexas/prestonlab/temple/integration_prepost/mni_${comp}/randomise_out/

randomise -i /corral-repl/utexas/prestonlab/temple//integration_prepost/mni_${comp}/${roi}/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/temple/integration_prepost/mni_${comp}/randomise_out/${roi}_cont_acc \
-d /corral-repl/utexas/prestonlab/temple/randomise_files/acc_cont.mat \
-t /corral-repl/utexas/prestonlab/temple/randomise_files/acc_cont.con \
-m $grp_mask_path \
-n 5000 -x --uncorrp


randomise -i //corral-repl/utexas/prestonlab/temple/integration_prepost/mni_${comp}/${roi}/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/temple/integration_prepost/mni_${comp}/randomise_out/${roi}_cont_age \
-d /corral-repl/utexas/prestonlab/temple/randomise_files/age_cont.mat \
-t /corral-repl/utexas/prestonlab/temple/randomise_files/age_cont.con \
-m $grp_mask_path \
-n 5000 -x --uncorrp

randomise -i /corral-repl/utexas/prestonlab/temple/integration_prepost/mni_${comp}/${roi}/group_z.nii.gz \
-o /corral-repl/utexas/prestonlab/temple/integration_prepost/mni_${comp}/randomise_out/${roi}_group_mean \
-m $grp_mask_path \
-1 \
-n 5000 -x  --uncorrp
