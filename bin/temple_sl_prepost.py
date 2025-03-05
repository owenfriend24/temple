#!/usr/bin/env python
import subprocess
subprocess.run(['/bin/bash', '-c', 'source /home1/09123/ofriend/analysis/temple/rsa/bin/activate'])
### import python libraries needed for the analysis ###
import numpy as N
import nibabel
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.datasets.mri import *
import os
import sys
from random import sample
from mvpa2.datasets.mri import *
from mvpa2.mappers.detrend import *
from mvpa2.mappers.zscore import *
from mvpa2.clfs.svm import *
from mvpa2.generators.partition import *
from mvpa2.measures.base import *
from mvpa2.measures import *
from mvpa2.measures.searchlight import *
from mvpa2.misc.stats import *
from mvpa2.base.node import *
from mvpa2.clfs.meta import *
from mvpa2.clfs.stats import *
from mvpa2.featsel.base import *
from mvpa2.featsel.helpers import *
from mvpa2.generators.permutation import *
from mvpa2.generators.base import *
from mvpa2.mappers.fx import *
from mvpa2.measures.anova import *
from mvpa2.base.dataset import *
import sys
import subprocess
import argparse

### import custom searchlight function ###
from searchlight_function_prepost import *
from searchlight_function_prepost_droprun import *

### use argument parser to set up experiment/subject info and drop runs if necessary
def get_args():
    parser = argparse.ArgumentParser(description="Process fMRI data for pre/post comparison.")

    # Required arguments
    parser.add_argument("subject_id", help="Subject identifier (e.g., temple016)")
    parser.add_argument("comparison", help="Comparison type (e.g., AC)")
    parser.add_argument("masktype", help="Mask type (e.g., whole_brain)")
    # Optional argument: drop a specific run
    parser.add_argument("--drop_run", type=int, choices=[1, 2, 3, 4, 5, 6], default=None,
                        help="Run number to drop (1 through 6). Default is None (keep all runs).")

    return parser.parse_args()


### Main script execution ###
if __name__ == "__main__":
    args = get_args()
    sbj = args.subject_id
    comparison = args.comparison
    masktype = args.masktype
    drop_run = args.drop_run

    expdir = '/corral-repl/utexas/prestonlab/temple/'
    # expdir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
    subjdir = os.path.join(expdir, f'sub-{sbj}')
    betadir = os.path.join(subjdir, 'betaseries')
    # resultdir = os.path.join(expdir, f'integration_prepost/prepost_{comparison}')
    temp_result_dir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/'
    resultdir = os.path.join(temp_result_dir, f'integration_prepost/prepost_{comparison}')
    out_dir = os.path.join(resultdir, f'sub-{sbj}')
    os.makedirs(out_dir, exist_ok=True)
    #expdir = '/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
    niter= 1000

    ### masks for data to analyze ###
    if masktype == 'whole_brain':
        masks = ['brainmask_func_dilated']

    if drop_run is not None:
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comparison}_items_drop{drop_run}.txt',
            unpack=True
        )
    else:
        # Load phase, run, triad, and item data
        phase, run, triad, item = np.loadtxt(
            f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comparison}_items.txt',
            unpack=True
        )
    ### directories ###

    ###
    for mask in masks:
        if masktype == 'whole_brain':
            slmask = f'{expdir}/freesurfer/sub-{sbj}/mri/out/brainmask_func_dilated.nii.gz'

        #load in data
        if comparison == 'ABC':
            ds = fmri_dataset(os.path.join(betadir, f'pre_post_items.nii.gz'), mask=slmask)
        else:
            ds = fmri_dataset(os.path.join(betadir, f'pre_post_{comparison}_items.nii.gz'), mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]


        if drop_run is not None:
            measure = searchlight_function_prepost('correlation',1,niter)
        else:
            measure = searchlight_function_prepost_droprun('correlation',1,niter)

        #similarity measure
        sl_func = searchlight_function_prepost('correlation',1,niter)


        #run the searchlight
        sl = sphere_searchlight(sl_func,radius = 3)
        sl_map = sl(ds)

        #save out map
        subjoutfile = f'{out_dir}/{sbj}_prepost_{comparison}_{mask}_z.nii.gz' #z-score computed within searchlight
        map2nifti(ds,sl_map.samples).to_filename(subjoutfile)
