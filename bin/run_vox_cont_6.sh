#!/bin/bash

sub=$1

source $HOME/analysis/temple/rsa/bin/activate
python $HOME/analysis/moshigo_model/bin/voxelwise_parallel_6run_cont.py --chunk ${sub}