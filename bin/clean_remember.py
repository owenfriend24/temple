#!/usr/bin/env python

import pandas as pd
import os
from pathlib import Path
import argparse
from temple_utils import get_age_groups

# one important note to start - triplets/triads are ordered 1-4 based on the order of beta images
#   within the pre_post betaseries. Those are organized by item 1-12, which is set by fix_arrow and prep_arrow
#   as the first step to generating beta images. This means that triad 1 is item 1-3, triad 2 is item 4-6, etc.
#   So, by the time we assess accuracy by triplet, triplet 4 will be items 10, 11, 12, etc.

def process_subject(subject, master_dir):
    # load in data
    rem_dir = f'{master_dir}/sub-{subject}/beh/sub-{subject}_task-remember_events.tsv'
    rem = pd.read_table(rem_dir)

    # check if file has already been processed
    processed_cols = {'triad_1', 'triad_2', 'correct_triad'}
    if processed_cols.issubset(rem.columns):
        print(f'already processed {subject}')
        return
    #set up new df for cleaned data
    clean = pd.DataFrame(columns = ['subject', 'trial', 'triad_1', 'triad_2', 'correct_triad', 'response',
                                    'side_presented', 'side_chosen', 'correct_choice', 'RT', 'repetitions'])

    # for each row, aggregate presented items into a single array
    for index, row in rem.iterrows():
        triad_1 = [row['item1'], row['item2'], row['item3']]
        triad_2 = [row['item4'], row['item5'], row['item6']]

        if row['side'] == 1:
            corr_triad = triad_1
        else:
            corr_triad = triad_2

        if sum(corr_triad) == 6:
            tri_num = 1
        elif sum(corr_triad) == 15:
            tri_num = 2
        elif sum(corr_triad) == 24:
            tri_num = 3
        else:
            tri_num = 4

        clean.loc[len(clean)] = [subject, row['trial'], triad_1, triad_2, tri_num, row['order_resp'],
                                 row['side'], row['side_resp'], row['acc'], row['response_time'], row['reps']]

    clean.to_csv(rem_dir, sep = '\t', index = False)



def get_subdirectories(master_dir):
    return [d.name for d in Path(master_dir).iterdir() if d.is_dir() and d.name.startswith("sub-temple")]

def aggregate_subjects(master_dir):
    all_dfs = []
    for sub in get_subdirectories(master_dir):
        tsv_path = f'{master_dir}/{sub}/beh/{sub}_task-remember_events.tsv'
        if os.path.exists(tsv_path):
            all_dfs.append(pd.read_table(tsv_path))
        else:
            print(f"no csv found for {sub}")
    aggregated = pd.concat(all_dfs, ignore_index = True, sort = False)
    aggregated.to_csv(f'{master_dir}/beh/remember_aggregated.csv')
    return aggregated

# summarize by subject while getting rid of non-numerical fields (i.e., collapsing all triads)
def summarize_by_subject(master_dir, aggregate_file):
    by_subject = aggregate_file.groupby("subject").agg(
        trials=("trial","count"),
        accuracy=("correct_choice","mean"),
        avg_RT=("RT", "mean"),
        avg_repetitions=("repetitions","mean")
    ).reset_index()
    by_subject.to_csv(f'{master_dir}/beh/remember_by_subject.csv')

# summarize by subject and triad, pulling separate averages by triad
def summarize_by_triad(master_dir, aggregate_file):
    by_triad = aggregate_file.groupby(["subject", "correct_triad"]).agg(
        trials=("trial", "count"),
        accuracy=("correct_choice", "mean"),
        avg_RT=("RT", "mean"),
        avg_repetitions=("repetitions", "mean")
    ).reset_index()
    by_triad.to_csv(f'{master_dir}/beh/remember_by_triad.csv')


def main(subject, master_dir, by_subject, by_triad):
    if subject == 'ALL':
        print('processing all subjects')
        subs = get_age_groups.get_all_subjects()
        for sub in subs:
            process_subject(sub, master_dir)

    elif subject == 'AGGREGATE':
        aggregate = aggregate_subjects(master_dir)
        if by_subject:
            summarize_by_subject(master_dir, aggregate)
        if by_triad:
            summarize_by_triad(master_dir, aggregate)

    else:
        process_subject(subject, master_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("subject", help="subject (e.g., temple100), ALL (process all subs),"
                                        "AGGREGATE (combine all processed subjects)")
    parser.add_argument("master_dir", help="where subject directories are located")
    parser.add_argument("--by_subject", action=argparse.BooleanOptionalAction, default=False,
                        help="summarize aggregate data by subject")
    parser.add_argument("--by_triad", action=argparse.BooleanOptionalAction, default=False,
                        help="summarize aggregate data by subject and triad")
    args = parser.parse_args()
    main(args.subject, args.master_dir, args.by_subject, args.by_triad)

