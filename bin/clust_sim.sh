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

mkdir -p ${fmriprep_dir}/searchlight/clust_sim_0917_new
cd ${fmriprep_dir}/searchlight/clust_sim_0917_new

#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/template/b_hip_func.nii.gz -acf 0.645774 2.459366 7.224626 -nodec -prefix ad_hip_

#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/templates/b_hip_func.nii.gz -acf 0.591844 2.46300 7.721965 -nodec -prefix child_hip_

#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/templates/b_hip_ant_func.nii.gz -acf 0.591844 2.46300 7.721965 -nodec -prefix chi_ant_

#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/templates/b_hip_ant_func.nii.gz -acf 0.645774 2.459366 7.224626 -nodec -prefix ad_ant_

#3dClustSim -mask /home1/09123/ofriend/analysis/temple/bin/templates/b_hip_ant_func_mask.nii.gz -acf 0.61880875 2.4611827 7.47329567 -nodec -prefix ant_hip_group_mask_


#3dClustSim -mask /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/group_masks/all_wb_avg_mask.nii.gz -acf 0.61880875 2.4611827 7.47329567 -nodec -prefix full_wb_
3dClustSim -mask /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/group_masks/75_masks/all_hip_ant_avg_075.nii.gz -acf 0.61880875 2.4611827 7.47329567 -nodec -prefix full_hip_75_

#cd ${fmriprep_dir}/searchlight/clust_sim_0812/brainmask_func_dilated

#3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/group_masks/adult_wb_avg_mask.nii.gz -acf 0.645774 2.459366 7.224626 -nodec -prefix ad_wb_

#3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/group_masks/child_wb_avg_mask.nii.gz -acf 0.591844 2.46300 7.721965 -nodec -prefix child_wb_



#cd ${fmriprep_dir}/searchlight/clust_sim_0812/b_hip

3dClustSim -mask /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/group_masks/75_masks/adult_hip_ant_avg_075.nii.gz -acf 0.645774 2.459366 7.224626 -nodec -prefix ad_hip_75_

3dClustSim -mask /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/group_masks/75_masks/child_hip_ant_avg_075.nii.gz -acf 0.591844 2.46300 7.721965 -nodec -prefix child_hip_75_
