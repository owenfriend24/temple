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

subprocess.run('. /home1/09123/ofriend/analysis/temple/rsa/bin/activate', shell = True)

### set up expriment info ###
expdir = '/corral-repl/utexas/prestonlab/temple/'
resultdir = expdir+'/searchlight/prepost_AC'
sbj = sys.argv[1]
masktype = sys.argv[2]

### masks for data to analyze ###
if masktype == 'mni':
    masks = ['b_hip','b_mpfc']
elif masktype == 'freesurfer':
    masks = ['b_gray']
elif masktype == 'ants':
    masks = ['l_ca1','r_ca1','l_dg','r_dg','l_ca23','r_ca23','l_ca23dg','r_ca23dg','b_ca1','b_dg','b_ca23']
elif masktype == 'seg':
    masks = ['gm']
elif masktype == 'whole_brain':
    masks = ['brainmask_func_dilated']
elif masktype == 'hippocampus':
    masks = ['b_hip', 'b_hip_ant', 'b_hip_post', 'b_hip_body', 'b_hip_tail']
### searchlight information ###
#niter = 1000
phase,run,triad,item = loadtxt('/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_AC_items.txt',unpack=1)
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
        elif masktype == 'hippocampus':
            slmask = expdir+f'/sub-%s/transforms/{mask}.nii.gz'%(sbj)

        #load in data
        ds = fmri_dataset(betadir+'/pre_post_AC_items.nii.gz',mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]

        #similarity measure
        measure = prepost_roi('correlation', 1, comparison)

        # call the measure object to obtain within-pair and across-pair similarity values
        within, across = measure(ds)
        
        #within, across = prepost_roi('correlation',1,comparison)
        #results_w = within(ds)
        #results_a = across(ds)
        
        os.chdir(f"/{expdir}/searchlight/prepost_AC")
        
        subjoutfile_w = "%s_prepost_%s_%s.txt"%(sbj,'within',mask)
        subjoutfile_a = "%s_prepost_%s_%s.txt"%(sbj,'across',mask)

        savetxt(subjoutfile_w,within,fmt="%.8f")
        savetxt(subjoutfile_a,across,fmt="%.8f")
     
        """
        #for testing with whole roi
        #results = sl_func(ds)
        #os.chdir("/corral-repl/utexas/prestonlab/garnet/results/searchlight")
        #subjoutfile = "%s_prepost_%s_%s.txt"%(sbj,comparison,mask)
        #savetxt(subjoutfile,results,fmt="%.8f")


        #run the searchlight
        sl = sphere_searchlight(sl_func,radius = 3)
        sl_map = sl(ds)

        #save out map
        #subjoutfile = resultdir+'/%s_prepost_%s_%s.nii.gz'%(sbj,comparison,mask) #p-score computed within searchlight
        subjoutfile = resultdir+'/%s_prepost_%s_z.nii.gz'%(sbj,mask) #z-score computed within searchlight
        map2nifti(ds,sl_map.samples).to_filename(subjoutfile)
        """
