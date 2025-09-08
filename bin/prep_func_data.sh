#!/bin/env bash

if [[ $# -lt 3 ]]; then
    echo "Usage: prep_func_data.sh freesurfer_dir fmriprep_dir subject"
    exit 1
fi

fsdir=$1
fmdir=$2
subject=$3

# Load any necessary modules
module load python3/3.9.7

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/temple/profile

# Run your Python script

python /home1/09123/ofriend/analysis/temple/bin/prep_func_data.py "${fsdir}" "${fmdir}" "${subject}"
mni_transforms.sh $fmdir $subject
temple_smooth.sh $fmdir $fsdir $subject "collector"
temple_smooth.sh $fmdir $fsdir $subject "arrow"


# do some extra post-processing/analysis steps that get done for all subjects identically
last3="${subject: -3}"

events_bids.py "/work/09123/ofriend/ls6/temple/sourcebehav" $fmdir $last3
clean_collector.py $fmdir $subject
clean_arrow.py $fmdir $subject
batch_betaseries.sh $subject
move_to_corral.sh $fmdir $subject
prep_coronal.sh $subject