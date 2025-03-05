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


class sl_symmetry_function(Measure):

    def __init__(self, metric, output, comp, niter):
        Measure.__init__(self)

        self.metric = metric
        self.comp = comp
        self.dsm = []
        self.output = output
        self.niter = niter

    def __call__(self, dataset):

        self.dsm = rsa.PDist( \
            square=True, \
            pairwise_metric=self.metric, \
            center_data=False)

        ### calculate the dsm ###
        dsm_data = self.dsm(dataset)
        dsm_data = 1 - dsm_data.samples
        ### convert coefficients to Fisher's Z ###
        dsm_diff = (arctanh(dsm_data))
        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        # what we need to do here is pull the observed stat for forward AND backward integration,
        # then combine thsoe z-scores using Stouffer's method (dividing by sq. root of 2)

        ### loop through the data to sort the within and across comparisons ###

        # forward direction first
        n = len(dsm_diff)
        for x in range(n):
            for y in range(x + 1, n):
                dstmp = dsm_diff[x, y]

                if dataset.sa['phase'][x] != dataset.sa['phase'][y]:
                    if (dataset.sa['item'][x] == 2) & (dataset.sa['item'][y] == 1):
                        if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
                            within.append(dstmp)
                        elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad
                            across.append(dstmp)
        within = array(within)
        across = array(across)
        obsstat = mean(within) - mean(across)

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
            randstat.append(mean(within_shuff) - mean(across_shuff))

        ### calculate the p-value for the center searchlight sphere voxel ###
        randstat = array(randstat)

        z_stat_fwd = (obsstat - mean(randstat)) / std(randstat)



     # go again in the backward direction
        for x in range(n):
            for y in range(x + 1, n):
                dstmp = dsm_diff[x, y]

                if dataset.sa['phase'][x] != dataset.sa['phase'][y]:
                    if (dataset.sa['item'][x] == 1) & (dataset.sa['item'][y] == 2):
                        if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
                            within.append(dstmp)
                        elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad
                            across.append(dstmp)
        within = array(within)
        across = array(across)
        obsstat = mean(within) - mean(across)

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
            randstat.append(mean(within_shuff) - mean(across_shuff))

        ### calculate the p-value for the center searchlight sphere voxel ###
        randstat = array(randstat)

        z_stat_bwd = (obsstat - mean(randstat)) / std(randstat)


        return (z_stat_fwd + z_stat_bwd)/sqrt(2)

