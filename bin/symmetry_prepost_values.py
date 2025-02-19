#!/usr/bin/env python

import subprocess

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
from symmetry_function import *

### set up expriment info ###
if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <subject_id> <comparison> <masktype>")
    print("Example: symmetry_prepost_values.py temple016 AC b_hip_subregions")
    sys.exit(1)

sbj = sys.argv[1]
masktype = sys.argv[2]
comp = sys.argv[3]

expdir = '/corral-repl/utexas/prestonlab/temple/'

### masks for data to analyze ###

if masktype == 'whole_brain':
    masks = ['brainmask_func_dilated']
elif masktype == 'b_hip':
    masks = ['b_hip']
elif masktype == 'b_hip_subregions':
    masks = ['warp-b_hip', 'warp-b_hip_ant', 'warp-b_hip_post', 'warp-b_hip_body']

### searchlight information ###

phase, run, triad, item = loadtxt(f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comp}_items.txt',
                                  unpack=1)

### directories ###
subjdir = f'{expdir}/sub-{sbj}/'
betadir = subjdir + '/betaseries'


for mask in masks:
    if masktype == 'b_hip_subregions':
        slmask = f'{subjdir}/transforms/{mask}.nii.gz'


    # load in data - need to swap order if going backward
    if comp in ['BA', 'CB', 'CA']:
        c_fwd = comp[::-1]
    else:
        c_fwd = comp
    ds = fmri_dataset(betadir + f'/pre_post_{c_fwd}_items.nii.gz', mask=slmask)
    ds.sa['phase'] = phase[:]
    ds.sa['run'] = run[:]
    ds.sa['triad'] = triad[:]
    ds.sa['item'] = item[:]

    # similarity measure
    sl_func = symmetry_function('correlation', 1, comp)

    within, across = sl_func(ds)

    resultdir = expdir + f'/integration_prepost/symmetry_{comp}/sub-{sbj}'
    os.makedirs(f'{resultdir}', exist_ok=True)
    out_file_w = f"{resultdir}/{sbj}_symmetry_{comp}_within_{mask}"
    out_file_a = f"{resultdir}/{sbj}_symmetry_{comp}_across_{mask}"



    savetxt(out_file_w, within, fmt="%.8f")
    savetxt(out_file_a, across, fmt="%.8f")