#!/bin/bash
#
# run heudiconv and post-process new subject

if [[ $# -lt 1 ]]; then
    echo "Usage: quick_heu.sh subject"
    exit 1
fi

export PATH=/home1/09123/ofriend/analysis/temple/bin:$PATH
source /home1/09123/ofriend/analysis/temple/profile
subject=$1

temple_heudiconv.sh ${subject} $WORK/temple/sourcedata2 $HOME/analysis/temple/bin/temple_heuristic.py $SCRATCH/temple/new_prepro

temple_bids_post.py $SCRATCH/temple/new_prepro

sub_bids="${subject/_/}"

temple_fmriprep_nofs.sh $SCRATCH/temple/new_prepro $sub_bids
