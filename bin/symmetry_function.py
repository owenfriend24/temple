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


class symmetry_function(Measure):

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


        # calculate the dsm
        dsm_data = self.dsm(dataset)
        dsm_data = 1 - dsm_data.samples
        # convert coefficients to Fisher's Z
        dsm_diff = (arctanh(dsm_data))
        # set up the vectors to hold the sorted data
        within = []
        across = []

        # loop through the data to sort the within and across comparisons
        # forward integration
        if self.comp in ['AB', 'BC', 'AC']:
            first_item = 2
            second_item = 1
        # backward integration
        elif self.comp in ['BA', 'CB', 'CA']:
            first_item = 1
            second_item = 2
        else:
            raise ValueError("specify valid comparison (e.g., AB, CA")



        n = len(dsm_diff)
        for x in range(n):
            for y in range(x + 1, n):
                dstmp = dsm_diff[x, y]

                # comparing post representations to pre; only interested in post of A and pre of B/C or vice versa
                # are the items different phases?
                if (dataset.sa['phase'][x] != dataset.sa['phase'][y]):
                    # parse whether we're looking for forward or backward integration
                    if (dataset.sa['item'][x] == first_item) & (dataset.sa['item'][y] == second_item):
                        if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
                            within.append(dstmp)
                            print(f"within comparison: phase {dataset.sa['phase'][x]} run {dataset.sa['run'][x]} triad {dataset.sa['triad'][x]} item {dataset.sa['item'][x]} to phase {dataset.sa['phase'][y]} run {dataset.sa['run'][y]} triad {dataset.sa['triad'][y]} item {dataset.sa['item'][y]}: {dstmp}")

                        elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad

                            across.append(dstmp)
                            print(f"across comparison: phase {dataset.sa['phase'][x]} run {dataset.sa['run'][x]} triad {dataset.sa['triad'][x]} item {dataset.sa['item'][x]} to phase {dataset.sa['phase'][y]} run {dataset.sa['run'][y]} triad {dataset.sa['triad'][y]} item {dataset.sa['item'][y]}: {dstmp}")

        within = array(within)
        across = array(across)

        return within, across
