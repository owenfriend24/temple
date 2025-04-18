#!/bin/env bash
#
# cluster simulations for preliminary age group RS analyses

if [[ $# -lt 1 ]]; then
    echo "Usage: clust_sim.sh fmriprep_dir"
    exit 1
fi

fmriprep_dir=$1

module load afni
export OMP_NUM_THREADS=None

mkdir -p ${fmriprep_dir}/searchlight/clust_sim
cd ${fmriprep_dir}/searchlight/clust_sim

3dClustSim -mask ${fmriprep_dir}/group_masks/all_wb_avg_mask.nii.gz-acf 0.506715994 2.40899271 8.45713334 -nodec -prefix mni_gm_group_full_
#
3dClustSim -mask ${fmriprep_dir}/group_masks/all_hip_avg_mask.nii.gz -acf 0.506715994 2.40899271 8.45713334 -nodec -prefix mni_hip_group_ull_
#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/templates/gm_mni/gray_17_masked.nii.gz -acf 0.506715994 2.40899271 8.45713334 -nodec -prefix mni_gm_full_
#
#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/templates/b_hip_func.nii.gz -acf 0.506715994 2.40899271 8.45713334 -nodec -prefix mni_gm_hip_full_

#cd ${fmriprep_dir}/searchlight/clust_sim_0812/brainmask_func_dilated

#3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/group_masks/adult_wb_avg_mask.nii.gz -acf 0.645774 2.459366 7.224626 -nodec -prefix ad_wb_

#3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/group_masks/child_wb_avg_mask.nii.gz -acf 0.591844 2.46300 7.721965 -nodec -prefix child_wb_



#cd ${fmriprep_dir}/searchlight/clust_sim_0812/b_hip

