#!/usr/bin/env python

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

### import custom searchlight function ###
from prepost_roi import *

### set up experiment info ###
expdir = '/corral-repl/utexas/prestonlab/temple/'

sbj = sys.argv[1]
comparison = sys.argv[2]
masktype = sys.argv[3]


### masks for data to analyze ###
if masktype == 'b_hip_subregions':
    masks = ['warp-b_hip', 'warp-b_hip_ant', 'warp-b_hip_post', 'warp-b_hip_body']
else:
    raise ValueError('no valid mask')

phase, run, triad, item = loadtxt(f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comparison}_items.txt', unpack=1)

### directories ###
subjdir = expdir + '/sub-%s' % (sbj)
betadir = subjdir + '/betaseries'
resultdir = expdir + f'/integration_prepost/prepost_{comparison}'

out_dir = f"{resultdir}/sub-{sbj}"
os.makedirs(out_dir, exist_ok=True)
for mask in masks:
    if masktype == 'b_hip_subregions':
        slmask = f'{subjdir}/transforms/{mask}.nii.gz'

    # load in data
    ds = fmri_dataset(betadir + f'/pre_post_{comparison}_items.nii.gz', mask=slmask)
    ds.sa['phase'] = phase[:]
    ds.sa['run'] = run[:]
    ds.sa['triad'] = triad[:]
    ds.sa['item'] = item[:]

    # similarity measure
    measure = prepost_roi('correlation', 1, comparison)

    # call the measure object to obtain within-pair and across-pair similarity values
    within, across = measure(ds)



    out_file_w = f"{out_dir}/{sbj}_prepost_{comparison}_within_{mask}.txt"
    out_file_a = f"{out_dir}/{sbj}_prepost_{comparison}_across_{mask}.txt"

    savetxt(out_file_w, within, fmt="%.8f")
    savetxt(out_file_a, across, fmt="%.8f")
