#!/bin/bash
#
# Usage:
#   timeseries_acf.sh corral subject fmriprep_dir roi type(boundary|ppi|ppi_inverse) ppi_roi(optional)
#
# Notes:
# - roi can be: gm | b_hip | b_hip_ant | both
# - If roi is "both" (or anything else unrecognized), the script runs for both gm and b_hip.


if [[ $# -lt 5 ]]; then
    echo "Usage: timeseries_acf.sh corral subject fmriprep_dir roi type(boundary|ppi|ppi_inverse) ppi_roi(optional)"
    exit 1
fi

corral="$1"
subject="$2"
fmriprep_dir="$3"
roi_arg="${4:-both}"
type="$5"
ppi_roi="${6:-}"

module load afni

# Determine ROI list: default/base is both gm and b_hip
declare -a ROIS_TO_RUN
case "${roi_arg}" in
  gm|b_hip|b_hip_ant)
    ROIS_TO_RUN=("${roi_arg}")
    ;;
  both|*)
    ROIS_TO_RUN=("gm" "b_hip")
    ;;
esac

# Base directory by type
case "${type}" in
  boundary)
    base="${fmriprep_dir}/sub-${subject}/univ/"
    ;;
  ppi)
    base="${fmriprep_dir}/sub-${subject}/univ/ppi"
    ;;
  ppi_inverse)
    base="${fmriprep_dir}/sub-${subject}/univ/ppi_inverse"
    ;;
  *)
    echo "Unknown type: ${type}. Must be boundary | ppi | ppi_inverse"
    exit 1
    ;;
esac

for roi in "${ROIS_TO_RUN[@]}"; do
    # Mask path per ROI
    case "${roi}" in
      gm)
        mask_path="${corral}/freesurfer/sub-${subject}/mri/b_gray_func.nii.gz"
        ;;
      b_hip)
        mask_path="${corral}/sub-${subject}/masks/hip_masks/func-b_hip.nii.gz"
        ;;
      b_hip_ant)
        mask_path="${corral}/sub-${subject}/masks/hip_masks/func-b_hip_ant.nii.gz"
        ;;
      *)
        echo "Unknown ROI: ${roi}"
        exit 1
        ;;
    esac

    # Output file per ROI
    out_file="${corral}/clust_sim/acf/by_subject_run_${roi}_${type}_acf.txt"
    mkdir -p "$(dirname "${out_file}")"

    for run in {1..4}; do
        if [[ "${type}" == 'boundary' ]]; then
            res_img="/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-${subject}/univ/out_run${run}.feat/stats/res4d.nii.gz"
        else
            # ppi or ppi_inverse require ppi_roi
            if [[ -z "${ppi_roi}" ]]; then
                echo "Error: type '${type}' requires ppi_roi argument."
                exit 1
            fi
            res_img="/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-${subject}/univ/${type}/${ppi_roi}_out_run${run}.feat/stats/res4d.nii.gz"
        fi

        # Compute ACF coefficients
        output=$(3dFWHMx -mask "${mask_path}" -ACF NULL -input "${res_img}" -arith)
        acf_coefs=$(echo "$output" | tail -n 1 | awk '{print $(NF-3), $(NF-2), $(NF-1), $NF}')

        echo "$subject $run $acf_coefs" >> "${out_file}"
        echo "Wrote ACF for sub-${subject} run ${run} ROI=${roi} -> ${out_file}"
    done
done
