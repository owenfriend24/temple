"""Utilities for loading Temple behavioral data."""

import numpy as np
from scipy.spatial import distance
from scipy import stats
from sklearn import linear_model
import pandas as pd
import os

from temple import raw


def get_subj_list():
    """Get IDs of included Temple participants."""
    participant_list = [
    16, 19, 20, 22, 24, 25, 29, 30, 32, 34,
    33, 35, 36, 37, 38, 41, 42, 50,
    51 ]
    return participant_list


def _load_bids_events_subject(bids_dir, phase, data_type, task, subject, runs=None):
    """Load events for one subject from a BIDS directory."""
    subj_dir = os.path.join(bids_dir, f'sub-temple{subject:03d}', phase)
    if not os.path.exists(subj_dir):
        raise IOError(f'Subject directory does not exist: {subj_dir}')

    if runs is not None:
        df_list = []
        for run in runs:
            file = os.path.join(
                subj_dir, f'sub-temple{subject:03d}_task-{task}_run-{run:02}_{data_type}.tsv'
            )
            df_run = pd.read_table(file)
            df_run['run'] = run
            df_list.append(df_run)
        data = pd.concat(df_list, axis=0)
    else:
        file = os.path.join(subj_dir, f'sub-temple{subject:03d}_task-{task}_{data_type}.tsv')
        data = pd.read_table(file)
        data['run'] = 1
    data['subject'] = subject
    return data


def _load_bids_events(bids_dir, phase, data_type, task, subjects=None, runs=None):
    """Load events for multiple subjects from a BIDS directory."""
    if subjects is None:
        subjects = get_subj_list()
    elif not isinstance(subjects, list):
        subjects = [subjects]

    data = pd.concat(
        [
            _load_bids_events_subject(bids_dir, phase, data_type, task, subject, runs)
            for subject in subjects
        ],
        axis=0,
    )
    return data


def load_arrow_task(bids_dir, subjects=None):
    """Load structure learning events."""
    if subjects is None:
        subjects = get_subj_list()
    elif not isinstance(subjects, list):
        subjects = [subjects]

    data_list = []
    for subject in subjects:
        subj_data = _load_bids_events_subject(
            bids_dir, 'func', 'events', 'arrow', subject, runs=list(range(1, 7))
        )

        data_list.append(subj_data)
    data = pd.concat(data_list, axis=0)
    return data


def load_collector_task(bids_dir, subjects=None):
    """Load structure learning events."""
    if subjects is None:
        subjects = get_subj_list()
    elif not isinstance(subjects, list):
        subjects = [subjects]

    data_list = []
    for subject in subjects:
        subj_data = _load_bids_events_subject(
            bids_dir, 'func', 'events', 'collector', subject, runs=list(range(1, 5))
        )

        data_list.append(subj_data)
    data = pd.concat(data_list, axis=0)
    return data


def load_remember_task(bids_dir, subjects=None):
    """Load structure learning events."""
    if subjects is None:
        subjects = get_subj_list()
    elif not isinstance(subjects, list):
        subjects = [subjects]

    data_list = []
    for subject in subjects:
        subj_data = _load_bids_events_subject(
            bids_dir, 'beh', 'events', 'remember', subject, runs=None
        )

        data_list.append(subj_data)
    data = pd.concat(data_list, axis=0)
    return data


def collector_correction(data):
    """THIS DOES NOT WORK YET"""


    # get odd trial plus the trial after for delayed response
    tmp1 = data.copy()
    tmp1['odd2'] = np.hstack([[2.], data.odd[:-1].values.tolist()])
    tmp2 = tmp1[tmp1['odd2']==1.]
    tmp2 = tmp2[tmp2.acc == 0.]
    tmp3 = tmp2[['trial', 'subject', 'run']]
    for i in range(len(tmp3)):
        trial, subject, run = tmp3.iloc[i, :]
        trial -= 1
        data.query(f"trial=={trial} and subject=={subject} and run=={run}")['acc'] = 1.
    post = sum(data[data.odd == 1.].acc.values)

    return data


def collector_perf(bids_dir, results_dir):
    """ """
    data = raw.load_collector(bids_dir, subjects=None)
    odd = data[data.odd == 1.]
    odd[['subject', 'response_time', 'acc']].groupby(['subject']).mean().reset_index(inplace=True)
    odd.to_csv(os.path.join(results_dir, 'remember_accuracy_by_subject.csv'))
    
    # # plotting
    # odd[['subject', 'response_time', 'acc']].groupby(['subject']).mean().reset_index(inplace=True)


def arrow_perf(bids_dir, results_dir):
    """ """
    data = raw.load_arrow(bids_dir, subjects=None)
    data[['subject', 'response_time', 'acc']].groupby(['subject']).mean().reset_index(inplace=True)
    data.to_csv(os.path.join(results_dir, 'arrow_accuracy_by_subject.csv'))

    # # plotting
    # data[['subject', 'run', 'response_time', 'acc']].groupby(['subject']).mean().reset_index(inplace=True)


def remember_perf(bids_dir, results_dir):
    """ """
    data = raw.load_remember(bids_dir, subjects=None)
    data[['subject', 'response_time', 'acc']].groupby(['subject']).mean().reset_index(inplace=True)
    data.to_csv(os.path.join(results_dir, 'remember_accuracy_by_subject.csv'))
