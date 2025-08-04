#!/bin/bash

if [[ $# -lt 4 ]]; then
    echo "Usage: edit_first_fsf.sh template out_path subject fmriprep_dir"
    exit 1
fi

out_path=$1
subject=$2

if [ "$subject" == "temple114" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_boundary_drop1.fsf"
elif [ "$subject" == "temple107" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_boundary_drop2.fsf"
elif [ "$subject" == "temple064" ]; then
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_boundary_drop3.fsf"
else
    template="/home1/09123/ofriend/analysis/temple/univ/level2_templates/2ndlevel_boundary_allruns.fsf"
fi
#
python edit_first_uni.py $template $out_path $subject 5 222 222


