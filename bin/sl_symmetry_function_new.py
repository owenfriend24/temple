"""Dissimilarity measure"""

__docformat__ = 'restructuredtext'

import numpy as np
from numpy.random import shuffle
from scipy.stats.mstats import zscore
from mvpa2.measures.base import Measure
from mvpa2.measures import rsa

class sl_symmetry_function_new(Measure):

    def __init__(self, metric, output, comp, niter):
        Measure.__init__(self)
        self.metric = metric
        self.comp = comp
        self.dsm = []
        self.output = output
        self.niter = niter

    def __call__(self, dataset):

        self.dsm = rsa.PDist(
            square=True,
            pairwise_metric=self.metric,
            center_data=False
        )

        ### Calculate the DSM ###
        dsm_data = self.dsm(dataset)
        dsm_data = 1 - dsm_data.samples
        dsm_diff = np.arctanh(dsm_data)  # Fisher's Z transform

        ### Vectorized extraction of comparisons ###
        n = len(dsm_diff)
        within_fwd, across_fwd = [], []
        within_bwd, across_bwd = [], []

        indices_x, indices_y = np.triu_indices(n, k=1)  # Get upper triangle indices

        for x, y in zip(indices_x, indices_y):
            dstmp = dsm_diff[x, y]

            if dataset.sa['phase'][x] != dataset.sa['phase'][y]:
                if dataset.sa['triad'][x] == dataset.sa['triad'][y]:  # Within triad
                    if dataset.sa['item'][x] == 2 and dataset.sa['item'][y] == 1:  # Forward
                        within_fwd.append(dstmp)
                    elif dataset.sa['item'][x] == 1 and dataset.sa['item'][y] == 2:  # Backward
                        within_bwd.append(dstmp)
                else:  # Across triad
                    if dataset.sa['item'][x] == 2 and dataset.sa['item'][y] == 1:  # Forward
                        across_fwd.append(dstmp)
                    elif dataset.sa['item'][x] == 1 and dataset.sa['item'][y] == 2:  # Backward
                        across_bwd.append(dstmp)

        ### Convert lists to NumPy arrays ###
        within_fwd = np.array(within_fwd)
        across_fwd = np.array(across_fwd)
        within_bwd = np.array(within_bwd)
        across_bwd = np.array(across_bwd)

        ### Compute observed statistics ###
        obsstat_fwd = np.mean(within_fwd) - np.mean(across_fwd)
        obsstat_bwd = np.mean(within_bwd) - np.mean(across_bwd)

        ### Combined within/across arrays for permutation test ###
        randcat_fwd = np.concatenate([within_fwd, across_fwd])
        randcat_bwd = np.concatenate([within_bwd, across_bwd])

        n_within_fwd, n_across_fwd = len(within_fwd), len(across_fwd)
        n_within_bwd, n_across_bwd = len(within_bwd), len(across_bwd)

        ### Vectorized Permutation Test ###
        randstat_fwd = np.zeros(self.niter)
        randstat_bwd = np.zeros(self.niter)

        for i in range(self.niter):
            shuffle(randcat_fwd)
            shuffle(randcat_bwd)

            randstat_fwd[i] = np.mean(randcat_fwd[:n_within_fwd]) - np.mean(randcat_fwd[n_within_fwd:])
            randstat_bwd[i] = np.mean(randcat_bwd[:n_within_bwd]) - np.mean(randcat_bwd[n_within_bwd:])

        ### Compute Z-scores ###
        z_stat_fwd = (obsstat_fwd - np.mean(randstat_fwd)) / np.std(randstat_fwd)
        z_stat_bwd = (obsstat_bwd - np.mean(randstat_bwd)) / np.std(randstat_bwd)

        ### return minimum z score, ensuring that we're only looking for integration in both fwd and bwd directions
        return min(z_stat_fwd, z_stat_bwd)
