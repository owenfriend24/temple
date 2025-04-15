#!/bin/bash
#


if [[ $# -lt 2 ]]; then
    echo "Usage: temple_acf.sh fmriprep_dir subject"
    exit 1
fi

fmriprep_dir="$1"
subject="$2"
module load afni
out_file="${fmriprep_dir}/acf/sorted_acf.txt"

for run in {1..6}; do
    output=$(3dFWHMx -mask "/corral-repl/utexas/prestonlab/temple/freesurfer/sub-${subject}/mri/out/brainmask_func_dilated.nii.gz" -ACF NULL -input "${fmriprep_dir}/sub-${subject}/betaseries/sub-${subject}_run-${run}_resid.nii.gz" -arith)
    acf_coefs=$(echo "$output" | tail -n 1 | awk '{print $(NF-3), $(NF-2), $(NF-1), $NF}')
    echo "$subject $run $acf_coefs" >> "$out_file"
done
