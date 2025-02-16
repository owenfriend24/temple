#!/bin/env bash
#
# compress raw data for Box backups

if [[ $# -lt 1 ]]; then
    echo "Usage:  compress.sh sub"
    exit 1
fi

sub=$1

tar -czvf /work/09123/ofriend/ls6/temple/sourcedata2/${sub}.tar.gz /work/09123/ofriend/ls6/temple/sourcedata2/${sub}
