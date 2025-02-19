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

class prepost_roi(Measure):

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
        pre_dist = dsm_pre.samples
        post_dist = dsm_post.samples
        dsm_pre = 1 - dsm_pre.samples
        dsm_post = 1 - dsm_post.samples

        ### calculate the difference to determine representational change ###
            # this is a very important step conceptually, this is where we take the pre and post DSM's
            # and normalize and subtract them, which means we now have every possible comparison.
            # That means the later steps are going to be where we essentially prune those comparisons
            # and in doing so only take the values that include comparisons derived across runs to avoid
            # the inherent autocorrelation of the bold signal
        dsm_diff = numpy.subtract(arctanh(dsm_post), arctanh(dsm_pre)) # len 24

        # older code looking at a different distance metric
        #dist_df = numpy.subtract(post_dist, pre_dist)


        ### set up the vectors to hold the sorted data ###
        within = []
        across = []
        
        #w_distance = []
        #a_distance = []

        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm_diff)

        for x in range(n):

            for y in range(x + 1, n):

                dstmp = dsm_diff[x, y]
                #dst = dist_df[x,y]

                if dataset.sa['run'][x] != dataset.sa['run'][y]:  # only do across run comparisons (post: 6(1) to 5(3); 6(1) to 4(3);  - so for item 1 to 3; two representational change values. 

                    if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad

                        if dataset.sa['item'][x] != dataset.sa['item'][y]:  # a vs. c

                            within.append(dstmp)
                            #w_distance.append(dst)
                            #print(f"within comparison: "
                                 # f"run {dataset.sa['run'][x]} triad {dataset.sa['triad'][x]} item {dataset.sa['item'][x]} to "
                                #  f"run {dataset.sa['run'][y]} triad {dataset.sa['triad'][y]} item {dataset.sa['item'][y]}: {dstmp}")

                    elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad

                        if dataset.sa['item'][x] != dataset.sa['item'][y]:  # a vs. c

                            across.append(dstmp)
                            #a_distance.append(dst)
                            #print(f"across comparison: "
                                #  f"triad {dataset.sa['triad'][x]} item {dataset.sa['item'][x]} to "
                                 # f"triad {dataset.sa['triad'][y]} item {dataset.sa['item'][y]}: {dstmp}")


        #### convert items to arrays ###
        
        # length 24 - 
        within = array(within)
        
        # length 72 - 
        across = array(across)

        #w_distance = array(w_distance)
        #a_distance = array(a_distance)
        
        
        # return both of these

        return within, across
        
        