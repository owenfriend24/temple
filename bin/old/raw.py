"""Work with raw behavioral data."""

import os
from glob import glob
from scipy.io import loadmat
import pdb

import numpy as np
import pandas as pd

from temple import tasks


triads = np.repeat(np.arange(1, 5), 3)
positions = np.tile([1, 2, 3], 4)
items = np.arange(1, 13)


def get_subj_dir(data_dir, subject_num):
    """
    Get the path to the data directory for a subject.
    Parameters
    ----------
    data_dir : str
        Path to the base directory with subdirectories for each
        subject.
    subject_num : int
        Subject number without initials.
    Returns
    -------
    subj_dir : str
        Path to the base directory for the subject.
    """
    # check that the base directory exists
    if not os.path.exists(data_dir):
        raise IOError(f'Directory does not exist: {data_dir}')

    # look for directories with the correct pattern
    dir_search = glob(os.path.join(data_dir, f'temple{subject_num:03d}'))
    if len(dir_search) != 1:
        raise IOError(f'Problem finding subject directory for {subject_num:03d}')
    return dir_search[0]


def load_phase_subject(data_dir, subject_num, file_pattern):
    """Load log as a DataFrame."""
    # get the first file matching the log file pattern
    subj_dir = get_subj_dir(data_dir, subject_num)
    file_search = glob(os.path.join(subj_dir, file_pattern))
    if len(file_search) != 1:
        raise IOError(f'Problem finding log: {file_pattern}')
    run_file = file_search[0]

    # read log, fixing problem with spaces in column names
    df = pd.read_csv(run_file, sep='\t', skipinitialspace=True)
    return df


def load_phase_subject_mat(data_dir, subject_num, file_pattern):

    subj_dir = get_subj_dir(data_dir, subject_num)
    file_search = glob(os.path.join(subj_dir, file_pattern))
    if len(file_search) != 1:
        raise IOError(f'Problem finding log: {file_pattern}')
    run_file = file_search[0]

    # read log, fixing problem with spaces in column names
    df = loadmat(run_file, squeeze_me=True, simplify_cells=True)['d']
    return df


def process_mat_file(df):
    """Process .mat file of the run (not the txt file)"""
    pdf = {
        'item': df['trials'],
        'objects': df['trials'],
        'triads': df['trials'],
        'onset': df['onsets'],
        'acc': df['correct'],
        'resp': df['resp'],
        'rt': df['rt'],
        'trial': np.arange(1, df['Ntrials']+1)
    }
    return pd.DataFrame(pdf)


def load_run(data_dir, subject_num, phase, run_num, mat=False):
    """Load dataframe for one structured learning run."""
    # load structure learning run
    if mat:
        file_pattern = (
            f'{phase}_{run_num:02d}_{subject_num:03d}.mat'
        )
        ddf = load_phase_subject_mat(data_dir, subject_num, file_pattern)
        df = process_mat_file(ddf)
    else:
        file_pattern = (
            f'{phase}_{run_num:02d}_{subject_num:03d}.txt'
        )
        df = load_phase_subject(data_dir, subject_num, file_pattern)

    return df


def load_test(data_dir, subject_num):
    """Load dataframe for one structured learning run."""
    # load structure learning run
    file_pattern = (
        f'test_{subject_num:03d}_1.txt'
    )
    df = load_phase_subject(data_dir, subject_num, file_pattern)
    return df


def load_header(data_dir, subject_num):
    """Load header file with object information."""

    subj_dir = get_subj_dir(data_dir, subject_num)
    file_pattern = (
        f'{subject_num:03d}_header.mat'
    )
    # pretty rigid search
    file_search = glob(os.path.join(subj_dir, file_pattern))
    if len(file_search) != 1:
        raise IOError(f'Problem finding log: {file_pattern}')
    header_file = file_search[0]
    
    return loadmat(header_file, squeeze_me=True, simplify_cells=True)


def load_subject_objects(data_dir, subject_num):
    """ """
    h = load_header(data_dir, subject_num)
    return h['h']['obj']['objs'].tolist()


def load_odd_vector(data_dir, subject_num, run_num):
    """Load oddball trials for collector game."""
    h = load_header(data_dir, subject_num)
    return h['h']['enc'][run_num-1]['oddVec']


def add_time(run_df, subject_num, part, run):
    """ """
    if (subject_num == 19) or (subject_num == 20) or (subject_num == 23):
        if part == 'collector':
            run_df['onset'] += 10

        elif (part == 'arrow') and (run < 4):
            run_df['onset'] += 10

    elif (subject_num == 24) or (subject_num == 25) or (subject_num == 29) or (subject_num == 30):
        if part == 'arrow' or part == 'collector':
            run_df['onset'] += 10

    else:
        pass

    return run_df


