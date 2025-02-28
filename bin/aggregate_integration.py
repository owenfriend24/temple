#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
import numpy as np
from temple_utils import get_age_groups


def run(command):
    subprocess.run(command, shell=True)

def aggregate_csv_files(measure, comparison, csv_files, master_dir):
    aggregated_data = []

    for file_path in csv_files:
        if file_path.exists():
            df = pd.read_csv(file_path)
            aggregated_data.append(df)
        else:
            print(f"no file found at {file_path}")

    if aggregated_data:
        master_df = pd.concat(aggregated_data, ignore_index=True)

        if measure in ['prepost', 'both']:
            master_output_path = f"{master_dir}/aggregated_{comparison}_prepost.csv"
            master_df.to_csv(master_output_path, index=False)
            print(f"Aggregated prepost file saved at: {master_output_path}")

        if measure in ['symmetry', 'both']:
            master_output_path = f"{master_dir}/aggregated_{comparison}_symmetry.csv"
            master_df.to_csv(master_output_path, index=False)
            print(f"Aggregated symmetry file saved at: {master_output_path}")
    else:
        print("No CSV files were found for aggregation.")



def main(measure, master_dir, comparison, mask, agg_file):
    subjects = get_age_groups.get_all_subjects()

    drop_runs = {
        "temple023": 6,
        "temple030": 6,
        "temple070": 3,
        "temple115": 3,
        "temple116": 5,
    }
    output_csv_files = []

    for sub in subjects:
        # Check if subject has a run to drop
        drop_run = drop_runs.get(sub, None)
        drop_flag = f"--drop_run {drop_run} " if drop_run is not None else ""
        if measure in ["prepost", "both"]:
            run(f"integration_prepost_values.py {drop_flag}{sub} {comparison} {mask}")
            run(f"merge_integration.py {drop_flag}{sub} {master_dir} {comparison} {mask}")

            # fix for corrected filepath
            output_csv_files.append(f"{master_dir}/prepost_{comparison}/sub-{sub}/sub-{sub}_{comparison}_{mask}_master.csv")

        if measure in ["symmetry", "both"]:
            bwd_comp = comparison[::-1]
            run(f"symmetry_prepost_values.py {drop_flag}{sub} {comparison} {mask}")
            run(f"symmetry_prepost_values.py {drop_flag}{sub} {bwd_comp} {mask}")
            run(f"merge_symmetry.py {drop_flag}{sub} {master_dir} {comparison} {mask}")

            # fix for corrected filepath
            output_csv_files.append(f"{master_dir}/symmetry_{comparison}/sub-{sub}/sub-{sub}_{comparison}_{mask}_master.csv")

    if agg_file:
        aggregate_csv_files(measure, comparison, output_csv_files, master_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("measure", help="prepost, symmetry, both")
    parser.add_argument("master_dir", help="where folders containing .txt files for each comparison are stored")
    parser.add_argument("comparison", help="options: AB, BC, AC")
    parser.add_argument("mask", help="mask name e.g., b_hip_subregions, b_hip_subfields, etc.")
    parser.add_argument("--agg_file", type=bool, default=False,
                        help="write aggregate file - boolean")
    args = parser.parse_args()
    main(args.measure, args.master_dir, args.comparison, args.mask, args.agg_file)