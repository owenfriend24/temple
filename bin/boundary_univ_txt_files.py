#!/usr/bin/env python
#
# generate .txt files without headers for motion confounds or for collector behavioral data

from pathlib import Path
import pandas as pd
import os
import argparse

def main(sub, file_type, weight_by_accuracy):

    func_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/func/'
    out_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/univ/'
    os.makedirs(out_dir, exist_ok=True)

    if file_type == 'motion' or file_type == 'both':
        conf1 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-01_desc-confounds_timeseries.tsv')
        conf2 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-02_desc-confounds_timeseries.tsv')
        conf3 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-03_desc-confounds_timeseries.tsv')
        conf4 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-04_desc-confounds_timeseries.tsv')
        
        col_names = ['csf', 'white_matter', 'trans_x', 'trans_y', 'trans_z', 'rot_x', 'rot_y', 'rot_z', 'framewise_displacement', 'dvars']

        # dont need derivatives for FD, DVARS
        for c in range(8):
            col_names.append(col_names[c] + '_derivative1')
        
        run = 1
        for conf in [conf1, conf2, conf3, conf4]:
            u_conf = conf[col_names]
            u_conf = u_conf.fillna(0)
            out = f'{out_dir}/sub-{sub}_task-collector_run-0{run}_formatted_confounds.txt'
            u_conf.to_csv(out, sep='\t', header=False, index=False)
            run += 1
    if weight_by_accuracy:
        trip_master = pd.read_csv('/corral-repl/utexas/prestonlab/temple/beh/remember_by_triad.csv')
        trip_ref = trip_master[trip_master['subject'] == sub]

    if file_type == 'collector' or file_type == 'both':
        c1 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-01_events_fixed.tsv')
        c2 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-02_events_fixed.tsv')
        c3 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-03_events_fixed.tsv')
        c4 = pd.read_table(f'{func_dir}/sub-{sub}_task-collector_run-04_events_fixed.tsv')

        run = 1
        for col_run in [c1, c2, c3, c4]:
            # third items in triad
            third_items = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
            ref = col_run[col_run['position'] == 3]

            print(ref)

            for index, row in ref.iterrows():
                if weight_by_accuracy:
                    trip_id = row['triad']
                    trip_lookup = trip_ref[trip_ref['correct_triad'] == trip_id]
                    item_weight = trip_lookup['accuracy'].values[0]
                else:
                    item_weight = 1.0
                third_items.loc[len(third_items)] = [row['onset'], row['duration'], item_weight]
            out = f'{out_dir}/sub-{sub}_task-collector_run-{run}_third_items.txt'
            third_items.to_csv(out, sep='\t', header=False, index=False)
            
            # first items in triad
            first_items = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
            ref = col_run[col_run['position'] == 1]
            for index, row in ref.iterrows():
                if weight_by_accuracy:
                    trip_id = row['triad']
                    trip_lookup = trip_ref[trip_ref['correct_triad'] == trip_id]
                    item_weight = trip_lookup['accuracy'].values[0]
                else:
                    item_weight = 1.0
                first_items.loc[len(first_items)] = [row['onset'], row['duration'], item_weight]
            out = f'{out_dir}/sub-{sub}_task-collector_run-{run}_first_items.txt'
            first_items.to_csv(out, sep='\t', header=False, index=False)
            
            others = pd.DataFrame(columns = ['onset', 'duration', 'weight'])
            ref = col_run[(col_run['position'] != 1) & (col_run['position'] != 3)]
            for index, row in ref.iterrows():
                if weight_by_accuracy:
                    trip_id = row['triad']
                    trip_lookup = trip_ref[trip_ref['correct_triad'] == trip_id]
                    item_weight = trip_lookup['accuracy'].values[0]
                else:
                    item_weight = 1.0
                others.loc[len(others)] = [row['onset'], row['duration'], item_weight]
            out = f'{out_dir}/sub-{sub}_task-collector_run-{run}_others.txt'
            others.to_csv(out, sep='\t', header=False, index=False)
            run += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sub", help="subject number e.g. temple001")
    parser.add_argument("file_type", help="motion, collector, or both")
    parser.add_argument("--weight_by_accuracy", action="store_true",
                        help="If set, weight by accuracy (default: False)")
    args = parser.parse_args()
    main(args.sub, args.file_type, args.weight_by_accuracy)
