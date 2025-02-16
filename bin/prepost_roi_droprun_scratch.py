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

class prepost_roi_droprun_scratch(Measure):

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

        ### calculate the difference to determine representational change ###
        #dsm_diff = numpy.subtract(arctanh(dsm_post), arctanh(dsm_pre)) # len 24

        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        ### loop through the data to sort the within and across comparisons ###
        n_pre = len(dsm_pre)
        n_post = len(dsm_post)

        for x in range(n_pre):

            for y in range(x + 1, n_pre):

                    for z in range(n_post):
                        for q in range(z + 1, n_post):

                            if (pre.sa['run'][x] != pre.sa['run'][y]) & (post.sa['run'][z] != post.sa['run'][q]):
                                pre_runx = pre.sa['run'][x]
                                pre_runy = pre.sa['run'][y]
                                post_runx = post.sa['run'][z]
                                post_runy = post.sa['run'][q]
                                print(f'pre run {pre_runx} and pre run {pre_runy} vs post run {post_runx} and post run {post_runy}')
                                if (pre.sa['triad'][x] == pre.sa['triad'][y]) & (post.sa['run'][z] == post.sa['run'][q]):  # within triad

                                    if (pre.sa['item'][x] != pre.sa['item'][y]) & (post.sa['run'][z] != post.sa['run'][q]):   # a vs. c

                                        within.append((dsm_post[z][q]) - (dsm_pre[x][y]))

                                elif (pre.sa['triad'][x] != pre.sa['triad'][y]) & (post.sa['run'][z] != post.sa['run'][q]):  # across triad

                                    if (pre.sa['item'][x] != pre.sa['item'][y]) & (post.sa['item'][z] != post.sa['item'][q]):  # a vs. c

                                        across.append((dsm_post[z][q]) - (dsm_pre[x][y]))
        

# may just need to set up the direct comparisons I want

        
        #### convert items to arrays ###
        
        # length 24 - 
        within = array(within)
        
        # length 72 - 
        across = array(across)
        
        dsm_diff = within
        # return both of these

        return dsm_diff, within, across
        
        