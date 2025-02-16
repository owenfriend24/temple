#!/usr/bin/env python
# 
# fix arrow runs to correctly reflect triads and objects

from pathlib import Path
import pandas as pd
import os
import argparse
import subprocess





def make_dir(dir):
    subprocess.run(f'mkdir -p {dir}', shell=True)

def copy_files(src, dest):
    subprocess.run(f'cp {src} {dest}', shell=True)


def main(data_dir, sub):
    func_dir = Path(data_dir) / f'sub-{sub}' / 'func'
    orig_events_dir = func_dir / 'orig_events'
        # Filtering files to exclude those containing 'preproc' or 'fsaverage' and ending with 'events.tsv'
    files_to_copy = list(func_dir.glob('*events.tsv'))
    files_to_copy = [file for file in files_to_copy if 'preproc' not in str(file) and 'fsaverage' not in str(file)]

    make_dir(orig_events_dir)
    
    # Copying the filtered files to the orig_events_dir
    for file in files_to_copy:
        copy_files(file, orig_events_dir)
    
    a1 = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-01_events.tsv')
    a2 = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-02_events.tsv')
    a3 = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-03_events.tsv')
    a4 = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-04_events.tsv')
    a5 = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-05_events.tsv')
    a6 = pd.read_table(func_dir / f'sub-{sub}_task-arrow_run-06_events.tsv')

    run = 1
    for arr_run in [a1, a2, a3, a4, a5, a6]:
        arr_run = arr_run.rename(columns = {'object':'obj_id'})
        arr_run.insert(3, 'object', 0, True)
        for index, row in arr_run.iterrows():
            arr_run.at[index, 'object'] = (row['triad'] - 1) * 3 + row['position']
        arr_run = arr_run.dropna(subset = 'object')
        out = (func_dir / f'sub-{sub}_task-arrow_run-0{run}_events.tsv')
        arr_run.to_csv(out, sep='\t', index=False)
        print('fixed run ' + str(run))
        run += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="fmriprep directory")
    parser.add_argument("sub", help="subject number e.g. temple001")
    args = parser.parse_args()
    main(args.data_dir, args.sub)

