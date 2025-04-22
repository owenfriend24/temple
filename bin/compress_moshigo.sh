#!/bin/env bash
#
# compress raw data for Box backups

if [[ $# -lt 1 ]]; then
    echo "Usage:  compress.sh sub"
    exit 1
fi

sub=$1

count=$(find /corral-repl/utexas/prestonlab/moshiGO1/ -type f | wc -l)
echo "$count total files"

#tar -czvf /scratch/09123/ofriend/moshi/${sub}_univariate.tar.gz  /corral-repl/utexas/prestonlab/moshiGO1/${sub}/BOLD/univariate

# to list files within a tarball: tar -tf file

#cp -R /corral-repl/utexas/prestonlab/moshiGO1/${sub}/BOLD/univariate /scratch/09123/ofriend/moshi/${sub}_univariate
#
#echo "copied file to scratch"
#
## test compress and then delete a directory
#tar -czf /scratch/09123/ofriend/moshi/${sub}_univariate.tar.gz /scratch/09123/ofriend/moshi/${sub}_univariate && rm -rf /scratch/09123/ofriend/moshi/${sub}_univariate
