#!/bin/bash
#


if [[ $# -lt 2 ]]; then
    echo "Usage: run_third_feat.sh fmriprep_dir ppi/uni"
    exit 1
fi

fmriprep_dir=$1
model=$2

if [[ "${model}" == "uni" ]]; then
    echo "running third level univariate analysis"
#    feat "/home1/09123/ofriend/analysis/temple/univ/3rdlevel_boundary.fsf"
 #   feat "/home1/09123/ofriend/analysis/temple/univ/3rdlevel_boundary_4v1.fsf"
    feat "/home1/09123/ofriend/analysis/temple/univ/3rdlevel_boundary_1v4.fsf"
fi

if [[ "${model}" == "ppi" ]]; then
    echo "running third level ppi analysis"
    #feat "/home1/09123/ofriend/analysis/temple/univ/3rdlevel_boundary_ppi.fsf"
    feat "/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/3rd_ppi_cont_new_new.fsf"
    feat "/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/3rd_ppi_grouped_new_new.fsf"
fi



