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
from prepost_roi_droprun import *

#subprocess.run('. /home1/09123/ofriend/analysis/temple/rsa/bin/activate', shell = True)

### set up expriment info ###
expdir = '/scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep'
resultdir = expdir+'/searchlight/prepost_AC'
sbj = sys.argv[1]
masktype = sys.argv[2]

ad = [19, 20, 22, 23, 25, 37, 57, 59, 74, 72, 16, 24, 50, 56, 73, 71, 76]
ten = [29, 51, 30, 33, 35, 60, 36, 32, 45, 38, 42, 63]
sev = [41, 64, 70, 34, 65, 66, 53, 68]

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
elif masktype == 'b_hip':
    masks = ['b_hip', 'right_hip', 'left_hip']
elif masktype == 'sl':
    if int(sbj[-2:]) in ad:
        masks = ['b_hip', 'b_hip_ant', 'b_hip_post', 'b_hip_body', 'ad_abc_hip', 'ad_abc_wb_14832', 'ad_abc_wb_14837', 'ad_abc_wb_14845', 'ad_abc_wb_14849', 'ad_abc_wb_14861', 'ad_ac_hip', 'ad_ac_wb_15310', 'ad_ac_wb_15335', 'ad_ac_wb_15337']
    elif int(sbj[-2:]) in ten:
        masks = ['b_hip', 'b_hip_ant', 'b_hip_post', 'b_hip_body', 'te_abc_wb_14682', 'te_abc_wb_14685', 'te_abc_wb_14687', 'te_ac_hip_32408', 'te_ac_hip_32409', 'te_ac_hip_32410', 'te_ac_hip_32411', 'te_ac_wb_14724', 'te_ac_wb_14732']
    elif int(sbj[-2:]) in sev:
        masks = ['b_hip', 'b_hip_ant', 'b_hip_post', 'b_hip_body', 'se_abc_wb_10061', 'se_ac_hip_25566', 'se_ac_hip_25567', 'se_ac_hip_25568', 'se_ac_wb_10561', 'se_ac_wb_10562', 'se_ac_wb_10566', 'se_ac_wb_10572', 'se_ac_wb_10573']


### searchlight information ###
niter = 1000
phase,run,triad,item = loadtxt('/home1/09123/ofriend/analysis/temple/bin/templates/pre_post_ABC_items_drop3.txt',unpack=1)
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
            slmask = expdir+'/sourcedata/freesurfer/sub-%s/mri/out/%s_func.nii.gz'%(sbj, mask)
        elif masktype == 'sl':
            slmask = expdir+'/sub-%s/transforms/%s.nii.gz'%(sbj, mask)

        #load in data
        ds = fmri_dataset(betadir+'/pre_post_items.nii.gz',mask=slmask)
        ds.sa['phase'] = phase[:]
        ds.sa['run'] = run[:]
        ds.sa['triad'] = triad[:]
        ds.sa['item'] = item[:]

        #similarity measure
        measure = prepost_roi_droprun('correlation', 1, comparison)

        # call the measure object to obtain within-pair and across-pair similarity values
        dsm_diff, within, across = measure(ds)
        
        #within, across = prepost_roi('correlation',1,comparison)
        #results_w = within(ds)
        #results_a = across(ds)
        
        subjoutfile_w = "%s/%s_prepost_%s_%s.txt"%(sbj, sbj,'within',mask)
        subjoutfile_a = "%s/%s_prepost_%s_%s.txt"%(sbj, sbj,'across',mask)
        #subjoutfile_d = "%s/%s_prepost_%s_%s.txt"%(sbj, sbj,'dsdiff',mask)
        
        os.chdir("/scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep/searchlight/prepost_ABC_txt")
        
        savetxt(subjoutfile_w,within,fmt="%.8f")
        savetxt(subjoutfile_a,across,fmt="%.8f")
        #savetxt(subjoutfile_d,dsm_diff,fmt="%.8f")
         
       