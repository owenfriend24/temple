#!/usr/bin/env python
#
# generate .txt files without headers for motion confounds or for collector behavioral data

from pathlib import Path
import pandas as pd
import os
import argparse


def main(data_dir, file_type, sub):
    out_dir = f'/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-{sub}/func/arrow_txt'
    os.makedirs(out_dir, exist_ok=True)
    func_dir = data_dir + f'/sub-{sub}/func/'
    
    if file_type == 'motion' or file_type == 'both':
        conf1 = pd.read_table(func_dir + f'/sub-{sub}_task-arrow_run-01_desc-confounds_timeseries.tsv')
        conf2 = pd.read_table(func_dir + f'/sub-{sub}_task-arrow_run-02_desc-confounds_timeseries.tsv')
        conf3 = pd.read_table(func_dir + f'/sub-{sub}_task-arrow_run-03_desc-confounds_timeseries.tsv')
        conf4 = pd.read_table(func_dir + f'/sub-{sub}_task-arrow_run-04_desc-confounds_timeseries.tsv')
        conf5 = pd.read_table(func_dir + f'/sub-{sub}_task-arrow_run-05_desc-confounds_timeseries.tsv')
        conf6 = pd.read_table(func_dir + f'/sub-{sub}_task-arrow_run-06_desc-confounds_timeseries.tsv')
        
        col_names = ['csf', 'white_matter', 'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z']
        for c in range(8):
            col_names.append(col_names[c] + '_derivative1')
        
        confs = [(conf1, 'conf1'), (conf2, 'conf2'), (conf3, 'conf3'), (conf4, 'conf4'),(conf5, 'conf5'),(conf6, 'conf6')]
        
        for conf, name in confs:
            run = name[-1]
            u_conf = conf[col_names]
            u_conf = u_conf.fillna(0)
            out = (out_dir + f'/sub-{sub}_task-arrow_run-0{run}_formatted_confounds.txt')
            u_conf.to_csv(out, sep='\t', header=False, index=False)
            #run += 1
            
            
        
    
    if file_type == 'arrow' or file_type == 'both':
        c1 = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-01_events.tsv')
        c2 = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-02_events.tsv')
        c3 = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-03_events.tsv')
        c4 = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-04_events.tsv')
        c5 = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-05_events.tsv')
        c6 = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-06_events.tsv')
        

        arrs = [(c1, 'c1'), (c2, 'c2'), (c3, 'c3'), (c4, 'c4'),(c5, 'c5'),(c6, 'c6')]
        for arr, name in arrs:
            run = name[-1]
            # third items in triad
            for item in range(1, 13, 1):
                items = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
                ref = arr[arr['object'] == item]
                for index, row in ref.iterrows():
                    items.loc[len(items)] = [float(row['onset']), float(row['duration']), float(1.0)]
                out = out_dir + f'/sub-{sub}_task-arrow_run-{run}_item-{item}.txt'
                items.to_csv(out, sep='\t', header=False, index=False)
            #run += 1
            
        
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="main directory where subjects are located (e.g., derivatives/fmriprep/)")
    parser.add_argument("file_type", help="motion, collector, or both")
    parser.add_argument("sub", help="subject number e.g. temple001")
    args = parser.parse_args()
    main(args.data_dir, args.file_type, args.sub)
