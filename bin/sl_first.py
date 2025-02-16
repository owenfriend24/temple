#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import numpy as np
import nibabel as nib
from nilearn.image import iter_img
from nilearn.decoding import SearchLight
from scipy.stats import zscore
from scipy.spatial.distance import pdist
import random
import pandas as pd
from sklearn.metrics import pairwise_distances

def main(fs_dir, beta_dir, sub):
    beta_path = (f'{beta_dir}/sub-{sub}/func/sub-{sub}_arrow_all_betaseries.nii.gz')
    data = nib.load(beta_path).get_fdata()

    mask_path = (f'{fs_dir}/sub-{sub}/mri/out/brainmask_func_dilated.nii.gz')
    mask = nib.load(mask_path).get_fdata()

    radius = 3
    num_perms = 1000

    data_flat = data.reshape(data.shape[3], -1)
    mask_flat = mask.reshape(-1)

    # initialize empty z map with same shape as brain mask/original data
    z_map = np.zeros_like(mask)
    p_map = np.zeros_like(mask)

    # Iterate through the flattened beta image
    for voxel_idx, voxel_value in enumerate(mask_flat):
        # Check if the voxel is within the mask
        if voxel_value != 0:
            # Extract subset of data within the searchlight sphere
            x, y, z = np.unravel_index(voxel_idx, mask.shape)

            sub_data = data[x-radius:x+radius+1, y-radius:y+radius+1, z-radius:z+radius+1]
            sub_data = sub_data.reshape(sub_data.shape[3], -1)

            # omit voxels that are in mask but not functional data (slightly different bounding at bottom of brain; 
            # eventually will want to make specific functional mask)
            if sub_data.shape[1] != 0:

                pre_data = sub_data[:36]
                post_data = sub_data[36:]

                rdm_pre = pairwise_distances(pre_data, metric='correlation')
                rdm_post = pairwise_distances(post_data, metric='correlation')

                rdm_pre = pd.DataFrame(1 - rdm_pre)
                rdm_post = pd.DataFrame(1 - rdm_post)

                # just get rid of the 1's on the diagonal to avoid divide by zero warnings when fisher transforming; 
                # not actually using these diagonal values anyway
                epsilon = 0.000001
                np.fill_diagonal(rdm_pre.values, epsilon)
                np.fill_diagonal(rdm_post.values, epsilon)


                rdm_diff = np.subtract(np.arctanh(rdm_post), np.arctanh(rdm_pre))

                within_triad_sim = []
                across_triad_sim = []

                n = len(rdm_diff)
                for x in range(n):
                    for y in range(x+1, n):
                        obs_diff = rdm_diff[x][y]
                        triad_x = (x % 12) // 3
                        triad_y = (y % 12) // 3

                        # omit comparisons within the same run
                        if (x // 12) != (y // 12):

                            # if items are in the same triad (so AB and AC similarity together)
                            if triad_x == triad_y:
                                within_triad_sim.append(obs_diff)

                            else:
                                across_triad_sim.append(obs_diff)


                within_triad_sim = np.array(within_triad_sim)
                across_triad_sim = np.array(across_triad_sim)

                obs_within_avg = np.nanmean(within_triad_sim)
                obs_across_avg = np.nanmean(across_triad_sim)
                obs_stat = obs_within_avg - obs_across_avg



                # now need to compare obs_stat to a null distribution using a permutation test
                n_within = len(within_triad_sim)
                n_across = len(across_triad_sim)
                n_total = n_within + n_across

                randstat = []
                for perm in range(num_perms):
                    randcat = np.concatenate([within_triad_sim, across_triad_sim])
                    random.shuffle(randcat)
                    within_shuff = randcat[0:n_within]
                    across_shuff = randcat[n_within:n_total]
                    randstat.append(np.mean(within_shuff) - np.mean(across_shuff))

                # extract z value for this sphere:
                z_val = (obs_stat - np.mean(randstat))/np.std(randstat)
                z_map[x, y, z] = z_val

                p = np.sum(randstat > obs_stat) / num_perms
                p_map[x, y, z] = p


    z_map_img = nib.Nifti1Image(z_map, affine=None)
    nib.save(z_map_img, f'{beta_dir}/sub-{sub}func/sub-{sub}_within_triad_similarity_Zmap.nii.gz')

    p_map_img = nib.Nifti1Image(p_map, affine=None)
    nib.save(p_map_img, f'{beta_dir}/sub-{sub}func/sub-{sub}_within_triad_similarity_Pmap.nii.gz')

          
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="freesurfer directory")
    parser.add_argument("beta_dir", help="path to directory with betaseries image")
    parser.add_argument("sub", help="subject number; include full templeXXX")
    args = parser.parse_args()
    main(args.fs_dir, args.beta_dir, args.sub)
