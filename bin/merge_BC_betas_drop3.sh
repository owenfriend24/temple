#!/bin/bash

### set up experiment info ###
expdir='/corral-repl/utexas/prestonlab/temple/'
sub=$1


betadir=$expdir/sub-${sub}/betaseries

cd $betadir

#match

fslmerge -t pre_BC_items.nii.gz betaOUT_run-1_ev-002 betaOUT_run-1_ev-003 betaOUT_run-1_ev-005 betaOUT_run-1_ev-006 betaOUT_run-1_ev-008 betaOUT_run-1_ev-009 betaOUT_run-1_ev-011 betaOUT_run-1_ev-012 betaOUT_run-2_ev-002 betaOUT_run-2_ev-003 betaOUT_run-2_ev-005 betaOUT_run-2_ev-006 betaOUT_run-2_ev-008 betaOUT_run-2_ev-009 betaOUT_run-2_ev-011 betaOUT_run-2_ev-012

fslmerge -t post_BC_items.nii.gz betaOUT_run-4_ev-002 betaOUT_run-4_ev-003 betaOUT_run-4_ev-005 betaOUT_run-4_ev-006 betaOUT_run-4_ev-008 betaOUT_run-4_ev-009 betaOUT_run-4_ev-011 betaOUT_run-4_ev-012 betaOUT_run-5_ev-002 betaOUT_run-5_ev-003 betaOUT_run-5_ev-005 betaOUT_run-5_ev-006 betaOUT_run-5_ev-008 betaOUT_run-5_ev-009 betaOUT_run-5_ev-011 betaOUT_run-5_ev-012 betaOUT_run-6_ev-002 betaOUT_run-6_ev-003 betaOUT_run-6_ev-005 betaOUT_run-6_ev-006 betaOUT_run-6_ev-008 betaOUT_run-6_ev-009 betaOUT_run-6_ev-011 betaOUT_run-6_ev-012


fslmerge -t pre_post_BC_items.nii.gz pre_BC_items.nii.gz post_BC_items.nii.gz

