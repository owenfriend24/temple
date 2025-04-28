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


class searchlight_function_AC_differentiation(Measure):

    def __init__(self, metric, output, niter):
        Measure.__init__(self)

        self.metric = metric
        self.dsm = []
        self.output = output
        self.niter = niter

    def __call__(self, dataset):

        self.dsm = rsa.PDist( \
            square=True, \
            pairwise_metric=self.metric, \
            center_data=False)

        ### split up the data set into pre and post ###
        pre = dataset[dataset.sa.phase == 1]
        post = dataset[dataset.sa.phase == 2]

        ### calculate the dsm separately for each phase ###
        dsm_pre = self.dsm(pre)
        dsm_post = self.dsm(post)
        dsm_pre = 1 - dsm_pre.samples
        dsm_post = 1 - dsm_post.samples

        ### calculate the difference to determine representational change ###
        dsm_diff = numpy.subtract(arctanh(dsm_post), arctanh(dsm_pre))

        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm_diff)

        for x in range(n):
            for y in range(x + 1, n):
                dstmp = dsm_diff[x, y]
                if dataset.sa['run'][x] != dataset.sa['run'][y]:  # only do across run comparisons
                    if dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad for weak pairs
                        if abs(dataset.sa['item'][x] - dataset.sa['item'][y]) == 2:  # e.g., a vs. c - (3 vs 1 or 1 vs 3)
                            within.append(dstmp)
                        elif abs(dataset.sa['item'][x] - dataset.sa['item'][y]) == 1:  # a and b or b and c for shuffle
                            across.append(dstmp)

        #### convert items to arrays ###
        within = array(within)
        across = array(across)

        ### calculate the observed statistic ###
        obsstat = mean(across) - mean(within)

        ### determine the number of within/across comparisons for the permutation test ###
        n_within = len(within)
        n_across = len(across)
        n_total = n_within + n_across

        ### calculate the random statistic ###
        randstat = []
        for iter in range(self.niter):
            randcat = numpy.concatenate([within, across])
            random.shuffle(randcat)
            within_shuff = randcat[0:n_within]
            across_shuff = randcat[n_within:n_total]

            randstat.append(mean(across_shuff) - mean(within_shuff))

        ### calculate the p-value for the center searchlight sphere voxel ###
        randstat = array(randstat)


        # if self.comp == 'separation':
        #     return mean(randstat <= obsstat)

        # return mean(randstat>=obsstat)
        return (obsstat - mean(randstat)) / std(randstat)
