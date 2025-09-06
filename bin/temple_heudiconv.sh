#!/bin/bash
#
# Run heudiconv to convert raw data for one subject.

if [[ $# -lt 4 ]]; then
    echo "Usage: temple_heudiconv.sh subject raw_dir heuristic bids_dir"
    exit 1
fi

subject=$1
raw_dir=$2
heuristic=$3
bids_dir=$4

subj_id=$subject
subj_raw_dir=$raw_dir/$subject

if [[ ! -d $subj_raw_dir ]]; then
    echo "Error: raw directory not found: $subj_raw_dir"
    exit 1
fi

if [[ ! -f $heuristic ]]; then
    echo "Error: heuristic file does not exist: $heuristic"
    exit 1
fi

image=/work/03206/mortonne/software/images/heudiconv-0.11.3.sif
module load tacc-singularity
if [[ $subj_id == "temple_037" ]] || [[ $subj_id == "temple_042" ]]; then
    echo "Running subject: $subj_id with different directory structure"
    singularity run "$image" \
        -s "$subject" \
        -f "$heuristic" \
        -b \
        -o "$bids_dir" \
        --minmeta \
        --files "$subj_raw_dir"/*/*/* \
        --overwrite

elif [[ $subj_id == "temple_131" ]] ; then
    singularity run "$image" \
        -s "$subject" \
        -f "$heuristic" \
        -b \
        -o "$bids_dir" \
        --minmeta \
        --files /work/09123/ofriend/ls6/temple/sourcedata2/temple_131/*/*/* \
          /work/09123/ofriend/ls6/temple/sourcedata2/temple_13111*/*/* \
        --overwrite

else
    singularity run "$image" \
        -s "$subject" \
        -f "$heuristic" \
        -b \
        -o "$bids_dir" \
        --minmeta \
        --files "$subj_raw_dir"/*.* \
        --overwrite 

fi
