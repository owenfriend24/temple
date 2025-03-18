#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 2 ]]; then
    echo "randomise_new.sh fmriprep_dir comp"
    exit 1
fi

fmriprep_dir=$1
comp=$2

source $HOME/analysis/temple/rsa/bin/activate

randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}_shuffle/prepost/group_z.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}_shuffle/prepost/randomise_out/grouped_age_ \
-d ${fmriprep_dir}/integration_prepost/randomise/age_grouped.mat \
-t ${fmriprep_dir}/integration_prepost/randomise/age_grouped.con \
-m /home1/09123/ofriend/analysis/temple/bin/templates/gm_mni/gray_17_masked.nii.gz \
-n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}_shuffle/prepost/child_group_z.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}_shuffle/prepost/randomise_out/child_parametric_age_ \
-d ${fmriprep_dir}/integration_prepost/randomise/age_param_child.mat \
-t ${fmriprep_dir}/integration_prepost/randomise/age_param_child.con \
-m /home1/09123/ofriend/analysis/temple/bin/templates/gm_mni/gray_17_masked.nii.gz \
-n 5000 -x  --uncorrp


randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}_shuffle/prepost/adult_group_z.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}_shuffle/prepost/randomise_out/adult_z_ \
-m /home1/09123/ofriend/analysis/temple/bin/templates/gm_mni/gray_17_masked.nii.gz \
-1 \
-n 5000 -x  --uncorrp