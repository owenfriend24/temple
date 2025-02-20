#!/usr/bin/env python
import os
import subprocess
from pathlib import Path
import argparse

def run(command):
    # print(f"Running command: {command}")
    subprocess.run(command, shell=True)

# Function to smooth functional data with a 4.0 FWHM kernel
# Function to smooth functional data with a 4.0 FWHM kernel
def smooth_func(fs_dir, fmriprep_dir, sub, task, num_runs):
    fs_dir = Path(fs_dir)
    mask = fs_dir / f'sub-{sub}/mri/out/brainmask_func.nii.gz'
    func_dir = Path(fmriprep_dir) / f'sub-{sub}/func'
    kernel = 4.0

    for func_run in range(1, int(num_runs) + 1):
        func_input = func_dir / f'skullstripped_T1/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold_ss.nii.gz'
        func_output = func_dir / f'skullstripped_T1/sub-{sub}_task-{task}_run-0{func_run}_space-T1w_desc-preproc_bold_ss_4mm.nii.gz'
        run(f'smooth_susan {func_input} {mask} {kernel} {func_output}')

def main(fs_dir, fmriprep_dir, sub, task, num_runs):
    run('source /home1/09123/ofriend/analysis/temple/profile')
    extract_fs(fs_dir, sub)
    print(f'\n\nMASK EXTRACTED FOR SUB-{sub}\n\n')
    extract_func(fs_dir, fmriprep_dir, sub, task, num_runs)
    print(f'\n\nSKULLSTRIPPING COMPLETE FOR SUB-{sub}\n\n')
    smooth_func(fs_dir, fmriprep_dir, sub, task, num_runs)
    print(f'\n\nSMOOTHING COMPLETE FOR SUB-{sub}\n\n')
