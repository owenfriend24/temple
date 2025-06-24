#!/bin/bash

if [[ $# -lt 4 ]]; then
    echo "Usage: edit_first_fsf.sh template out_path subject fmriprep_dir"
    exit 1
fi

template=$1
out_path=$2
subject=$3
fm_dir=$4


mkdir -p $out_path

nifti_file1=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-01_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
# dimensions of functional images; num voxels doesn't actually affect Feat output for this analysis but editing just in case
d1=$(fslinfo "$nifti_file1" | awk '$1 == "dim1" {print $2}')
d2=$(fslinfo "$nifti_file1" | awk '$1 == "dim2" {print $2}')
d3=$(fslinfo "$nifti_file1" | awk '$1 == "dim3" {print $2}')


num_vols1=$(fslinfo "$nifti_file1" | awk '$1 == "dim4" {print $2}')
num_vox1=$((num_vols1*d1*d2*d3))

nifti_file2=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-02_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols2=$(fslinfo "$nifti_file2" | awk '$1 == "dim4" {print $2}')
num_vox2=$((num_vols2*d1*d2*d3))

nifti_file3=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-03_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols3=$(fslinfo "$nifti_file3" | awk '$1 == "dim4" {print $2}')
num_vox3=$((num_vols3*d1*d2*d3))

nifti_file4=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-04_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols4=$(fslinfo "$nifti_file4" | awk '$1 == "dim4" {print $2}')
num_vox4=$((num_vols4*d1*d2*d3))

python edit_first_ppi.py $template $out_path $subject 1 $num_vols1 $num_vox1
python edit_first_ppi.py $template $out_path $subject 2 $num_vols2 $num_vox2
python edit_first_ppi.py $template $out_path $subject 3 $num_vols3 $num_vox3
python edit_first_ppi.py $template $out_path $subject 4 $num_vols4 $num_vox4


