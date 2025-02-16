#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: prep_univ_files.sh fmriprep_dir subject"
    exit 1
fi

fmdir=$1
subject=$2

# Load any necessary modules
module load python

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/temple/profile

# Move to the directory containing your Python script
cd /home1/09123/ofriend/analysis/temple/bin

# create univ folder in subject directory
mkdir "$fmdir/sub-$subject/univ"

# Run your Python script
python fix_collector.py "$fmdir $subject"
python univ_text_files.py "$fmdir both $subject $fmdir/sub-$subject/univ"