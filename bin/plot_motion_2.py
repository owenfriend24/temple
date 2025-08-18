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


def plot_spike_grid(sub, out_path):
    """
    For each task, create a grid figure (one row per run) showing:
      - Alternating colors per TR for all bars
      - Tall bars at TRs with spikes (FD>FD_THR & zDVARS>ZDVARS_THR)
      - Hatch overlay on spike bars to distinguish them while preserving alternation
      - Text per row with spike count and percent
    Saves: sub-{sub}_{task}_spikes_grid.png
    """
    df = pd.read_csv(out_path + 'all_motion.csv')
    if df.empty:
        return

    base_color_even = '#d9d9d9'  # light gray
    base_color_odd  = '#b3b3b3'  # darker gray
    hatch_color     = 'black'    # hatch overlay color for spikes

    for task in ['arrow', 'collector', 'movie']:
        task_df = df[df['task'] == task]
        if task_df.empty:
            continue

        run_ids = sorted(task_df['run'].unique())
        n_runs = len(run_ids)
        if n_runs == 0:
            continue

        fig, axes = plt.subplots(
            nrows=n_runs, ncols=1,
            figsize=(16, 1.6 * n_runs + 1),
            sharex=False, sharey=True,
            constrained_layout=True
        )

        if n_runs == 1:
            axes = [axes]  # unify indexing

        for i, run_id in enumerate(run_ids):
            ax = axes[i]
            run_df = task_df[task_df['run'] == run_id].sort_values('tr')
            if run_df.empty:
                continue

            tr = run_df['tr'].to_numpy()
            fd = pd.to_numeric(run_df['fd'], errors='coerce').fillna(0).to_numpy()
            dv = pd.to_numeric(run_df['dvars'], errors='coerce').fillna(0).to_numpy()

            both = (fd > FD_THR) & (dv > ZDVARS_THR)
            n_tr = len(tr)
            n_spikes = int(both.sum())
            pct_spikes = 100.0 * n_spikes / n_tr if n_tr else 0.0

            # Heights: tall for spikes, short otherwise
            heights = np.where(both, 1.0, 0.15)

            # Alternating colors by TR parity (preserved even when spikes)
            bar_colors = np.where((tr % 2) == 0, base_color_even, base_color_odd)

            # Base bars (alternating colors)
            ax.bar(tr, heights, width=1.0, align='center',
                   color=bar_colors, edgecolor='none', zorder=1)

            # Overlay hatch on spike bars so they pop but keep alternation visible
            spike_trs = tr[both]
            if n_spikes > 0:
                # Draw transparent bars with hatch only at spike TRs
                ax.bar(spike_trs, np.full(n_spikes, 1.0), width=1.0, align='center',
                       facecolor='none', edgecolor=hatch_color, hatch='////',
                       linewidth=0.0, zorder=2)

            # Cosmetics for each row
            ax.set_ylim(0, 1.15)
            ax.set_xlim(tr.min() - 1, tr.max() + 1)
            ax.set_yticks([0.15, 1.0], ['good', 'spike'])
            ax.grid(axis='x', linestyle=':', alpha=0.35)
            ax.set_ylabel(f'run {run_id:02d}', rotation=0, labelpad=30, va='center', fontsize=11)

            # Annotate spike count & percent on each row (top-right)
            ax.text(0.995, 0.93,
                    f"spikes: {n_spikes}/{n_tr} ({pct_spikes:.1f}%)",
                    ha='right', va='top', transform=ax.transAxes,
                    fontsize=11, bbox=dict(boxstyle='round,pad=0.25',
                                           facecolor='white', alpha=0.85,
                                           edgecolor='none'))

            # X label on last row only
            if i == n_runs - 1:
                ax.set_xlabel('TR', fontsize=12)
            else:
                ax.set_xticklabels([])

        fig.suptitle(
            f"Sub {sub} · {task} · spikes where FD>{FD_THR} & zDVARS>{ZDVARS_THR}",
            fontsize=15, y=1.02
        )
        out_file = os.path.join(out_path, f"sub-{sub}_{task}_spikes_grid.png")
        fig.savefig(out_file, dpi=150, bbox_inches='tight')
        plt.close(fig)




def evaluate_and_report(sub, out_path):
    """
    Prints ONE line per subject that includes:
      - Either "EXCLUDE RUNS ..." or "ALL RUNS OK"
      - Per-run spike stats: task-run: n (pct%)
    Run exclusion rule: fraction of TRs with BOTH FD>FD_THR and zDVARS>ZDVARS_THR > EXCLUDE_FRACTION.
    """
    df = pd.read_csv(out_path + 'all_motion.csv')
    if df.empty:
        print(f"ALL RUNS OK | (no motion file rows found) for sub {sub}")
        return

    exclusions = []
    run_stats = []  # collect "task-rr: n (p%)" entries

    for task in ['arrow', 'collector', 'movie']:
        task_df = df[df['task'] == task]
        if task_df.empty:
            continue
        for run_id in sorted(task_df['run'].unique()):
            run_df = task_df[task_df['run'] == run_id].sort_values('tr')

            # compute spikes and fraction
            fd = pd.to_numeric(run_df['fd'], errors='coerce').fillna(0).to_numpy()
            dv = pd.to_numeric(run_df['dvars'], errors='coerce').fillna(0).to_numpy()
            both = (fd > FD_THR) & (dv > ZDVARS_THR)

            n_tr = len(run_df)
            n_spikes = int(both.sum())
            pct_spikes = 100.0 * n_spikes / n_tr if n_tr else 0.0
            frac = n_spikes / n_tr if n_tr else 0.0

            if frac > EXCLUDE_FRACTION:
                exclusions.append(f"{task}-{run_id:02d}")

            run_stats.append(f"{task}-{run_id:02d}: {n_spikes} ({pct_spikes:.1f}%)")

    stats_str = "; ".join(run_stats) if run_stats else "no runs found"

    if len(exclusions) == 0:
        print(f"ALL RUNS OK for sub {sub} | {stats_str}")
    else:
        joined = ", ".join(exclusions)
        print(f"EXCLUDE RUNS {joined} for sub {sub} | {stats_str}")


def main(data_dir, sub):
    base_dir = os.path.join(data_dir, f'sub-{sub}', 'func') + '/'
    out_dir = os.path.join(data_dir, 'motion') + '/'
    run_com(f'mkdir -p {out_dir}sub-{sub}')
    out_path = out_dir + f'sub-{sub}/'

    format_motion_data(sub, base_dir, out_path)

    # (Optional) Keep original FD/DVARS time series figures if you like:
    plot_arrow(sub, out_path)
    plot_collector(sub, out_path)
    plot_movie(sub, out_path)

    # NEW: grid spikes per task
    plot_spike_grid(sub, out_path)

    # ONE summary line per subject with per-run spike stats
    evaluate_and_report(sub, out_path)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data_dir", help="data directory")
    parser.add_argument("sub", help="subject number")
    args = parser.parse_args()
    main(args.data_dir, args.sub)
