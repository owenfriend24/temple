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

module load afni

for roi in 'gm' 'b_hip' 'b_hip_ant'; do
  if [[ $roi == 'gm' ]]; then
          mask_path="${corral}/freesurfer/sub-${subject}/mri/b_gray_func.nii.gz"
  elif [[ $roi == 'b_hip' ]]; then
          mask_path="${corral}/sub-${subject}/masks/hip_masks/func-b_hip.nii.gz"
  elif [[ $roi == 'b_hip_ant' ]]; then
          mask_path="${corral}/sub-${subject}/masks/hip_masks/func-b_hip_ant.nii.gz"
  fi

  # Runs to drop per subject
  declare -A DROP_RUNS=(
      [temple023]=6
  #    [temple030]=6
  #    [temple070]=3
  #    [temple116]=5
  )

  drop_run="${DROP_RUNS[$subject]:-}"

  for run in {1..6}; do
      if [[ -n "${drop_run}" && "${run}" -eq "${drop_run}" ]]; then
          echo "Skipping subject ${subject} run ${run}"
          continue
      fi

      out_file="${corral}/clust_sim/acf/by_subject_run_${roi}_acf.txt"

      output=$(3dFWHMx -mask ${mask_path} -ACF NULL -input "${fmriprep_dir}/residuals/sub-${subject}/sub-${subject}_run-${run}_resid.nii.gz" -arith)
      acf_coefs=$(echo "$output" | tail -n 1 | awk '{print $(NF-3), $(NF-2), $(NF-1), $NF}')
      echo "$subject $run $acf_coefs" >> "$out_file"
  done
done