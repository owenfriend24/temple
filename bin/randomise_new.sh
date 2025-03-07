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

randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}/dev_z_${comp}.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}/randomise_out/child_parametric_age_ \
-d ${fmriprep_dir}/randomise/age_parametric_child_only.mat \
-t ${fmriprep_dir}/randomise/age_parametric_child_only.con \
-n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}/group_z_${comp}.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}/randomise_out/grouped_age_2_ \
-d ${fmriprep_dir}/randomise/age_grouped_2.mat \
-t ${fmriprep_dir}/randomise/age_grouped_2.con \
-n 5000 -x  --uncorrp