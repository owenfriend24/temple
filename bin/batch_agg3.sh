#!/bin/bash

comps=$1


source /home1/09123/ofriend/analysis/temple/rsa/bin/activate

aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
BC searchlight --agg_file
