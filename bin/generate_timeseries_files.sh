#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: generate_timeseries_files.sh subject roi(optional) omit_second(optional)"
    exit 1
fi

subject=$1
roi=$2
omit_second=$3

cd /home1/09123/ofriend/analysis/temple/bin/

if [[ "$omit_second" == "omit_second" ]]; then
    omit_flag="--omit_second"
else
    omit_flag=""
fi

# univariate
boundary_univ_txt_files.py "${subject}" both
edit_first_fsf.sh "${subject}" boundary ${omit_flag}
edit_second_fsf.sh "${subject}" boundary

# ppi
if [[ -n "$roi" ]]; then
    ppi_txt_behav.py "${subject}" both ${omit_flag}
    ppi_extract_eigen.sh "${subject}" "${roi}"
    edit_first_fsf.sh "${subject}" ppi "${roi}"
    edit_first_fsf.sh "${subject}" ppi_inverse "${roi}"
    edit_second_fsf.sh "${subject}" ppi "${roi}"
    edit_second_fsf.sh "${subject}" ppi_inverse "${roi}"
fi