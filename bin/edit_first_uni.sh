#!/bin/bash

if [[ $# -lt 4 ]]; then
    echo "Usage: edit_first_fsf.sh template out_path subject fmriprep_dir"
    exit 1
fi

template=$1
out_path=$2
subject=$3
fm_dir=$4



# Load any necessary modules
module load python3/3.9.7

# Activate your virtual environment if you're using one
source /home1/09123/ofriend/analysis/temple/profile

# Move to the directory containing your Python script
cd /home1/09123/ofriend/analysis/temple/bin

# dimensions of functional images
d1=$(fslinfo "$nifti_file1" | awk '$1 == "dim1" {print $2}')
d2=$(fslinfo "$nifti_file1" | awk '$1 == "dim2" {print $2}')
d3=$(fslinfo "$nifti_file1" | awk '$1 == "dim3" {print $2}')


nifti_file1=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-01_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols1=$(fslinfo "$nifti_file1" | awk '$1 == "dim4" {print $2}')
num_vox1=$((num_vols1*d1*d2*d3))
echo $num_vox1

nifti_file2=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-02_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols2=$(fslinfo "$nifti_file2" | awk '$1 == "dim4" {print $2}')
num_vox2=$((num_vols2*d1*d2*d3))
echo $num_vox2

nifti_file3=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-03_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols3=$(fslinfo "$nifti_file3" | awk '$1 == "dim4" {print $2}')
num_vox3=$((num_vols3*d1*d2*d3))
echo $num_vox3

nifti_file4=$fm_dir/sub-"$subject"/func/sub-"$subject"_task-collector_run-04_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols4=$(fslinfo "$nifti_file4" | awk '$1 == "dim4" {print $2}')
num_vox4=$((num_vols4*d1*d2*d3))
echo $num_vox4

# Run your Python script
python edit_first_uni.py $template $out_path $subject 1 $num_vols1 $num_vox1
python edit_first_uni.py $template $out_path $subject 2 $num_vols2 $num_vox2
python edit_first_uni.py $template $out_path $subject 3 $num_vols3 $num_vox3
python edit_first_uni.py $template $out_path $subject 4 $num_vols4 $num_vox4


