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


        if self.drop_run in [1, 2, 3]:  # Dropped a pre run
            pre_indices = where(dataset.sa.phase == 1)[0]  # Indices for pre phase (16 trials)
            post_indices = where(dataset.sa.phase == 2)[0]  # Indices for post phase (24 trials)
        elif self.drop_run in [4, 5, 6]:  # Dropped a post run
            pre_indices = where(dataset.sa.phase == 1)[0]  # Indices for pre phase (24 trials)
            post_indices = where(dataset.sa.phase == 2)[0]  # Indices for post phase (16 trials)
        else:
            raise ValueError(f"Invalid drop_run value: {self.drop_run}. Must be 1-6.")

        pre_size = len(pre_indices)
        post_size = len(post_indices)

        print(f"Pre matrix size: {pre_size}x{pre_size}")
        print(f"Post matrix size: {post_size}x{post_size}")


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
        within = []
        across = []

        for i, pre_x in enumerate(pre_indices):
            for j, post_y in enumerate(post_indices):

                if dataset.sa['run'][pre_x] != dataset.sa['run'][post_y]:  # Across-run only
                    if dataset.sa['triad'][pre_x] == dataset.sa['triad'][post_y]:  # Within-triad
                        if dataset.sa['item'][pre_x] != dataset.sa['item'][post_y]:  # A vs. C

                            # Correct DSM index mapping
                            dstmp = dsm_post[j, j] - dsm_pre[i, i]
                            within.append(dstmp)

                            print(
                                f"within: pre_run={dataset.sa['run'][pre_x]} to post_run={dataset.sa['run'][post_y]}, "
                                f"triad {dataset.sa['triad'][pre_x]}: {dstmp}")

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
        
        