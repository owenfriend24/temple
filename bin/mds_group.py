#!/usr/bin/env python
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import os
import os
import nibabel as nib
from nilearn import image
from nilearn import masking
from scipy.stats import pearsonr
from sklearn.metrics import pairwise_distances
import os
import subprocess
from pathlib import Path
import argparse
import pandas as pd
def run_com(command):
    print(f"Running command: {command}")
    subprocess.run(command, shell=True)


def get_adults():
    ads = [19, 20, 22, 23, 25, 37, 57, 58, 59, 74, 72, 16, 24, 50, 56, 73, 71, 76]
    adults = []
    for a in ads:
        adults.append(f'temple0{a}')
    return adults

def main(fmriprep_dir, mask_label):
    ads = get_adults()
    ad_dfs = []
    for a in ads:
        ad_dfs.append(pd.read_csv(f'{fmriprep_dir}/sub-{a}/betaseries/avg_post_dists_{mask_label}.csv'))
    ad_mask_avg = pd.DataFrame()
    for df in ad_dfs:
        if ad_mask_avg.empty:
            ad_mask_avg = df.copy()
        else:
            ad_mask_avg += df
    ad_mask_avg /= len(ad_dfs)
    ad_mask_avg.to_csv(f'{fmriprep_dir}/searchlight/adult_avg_post_dists_{mask_label}.csv')
                       
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fmriprep_dir", help="fmriprep derivatives directory")
    parser.add_argument("mask_label", help="mask label for output")
    args = parser.parse_args()
    main(args.fmriprep_dir, args.mask_label)