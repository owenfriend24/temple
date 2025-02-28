#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from temple_utils import get_age_groups, integration_indices

def create_subject_file(subject, master_dir, comparison, mask, drop_run):
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

    # sets up subject data table
    comp_data = pd.DataFrame(columns=['subject', 'age_group', 'roi', 'triplet',
                                      'comparison', 'within_sim', 'across_sim', 'difference'])

    # Define masks/ROIs to pull similarity values from
    if mask == 'b_hip_subregions':
        masks = ['warp-b_hip', 'warp-b_hip_ant', 'warp-b_hip_post', 'warp-b_hip_body']
    elif mask == 'b_ifg_subregions':
        masks = ['b_ifg_full_func', 'b_pars_opercularis_func', 'b_pars_orbitalis_func', 'b_pars_triangularis_func']
    else:
        raise ValueError('no valid mask')

    # Process both forward and backward integration within an ROI

    comp_dir = f'{master_dir}/prepost_{comparison}/'
    sub_dir = f'{comp_dir}/sub-{subject}'
    for mask in masks:
        within_filename = f'{sub_dir}/{subject}_prepost_{comparison}_within_{mask}.txt'
        within = pd.read_csv(within_filename, sep='\t', header=None)
        print(f'within length: {len(within)}')

        across_filename = f'{sub_dir}/{subject}_prepost_{comparison}_across_{mask}.txt'
        across = pd.read_csv(across_filename, sep='\t', header=None)
        print(f'across length: {len(across)}')

        for triad in [1, 2, 3, 4]:
            if drop_run is not None:
                within_indices = integration_indices.pull_within_prepost_indices_droprun(triad)
                across_indices = integration_indices.pull_across_prepost_indices_droprun(triad)
                print(f'within indices: {within_indices}')
                print(f'across indices: {across_indices}')
            else:
                within_indices = integration_indices.pull_within_prepost_indices(triad)
                across_indices = integration_indices.pull_across_prepost_indices(triad)
            within_df = within.iloc[within_indices]
            within_sim = np.mean(within_df)


            across_df = across.iloc[across_indices]
            across_sim = np.mean(across_df)

            comp_data.loc[len(comp_data)] = [
                subject, age_group, mask, triad, comparison,
                within_sim, across_sim, (within_sim - across_sim)
            ]
    return comp_data






def run(command):
    subprocess.run(command, shell=True)

def main(subject, master_dir, comparison, mask, drop_run):
    run('source /home1/09123/ofriend/analysis/temple/profile')
    out_file = f'{master_dir}/prepost_{comparison}/sub-{subject}/sub-{subject}_{comparison}_{mask}_master.csv'
    df = create_subject_file(subject, master_dir, comparison, mask, drop_run)
    df.to_csv(out_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="e.g., temple100")
    parser.add_argument("master_dir", help="where folders containing .txt files for each comparison are stored")
    parser.add_argument("comparison", help="options: AB, BC, AC")
    parser.add_argument("mask", help="mask name e.g., b_hip_subregions, b_hip_subfields, b_ifg_subregions, etc.")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")
    args = parser.parse_args()
    main(args.subject, args.master_dir, args.comparison, args.mask, args.drop_run)