#!/bin/bash

if [[ $# -lt 1 ]]; then
    echo "Usage: generate_timeseries_files.sh subject roi(optional) omit_second(optional)"
    exit 1
fi

subject=$1
roi=$2

omit_flag=""
acc_flag=""

# Look through all args for either spelling, anywhere on the command line
for arg in "$@"; do
  case "$arg" in
    --omit_second|omit_second)
      omit_flag="--omit_second"
      ;;
    --weight_by_accuracy|weight_by_acc|weight_byaccuracy|weight_by)
      acc_flag="--weight_by_accuracy"
      ;;
  esac
done

# univariate
boundary_univ_txt_files.py "${subject}" both ${acc_flag}
edit_first_fsf.sh "${subject}" boundary ${roi} ${omit_flag}
edit_second_fsf.sh "${subject}" boundary

# ppi
#

# ignore ppi for now while testing weighted univariate

if [[ -n "$roi" ]]; then
    ppi_txt_behav.py "${subject}" both ${omit_flag}
    ppi_extract_eigen.sh "${subject}" "${roi}"
    edit_first_fsf.sh "${subject}" ppi "${roi}"
    edit_first_fsf.sh "${subject}" ppi_inverse "${roi}"
    edit_second_fsf.sh "${subject}" ppi "${roi}"
    edit_second_fsf.sh "${subject}" ppi_inverse "${roi}"
fi