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

cd /corral-repl/utexas/prestonlab/temple/clust_sim/gm
3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/gm/gm_binary/prob_mask.nii.gz -acf 0.505 2.274 8.43 -nodec -prefix gm_50

#cd /corral-repl/utexas/prestonlab/temple/clust_sim/b_hip
#3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_func.nii.gz -acf 0.886 2.483 1.577 -nodec -prefix hip_full
#
#cd /corral-repl/utexas/prestonlab/temple/clust_sim/b_hip_ant
#3dClustSim -mask /corral-repl/utexas/prestonlab/temple/group_masks/hip_func/b_hip_ant_func.nii.gz -acf 0.977 2.29 0.913 -nodec -prefix hip_ant

