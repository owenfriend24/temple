#!/bin/bash
#

if [[ $# -lt 2 ]]; then
    echo "Usage: temple_acf.sh corral subject fmriprep_dir"
    exit 1
fi

corral="$1"
subject="$2"
fmriprep_dir="$3"
roi="$4"
type="$5"

module load afni
out_file="${corral}/clust_sim/acf/by_subject_run_${roi}_${type}_acf.txt"

if [[ $roi == 'gm' ]]; then
        mask_path="${corral}/freesurfer/sub-${subject}/mri/b_gray_func.nii.gz"
elif [[ $roi == 'b_hip' ]]; then
        mask_path="${corral}/sub-${subject}/masks/hip_masks/func-b_hip.nii.gz"
elif [[ $roi == 'b_hip_ant' ]]; then
        mask_path="${corral}/sub-${subject}/masks/hip_masks/func-b_hip_ant.nii.gz"
fi

if [[ $type == 'boundary' ]]; then
        base="${fmriprep_dir}/sub-${subject}/univ/"
elif [[ $type == 'ppi' ]]; then
        base="${fmriprep_dir}/sub-${subject}/univ/ppi"
elif [[ $type == 'ppi_inverse' ]]; then
        base="${fmriprep_dir}/sub-${subject}/univ/ppi_inverse"
fi


# NEED TO UPDATE FOR COLLECTOR
declare -A DROP_RUNS=(
    [temple023]=6
    [temple030]=6
    [temple070]=3
    [temple116]=5
)

drop_run="${DROP_RUNS[$subject]:-}"

for run in {1..4}; do
    if [[ -n "${drop_run}" && "${run}" -eq "${drop_run}" ]]; then
        echo "Skipping subject ${subject} run ${run}"
        continue
    fi

    if [[ $type == 'boundary' ]]; then
        res_img="/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-${subject}/univ/out_run${run}/stats/res4d.nii.gz"
    else
        res_img="/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-${subject}/univ/${roi}_out_run${run}/stats/res4d.nii.gz"
    fi

    output=$(3dFWHMx -mask ${mask_path} -ACF NULL -input "${res_img}" -arith)
    acf_coefs=$(echo "$output" | tail -n 1 | awk '{print $(NF-3), $(NF-2), $(NF-1), $NF}')
    echo "$subject $run $acf_coefs" >> "$out_file"
done
