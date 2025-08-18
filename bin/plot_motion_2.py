#!/usr/bin/env python

from pathlib import Path
import json
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
import subprocess


FD_THR = 0.5
ZDVARS_THR = 1.5          # standardized DVARS threshold
EXCLUDE_FRACTION = 1/3    # > 1/3 of TRs with BOTH metrics over threshold


def run_com(command):
    subprocess.run(command, shell=True)


def format_motion_data(sub, base_dir, out_path):
    df = pd.DataFrame(columns=['sub', 'task', 'run', 'tr', 'dvars', 'fd'])

    # arrow: runs 1..6
    for run in range(1, 7):
        task = 'arrow'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index + 1
                fd = pd.to_numeric(data.get('framewise_displacement', pd.Series([np.nan]*len(data))).iloc[index], errors='coerce')
                dvars = pd.to_numeric(data.get('std_dvars', pd.Series([np.nan]*len(data))).iloc[index], errors='coerce')
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]

    # collector: runs 1..4
    for run in range(1, 5):
        task = 'collector'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index + 1
                fd = pd.to_numeric(data.get('framewise_displacement', pd.Series([np.nan]*len(data))).iloc[index], errors='coerce')
                dvars = pd.to_numeric(data.get('std_dvars', pd.Series([np.nan]*len(data))).iloc[index], errors='coerce')
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]

    # movie: runs 1..2
    for run in range(1, 3):
        task = 'movie'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index + 1
                fd = pd.to_numeric(data.get('framewise_displacement', pd.Series([np.nan]*len(data))).iloc[index], errors='coerce')
                dvars = pd.to_numeric(data.get('std_dvars', pd.Series([np.nan]*len(data))).iloc[index], errors='coerce')
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]

    df.to_csv(out_path + 'all_motion.csv', index=False)


def _silent_plot_one_task(df, task, sub, out_path, xlim, tag):
    a_data = df[df['task'] == task]
    if a_data.empty:
        return

    run_data = {r: a_data[a_data['run'] == r] for r in sorted(a_data['run'].unique())}
    sns.set_palette("viridis")

    for measure in ['fd', 'dvars']:
        plt.figure(figsize=(15, 8))
        for run_number, run in run_data.items():
            mn = round(np.nanmean(run[measure]), 3)
            sd = round(np.nanstd(run[measure]), 3)

            if measure == 'fd':
                num_t = int((run[measure] > FD_THR).sum())
                label = f'run{run_number}: m={mn}, sd={sd}, >{FD_THR}={num_t} TRs'
            else:
                num_t = int((run[measure] > ZDVARS_THR).sum())
                label = f'run{run_number}: m={mn}, sd={sd}, >{ZDVARS_THR}={num_t} TRs'

            plt.plot(run['tr'].to_numpy(), run[measure].to_numpy(), linestyle='-', linewidth=2, label=label)

        plt.xlabel('TR', fontsize=14)
        if measure == 'dvars':
            plt.ylabel('Standardized DVARS Value', fontsize=14)
            plt.title(f'{tag}: Sub {sub} - DVARS', fontsize=20)
            plt.axhline(y=ZDVARS_THR, color='r', linestyle='-')
        else:
            plt.ylabel('Framewise Displacement', fontsize=14)
            plt.title(f'{tag}: Sub {sub} - Framewise Displacement', fontsize=20)
            plt.axhline(y=FD_THR, color='r', linestyle='-')

        major_locator = MultipleLocator(base=10)
        plt.gca().xaxis.set_major_locator(major_locator)
        plt.xlim(0, xlim)
        plt.legend(fontsize=12)
        plt.tight_layout()
        plt.grid(True)
        plt.savefig(out_path + f'{sub}-{task}-{measure}.png')
        plt.close()


def plot_arrow(sub, out_path):
    df = pd.read_csv(out_path + 'all_motion.csv')
    _silent_plot_one_task(df, 'arrow', sub, out_path, xlim=104, tag='Arrow')


def plot_collector(sub, out_path):
    df = pd.read_csv(out_path + 'all_motion.csv')
    _silent_plot_one_task(df, 'collector', sub, out_path, xlim=150, tag='Collector')


def plot_movie(sub, out_path):
    df = pd.read_csv(out_path + 'all_motion.csv')
    _silent_plot_one_task(df, 'movie', sub, out_path, xlim=200, tag='Movie')


def fraction_both_only(run_df):
    """
    Return the fraction of TRs where BOTH conditions are true:
       (FD > FD_THR) AND (zDVARS > ZDVARS_THR).
    NOTE: Neighbor padding (-1, +1, +2) does NOT count toward this fraction.
    """
    n = len(run_df)
    if n == 0:
        return 0.0

    fd = pd.to_numeric(run_df['fd'], errors='coerce').fillna(0).to_numpy()
    dv = pd.to_numeric(run_df['dvars'], errors='coerce').fillna(0).to_numpy()

    both = (fd > FD_THR) & (dv > ZDVARS_THR)
    return both.mean()


def evaluate_and_report(sub, out_path):
    """
    Prints ONE line per subject:
      - "all good"
      - or "EXCLUDE RUNS task-run labels for sub {sub}"
    Based on: fraction of TRs with BOTH metrics over threshold > 1/3.
    """
    df = pd.read_csv(out_path + 'all_motion.csv')
    if df.empty:
        print("all good")
        return

    exclusions = []
    for task in ['arrow', 'collector', 'movie']:
        task_df = df[df['task'] == task]
        if task_df.empty:
            continue
        for run_id in sorted(task_df['run'].unique()):
            run_df = task_df[task_df['run'] == run_id].sort_values('tr')
            frac = fraction_both_only(run_df)
            if frac > EXCLUDE_FRACTION:
                exclusions.append(f"{task}-{run_id:02d}")

    if len(exclusions) == 0:
        print("all good")
    else:
        joined = ", ".join(exclusions)
        print(f"EXCLUDE RUNS {joined} for sub {sub}")


def main(data_dir, sub):
    base_dir = os.path.join(data_dir, f'sub-{sub}', 'func') + '/'
    out_dir = os.path.join(data_dir, 'motion') + '/'
    run_com(f'mkdir -p {out_dir}sub-{sub}')
    out_path = out_dir + f'sub-{sub}/'

    format_motion_data(sub, base_dir, out_path)

    # Optional plots (quiet)
    plot_arrow(sub, out_path)
    plot_collector(sub, out_path)
    plot_movie(sub, out_path)

    # ONE summary line per subject:
    evaluate_and_report(sub, out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="data directory")
    parser.add_argument("sub", help="subject number")
    args = parser.parse_args()
    main(args.data_dir, args.sub)
