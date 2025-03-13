#!/bin/bash

# using grep to change the commands wasn't working, can go back and make this code cleaner/less redundant later

# set up experiment info
expdir='/scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep'
#expdir='/corral-repl/utexas/prestonlab/temple/'
sub=$1
drop_run=$2

betadir=$expdir/sub-${sub}/betaseries

# changing the current directory sometimes causes problems when running jobs in parallel, so used the full path in all calls below

#match
if [ "$drop_run" = "3" ]; then
  # ABC
  fslmerge -t ${betadir}/pre_items.nii.gz ${betadir}/betaOUT_run-1* ${betadir}/betaOUT_run-2*
  fslmerge -t ${betadir}/post_items.nii.gz ${betadir}/betaOUT_run-5* ${betadir}/betaOUT_run-4* ${betadir}/betaOUT_run-6*

  # AC
  fslmerge -t ${betadir}/pre_AC_items.nii.gz ${betadir}/betaOUT_run-1_ev-001 ${betadir}/betaOUT_run-1_ev-003 \
  ${betadir}/betaOUT_run-1_ev-004 ${betadir}/betaOUT_run-1_ev-006 ${betadir}/betaOUT_run-1_ev-007 \
  ${betadir}/betaOUT_run-1_ev-009 ${betadir}/betaOUT_run-1_ev-010 ${betadir}/betaOUT_run-1_ev-012 \
  ${betadir}/betaOUT_run-2_ev-001 ${betadir}/betaOUT_run-2_ev-003 ${betadir}/betaOUT_run-2_ev-004 \
  ${betadir}/betaOUT_run-2_ev-006 ${betadir}/betaOUT_run-2_ev-007 ${betadir}/betaOUT_run-2_ev-009 \
  ${betadir}/betaOUT_run-2_ev-010 ${betadir}/betaOUT_run-2_ev-012

  fslmerge -t ${betadir}/post_AC_items.nii.gz ${betadir}/betaOUT_run-4_ev-001 ${betadir}/betaOUT_run-4_ev-003 \
  ${betadir}/betaOUT_run-4_ev-004 ${betadir}/betaOUT_run-4_ev-006 ${betadir}/betaOUT_run-4_ev-007 \
  ${betadir}/betaOUT_run-4_ev-009 ${betadir}/betaOUT_run-4_ev-010 ${betadir}/betaOUT_run-4_ev-012 \
  ${betadir}/betaOUT_run-5_ev-001 ${betadir}/betaOUT_run-5_ev-003 ${betadir}/betaOUT_run-5_ev-004 \
  ${betadir}/betaOUT_run-5_ev-006 ${betadir}/betaOUT_run-5_ev-007 ${betadir}/betaOUT_run-5_ev-009 \
  ${betadir}/betaOUT_run-5_ev-010 ${betadir}/betaOUT_run-5_ev-012 ${betadir}/betaOUT_run-6_ev-001 \
  ${betadir}/betaOUT_run-6_ev-003 ${betadir}/betaOUT_run-6_ev-004 ${betadir}/betaOUT_run-6_ev-006 \
  ${betadir}/betaOUT_run-6_ev-007 ${betadir}/betaOUT_run-6_ev-009 ${betadir}/betaOUT_run-6_ev-010 \
  ${betadir}/betaOUT_run-6_ev-012

  # AB
  fslmerge -t ${betadir}/pre_AB_items.nii.gz ${betadir}/betaOUT_run-1_ev-001 ${betadir}/betaOUT_run-1_ev-002 \
  ${betadir}/betaOUT_run-1_ev-004 ${betadir}/betaOUT_run-1_ev-005 ${betadir}/betaOUT_run-1_ev-007 \
  ${betadir}/betaOUT_run-1_ev-008 ${betadir}/betaOUT_run-1_ev-010 ${betadir}/betaOUT_run-1_ev-011 \
  ${betadir}/betaOUT_run-2_ev-001 ${betadir}/betaOUT_run-2_ev-002 ${betadir}/betaOUT_run-2_ev-004 \
  ${betadir}/betaOUT_run-2_ev-005 ${betadir}/betaOUT_run-2_ev-007 ${betadir}/betaOUT_run-2_ev-008 \
  ${betadir}/betaOUT_run-2_ev-010 ${betadir}/betaOUT_run-2_ev-011

  fslmerge -t ${betadir}/post_AB_items.nii.gz ${betadir}/betaOUT_run-4_ev-001 ${betadir}/betaOUT_run-4_ev-002 \
  ${betadir}/betaOUT_run-4_ev-004 ${betadir}/betaOUT_run-4_ev-005 ${betadir}/betaOUT_run-4_ev-007 \
  ${betadir}/betaOUT_run-4_ev-008 ${betadir}/betaOUT_run-4_ev-010 ${betadir}/betaOUT_run-4_ev-011 \
  ${betadir}/betaOUT_run-5_ev-001 ${betadir}/betaOUT_run-5_ev-002 ${betadir}/betaOUT_run-5_ev-004 \
  ${betadir}/betaOUT_run-5_ev-005 ${betadir}/betaOUT_run-5_ev-007 ${betadir}/betaOUT_run-5_ev-008 \
  ${betadir}/betaOUT_run-5_ev-010 ${betadir}/betaOUT_run-5_ev-011 ${betadir}/betaOUT_run-6_ev-001 \
  ${betadir}/betaOUT_run-6_ev-002 ${betadir}/betaOUT_run-6_ev-004 ${betadir}/betaOUT_run-6_ev-005 \
  ${betadir}/betaOUT_run-6_ev-007 ${betadir}/betaOUT_run-6_ev-008 ${betadir}/betaOUT_run-6_ev-010 \
  ${betadir}/betaOUT_run-6_ev-011

  fslmerge -t ${betadir}/pre_BC_items.nii.gz ${betadir}/betaOUT_run-1_ev-002 ${betadir}/betaOUT_run-1_ev-003 ${betadir}/betaOUT_run-1_ev-005 ${betadir}/betaOUT_run-1_ev-006 \
  ${betadir}/betaOUT_run-1_ev-008 ${betadir}/betaOUT_run-1_ev-009 ${betadir}/betaOUT_run-1_ev-011 ${betadir}/betaOUT_run-1_ev-012 ${betadir}/betaOUT_run-2_ev-002 \
  ${betadir}/betaOUT_run-2_ev-003 ${betadir}/betaOUT_run-2_ev-005 ${betadir}/betaOUT_run-2_ev-006 ${betadir}/betaOUT_run-2_ev-008 ${betadir}/betaOUT_run-2_ev-009 \
  ${betadir}/betaOUT_run-2_ev-011 ${betadir}/betaOUT_run-2_ev-012

  fslmerge -t ${betadir}/post_BC_items.nii.gz ${betadir}/betaOUT_run-4_ev-002 ${betadir}/betaOUT_run-4_ev-003 ${betadir}/betaOUT_run-4_ev-005 ${betadir}/betaOUT_run-4_ev-006 \
  ${betadir}/betaOUT_run-4_ev-008 ${betadir}/betaOUT_run-4_ev-009 ${betadir}/betaOUT_run-4_ev-011 ${betadir}/betaOUT_run-4_ev-012 ${betadir}/betaOUT_run-5_ev-002 \
  ${betadir}/betaOUT_run-5_ev-003 ${betadir}/betaOUT_run-5_ev-005 ${betadir}/betaOUT_run-5_ev-006 ${betadir}/betaOUT_run-5_ev-008 ${betadir}/betaOUT_run-5_ev-009 \
  ${betadir}/betaOUT_run-5_ev-011 ${betadir}/betaOUT_run-5_ev-012 ${betadir}/betaOUT_run-6_ev-002 ${betadir}/betaOUT_run-6_ev-003 ${betadir}/betaOUT_run-6_ev-005 \
  ${betadir}/betaOUT_run-6_ev-006 ${betadir}/betaOUT_run-6_ev-008 ${betadir}/betaOUT_run-6_ev-009 ${betadir}/betaOUT_run-6_ev-011 ${betadir}/betaOUT_run-6_ev-012


