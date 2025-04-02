#!/bin/env bash
#
# compress raw data for Box backups

if [[ $# -lt 1 ]]; then
    echo "Usage:  compress.sh sub"
    exit 1
fi

sub=$1

tar -czvf /scratch/09123/ofriend/moshi/${sub}_univariate.tar.gz \
     /corral-repl/utexas/prestonlab/moshiGO1/moshiGO_201/${sub}/BOLD/univariate