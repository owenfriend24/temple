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

## RSA
#cd /corral-repl/utexas/prestonlab/temple/clust_sim/gm
#3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/gm/gm_binary/prob_mask.nii.gz -acf 0.498 2.413 8.441 -nodec -prefix gm_50
#
#cd /corral-repl/utexas/prestonlab/temple/clust_sim/b_hip
#3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_func.nii.gz -acf 0.878 2.489 1.873 -nodec -prefix hip_full
#
#cd /corral-repl/utexas/prestonlab/temple/clust_sim/b_hip_ant
#3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_ant_func.nii.gz -acf 0.975 2.298 0.931 -nodec -prefix hip_ant

# UNIV-BOUNDARY
cd /corral-repl/utexas/prestonlab/temple/clust_sim/gm
3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/gm/gm_binary/prob_mask.nii.gz -acf 0.520 2.405 8.276 -nodec -prefix gm_50_univ_boundary

cd /corral-repl/utexas/prestonlab/temple/clust_sim/b_hip
3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_func.nii.gz -acf 0.859 2.546 2.125 -nodec -prefix hip_full_univ_boundary

# PPI
cd /corral-repl/utexas/prestonlab/temple/clust_sim/gm
3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/gm/gm_binary/prob_mask.nii.gz -acf 0.520 2.400 8.310 -nodec -prefix gm_50_PPI

cd /corral-repl/utexas/prestonlab/temple/clust_sim/b_hip
3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_func.nii.gz -acf 0.8777 2.511 1.871 -nodec -prefix hip_full_PPI