fi

if [ "$drop_run" = "6" ]; then
  # ABC
  fslmerge -t ${betadir}/pre_items.nii.gz ${betadir}/betaOUT_run-1* ${betadir}/betaOUT_run-2* ${betadir}/betaOUT_run-3*
  fslmerge -t ${betadir}/post_items.nii.gz ${betadir}/betaOUT_run-4* ${betadir}/betaOUT_run-5*

  # AC
  fslmerge -t ${betadir}/pre_AC_items.nii.gz ${betadir}/betaOUT_run-1_ev-001 ${betadir}/betaOUT_run-1_ev-003 \
  ${betadir}/betaOUT_run-1_ev-004 ${betadir}/betaOUT_run-1_ev-006 ${betadir}/betaOUT_run-1_ev-007 \
  ${betadir}/betaOUT_run-1_ev-009 ${betadir}/betaOUT_run-1_ev-010 ${betadir}/betaOUT_run-1_ev-012 \
  ${betadir}/betaOUT_run-2_ev-001 ${betadir}/betaOUT_run-2_ev-003 ${betadir}/betaOUT_run-2_ev-004 \
  ${betadir}/betaOUT_run-2_ev-006 ${betadir}/betaOUT_run-2_ev-007 ${betadir}/betaOUT_run-2_ev-009 \
  ${betadir}/betaOUT_run-2_ev-010 ${betadir}/betaOUT_run-2_ev-012 ${betadir}/betaOUT_run-3_ev-001 \
  ${betadir}/betaOUT_run-3_ev-003 ${betadir}/betaOUT_run-3_ev-004 ${betadir}/betaOUT_run-3_ev-006 \
  ${betadir}/betaOUT_run-3_ev-007 ${betadir}/betaOUT_run-3_ev-009 ${betadir}/betaOUT_run-3_ev-010 \
  ${betadir}/betaOUT_run-3_ev-012

  fslmerge -t ${betadir}/post_AC_items.nii.gz ${betadir}/betaOUT_run-4_ev-001 ${betadir}/betaOUT_run-4_ev-003 \
  ${betadir}/betaOUT_run-4_ev-004 ${betadir}/betaOUT_run-4_ev-006 ${betadir}/betaOUT_run-4_ev-007 \
  ${betadir}/betaOUT_run-4_ev-009 ${betadir}/betaOUT_run-4_ev-010 ${betadir}/betaOUT_run-4_ev-012 \
  ${betadir}/betaOUT_run-5_ev-001 ${betadir}/betaOUT_run-5_ev-003 ${betadir}/betaOUT_run-5_ev-004 \
  ${betadir}/betaOUT_run-5_ev-006 ${betadir}/betaOUT_run-5_ev-007 ${betadir}/betaOUT_run-5_ev-009 \
  ${betadir}/betaOUT_run-5_ev-010 ${betadir}/betaOUT_run-5_ev-012

  # AB
  fslmerge -t ${betadir}/pre_AB_items.nii.gz ${betadir}/betaOUT_run-1_ev-001 ${betadir}/betaOUT_run-1_ev-002 \
  ${betadir}/betaOUT_run-1_ev-004 ${betadir}/betaOUT_run-1_ev-005 ${betadir}/betaOUT_run-1_ev-007 \
  ${betadir}/betaOUT_run-1_ev-008 ${betadir}/betaOUT_run-1_ev-010 ${betadir}/betaOUT_run-1_ev-011 \
  ${betadir}/betaOUT_run-2_ev-001 ${betadir}/betaOUT_run-2_ev-002 ${betadir}/betaOUT_run-2_ev-004 \
  ${betadir}/betaOUT_run-2_ev-005 ${betadir}/betaOUT_run-2_ev-007 ${betadir}/betaOUT_run-2_ev-008 \
  ${betadir}/betaOUT_run-2_ev-010 ${betadir}/betaOUT_run-2_ev-011 ${betadir}/betaOUT_run-3_ev-001 \
  ${betadir}/betaOUT_run-3_ev-002 ${betadir}/betaOUT_run-3_ev-004 ${betadir}/betaOUT_run-3_ev-005 \
  ${betadir}/betaOUT_run-3_ev-007 ${betadir}/betaOUT_run-3_ev-008 ${betadir}/betaOUT_run-3_ev-010 \
  ${betadir}/betaOUT_run-3_ev-011

  fslmerge -t ${betadir}/post_AB_items.nii.gz ${betadir}/betaOUT_run-4_ev-001 ${betadir}/betaOUT_run-4_ev-002 \
  ${betadir}/betaOUT_run-4_ev-004 ${betadir}/betaOUT_run-4_ev-005 ${betadir}/betaOUT_run-4_ev-007 \
  ${betadir}/betaOUT_run-4_ev-008 ${betadir}/betaOUT_run-4_ev-010 ${betadir}/betaOUT_run-4_ev-011 \
  ${betadir}/betaOUT_run-5_ev-001 ${betadir}/betaOUT_run-5_ev-002 ${betadir}/betaOUT_run-5_ev-004 \
  ${betadir}/betaOUT_run-5_ev-005 ${betadir}/betaOUT_run-5_ev-007 ${betadir}/betaOUT_run-5_ev-008 \
  ${betadir}/betaOUT_run-5_ev-010 ${betadir}/betaOUT_run-5_ev-011

  fslmerge -t ${betadir}/pre_BC_items.nii.gz ${betadir}/betaOUT_run-1_ev-002 ${betadir}/betaOUT_run-1_ev-003 ${betadir}/betaOUT_run-1_ev-005 ${betadir}/betaOUT_run-1_ev-006 \
  ${betadir}/betaOUT_run-1_ev-008 ${betadir}/betaOUT_run-1_ev-009 ${betadir}/betaOUT_run-1_ev-011 ${betadir}/betaOUT_run-1_ev-012 ${betadir}/betaOUT_run-2_ev-002 \
  ${betadir}/betaOUT_run-2_ev-003 ${betadir}/betaOUT_run-2_ev-005 ${betadir}/betaOUT_run-2_ev-006 ${betadir}/betaOUT_run-2_ev-008 ${betadir}/betaOUT_run-2_ev-009 \
  ${betadir}/betaOUT_run-2_ev-011 ${betadir}/betaOUT_run-2_ev-012 ${betadir}/betaOUT_run-3_ev-002 ${betadir}/betaOUT_run-3_ev-003 ${betadir}/betaOUT_run-3_ev-005 \
  ${betadir}/betaOUT_run-3_ev-006 ${betadir}/betaOUT_run-3_ev-008 ${betadir}/betaOUT_run-3_ev-009 ${betadir}/betaOUT_run-3_ev-011 ${betadir}/betaOUT_run-3_ev-012

  fslmerge -t ${betadir}/post_BC_items.nii.gz ${betadir}/betaOUT_run-4_ev-002 ${betadir}/betaOUT_run-4_ev-003 ${betadir}/betaOUT_run-4_ev-005 ${betadir}/betaOUT_run-4_ev-006 \
  ${betadir}/betaOUT_run-4_ev-008 ${betadir}/betaOUT_run-4_ev-009 ${betadir}/betaOUT_run-4_ev-011 ${betadir}/betaOUT_run-4_ev-012 ${betadir}/betaOUT_run-5_ev-002 \
  ${betadir}/betaOUT_run-5_ev-003 ${betadir}/betaOUT_run-5_ev-005 ${betadir}/betaOUT_run-5_ev-006 ${betadir}/betaOUT_run-5_ev-008 ${betadir}/betaOUT_run-5_ev-009 \
  ${betadir}/betaOUT_run-5_ev-011 ${betadir}/betaOUT_run-5_ev-012

