#!/bin/bash

sub=$1


rm -R /corral-repl/utexas/prestonlab/temple/sub-${sub}/betaseries

cp -R /scratch/09123/ofriend/temple/new_prepro/fmriprep/derivatives/sub-${sub}/betaseries /corral-repl/utexas/prestonlab/temple/sub-${sub}/
