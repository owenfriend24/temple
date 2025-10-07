#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: generate_timeseries_files.sh subject roi(optional) omit_second(optional)"
    exit 1
fi

subject=$1
roi=$2
omit_second=$3
weight_by_acc=$4

cd /home1/09123/ofriend/analysis/temple/bin/

if [[ "$omit_second" == "omit_second" ]]; then
    omit_flag="--omit_second"
else
    omit_flag=""
fi

if [[ "$weight_by_acc" == "weight_by_acc" ]]; then
    acc_flag="--weight_by_accuracy"
else
    acc_flag=""
fi

# univariate
boundary_univ_txt_files.py "${subject}" both ${acc_flag}
edit_first_fsf.sh "${subject}" boundary ${omit_flag}
edit_second_fsf.sh "${subject}" boundary

# ppi
#

# ignore ppi for now while testing weighted univariate

#if [[ -n "$roi" ]]; then
#    ppi_txt_behav.py "${subject}" both ${omit_flag}
#    ppi_extract_eigen.sh "${subject}" "${roi}"
#    edit_first_fsf.sh "${subject}" ppi "${roi}"
#    edit_first_fsf.sh "${subject}" ppi_inverse "${roi}"
#    edit_second_fsf.sh "${subject}" ppi "${roi}"
#    edit_second_fsf.sh "${subject}" ppi_inverse "${roi}"
#fi