fi


if [ "$drop_run" = "5" ]; then
  # ABC
  fslmerge -t ${betadir}/pre_items.nii.gz ${betadir}/betaOUT_run-1* ${betadir}/betaOUT_run-2* ${betadir}/betaOUT_run-3*
  fslmerge -t ${betadir}/post_items.nii.gz ${betadir}/betaOUT_run-4* ${betadir}/betaOUT_run-6*

  # AC
  fslmerge -t ${betadir}/pre_AC_items.nii.gz ${betadir}/betaOUT_run-1_ev-001 ${betadir}/betaOUT_run-1_ev-003 \
  ${betadir}/betaOUT_run-1_ev-004 ${betadir}/betaOUT_run-1_ev-006 ${betadir}/betaOUT_run-1_ev-007 \
  ${betadir}/betaOUT_run-1_ev-009 ${betadir}/betaOUT_run-1_ev-010 ${betadir}/betaOUT_run-1_ev-012 \
  ${betadir}/betaOUT_run-2_ev-001 ${betadir}/betaOUT_run-2_ev-003 ${betadir}/betaOUT_run-2_ev-004 \
  ${betadir}/betaOUT_run-2_ev-006 ${betadir}/betaOUT_run-2_ev-007 ${betadir}/betaOUT_run-2_ev-009 \
  ${betadir}/betaOUT_run-2_ev-010 ${betadir}/betaOUT_run-2_ev-012 ${betadir}/betaOUT_run-3_ev-001 \
  ${betadir}/betaOUT_run-3_ev-003 ${betadir}/betaOUT_run-3_ev-004 ${betadir}/betaOUT_run-3_ev-006 \
  ${betadir}/betaOUT_run-3_ev-007 ${betadir}/betaOUT_run-3_ev-009 ${betadir}/betaOUT_run-3_ev-010 \
  ${betadir}/betaOUT_run-3_ev-012

  fslmerge -t ${betadir}/post_AC_items.nii.gz ${betadir}/betaOUT_run-4_ev-001 ${betadir}/betaOUT_run-4_ev-003 \
  ${betadir}/betaOUT_run-4_ev-004 ${betadir}/betaOUT_run-4_ev-006 ${betadir}/betaOUT_run-4_ev-007 \
  ${betadir}/betaOUT_run-4_ev-009 ${betadir}/betaOUT_run-4_ev-010 ${betadir}/betaOUT_run-4_ev-012 \
  ${betadir}/betaOUT_run-6_ev-001 ${betadir}/betaOUT_run-6_ev-003 ${betadir}/betaOUT_run-6_ev-004 \
  ${betadir}/betaOUT_run-6_ev-006 ${betadir}/betaOUT_run-6_ev-007 ${betadir}/betaOUT_run-6_ev-009 \
  ${betadir}/betaOUT_run-6_ev-010 ${betadir}/betaOUT_run-6_ev-012

  # AB
  fslmerge -t ${betadir}/pre_AB_items.nii.gz ${betadir}/betaOUT_run-1_ev-001 ${betadir}/betaOUT_run-1_ev-002 \
  ${betadir}/betaOUT_run-1_ev-004 ${betadir}/betaOUT_run-1_ev-005 ${betadir}/betaOUT_run-1_ev-007 \
  ${betadir}/betaOUT_run-1_ev-008 ${betadir}/betaOUT_run-1_ev-010 ${betadir}/betaOUT_run-1_ev-011 \
  ${betadir}/betaOUT_run-2_ev-001 ${betadir}/betaOUT_run-2_ev-002 ${betadir}/betaOUT_run-2_ev-004 \
  ${betadir}/betaOUT_run-2_ev-005 ${betadir}/betaOUT_run-2_ev-007 ${betadir}/betaOUT_run-2_ev-008 \
  ${betadir}/betaOUT_run-2_ev-010 ${betadir}/betaOUT_run-2_ev-011 ${betadir}/betaOUT_run-3_ev-001 \
  ${betadir}/betaOUT_run-3_ev-002 ${betadir}/betaOUT_run-3_ev-004 ${betadir}/betaOUT_run-3_ev-005 \
  ${betadir}/betaOUT_run-3_ev-007 ${betadir}/betaOUT_run-3_ev-008 ${betadir}/betaOUT_run-3_ev-010 \
  ${betadir}/betaOUT_run-3_ev-011

  fslmerge -t ${betadir}/post_AB_items.nii.gz ${betadir}/betaOUT_run-4_ev-001 ${betadir}/betaOUT_run-4_ev-002 \
  ${betadir}/betaOUT_run-4_ev-004 ${betadir}/betaOUT_run-4_ev-005 ${betadir}/betaOUT_run-4_ev-007 \
  ${betadir}/betaOUT_run-4_ev-008 ${betadir}/betaOUT_run-4_ev-010 ${betadir}/betaOUT_run-4_ev-011 \
  ${betadir}/betaOUT_run-6_ev-001 ${betadir}/betaOUT_run-6_ev-002 ${betadir}/betaOUT_run-6_ev-004 \
  ${betadir}/betaOUT_run-6_ev-005 ${betadir}/betaOUT_run-6_ev-007 ${betadir}/betaOUT_run-6_ev-008 \
  ${betadir}/betaOUT_run-6_ev-010 ${betadir}/betaOUT_run-6_ev-011

  fslmerge -t ${betadir}/pre_BC_items.nii.gz ${betadir}/betaOUT_run-1_ev-002 ${betadir}/betaOUT_run-1_ev-003 ${betadir}/betaOUT_run-1_ev-005 ${betadir}/betaOUT_run-1_ev-006 \
  ${betadir}/betaOUT_run-1_ev-008 ${betadir}/betaOUT_run-1_ev-009 ${betadir}/betaOUT_run-1_ev-011 ${betadir}/betaOUT_run-1_ev-012 ${betadir}/betaOUT_run-2_ev-002 \
  ${betadir}/betaOUT_run-2_ev-003 ${betadir}/betaOUT_run-2_ev-005 ${betadir}/betaOUT_run-2_ev-006 ${betadir}/betaOUT_run-2_ev-008 ${betadir}/betaOUT_run-2_ev-009 \
  ${betadir}/betaOUT_run-2_ev-011 ${betadir}/betaOUT_run-2_ev-012 ${betadir}/betaOUT_run-3_ev-002 ${betadir}/betaOUT_run-3_ev-003 ${betadir}/betaOUT_run-3_ev-005 \
  ${betadir}/betaOUT_run-3_ev-006 ${betadir}/betaOUT_run-3_ev-008 ${betadir}/betaOUT_run-3_ev-009 ${betadir}/betaOUT_run-3_ev-011 ${betadir}/betaOUT_run-3_ev-012

  fslmerge -t ${betadir}/post_BC_items.nii.gz ${betadir}/betaOUT_run-4_ev-002 ${betadir}/betaOUT_run-4_ev-003 ${betadir}/betaOUT_run-4_ev-005 ${betadir}/betaOUT_run-4_ev-006 \
  ${betadir}/betaOUT_run-4_ev-008 ${betadir}/betaOUT_run-4_ev-009 ${betadir}/betaOUT_run-4_ev-011 ${betadir}/betaOUT_run-4_ev-012 \
  ${betadir}/betaOUT_run-6_ev-002 ${betadir}/betaOUT_run-6_ev-003 ${betadir}/betaOUT_run-6_ev-005 \
  ${betadir}/betaOUT_run-6_ev-006 ${betadir}/betaOUT_run-6_ev-008 ${betadir}/betaOUT_run-6_ev-009 ${betadir}/betaOUT_run-6_ev-011 ${betadir}/betaOUT_run-6_ev-012

fi


# merge the images by phase into pre post images
fslmerge -t ${betadir}/pre_post_items.nii.gz ${betadir}/pre_items.nii.gz ${betadir}/post_items.nii.gz
fslmerge -t ${betadir}/pre_post_AC_items.nii.gz ${betadir}/pre_AC_items.nii.gz ${betadir}/post_AC_items.nii.gz
fslmerge -t ${betadir}/pre_post_AB_items.nii.gz ${betadir}/pre_AB_items.nii.gz ${betadir}/post_AB_items.nii.gz
fslmerge -t ${betadir}/pre_post_BC_items.nii.gz ${betadir}/pre_BC_items.nii.gz ${betadir}/post_BC_items.nii.gz