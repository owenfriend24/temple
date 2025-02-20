#!/bin/bash

### set up experiment info ###
expdir='/scratch/09123/ofriend/temple/prepro_data/derivatives/fmriprep'
sub=$1

source /home1/09123/ofriend/analysis/temple/profile

fix_arrow.py $expdir $sub
fix_collector.py $expdir $sub
