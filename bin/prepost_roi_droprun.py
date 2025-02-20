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
        #print(f'length of pre-zs: {len(dsm_pre)}')
        dsm_post = arctanh(dsm_post)
        #print(f'length of post-zs: {len(dsm_post)}')

        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        n_pre = len(dsm_pre)
        n_post = len(dsm_post)
        print(f"n_pre {n_pre}")
        print(f"n_post {n_post}")
        dsm_diff = dsm_post

        x_len = max(n_pre, n_post)
        y_len = min(n_pre, n_post)
        print(f"x_len {x_len}")
        print(f"y_len {y_len}")

        # iterate based on whichever phase has a dropped run
        for x in range(y_len):

            for y in range(x + 1, x_len):

                dstmp = dsm_post[x, y] - dsm_pre[x, y]

                if dataset.sa['run'][x] != dataset.sa['run'][y]:  # only do across run comparisons
                    x_run = dataset.sa['run'][x]
                    y_run = dataset.sa['run'][y]
                    #print(f'run {x_run} not equal to run {y_run}')

                    if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
                        x_tri = dataset.sa['triad'][x]
                        y_tri = dataset.sa['triad'][y]
                        #print(f'triad {x_tri} of run {x_run} vs triad {y_tri} of run {y_run} for within comparison')
                        if dataset.sa['item'][x] != dataset.sa['item'][y]: # a vs. c
                            x_item = dataset.sa['item'][x]
                            y_item = dataset.sa['item'][y]

                            within.append(dstmp)
                            print(f"within: run {x_run} triad {x_tri} item {x_item} to "
                                  f"run {y_run} triad {y_tri} item {y_item}: {dstmp}")

                    elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad

                        if dataset.sa['item'][x] != dataset.sa['item'][y]:  # a vs. c

                            across.append(dstmp)
                            #print(f"across: run {x_run} triad {x_tri} item {x_item} to "
                              #    f"run {y_run} triad {y_tri} item {y_item}: {dstmp}")


        #### convert items to arrays ###

        # length 8... should be 12-
        # for example, if dropping run 3:
        # A1C2 to A4C5, A4C6, A5C4, A5C6, A6C4, A6C5
        # A2C1 to A4C5, A4C6, A5C4, A5C6, A6C4, A6C5
        within = array(within)
        
        # length  - 24
        across = array(across)

        # return both of these
        return within, across
        
        