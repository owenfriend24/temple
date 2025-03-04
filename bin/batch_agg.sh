#!/bin/bash

subject=$1


source /home1/09123/ofriend/analysis/temple/rsa/bin/activate

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AB b_hip_subregions --agg_file
#
#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AB b_ifg_subregions --agg_file

aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
AC b_hip_subregions --agg_file

aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
AC b_ifg_subregions --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#BC b_hip_subregions --agg_file
#
#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#BC b_ifg_subregions --agg_file
