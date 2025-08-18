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
ZDVARS_THR = 1.5
EXCLUDE_FRACTION = 1/3  # > 1/3 of TRs flagged after padding
PADDING = (-1, 0, 1, 2)  # prev 1, self, next 2


def run_com(command):
    subprocess.run(command, shell=True)


def format_motion_data(sub, base_dir, out_path):
    df = pd.DataFrame(columns=['sub', 'task', 'run', 'tr', 'dvars', 'fd'])
    for run in range(1, 7, 1):
        task = 'arrow'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index + 1
                fd = data['framewise_displacement'][index]
                dvars = data['std_dvars'][index]
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]
    for run in range(1, 5, 1):
        task = 'collector'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index + 1
                fd = data['framewise_displacement'][index]
                dvars = data['std_dvars'][index]
                df.loc[len(df)] = [sub, task, run, tr, dvars, fd]
    for run in range(1, 3, 1):
        task = 'movie'
        file_path = (base_dir + f'sub-{sub}_task-{task}_run-0{run}_desc-confounds_timeseries.tsv')
        if os.path.exists(file_path):
            data = pd.read_table(file_path)
            for index, row in data.iterrows():
                tr = index + 1
                fd = data['framewise_displacement'][index]
                dvars = data['std_dvars'][index]
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
            mn = round(np.mean(run[measure]), 3)
            sd = round(np.std(run[measure]), 3)

            if measure == 'fd':
                num_t = (run[measure] > FD_THR).sum()
                label = f'run{run_number}: m={mn}, sd={sd}, >{FD_THR}={num_t} TRs'
            else:
                num_t = (run[measure] > ZDVARS_THR).sum()
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


def fraction_flagged_with_padding(run_df):
    """
    Apply: (FD > 0.5 AND zDVARS > 1.5) then pad prev 1 and next 2 TRs.
    Return fraction of TRs flagged after padding.
    """
    n = len(run_df)
    if n == 0:
        return 0.0

    fd_bad = (run_df['fd'].to_numpy() > FD_THR)
    dv_bad = (run_df['dvars'].to_numpy() > ZDVARS_THR)
    both = fd_bad & dv_bad

    flagged = np.zeros(n, dtype=bool)
    bad_idx = np.where(both)[0]
    if bad_idx.size == 0:
        return 0.0

    for idx in bad_idx:
        for offset in PADDING:
            j = idx + offset
            if 0 <= j < n:
                flagged[j] = True

    return flagged.mean()


def evaluate_and_report(sub, out_path):
    """
    Prints ONE line per subject:
      - "all good"
      - or "EXCLUDE RUNS task-run labels for sub {sub}"
    """
    df = pd.read_csv(out_path + 'all_motion.csv')
    if df.empty:
        print(f"all good")  # nothing to evaluate
        return

    exclusions = []
    for task in ['arrow', 'collector', 'movie']:
        task_df = df[df['task'] == task]
        if task_df.empty:
            continue
        for run_id in sorted(task_df['run'].unique()):
            run_df = task_df[task_df['run'] == run_id].sort_values('tr')
            frac = fraction_flagged_with_padding(run_df)
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

    # Optional: keep plots but no noisy prints
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
