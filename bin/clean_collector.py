#!/usr/bin/env python
#
# fix collector runs to correctly reflect triads and objects

from pathlib import Path
import pandas as pd
import os
import argparse

def main(data_dir, sub):
    func_dir = data_dir + f'/sub-{sub}/func/'
    ref = pd.read_table(func_dir + f'sub-{sub}_task-arrow_run-04_events.tsv')

    c1 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-01_events.tsv')
    c2 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-02_events.tsv')
    c3 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-03_events.tsv')
    c4 = pd.read_table(func_dir + f'sub-{sub}_task-collector_run-04_events.tsv')


    ref_table = pd.DataFrame(columns = ['object', 'triad', 'position'])
    for triad in [1.0,2.0,3.0,4.0]:
        for pos in [1.0,2.0,3.0]:
            o = (ref[(ref['triad'] == triad) & (ref['position'] == pos)])['object'].values[0]
            ref_table.loc[len(ref_table)] = [o, triad, pos]
    
    run = 1
    for col_run in [c1, c2, c3, c4]:
        for index, row in col_run.iterrows():
            look = ref_table[ref_table['object'] == row['object']]
            if len(look) > 0:
                col_run.at[index, 'position'] = look.position.values[0]
                col_run.at[index, 'triad'] = look.triad.values
            
            
            out = (func_dir + f'sub-{sub}_task-collector_run-0{run}_events_fixed.tsv')
            col_run.to_csv(out, sep='\t', index=False)
        print('fixed run ' + str(run))
        run += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="fmriprep directory")
    parser.add_argument("sub", help="subject number e.g. temple001")
    args = parser.parse_args()
    main(args.data_dir, args.sub)
    
  
