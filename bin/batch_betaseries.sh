#!/bin/bash
if [[ $# -lt 1 ]]; then
    echo "Usage: batch_betaseries.sh subject"
    exit 1
fi
### set up experiment info ###
expdir='/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
sub=$1

source /home1/09123/ofriend/analysis/temple/profile

prep_arrow.py $expdir both $sub
beta_fsfs.sh $sub
beta_files.sh $sub

betadir=$expdir/sub-${sub}/betaseries
mkdir -p betadir
cd $betadir

source /home1/09123/ofriend/analysis/temple/rsa/bin/activate
betaseries_est.py $sub
merge_betas_prepost.sh $sub
