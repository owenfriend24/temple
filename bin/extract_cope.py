#!/usr/bin/env python

import os
import subprocess
import argparse
import pandas as pd

def run_com(command):
    subprocess.run(command, check=True)


def get_mean_pe(img):
    result = subprocess.run(
        ["fslstats", img, "-M"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return float(result.stdout.strip())

def back_project(sub, roi_path, roi_name):
    # back project the cluster mask into functional space for each subject

    in_path = roi_path
    out_dir = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/masks/univariate_rois/'
    os.makedirs(out_dir, exist_ok=True)
    out_path = f'{out_dir}/{roi_name}.nii.gz'

    ref_path = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/brainmask_func_dilated.nii.gz'
    affine_path = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/native_to_MNI_Affine.txt'
    warp_path = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/transforms/native_to_MNI_InverseWarp.nii.gz'

    cmd = [
        'antsApplyTransforms', '-d', '3',
        '-i', in_path,
        '-o', out_path,
        '-r', ref_path,
        '-n', 'NearestNeighbor',
        '-t', f'[{affine_path},1]',
        '-t', warp_path
    ]
    run_com(cmd)

def main(sub, roi_path, roi_name, analysis_type, ppi_roi):
    back_project(sub, roi_path, roi_name)
    rows = []
    output_csv = f"/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/cope_vals_{roi_name}.csv"

    mask = f'/corral-repl/utexas/prestonlab/temple/sub-{sub}/masks/univariate_rois/{roi_name}.nii.gz'

    if sub in ["temple107"]:
        runs = [1, 3, 4]
    elif sub in ["temple064"]:
        runs = [1, 2, 4]
    elif sub in ["temple114"]:
        runs = [2, 3, 4]
    else:
        runs = [1, 2, 3, 4]

    for run in runs:
        base = f"/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/sub-{sub}/univ"
        if analysis_type in ['ppi', 'ppi_inverse']:
            run_dir = f'{base}/{analysis_type}/{ppi_roi}_out_run{run}.feat'
        else:
            run_dir = f'{base}/out_run{run}.feat'

        out_mask_dir = f'{run_dir}/masked_rois'
        os.makedirs(out_mask_dir, exist_ok=True)
        masked_pe = f'{out_mask_dir}/{roi_name}_run{run}.nii.gz'

        run_com([
            "fslmaths",
            # make sure to use cope images in native space since clusters are back-projected
            f"{run_dir}/native/cope1.nii.gz",
            "-mas",
            mask,
            masked_pe
        ])
        mean_pe = get_mean_pe(masked_pe)
        rows.append([sub, run, roi_name, mean_pe])

    df = pd.DataFrame(rows, columns=["subject", "run", "mask", "mean_cope"])

    if os.path.exists(output_csv):
        df.to_csv(output_csv, mode="a", header=False, index=False)
    else:
        df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sub", help="subject number; include full templeXXX")
    parser.add_argument("roi_path", help="full path to ROI in MNI space")
    parser.add_argument("roi_name", help="shorthand name for ROI")
    parser.add_argument("analysis_type", help="boundary, ppi, ppi_inverse")
    parser.add_argument("ppi_roi", nargs='?', help="roi name if ppi", default = "")
    args = parser.parse_args()
    main(args.sub, args.roi_path, args.roi_name, args.analysis_type, args.ppi_roi)
