#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: generate_timeseries_files.sh subject"
    exit 1
fi

subject=$1
roi=$2

cd /home1/09123/ofriend/analysis/temple/bin/

# univariate
boundary_univ_txt_files.py "${subject}" both
edit_first_fsf.sh "${subject}" boundary
edit_second_fsf.sh "${subject}" boundary

# ppi
if [[ -n "$roi" ]]; then
    ppi_txt_behav.py "${subject}" both
    ppi_extract_eigen.sh "${subject}" "${roi}"
    edit_first_fsf.sh "${subject}" ppi "${roi}"
    edit_first_fsf.sh "${subject}" ppi_inverse "${roi}"
    edit_second_fsf.sh "${subject}" ppi "${roi}"
    edit_second_fsf.sh "${subject}" ppi_inverse "${roi}"
fi