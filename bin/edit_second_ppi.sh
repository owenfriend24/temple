#!/bin/bash

if [[ $# -lt 3 ]]; then
    echo "Usage: edit_first_fsf.sh template out_path subject"
    exit 1
fi

template=$1
out_path=$2
subject=$3
analysis_type=$4

# Load any necessary modules
module load python3/3.9.7

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/temple/profile

# Move to the directory containing your Python script
cd /home1/09123/ofriend/analysis/temple/bin

# Run your Python script
python edit_first_ppi.py $template $out_path $subject 5 222 222 $analysis_type

# clean this up later:
# 5 = run (not used)
# 222 vols = flags that it's second level analysis
# 222 voxels (not used)


