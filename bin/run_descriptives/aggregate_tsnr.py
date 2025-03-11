import os
import pandas as pd

def aggregate_tsnr(data_dir, subjects, masktype):
    """
    Aggregates tSNR values from `tsnr_by_roi` CSVs and whole-brain `tsnr_values.txt`
    for each subject across runs.

    Parameters:
    - data_dir: str, path to the root directory containing subject folders.
    - subjects: list of str, list of subject IDs.
    - masktype: str, mask type used (should match the `tsnr_by_roi` CSV filename).

    Returns:
    - A combined DataFrame with all tSNR data.
    - Saves the aggregated CSV to `data_dir/tsnr_aggregated.csv`.
    """

    all_data = []  # List to store per-subject data

    for subject in subjects:
        tsnr_dir = os.path.join(data_dir, f"sub-{subject}", "func", "tsnr")

        # Load tSNR by ROI
        roi_csv_path = os.path.join(tsnr_dir, f"tsnr_values_{masktype}.csv")
        if os.path.exists(roi_csv_path):
            df_roi = pd.read_csv(roi_csv_path)
            df_roi["subject"] = subject  # Add subject column
        else:
            print(f"Warning: Missing ROI CSV for subject {subject}")
            continue

        # Load whole-brain tSNR
        wholebrain_txt_path = os.path.join(tsnr_dir, "tsnr_values.txt")
        wholebrain_tsnr = {}

        if os.path.exists(wholebrain_txt_path):
            with open(wholebrain_txt_path, "r") as f:
                lines = [line.strip() for line in f.readlines()]

            # Store available values (could be fewer than 6)
            for i, value in enumerate(lines):
                run = i + 1  # Runs are 1-based (1 to 6)
                wholebrain_tsnr[run] = value

        else:
            print(f"Warning: Missing tsnr_values.txt for subject {subject}")

        # Convert whole-brain tSNR to a DataFrame
        df_wholebrain = pd.DataFrame({
            "run": range(1, 7),  # Ensure we cover all runs (1-6)
            "wholebrain_tsnr": [wholebrain_tsnr.get(run, None) for run in range(1, 7)],
            "subject": subject
        })

        # Ensure "run" is an integer in both DataFrames for merging
        df_roi["run"] = df_roi["run"].astype(int)
        df_wholebrain["run"] = df_wholebrain["run"].astype(int)

        # Merge ROI and Whole-Brain tSNR Data
        df_combined = pd.merge(df_roi, df_wholebrain, on=["subject", "run"], how="left")

        all_data.append(df_combined)

    # Concatenate all subject data
    if all_data:
        df_final = pd.concat(all_data, ignore_index=True)
        output_csv = os.path.join(data_dir, "tsnr_aggregated.csv")
        df_final.to_csv(output_csv, index=False)
        print(f"Saved aggregated tSNR data to {output_csv}")

        return df_final
    else:
        print("No valid data found for aggregation.")
        return None
