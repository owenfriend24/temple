#!/bin/bash

subject=$1
anat_dir=$2

export sub_id=sub-${subject}
export FREESURFER_HOME=/
source $FREESURFER_HOME/SetUpFreeSurfer.sh



recon-all -i ${anat_dir}/${sub_id}/anat/${sub_id}_T1w.nii.gz -subjid ${sub_id} -all

recon-all -subjid ${sub_id} -T2 ${anat_dir}/${sub_id}/anat/${sub_id}_T2w.nii.gz -T2pial

