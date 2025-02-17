#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: copy_ashs.sh ashs_dir subject"

    exit 1
fi

ashs_dir=$1
sub=$2

cp -R ${ashs_dir}/sub-${sub} /corral-repl/utexas/prestonlab/temple/ashs/