#!/bin/bash

sub=$1

python $HOME/analysis/moshigo_model/bin/pca_cluster_model.py
python $HOME/analysis/moshigo_model/bin/plot_pc_space.py
python $HOME/analysis/moshigo_model/bin/plot_ssm_traj.py