#!/usr/bin/env python
import os
import subprocess
from pathlib import Path
import argparse

def run(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)
    
    
def extract_func(fs_dir, fmriprep_dir, sub, task, run_num):
    
    run('module load ants')
    
    fs_dir = Path(fs_dir)
    src = fs_dir / f'sub-{sub}/mri'
    
    func_dir = Path(fmriprep_dir) / f'sub-{sub}/func'
    run(f'mkdir {func_dir}/skullstripped_T1')
    dest = func_dir / 'skullstripped_T1'
    
    highres_mask = fs_dir / f'sub-{sub}/mri/out/brainmask'
    mask_func = fs_dir / f'sub-{sub}/mri/out/brainmask_func'
    
    # prepare output directory
    func_data = func_dir / f'sub-{sub}_task-{task}_run-{run_num}_space-T1w_desc-preproc_bold'
    ref_func = func_dir / f'sub-{sub}_task-{task}_run-{run_num}_space-T1w_desc-preproc_bold'
    out_dir = dest / f'sub-{sub}_task-{task}_run-{run_num}_space-T1w_desc-preproc_bold_ss'

    # dilate to make a tighter brain extraction than the liberal one
    # originally used for the functionals
    run(f'fslmaths {highres_mask}.nii.gz -kernel sphere 3 -dilD {highres_mask}.nii.gz')
    
    # resample dilated mask into functional space
    run(f'ANTS 3 -m PR[{ref_func}, {highres_mask}.nii.gz, 1, 4] -t SyN[0.25] -r Gauss[3,0] -o ./mask_to_func -i 30x90x20 -i NearestNeighbor')
    
    run(f'WarpImageMultiTransform 3 {highres_mask}.nii.gz {mask_func}.nii.gz -R {ref_func}.nii.gz ./mask_to_funcWarp.nii.gz ./mask_to_funcAffine.txt --use-NN')

    # mask the unwarped epi
    run(f'fslmaths {func_data}.nii.gz -mas {mask_func}.nii.gz {out_dir}.nii.gz')
    
def main(fs_dir, fmriprep_dir, sub, task, run_num):
    extract_func(fs_dir, fmriprep_dir, sub, task, run_num)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="freesurfer directory")
    parser.add_argument("fmriprep_dir", help="fmriprep derivatives directory")
    parser.add_argument("sub", help="subject number; include full templeXXX")
    parser.add_argument("task", help="task_name")
    parser.add_argument("run_num", help="run number")
    args = parser.parse_args()
    main(args.fs_dir, args.fmriprep_dir, args.sub, args.task, args.run_num)

