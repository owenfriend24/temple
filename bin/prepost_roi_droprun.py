"""Dissimilarity measure"""

__docformat__ = 'restructuredtext'

import numpy
from numpy import *
from numpy.random import randint
import scipy.stats
from scipy.stats.mstats import zscore
from scipy.ndimage import convolve1d
from scipy.sparse import spdiags
from scipy.linalg import toeplitz
from mvpa2.measures.base import Measure
from mvpa2.measures import rsa

class prepost_roi_droprun(Measure):

    def __init__(self, metric, output, comp):
        Measure.__init__(self)

        self.metric = metric
        self.comp = comp
        self.dsm = []
        self.output = output

    def __call__(self, dataset):

        self.dsm = rsa.PDist( \
            square=True, \
            pairwise_metric=self.metric, \
            center_data=False)

        ### split up the data set into pre and post ###
        pre = dataset[dataset.sa.phase == 1]
        post = dataset[dataset.sa.phase == 2]

        ### calculate the dsm separately for each phase ###
        dsm_pre = self.dsm(pre) # for AC only; len 24
        dsm_post = self.dsm(post) # len 24
        dsm_pre = 1 - dsm_pre.samples
        dsm_post = 1 - dsm_post.samples

        dsm_pre = arctanh(dsm_pre)
        print(f'length of pre-zs: {len(dsm_pre)}')
        dsm_post = arctanh(dsm_post)
        print(f'length of post-zs: {len(dsm_post)}')

        ### calculate the difference to determine representational change ###
        #dsm_diff = numpy.subtract(arctanh(dsm_post), arctanh(dsm_pre)) # len 24

        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        ### loop through the data to sort the within and across comparisons ###
        n_pre = len(dsm_pre)
        n_post = len(dsm_post)

        dsm_diff = dsm_post

        x_len = max(n_pre, n_post)
        y_len = min(n_pre, n_post)

        for x in range(y_len):

            for y in range(x + 1, y_len):

                dstmp = dsm_post[x, y] - dsm_pre[x, y]

                if dataset.sa['run'][x] != dataset.sa['run'][y]:  # only do across run comparisons
                    x_run = dataset.sa['run'][x]
                    y_run = dataset.sa['run'][y]
                    #print(f'run {x_run} not equal to run {y_run}')

                    if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
                        x_tri = dataset.sa['triad'][x]
                        y_tri = dataset.sa['triad'][y]
                        #print(f'triad {x_tri} of run {x_run} vs triad {y_tri} of run {y_run} for within comparison')
                        if dataset.sa['item'][x] != dataset.sa['item'][y]:  # a vs. c

                            within.append(dstmp)
                            #print(f'within: x = {x}, y = {y}') 

                    elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad

                        if dataset.sa['item'][x] != dataset.sa['item'][y]:  # a vs. c

                            across.append(dstmp)
                            #print(f'across: x = {x}, y = {y}') 

        #### convert items to arrays ###
        
        # length 24 - 
        within = array(within)
        
        # length 72 - 
        across = array(across)
        
        
        # return both of these

        return dsm_diff, within, across
        
        