def load_arrow_runs_subject(data_dir, subject_num, mat=False):
    """Load dataframe with structured learning task for one subject."""
    objects = load_subject_objects(data_dir, subject_num)

    columns = ['onset', 'duration', 'trial', 'part', 'run', 'object', 'item',
               'position', 'triad', 'left_right', 'response', 'response_time', 'acc']

    # list of all runs to load
    phases = {
              'arrow_pt1': np.arange(1, 4),
              'arrow_pt2': np.arange(1, 4)
              }

    # load individual runs
    df_list = []
    arrow_run_n = 0
    for part, runs in phases.items():
        for run in runs:
            run_df = load_run(data_dir, subject_num, part, run, mat=mat)
            arrow_run_n += 1 # converts from part1 and part2 to 6 runs of arrow

            # some time adjustments for the first few subjects.
            run_df = add_time(run_df, subject_num, part, run)

            run_df['part'] = 'arrow' # circumvents part1 and part2
            run_df['duration'] = 1
            run_df['run'] = arrow_run_n
            df_list.append(run_df)
    
    # concatenate into one data frame
    df = pd.concat(df_list, sort=False, ignore_index=True)
    
    # replace item with object (from header file)
    df['object'] = df['item'].copy()
    df['object'].replace(to_replace=items, value=objects, inplace=True)
    df.rename(columns={'resp': 'response', 'rt': 'response_time'}, inplace=True)
    df = df[columns]
    df['subject'] = subject_num
    return df


def load_collector_runs_subject(data_dir, subject_num, mat=False):
    """Load dataframe with structured learning task for one subject."""
    objects = load_subject_objects(data_dir, subject_num)

    columns = ['onset', 'duration', 'trial', 'part', 'run', 'object',
               'position', 'triad', 'odd', 'response', 'response_time', 'acc']
    
    # list of all runs to load
    phases = {
              'familiar': [1, 2, 3, 4]
              }

    # load individual runs
    df_list = []
    for part, runs in phases.items():

        for run in runs:
            run_df = load_run(data_dir, subject_num, part, run, mat=mat)

            # some time adjustments for the first subjects.
            run_df = add_time(run_df, subject_num, part, run)

            # meta run
            run_df['run'] = run
            run_df['odd'] = load_odd_vector(data_dir, subject_num, run)# oddball vector for collector trials
            run_df.rename(columns={'resp': 'response'}, inplace=True)
            df_list.append(run_df)

    # concatenate into one data frame
    df = pd.concat(df_list, sort=False, ignore_index=True)

    # meta phase
    df['part'] = 'collector'
    df['duration'] = 1

    # replace position with item (from header file)
    df['position'] = df['item'].copy()
    df['position'].replace(to_replace=objects, value=positions, inplace=True)

    # replace triad with item (from header file)
    df['triad'] = df['item'].copy()
    df['triad'].replace(to_replace=objects, value=triads, inplace=True)

    # create clean object number
    if mat:
        df['object'] = df['item'].copy()
        df['object'].replace(to_replace=items, value=objects, inplace=True)
    else:
        df['object'] = df['item'].copy()

    df.rename(columns={'correct': 'acc', 'rt': 'response_time'}, inplace=True)
    df = df[columns]
    df['subject'] = subject_num
    return df 


def load_remember_subject(data_dir, subject_num):
    """ """
    columns = ['trial', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 
               'order', 'order_resp', 'side', 'side_resp', 'acc', 'response_time', 'reps']

    # header for foils
    h = load_header(data_dir, subject_num)
    foils = h['h']['test']['foils']
    
    # data
    df = load_test(data_dir, subject_num)
    
    # if wanting triads
    # df[['item1', 'item2', 'item3', 'item4', 'item5', 'item6']].replace(to_replace=items, value=triads, inplace=True)

    df.rename(columns={'corr': 'acc', 'rt': 'response_time', 'sdresp': 'side_resp', 'ordresp': 'order_resp'}, inplace=True)
    df = df[columns]
    df['subject'] = subject_num
    df['run'] = 1# used to write events
    df['part'] = 'remember'
    return df


def load_arrow_runs(data_dir, subjects=None, mat=False):
    """Load structure learning data for multiple subjects."""
    if subjects is None:
        subjects = tasks.get_subj_list()

    # load raw data for all subjects
    df_all = []
    for subject in subjects:
        df = load_arrow_runs_subject(data_dir, subject, mat=mat)
        df_all.append(df)

    raw = pd.concat(df_all, axis=0, ignore_index=True)

    return raw


def load_collector_runs(data_dir, subjects=None, mat=False):
    """Load structure learning data for multiple subjects."""
    if subjects is None:
        subjects = tasks.get_subj_list()

    # load raw data for all subjects
    df_all = []
    for subject in subjects:
        df = load_collector_runs_subject(data_dir, subject, mat=mat)
        df_all.append(df)

    raw = pd.concat(df_all, axis=0, ignore_index=True)
    raw['run'] = raw.run.values.astype(int)
    raw['position'] = raw.position.values.astype(int)
    raw['triad'] = raw.position.values.astype(int)
    return raw


def load_remember(data_dir, subjects=None):
    """Load remember trials"""
    if subjects is None:
        subjects = tasks.get_subj_list()

    # load raw data for all subjects
    df_all = []
    for subject in subjects:
        df = load_remember_subject(data_dir, subject)
        df_all.append(df)

    fdf = pd.concat(df_all, axis=0, ignore_index=True)

    return fdf