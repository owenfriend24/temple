#!/usr/bin/env python
#
# generate .txt files without headers for motion confounds or for collector behavioral data

from pathlib import Path
import pandas as pd
import os
import argparse


def main(data_dir, file_type, sub, out_dir):

    func_dir = data_dir + f'/sub-{sub}/func/'
    
    if file_type == 'motion' or file_type == 'both':
        conf1 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-01_desc-confounds_timeseries.tsv')
        conf2 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-02_desc-confounds_timeseries.tsv')
        conf3 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-03_desc-confounds_timeseries.tsv')
        conf4 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-04_desc-confounds_timeseries.tsv')
        
        col_names = ['csf', 'white_matter', 'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'framewise_displacement', 'dvars']
        for c in range(8):
            col_names.append(col_names[c] + '_derivative1')
        
        run = 1
        for conf in [conf1, conf2, conf3, conf4]:
            u_conf = conf[col_names]
            u_conf = u_conf.fillna(0)
            out = (out_dir + f'/sub-{sub}_task-collector_run-0{run}_formatted_confounds.txt')
            u_conf.to_csv(out, sep='\t', header=False, index=False)
            run += 1

    if file_type == 'collector' or file_type == 'both':
        c1 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-01_events_fixed.tsv')
        c2 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-02_events_fixed.tsv')
        c3 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-03_events_fixed.tsv')
        c4 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-04_events_fixed.tsv')

        run = 1
        for col_run in [c1, c2, c3, c4]:
            # third items in triad
            third_items = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
            ref = col_run[col_run['position'] == 3]
            for index, row in ref.iterrows():
                third_items.loc[len(third_items)] = [row['onset'], row['duration'], 1.0]
            out = out_dir + f'/sub-{sub}_task-collector_run-{run}_third_items.txt'
            third_items.to_csv(out, sep='\t', header=False, index=False)
            
            # first items in triad
            first_items = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
            ref = col_run[col_run['position'] == 1]
            for index, row in ref.iterrows():
                first_items.loc[len(first_items)] = [row['onset'], row['duration'], 1.0]
            out = out_dir + f'/sub-{sub}_task-collector_run-{run}_first_items.txt'
            first_items.to_csv(out, sep='\t', header=False, index=False)
            
            others = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
            ref = col_run[(col_run['position'] != 1) & (col_run['position'] != 3)]
            for index, row in ref.iterrows():
                others.loc[len(others)] = [row['onset'], row['duration'], 1.0]
            out = out_dir + f'/sub-{sub}_task-collector_run-{run}_others.txt'
            others.to_csv(out, sep='\t', header=False, index=False)
            run += 1
        
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="main directory where subjects are located (e.g., derivatives/fmriprep/)")
    parser.add_argument("file_type", help="motion, collector, or both")
    parser.add_argument("sub", help="subject number e.g. temple001")
    parser.add_argument("out_dir", help="where to write .txt files to")
    args = parser.parse_args()
    main(args.data_dir, args.file_type, args.sub, args.out_dir)
