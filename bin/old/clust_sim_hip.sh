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
cd ${fmriprep_dir}/searchlight/clust_sim_hip

#3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/sub-temple016/transforms/b_hip.nii.gz -acf 0.641050 2.454359 7.356880 -iter 2000 -nodec -prefix ad_out

#3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/sub-temple029/transforms/b_hip.nii.gz -acf 0.646152 2.454213 8.071233 -iter 2000 -nodec -prefix ten_out

3dClustSim -mask /scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/sub-temple041/transforms/b_hip.nii.gz -acf 0.587425 2.432855 7.539238 -iter 2000 -nodec -prefix sev_out
