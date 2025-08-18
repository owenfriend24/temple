#!/bin/bash

# Ensure at least one argument (subject) is provided
if [[ $# -lt 1 ]]; then
    echo "Usage: batch_betaseries.sh subject [drop_run=N]"
    exit 1
fi

### Set up experiment info ###
#expdir='/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
expdir='/corral-repl/utexas/prestonlab/temple/'
sub=$1
drop_run=""

# Check for optional drop_run argument
for arg in "$@"; do
    if [[ $arg == drop_run=* ]]; then
        drop_run="${arg#drop_run=}"
    fi
done

# Load environment
source /home1/09123/ofriend/analysis/temple/profile

# Run preprocessing steps
prep_arrow.py $expdir both $sub
beta_fsfs.sh $sub
beta_files.sh $sub

# Setup betaseries directory
betadir=$expdir/sub-${sub}/betaseries
mkdir -p "$betadir"
cd "$betadir"

# Activate Python environment
source /home1/09123/ofriend/analysis/temple/rsa/bin/activate
betaseries_est.py $sub

# Run appropriate merge script based on drop_run flag
if [[ -n $drop_run ]]; then
    echo "Dropping run $drop_run. Running merge_betas_drop1.sh..."
    merge_betas_drop1.sh $sub $drop_run
else
    echo "No run drop specified. Running merge_betas_prepost.sh..."
    merge_betas_prepost.sh $sub
fi
