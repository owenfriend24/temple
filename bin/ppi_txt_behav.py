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
            out = (out_dir + f'sub-{sub}_task-collector_run-0{run}_formatted_confounds.txt')
            u_conf.to_csv(out, sep='\t', header=False, index=False)
            run += 1
    
    
    if file_type == 'collector' or file_type == 'both':
        c1 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-01_events_fixed.tsv')
        c2 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-02_events_fixed.tsv')
        c3 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-03_events_fixed.tsv')
        c4 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-04_events_fixed.tsv')

        run = 1
        for col_run in [c1, c2, c3, c4]:
            # boundary contrast - where is hippocampus more connected to after boundary
            contrast = pd.DataFrame(columns = ['onset', 'duration', 'contrast'])
            for index, row in col_run.iterrows():
                if row['position'] == 1:
                    con = 1
                elif row['position'] == 3:
                    con = -1
                else:
                    con = 0
                contrast.loc[len(contrast)] = [row['onset'], row['duration'], con]
            behav_trs = contrast.onset.values.astype('int')
            out = out_dir + f'sub-{sub}_task-collector_run-0{run}_ppi_contrast.txt'
            contrast.to_csv(out, sep='\t', header=False, index=False)
            
            
            
            # inverse - where is hippocampus less connected to after boundary
            contrast_inv = pd.DataFrame(columns = ['onset', 'duration', 'contrast'])
            for index, row in col_run.iterrows():
                if row['position'] == 1:
                    con = -1
                elif row['position'] == 3:
                    con = 1
                else:
                    con = 0
                contrast_inv.loc[len(contrast_inv)] = [row['onset'], row['duration'], con]
            out = out_dir + f'sub-{sub}_task-collector_run-0{run}_ppi_inverse_contrast.txt'
            contrast_inv.to_csv(out, sep='\t', header=False, index=False)
            
            # task file - 1.0 for times we're interested in, 0.0 for times we're not
            task = pd.DataFrame(columns = ['onset', 'duration', 'contrast'])
            for index, row in col_run.iterrows():
                if row['position'] == 2:
                    con = 0
                else:
                    con = 1
                task.loc[len(task)] = [row['onset'], row['duration'], con]
            out = out_dir + f'sub-{sub}_task-collector_run-0{run}_task.txt'
            task.to_csv(out, sep='\t', header=False, index=False)
            
            run+=1
                
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="main directory where subjects are located (e.g., derivatives/fmriprep/)")
    parser.add_argument("file_type", help="motion, collector, or both")
    parser.add_argument("sub", help="subject number e.g. temple001")
    parser.add_argument("out_dir", help="where to write .txt files to")
    args = parser.parse_args()
    main(args.data_dir, args.file_type, args.sub, args.out_dir)