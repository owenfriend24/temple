#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from temple_utils import get_age_groups

def create_subject_file(subject, master_dir, comparison, mask):
    children = get_age_groups.get_children()
    adolescents = get_age_groups.get_adolescents()
    adults = get_age_groups.get_adults()
    if subject in children:
        age_group = 'child'
    elif subject in adolescents:
        age_group = 'adolescent'
    elif subject in adults:
        age_group = 'adult'
    else:
        raise ValueError('no age group assigned')


    # subject directory on tacc
    sub_dir=f'{master_dir}/sub-{subject}'

    # pull both forward and backward integration within an roi
    bwd_comp = comparison[::-1]

    comp_data = pd.DataFrame(columns=['subject', 'age_group', 'roi', 'triplet',
                                      'comparison', 'within_sim', 'across_sim', 'difference'])

    # Define masks/ROIs to pull similarity values from
    if mask == 'b_hip_subregions':
        masks = ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body']
    elif mask == 'lat_hip_subregions':
        masks = ['func-b_hip', 'func-b_hip_ant', 'func-b_hip_post', 'func-b_hip_body',
                 'func-l_hip', 'func-l_hip_ant', 'func-l_hip_post', 'func-l_hip_body',
                 'func-r_hip', 'func-r_hip_ant', 'func-r_hip_post', 'func-r_hip_body']
    elif mask == 'hip_subfields':
        masks = ['CA1_mask_B_func', 'CA23DG_mask_B_func', 'posthipp_mask_B_func', 'subiculum_mask_B_func']
        # masks = ['CA1_mask_B_func', 'CA1_mask_L_func', 'CA1_mask_R_func',
        #          'CA23DG_mask_B_func', 'CA23DG_mask_L_func', 'CA23DG_mask_R_func',
        #          'posthipp_mask_B_func', 'posthipp_mask_L_func', 'posthipp_mask_R_func',
        #          'subiculum_mask_B_func', 'subiculum_mask_L_func', 'subiculum_mask_R_func']
    elif mask == 'b_ifg_subregions':
        masks = ['b_ifg_full_func', 'b_pars_opercularis_func', 'b_pars_orbitalis_func', 'b_pars_triangularis_func']
    elif mask == 'searchlight':
        cluster_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{subject}/masks/sl_masks'
        masks = []
        for f in os.listdir(cluster_dir):
            if f.endswith('.nii') or f.endswith('.nii.gz'):
                if comparison in f:
                    name = f.replace('.nii.gz', '').replace('.nii', '')
                    masks.append(name)

    else:
        raise ValueError('Invalid mask type')

    # Process both forward and backward integration within an ROI
    for comp in [comparison, bwd_comp]:
        comp_dir = f'{master_dir}/symmetry_{comp}/'
        sub_dir = f'{comp_dir}/sub-{subject}'
        for mask in masks:
            symm_file = f'{sub_dir}/{subject}_symmetry_{comp}_{mask}_full.csv'
            symm_vals = pd.read_csv(symm_file)
            # print(f'file length: {len(prepost_vales)}')
            within_vals = symm_vals[symm_vals['comparison'] == 'within']
            across_vals = symm_vals[symm_vals['comparison'] == 'across']
            # within_filename = f'{sub_dir}/{subject}_symmetry_{comp}_within_{mask}.txt'
            # within = pd.read_csv(within_filename, sep='\t', header=None)
            #
            # across_filename = f'{sub_dir}/{subject}_symmetry_{comp}_across_{mask}.txt'
            # across = pd.read_csv(across_filename, sep='\t', header=None)

            for triad in [1, 2, 3, 4]:
                # within values are only compared within triad so it doesn't matter if we index based on triad_1 or triad_2,
                #   as both will be the same
                tri_within = within_vals[within_vals['triad_1'] == triad]

                # across triplet comparisons can have either triad_1 or triad_2 as the triad of interest (coming back to this
                #   as I refine what the baseline comparison will end up being)
                tri_across = across_vals[(across_vals['triad_1'] == triad) | (across_vals['triad_2'] == triad)]

                within_sim = np.mean(tri_within['value'])
                across_sim = np.mean(tri_across['value'])

                comp_data.loc[len(comp_data)] = [
                    subject, age_group, mask, triad, comp,
                    within_sim, across_sim, (within_sim - across_sim)
                ]
    return comp_data


def run(command):
    subprocess.run(command, shell=True)

def main(subject, master_dir, comparison, mask):
    run('source /home1/09123/ofriend/analysis/temple/profile')
    out_file = f'{master_dir}/symmetry_{comparison}/sub-{subject}/sub-{subject}_{comparison}_{mask}_master.csv'
    df = create_subject_file(subject, master_dir, comparison, mask)
    df.to_csv(out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="e.g., temple100")
    parser.add_argument("master_dir", help="where folders containing .txt files for each comparison are stored")
    parser.add_argument("comparison", help="options: AB, BC, AC, ABC")
    parser.add_argument("mask", help="mask name e.g., b_hip_subregions, hip_subfields,lat_hip_subregions etc.")
    args = parser.parse_args()
    main(args.subject, args.master_dir, args.comparison, args.mask)