#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: batch_beta.sh fm_dir subject"
    exit 1
fi

fm_dir=$1
subject=$2

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/temple/profile

func_dir=${fm_dir}/sub-${subject}/func

mkdir ${func_dir}/orig
mkdir ${func_dir}/ss_unsmoothed

for file in ${func_dir}/*MNI152NL*; do
  rm $file
done

for file in ${func_dir}/*T1w*.nii.gz; do
  mv $file ${func_dir}/orig
done

for file in ${func_dir}/skullstripped_T1/*_ss.nii.gz; do
  mv $file ${func_dir}/ss_unsmoothed
done

for file in ${func_dir}/skullstripped_T1/*_4mm.nii.gz; do
  mv $file ${func_dir}
done

cd ${func_dir}
find . -type f -name '*bold_ss_4mm.nii.gz' -exec bash -c 'mv "$1" "${1/bold_ss_4mm/bold}"' _ {} \;

rmdir ${func_dir}/skullstripped_T1
