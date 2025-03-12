#!/bin/bash

subject=$1


source /home1/09123/ofriend/analysis/temple/rsa/bin/activate

aggregate_integration.py both /corral-repl/utexas/temple/integration_prepost \
AB hip_subfields --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AB b_ifg_subregions --agg_file

#aggregate_integration.py both /corral-repl/utexas/temple/integration_prepost \
#AC hip_subfields --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AC b_ifg_subregions --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#BC b_hip_subregions --agg_file
#
#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#BC b_ifg_subregions --agg_file
