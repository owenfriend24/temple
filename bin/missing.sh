#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "missing.sh subjects (colon-separated) search_dir"
    exit 1
fi

subjects=$1       # colon-separated subject list
search_dir=$2     # directory to search in

IFS=':' read -ra subject_array <<< "$subjects"

for sub in "${subject_array[@]}"; do
    if ! ls "$search_dir"/*"$sub"* &> /dev/null; then
        echo "missing: $sub"
    fi
done
