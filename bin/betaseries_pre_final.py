#!/usr/bin/env python

### load in some modules to run the stuff ###
from mvpa2.misc.fsl.base import *
from mvpa2.datasets.mri import fmri_dataset
from mvpa2.measures.rsa import PDist
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
from copy import copy

### directory for experiment and design matrices ###
expdir = '/work/05409/nlv329/lonestar/Decouple2'
designdir =expdir+'/batch/analysis/ItemLevelGLM/designmats'

### subjects to analyze as the input ###
sub = sys.argv[1]

### regressor indices and output ###
good_evs = range(0,12)
output_evs = good_evs
ntrials_total = len(good_evs)

### runs to model ###
runs = ['1','2','3']

### all of the directories for this subject ###
subdir = expdir+'/decouple_%s'%(sub)
bolddir = subdir+'/BOLD'
modeldir = subdir+'/model/betaseries'
betadir = modeldir
mask = bolddir+'/antsreg/data/mask.nii.gz'
	
### for each run ###
for run in runs:
	
		matfile = designdir+'/final_pre_%s_%s.mat'%(sub,run)
		desmat = FslGLMDesign(matfile)
		nevs = desmat.mat.shape[1]
		ntp = desmat.mat.shape[0]
		
		# load in the data and the design matrix
		bolddata = bolddir+'/antsreg/data/arrow_%s_sm.nii.gz'%(run)
		confoundfile = bolddir+'/arrow_%s/QA/confound.txt'%(run)
        
   		# load data
		data = fmri_dataset(bolddata,mask=mask)
       
		# below here is a bunch of Jeannette stuff
		dm_nuisance = N.loadtxt(confoundfile)
		trial_ctr = 0
		all_conds = []
		beta_maker = N.zeros((ntrials_total,ntp))

    	# for all of the "good" evs
		for e in range(len(good_evs)):
    
			ev = good_evs[e]
                
			dm_toi = desmat.mat[:,ev]
                
			other_good_evs = [x for x in good_evs if x != ev]
			dm_otherevs = desmat.mat[:,other_good_evs]
			dm_otherevs = N.sum(dm_otherevs[:,:,N.newaxis],axis=1)

        	# Put together the design matrix
			dm_full = N.hstack((dm_toi[:,N.newaxis],dm_otherevs,dm_nuisance))
                
        	# making betas
			dm_full = dm_full - N.kron(N.ones((dm_full.shape[0],dm_full.shape[1])), \
                    	N.mean(dm_full,0))[0:dm_full.shape[0],0:dm_full.shape[1]]
			dm_full=N.hstack((dm_full,N.ones((ntp,1))))
			beta_maker_loop=N.linalg.pinv(dm_full)
			beta_maker[trial_ctr,:]=beta_maker_loop[0,:]
			trial_ctr+=1

    	# this uses Jeanette's trick of extracting the beta-forming vector for each
    	# trial and putting them together, which allows estimation for all trials
    	# at once
		glm_res_full = N.dot(beta_maker,data.samples)

		# map the data into images and save to betaseries directory
		for e in output_evs:
			outdata = zscore(glm_res_full[e])
			ni = map2nifti(data,data=outdata)
			ni.to_filename(betadir+'/pre_%s_ev%03d.nii.gz'%(run,e))
			