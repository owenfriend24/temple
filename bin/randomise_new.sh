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

randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}/symmetry/group_z_${comp}.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}/symmetry/randomise_out/parametric_age_ \
-d ${fmriprep_dir}/randomise/age_parametric.mat \
-t ${fmriprep_dir}/randomise/age_parametric.con \
-n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/integration_prepost/mni_${comp}/symmetry/group_z_${comp}.nii.gz \
-o ${fmriprep_dir}/integration_prepost/mni_${comp}/symmetry/randomise_out/grouped_age_ \
-d ${fmriprep_dir}/randomise/age_grouped.mat \
-t ${fmriprep_dir}/randomise/age_grouped.con \
-n 5000 -x  --uncorrp