#!/bin/bash

### set up experiment info ###
expdir='/corral-repl/utexas/prestonlab/temple'
sub=$1
run_to_drop=$2  # Run number to drop

betadir=$expdir/sub-${sub}/betaseries

cd $betadir

# Function to filter runs dynamically
filter_runs() {
    local pattern="betaOUT_run-${run_to_drop}"
    echo "$@" | tr ' ' '\n' | grep -v "$pattern" | tr '\n' ' '
}

# Define all files, then filter out the dropped run
pre_items=$(filter_runs betaOUT_run-1* betaOUT_run-2* betaOUT_run-3*)
post_items=$(filter_runs betaOUT_run-5* betaOUT_run-4* betaOUT_run-6*)

pre_AC_items=$(filter_runs betaOUT_run-1_ev-001 betaOUT_run-1_ev-003 betaOUT_run-1_ev-004 betaOUT_run-1_ev-006 \
betaOUT_run-1_ev-007 betaOUT_run-1_ev-009 betaOUT_run-1_ev-010 betaOUT_run-1_ev-012 betaOUT_run-2_ev-001 \
betaOUT_run-2_ev-003 betaOUT_run-2_ev-004 betaOUT_run-2_ev-006 betaOUT_run-2_ev-007 betaOUT_run-2_ev-009 \
betaOUT_run-2_ev-010 betaOUT_run-2_ev-012 betaOUT_run-3_ev-001 betaOUT_run-3_ev-003 betaOUT_run-3_ev-004 \
betaOUT_run-3_ev-006 betaOUT_run-3_ev-007 betaOUT_run-3_ev-009 betaOUT_run-3_ev-010 betaOUT_run-3_ev-012)

post_AC_items=$(filter_runs betaOUT_run-4_ev-001 betaOUT_run-4_ev-003 betaOUT_run-4_ev-004 betaOUT_run-4_ev-006 \
betaOUT_run-4_ev-007 betaOUT_run-4_ev-009 betaOUT_run-4_ev-010 betaOUT_run-4_ev-012 betaOUT_run-5_ev-001 \
betaOUT_run-5_ev-003 betaOUT_run-5_ev-004 betaOUT_run-5_ev-006 betaOUT_run-5_ev-007 betaOUT_run-5_ev-009 \
betaOUT_run-5_ev-010 betaOUT_run-5_ev-012 betaOUT_run-6_ev-001 betaOUT_run-6_ev-003 betaOUT_run-6_ev-004 \
betaOUT_run-6_ev-006 betaOUT_run-6_ev-007 betaOUT_run-6_ev-009 betaOUT_run-6_ev-010 betaOUT_run-6_ev-012)

pre_AB_items=$(filter_runs betaOUT_run-1_ev-001 betaOUT_run-1_ev-002 betaOUT_run-1_ev-004 betaOUT_run-1_ev-005 \
betaOUT_run-1_ev-007 betaOUT_run-1_ev-008 betaOUT_run-1_ev-010 betaOUT_run-1_ev-011 betaOUT_run-2_ev-001 \
betaOUT_run-2_ev-002 betaOUT_run-2_ev-004 betaOUT_run-2_ev-005 betaOUT_run-2_ev-007 betaOUT_run-2_ev-008 \
betaOUT_run-2_ev-010 betaOUT_run-2_ev-011 betaOUT_run-3_ev-001 betaOUT_run-3_ev-002 betaOUT_run-3_ev-004 \
betaOUT_run-3_ev-005 betaOUT_run-3_ev-007 betaOUT_run-3_ev-008 betaOUT_run-3_ev-010 betaOUT_run-3_ev-011)

post_AB_items=$(filter_runs betaOUT_run-4_ev-001 betaOUT_run-4_ev-002 betaOUT_run-4_ev-004 betaOUT_run-4_ev-005 \
betaOUT_run-4_ev-007 betaOUT_run-4_ev-008 betaOUT_run-4_ev-010 betaOUT_run-4_ev-011 betaOUT_run-5_ev-001 \
betaOUT_run-5_ev-002 betaOUT_run-5_ev-004 betaOUT_run-5_ev-005 betaOUT_run-5_ev-007 betaOUT_run-5_ev-008 \
betaOUT_run-5_ev-010 betaOUT_run-5_ev-011 betaOUT_run-6_ev-001 betaOUT_run-6_ev-002 betaOUT_run-6_ev-004 \
betaOUT_run-6_ev-005 betaOUT_run-6_ev-007 betaOUT_run-6_ev-008 betaOUT_run-6_ev-010 betaOUT_run-6_ev-011)

# Merge files excluding the dropped run
fslmerge -t pre_items.nii.gz "${pre_items}"
fslmerge -t post_items.nii.gz "${post_items}"
fslmerge -t pre_AC_items.nii.gz "${pre_AC_items}"
fslmerge -t post_AC_items.nii.gz "${post_AC_items}"
fslmerge -t pre_AB_items.nii.gz "${pre_AB_items}"
fslmerge -t post_AB_items.nii.gz "${post_AB_items}"

fslmerge -t pre_post_items.nii.gz pre_items.nii.gz post_items.nii.gz
fslmerge -t pre_post_AC_items.nii.gz pre_AC_items.nii.gz post_AC_items.nii.gz
fslmerge -t pre_post_AB_items.nii.gz pre_AB_items.nii.gz post_AB_items.nii.gz
