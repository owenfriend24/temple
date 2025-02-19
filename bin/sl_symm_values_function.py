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


class sl_symm_values_function(Measure):

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

        ### split up the data set into pre and post ### don't want to split up since we're not doing direct comparisons within pre and within post for this analysis
        #pre = dataset[dataset.sa.phase == 1]
        #post = dataset[dataset.sa.phase == 2]

        ### calculate the dsm ###
        dsm_data = self.dsm(dataset)
        dsm_data = 1 - dsm_data.samples
        ### convert coefficients to Fisher's Z ###
        dsm_diff = (arctanh(dsm_data))
        ### set up the vectors to hold the sorted data ###
        within = []
        across = []

        ### loop through the data to sort the within and across comparisons ###
        n = len(dsm_diff)

        for x in range(n):

            for y in range(x + 1, n):
                
                dstmp = dsm_diff[x, y]

                # comparing post representations to pre; only interested in post of A and pre of C (or B)

                # are the items different phases?
                #if (dataset.sa['phase'][x] == 2) & (dataset.sa['item'][x] == 1):
                if (dataset.sa['phase'][x] != dataset.sa['phase'][y]):
                    # I think I can just change the 2 to a 1 and 1 to a 2 below for ApreBpost ApreCpost?
                    if (dataset.sa['item'][x] == 2) & (dataset.sa['item'][y] == 1):
                        #print(f"ITEM 1: phase {dataset.sa['phase'][x]} and item {dataset.sa['item'][x]}")
                        #print()
                        #print(f"ITEM 2: phase {dataset.sa['phase'][y]} and item {dataset.sa['item'][y]}")
                        #print(f"ITEM 2: phase {dataset.sa['phase'][x]} and item {dataset.sa['item'][x]}")
                        if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
                            within.append(dstmp)
                            #print(f"within comparison: phase {dataset.sa['phase'][x]} run {dataset.sa['run'][x]} triad {dataset.sa['triad'][x]} item {dataset.sa['item'][x]} to phase {dataset.sa['phase'][y]} run {dataset.sa['run'][y]} triad {dataset.sa['triad'][y]} item {dataset.sa['item'][y]}: {dstmp}")

                        elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad

                            across.append(dstmp)
                            #print(f"across comparison: phase {dataset.sa['phase'][x]} run {dataset.sa['run'][x]} triad {dataset.sa['triad'][x]} item {dataset.sa['item'][x]} to phase {dataset.sa['phase'][y]} run {dataset.sa['run'][y]} triad {dataset.sa['triad'][y]} item {dataset.sa['item'][y]}: {dstmp}")

        #### convert items to arrays ###
        within = array(within)
        across = array(across)

        return within, across
