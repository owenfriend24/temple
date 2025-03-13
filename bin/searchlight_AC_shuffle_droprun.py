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


class searchlight_AC_shuffle_droprun(Measure):

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

        dsm_pre = arctanh(dsm_pre)
        dsm_post = arctanh(dsm_post)


        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        ### loop through the data to sort the within and across comparisons ###

        n_pre = len(dsm_pre)
        n_post = len(dsm_post)

        min_len = min(n_pre, n_post)

        for x in range(min_len):

            for y in range(x + 1, min_len):

                if dataset.sa['run'][x] != dataset.sa['run'][y]:  # only do across run comparisons

                    if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad

                        if abs(dataset.sa['item'][x] - dataset.sa['item'][y]) == 2:  # a vs. c
                            dstmp = dsm_post[x, y] - dsm_pre[x, y]
                            within.append(dstmp)

                    elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad
                        if abs(dataset.sa['item'][x] - dataset.sa['item'][y]) == 1:  # a vs. c
                            dstmp = dsm_post[x, y] - dsm_pre[x, y]
                            across.append(dstmp)

        #### convert items to arrays ###
        within = array(within)
        across = array(across)

        ### calculate the observed statistic ###
        obsstat = mean(within) - mean(across)
        #obsstat=mean(within)

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
            #randstat.append(mean(within_shuff))
            randstat.append(mean(within_shuff) - mean(across_shuff))

        ### calculate the z-stat for the center searchlight sphere voxel ###
        randstat = array(randstat)

        return (obsstat - mean(randstat)) / std(randstat)
