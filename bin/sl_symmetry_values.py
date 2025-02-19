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

### import custom searchlight function ###
from sl_symm_values_function import *


### set up expriment info ###

sbj = sys.argv[1]
masktype = sys.argv[2]
comp = sys.argv[3]

expdir = '/corral-repl/utexas/prestonlab/temple/'
resultdir = expdir+f'/integration_prepost/symmetry_{comp}/'

### masks for data to analyze ###

if masktype == 'whole_brain':
    masks = ['brainmask_func_dilated']
elif masktype == 'b_hip':
    masks = ['b_hip']

elif masktype == 'sl_hip':
    masks = ['warp-b_hip', 'warp-b_hip_ant', 'warp-b_hip_post', 'warp-b_hip_body']

### searchlight information ###
niter = 1000
phase,run,triad,item = loadtxt(f'/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_{comp}_items.txt',unpack=1)
#comparisons = ['separation','integration']
comparisons = ['integration']

### directories ###
subjdir = expdir+'/sub-%s'%(sbj)
betadir = subjdir+'/betaseries'

###
for comparison in comparisons:

    for mask in masks:

        if masktype == 'mni':
            slmask = subjdir+'/anatomy/antsreg/data/funcunwarpspace/rois/mni/%s.nii.gz'%(mask)
        elif masktype == 'freesurfer':
            slmask = subjdir+'/anatomy/bbreg/data/freesurfer_rois/%s.nii.gz'%(mask)
        elif masktype == 'ants':
            slmask = subjdir+'/anatomy/antsreg/data/funcunwarpspace/rois/schlimack_ants/%s.nii.gz'%(mask)
        elif masktype == 'seg':
            slmask = subjdir+'/anatomy/antsreg/data/funcunwarpspace/rois/seg/%s.nii.gz'%(mask)
        elif masktype == 'whole_brain':
            slmask = expdir+'/sourcedata/freesurfer/sub-%s/mri/out/brainmask_func_dilated.nii.gz'%(sbj)
        elif masktype == 'b_hip':
            slmask = expdir+'/sub-%s/transforms/b_hip.nii.gz'%(sbj)
        elif masktype == 'sl_hip':
            slmask = expdir+'/sub-%s/transforms/%s.nii.gz'%(sbj, mask)

        #load in data
        ds = fmri_dataset(betadir+f'/pre_post_{comp}_items.nii.gz',mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]

        #similarity measure
        sl_func = sl_symm_values_function('correlation',1,comparison,niter)

        within, across = sl_func(ds)
        
        out_file_w = f"{resultdir}/{sbj}_symmetry_{comp}_within_{mask}"
        out_file_a = f"{resultdir}/{sbj}_symmetry_{comp}_across_{mask}"

        os.makedirs(f'{resultdir}/sub-{sbj}', exist_ok=True)
        
        savetxt(out_file_w,within,fmt="%.8f")
        savetxt(out_file_a,across,fmt="%.8f")