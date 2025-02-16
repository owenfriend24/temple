#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
import argparse

def run(command):
    #print(f"Running command: {command}")
    subprocess.run(command, shell=True)

def extract_fs(fs_dir, sub):
    fs = Path(fs_dir)
    src = fs/f'sub-{sub}/mri'
    run(f'mkdir {src}/out') 
    run('module load freesurfer')
    dest = src/'out'
    
    src_names = ['orig', 'brainmask', 'aparc+aseg',
                 'aparc.a2009s+aseg', 'aparc.DKTatlas+aseg']
    dest_names = ['orig', 'orig_brain_auto', 'aparc+aseg',
                   'aparc.a2009s+aseg', 'aparc.DKTatlas+aseg']
    
    
    print('converting freesurfer .mgz images to Nifti')
    for i in range(len(src_names)):
        src_file = src / f'{src_names[i]}.mgz'  
        dest_file = dest / f'{dest_names[i]}.nii.gz'

        if not os.path.exists(src_file):
            run(f'echo FreeSurfer file not found: {src_file}')
            continue

        # convert to Nifti
        run(f'mri_convert {src_file} {dest_file}')

        # fix orientation
        run(f'fslreorient2std {dest_file} {dest_file}')

    # use the FS parcelation to get an improved brain extraction
    
    print('extracting brain with automatic mask')
    # mask for original brain extraction
    brain_auto = dest/'orig_brain_auto'
    mask_auto = dest/'brainmask_auto'
    run(f'fslmaths {brain_auto} -thr 0.5 -bin {mask_auto}')
    
    print('updating mask with freesurfer parcellations')
    # smooth and threshold the identified tissues; fill any remaining holes
    parcel = dest/'aparc+aseg'
    mask_surf = dest/'brainmask_surf'
    run(f'fslmaths {parcel} -thr 0.5 -bin -s 0.25 -bin -fillh26 {mask_surf}')
    # take intersection with original mask (assumed to include all cortex,
    # so don't want to extend beyond that)
    mask = dest/'brainmask'
    run(f'fslmaths {mask_surf} -mul {mask_auto} -bin {mask}')
    print(f'created brain mask image at {mask}')

    
    # create a brain-extracted image based on the orig image from
    # freesurfer (later images have various normalization things done that
    # won't match the MNI template as well)
    
    orig = dest/'orig'
    output = dest/'orig_brain'
    run(f'fslmaths {orig} -mas {mask} {output}')
    print(f'created skull stripped anatomical at {output}')

    # cortex
    cort_out = dest/'ctx'
    run(f'fslmaths {parcel} -thr 1000 -bin {cort_out}')
    print(f'created cortex image at {output}')

    # cerebral white matter
    lwm_out = dest/'l_wm'
    rwm_out = dest/'r_wm'
    wm_out = dest/'wm'
    run(f'fslmaths {parcel} -thr 2 -uthr 2 -bin {lwm_out}')
    run(f'fslmaths {parcel} -thr 41 -uthr 41 -bin {rwm_out}')
    run(f'fslmaths {lwm_out} -add {rwm_out} -bin {wm_out}')
    print(f'created white matter images at {wm_out}')

def main(fs_dir, sub):
    extract_fs(fs_dir, sub)
    print('done.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fs_dir", help="freesurfer directory")
    parser.add_argument("sub", help="subject number; include full templeXXX")
    args = parser.parse_args()
    main(args.fs_dir, args.sub)
