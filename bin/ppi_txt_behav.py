#!/usr/bin/env python
#
# generate .txt files without headers for motion confounds or for collector behavioral data

from pathlib import Path
import pandas as pd
import os
import argparse


def main(sub, file_type):
    
    # make sure to run ppi_extract_eigen in relevant roi first

    func_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/func/'
    ppi_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/univ/ppi/'
    inverse_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/univ/ppi_inverse/'

    for directory in [ppi_dir, inverse_dir]:
        os.makedirs(directory, exist_ok=True)

    if file_type == 'motion' or file_type == 'both':
        conf1 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-01_desc-confounds_timeseries.tsv')
        conf2 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-02_desc-confounds_timeseries.tsv')
        conf3 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-03_desc-confounds_timeseries.tsv')
        conf4 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-04_desc-confounds_timeseries.tsv')
        
        col_names = ['csf', 'white_matter', 'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'framewise_displacement', 'dvars']
        for c in range(8):
            col_names.append(col_names[c] + '_derivative1')
        
        run = 1
        for conf in [conf1, conf2, conf3, conf4]:
            u_conf = conf[col_names]
            u_conf = u_conf.fillna(0)
            out = f'{ppi_dir}/sub-{sub}_task-collector_run-0{run}_formatted_confounds.txt'
            u_conf.to_csv(out, sep='\t', header=False, index=False)
            run += 1
    
    
    if file_type == 'collector' or file_type == 'both':
        c1 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-01_events_fixed.tsv')
        c2 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-02_events_fixed.tsv')
        c3 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-03_events_fixed.tsv')
        c4 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-04_events_fixed.tsv')

        run = 1
        for col_run in [c1, c2, c3, c4]:
            # boundary contrast - where is ROI demonstrating increased connectivity after boundary
            contrast = pd.DataFrame(columns = ['onset', 'duration', 'contrast'])
            for index, row in col_run.iterrows():
                if row['position'] == 1:
                    con = 1
                elif row['position']  == 3: #in [2,3]:
                    con = -1
                else:
                    con = 0
                contrast.loc[len(contrast)] = [row['onset'], row['duration'], con]
            behav_trs = contrast.onset.values.astype('int')
            out = f'{ppi_dir}/sub-{sub}_task-collector_run-0{run}_ppi_contrast.txt'
            contrast.to_csv(out, sep='\t', header=False, index=False)

            # inverse - where is ROI showing diminished connectivity following boundary
            contrast_inv = pd.DataFrame(columns = ['onset', 'duration', 'contrast'])
            for index, row in col_run.iterrows():
                if row['position'] == 1:
                    con = -1
                elif row['position'] in [2, 3]:
                    con = 0.5
                else:
                    con = 0
                contrast_inv.loc[len(contrast_inv)] = [row['onset'], row['duration'], con]
            out = f'{inverse_dir}/sub-{sub}_task-collector_run-0{run}_ppi_inverse_contrast.txt'
            contrast_inv.to_csv(out, sep='\t', header=False, index=False)
            
            # task file - 1.0 for timepoints we're interested in, 0.0 for times we're not (basically just excluding B items)
            task = pd.DataFrame(columns = ['onset', 'duration', 'contrast'])
            for index, row in col_run.iterrows():
                if row['position'] in [1, 3]:
                    con = 1
                else:
                    con = 0
                task.loc[len(task)] = [row['onset'], row['duration'], con]
            out = f'{ppi_dir}/sub-{sub}_task-collector_run-0{run}_task.txt'
            task.to_csv(out, sep='\t', header=False, index=False)
            
            run+=1
                
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sub", help="subject number e.g. temple001")
    parser.add_argument("file_type", help="motion, collector, or both")
    args = parser.parse_args()
    main(args.sub, args.file_type)