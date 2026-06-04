#!/usr/bin/env python
"""Extract run-level high-motion counts from fMRIPrep confounds using plot_motion_2.py."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import pandas as pd

# Ensure local bin modules can be imported reliably.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import plot_motion_2 as pm2

TASK_RUNS = {
    'arrow': range(1, 7),
    'collector': range(1, 5),
    'movie': range(1, 3),
}


def find_subjects(data_dir: Path) -> list[str]:
    """Return sorted subject ids found under data_dir as sub-<id> directories."""
    subs = []
    for sub_dir in sorted(data_dir.glob('sub-*')):
        if sub_dir.is_dir():
            subs.append(sub_dir.name.replace('sub-', ''))
    return subs


def load_subjects(subjects_arg: str | None, data_dir: Path) -> list[str]:
    """Load subject ids either from a file or from the data directory."""
    if subjects_arg:
        subjects_path = Path(subjects_arg)
        if not subjects_path.exists():
            raise FileNotFoundError(f"Subject list file not found: {subjects_path}")
        return [line.strip() for line in subjects_path.read_text().splitlines() if line.strip()]
    return find_subjects(data_dir)


def extract_counts_for_subject(sub: str, data_dir: Path, output_dir: Path) -> pd.DataFrame:
    """Generate run-level FD/DVARS counts for a single subject."""
    base_dir = str(data_dir / f'sub-{sub}' / 'func') + '/'
    subject_output_dir = output_dir / f'sub-{sub}'
    subject_output_dir.mkdir(parents=True, exist_ok=True)
    pm2.format_motion_data(sub, base_dir, str(subject_output_dir) + '/')

    motion_df = pd.read_csv(subject_output_dir / 'all_motion.csv')
    if motion_df.empty:
        return pd.DataFrame(
            columns=[
                'subject', 'task', 'run', 'total_trs',
                'high_fd_volumes', 'high_zdvars_volumes', 'high_both_volumes',
                'fd_fraction', 'zdvars_fraction', 'both_fraction', 'status',
            ]
        )

    rows = []
    for task, run_range in TASK_RUNS.items():
        task_df = motion_df[motion_df['task'] == task]
        for run in run_range:
            run_df = task_df[task_df['run'] == run].sort_values('tr')
            if run_df.empty:
                rows.append({
                    'subject': sub,
                    'task': task,
                    'run': run,
                    'total_trs': 0,
                    'high_fd_volumes': pd.NA,
                    'high_zdvars_volumes': pd.NA,
                    'high_both_volumes': pd.NA,
                    'fd_fraction': pd.NA,
                    'zdvars_fraction': pd.NA,
                    'both_fraction': pd.NA,
                    'status': 'missing',
                })
                continue

            fd = pd.to_numeric(run_df['fd'], errors='coerce').fillna(0).to_numpy()
            zdvars = pd.to_numeric(run_df['dvars'], errors='coerce').fillna(0).to_numpy()
            high_fd = int((fd > pm2.FD_THR).sum())
            high_zdvars = int((zdvars > pm2.ZDVARS_THR).sum())
            high_both = int(((fd > pm2.FD_THR) & (zdvars > pm2.ZDVARS_THR)).sum())
            total_trs = len(run_df)

            rows.append({
                'subject': sub,
                'task': task,
                'run': run,
                'total_trs': total_trs,
                'high_fd_volumes': high_fd,
                'high_zdvars_volumes': high_zdvars,
                'high_both_volumes': high_both,
                'fd_fraction': high_fd / total_trs if total_trs else pd.NA,
                'zdvars_fraction': high_zdvars / total_trs if total_trs else pd.NA,
                'both_fraction': high_both / total_trs if total_trs else pd.NA,
                'status': 'ok',
            })

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extract the number of high-motion volumes per run for each subject.'
    )
    parser.add_argument('data_dir', help='Root fmriprep derivatives directory containing sub-<id>/func/')
    parser.add_argument(
        '--subjects',
        help='Optional text file with one subject id per line (e.g. temple100). If omitted, all sub-* directories are used.',
        default=None,
    )
    parser.add_argument(
        '--output',
        help='Output CSV path.',
        default='high_motion_run_counts.csv',
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    subjects = load_subjects(args.subjects, data_dir)
    if not subjects:
        raise ValueError('No subjects found in data directory or subject list file.')

    all_rows = []
    output_dir = data_dir / 'motion_counts_tmp'
    for sub in subjects:
        all_rows.append(extract_counts_for_subject(sub, data_dir, output_dir))

    result = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    result = result.sort_values(['subject', 'task', 'run'])
    result.to_csv(args.output, index=False)
    print(f'Wrote high-motion counts for {len(subjects)} subjects to {args.output}')


if __name__ == '__main__':
    main()
