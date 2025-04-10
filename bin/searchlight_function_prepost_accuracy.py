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
from scipy.stats import pearsonr


class searchlight_function_prepost_accuracy(Measure):

    def __init__(self, metric, output, niter, acc_array):
        Measure.__init__(self)

        self.metric = metric
        self.dsm = []
        self.output = output
        self.niter = niter
        self.acc_array = acc_array

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

        triads = np.unique(dataset.sa['triad'])
        triads.sort()  # Ensure consistent ordering
        triad_similarity = {triad: [] for triad in triads}
        accuracy_dict = dict(zip(triads, self.acc_array))



        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm_diff)

        for x in range(n):
            for y in range(x + 1, n):
                if dataset.sa['run'][x] != dataset.sa['run'][y]:  # across-run only
                    triad_x = dataset.sa['triad'][x]
                    triad_y = dataset.sa['triad'][y]
                    item_x = dataset.sa['item'][x]
                    item_y = dataset.sa['item'][y]

                    if triad_x == triad_y and item_x != item_y:
                        triad_similarity[triad_x].append(dsm_diff[x, y])

        triad_means = []
        triad_accuracies = []

        for triad in triads:
            sims = triad_similarity[triad]
            if len(sims) > 0:
                triad_means.append(np.mean(sims))
                triad_accuracies.append(accuracy_dict[triad])

        if len(triad_means) >= 2:
            r_obs, _ = pearsonr(triad_means, triad_accuracies)
            obsstat = np.arctanh(r_obs)  # Fisher z-transform
        else:
            return 0.0  # insufficient data

            ### Permutation test ###
        randstat = []
        for _ in range(self.niter):
            shuffled_acc = np.random.permutation(triad_accuracies)
            r_rand, _ = pearsonr(triad_means, shuffled_acc)
            randstat.append(np.arctanh(r_rand))

        randstat = np.array(randstat)

        ### Compute z-statistic ###
        zstat = (obsstat - np.mean(randstat)) / np.std(randstat)
        return zstat