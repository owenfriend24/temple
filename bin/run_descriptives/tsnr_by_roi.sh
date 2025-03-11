#!/bin/env bash

if [[ $# -lt 2 ]]; then
    echo "Usage: tsnr_by_roi data_dir subject masktype.  MAKE SURE YOU HAVE ALREADY RUN tsnr_maps.sh"
    exit 1
fi

fmdir=$1
subject=$2
masktype=$3

func_dir=${fmdir}/sub-${subject}/func
tsnr_dir=${func_dir}/tsnr
output_csv="${func_dir}/tsnr/tsnr_values_${masktype}.csv"

# Create CSV file with headers
echo "run,mask,tsnr,nvoxs" > ${output_csv}

# Define mask paths
if [[ "$masktype" == "b_hip_subregions" ]]; then
    masks=(
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-b_hip.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-b_hip_ant.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-b_hip_body.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-b_hip_post.nii.gz"
    )
elif [[ "$masktype" == "lat_hip_subregions" ]]; then
    masks=(
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-l_hip.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-l_hip_ant.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-l_hip_body.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-l_hip_post.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-r_hip.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-r_hip_ant.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-r_hip_body.nii.gz"
        "${fmdir}/sub-${subject}/masks/hip_masks/warp-r_hip_post.nii.gz"
    )
elif [[ "$masktype" == "hip_subfields" ]]; then
    masks=(
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_CA1_mask_B_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_CA23DG_mask_B_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_posthipp_mask_B_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_subiculum_mask_B_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_CA1_mask_L_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_CA23DG_mask_L_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_posthipp_mask_L_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_subiculum_mask_L_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_CA1_mask_R_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_CA23DG_mask_R_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_posthipp_mask_R_func.nii.gz"
        "${fmdir}/ashs/masks/sub-${subject}/subfield_masks/func/sub-${subject}_subiculum_mask_R_func.nii.gz"
    )

else
    echo "no valid masktype provided"
    exit 1
fi

# Loop over runs and masks
for run in 1 2 3 4 5 6; do
    tsnr_file="${tsnr_dir}/arrow_run_${run}_tsnr_map.nii.gz"

    for mask in "${masks[@]}"; do
        tsnr_value=$(fslstats ${tsnr_file} -k ${mask} -M)
        nvoxs=$(fslstats ${mask} -V | awk '{print $1}')  # Extracts voxel count
        echo "${run},${mask},${tsnr_value},${nvoxs}" >> ${output_csv}
    done
done

echo "Saved tSNR values to ${output_csv}"