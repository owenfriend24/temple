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

    def __init__(self, metric, output, comp, drop_run):
        Measure.__init__(self)

        self.metric = metric
        self.comp = comp
        self.dsm = []
        self.output = output
        self.drop_run = drop_run

    def __call__(self, dataset):

        # self.dsm = rsa.PDist( \
        #     square=True, \
        #     pairwise_metric=self.metric, \
        #     center_data=False)
        #
        # ### split up the data set into pre and post ###
        # pre = dataset[dataset.sa.phase == 1]
        # post = dataset[dataset.sa.phase == 2]
        #
        # ### calculate the dsm separately for each phase ###
        # dsm_pre = self.dsm(pre) # for AC only; len 24
        # dsm_post = self.dsm(post) # len 24
        # dsm_pre = 1 - dsm_pre.samples
        # dsm_post = 1 - dsm_post.samples

        # dsm_pre = arctanh(dsm_pre)
        # #print(f'length of pre-zs: {len(dsm_pre)}')
        # dsm_post = arctanh(dsm_post)
        # #print(f'length of post-zs: {len(dsm_post)}')

        self.dsm = rsa.PDist(square=True, pairwise_metric=self.metric, center_data=False)
        pre = dataset[dataset.sa.phase == 1]
        post = dataset[dataset.sa.phase == 2]

        dsm_pre = self.dsm(pre)  # e.g., shape: 16x16 if pre has 2 runs
        dsm_post = self.dsm(post)  # e.g., shape: 24x24 if post has 3 runs

        # Convert distances to correlations (or similarity) as needed
        dsm_pre = 1 - dsm_pre.samples
        dsm_post = 1 - dsm_post.samples

        # Apply transformation
        dsm_pre = arctanh(dsm_pre)
        dsm_post = arctanh(dsm_post)

        ### Now, instead of looping over a single index range, split by run.
        # Get indices for each run in each phase.
        # (Assume that dataset.sa['run'] is defined for each trial.)
        pre_runs = {}  # e.g., if pre has 2 runs, keys might be 1 and 2
        for r in unique(pre.sa['run']):
            pre_runs[r] = where(pre.sa['run'] == r)[0]

        post_runs = {}  # e.g., if post has 3 runs, keys might be 4,5,6 (or whatever labels)
        for r in unique(post.sa['run']):
            post_runs[r] = where(post.sa['run'] == r)[0]

        within = []
        across = []

        # Now iterate over every pair of runs—one from pre and one from post.
        for r_pre, idx_pre in pre_runs.items():
            for r_post, idx_post in post_runs.items():
                # For each pair of runs, iterate over every trial in the pre run
                # and every trial in the post run.
                for i in idx_pre:
                    for j in idx_post:
                        # Only compare if triad matches and items are different (A vs. C)
                        if pre.sa['triad'][i] == post.sa['triad'][j] and pre.sa['item'][i] != post.sa['item'][j]:
                            # Now, here we must extract the DSM values.
                            # Since dsm_pre is computed on the entire pre-phase dataset, the index i here
                            # corresponds to the row/column in dsm_pre.
                            # Similarly, j corresponds to the index in dsm_post.
                            dstmp = dsm_post[j, j] - dsm_pre[i, i]
                            within.append(dstmp)
                            print(f"within: pre_run {r_pre}, triad {pre.sa['triad'][i]}, item {pre.sa['item'][i]} "
                                  f"to post_run {r_post}, triad {post.sa['triad'][j]}, item {post.sa['item'][j]}: {dstmp}")
                # (You can add similar logic for 'across' comparisons if needed.)

        ### Convert lists to arrays for output
        within = array(within)
        across = array(across)

        return within, across


        # ### set up the vectors to hold the sorted data ###
        # within = []
        # across = []
        #
        # n_pre = len(dsm_pre)
        # n_post = len(dsm_post)
        # print(f"n_pre {n_pre}")
        # print(f"n_post {n_post}")
        # dsm_diff = dsm_post
        #
        # x_len = max(n_pre, n_post)
        # y_len = min(n_pre, n_post)
        # print(f"x_len {x_len}")
        # print(f"y_len {y_len}")
        #
        # # iterate based on whichever phase has a dropped run
        # for x in range(y_len):
        #
        #     for y in range(x + 1, x_len):
        #
        #         dstmp = dsm_post[x, y] - dsm_pre[x, y]
        #
        #         if dataset.sa['run'][x] != dataset.sa['run'][y]:  # only do across run comparisons
        #             x_run = dataset.sa['run'][x]
        #             y_run = dataset.sa['run'][y]
        #             #print(f'run {x_run} not equal to run {y_run}')
        #
        #             if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # within triad
        #                 x_tri = dataset.sa['triad'][x]
        #                 y_tri = dataset.sa['triad'][y]
        #                 #print(f'triad {x_tri} of run {x_run} vs triad {y_tri} of run {y_run} for within comparison')
        #                 if dataset.sa['item'][x] != dataset.sa['item'][y]: # a vs. c
        #                     x_item = dataset.sa['item'][x]
        #                     y_item = dataset.sa['item'][y]
        #
        #                     within.append(dstmp)
        #                     print(f"within: run {x_run} triad {x_tri} item {x_item} to "
        #                           f"run {y_run} triad {y_tri} item {y_item}: {dstmp}")
        #
        #             elif dataset.sa['triad'][x] != dataset.sa['triad'][y]:  # across triad
        #
        #                 if dataset.sa['item'][x] != dataset.sa['item'][y]:  # a vs. c
        #
        #                     across.append(dstmp)
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
        
        