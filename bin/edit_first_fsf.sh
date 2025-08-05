#!/bin/bash

if [[ $# -lt 2 ]]; then
    echo "Usage: edit_first_fsf.sh subject type (boundary, ppi, ppi_inverse)"
    exit 1
fi

subject=$1
type=$2
# only needed for ppi analyses
roi=$3

if [ "$type" == "boundary" ]; then
    template=/home1/09123/ofriend/analysis/temple/univ/level1_templates/boundary_sensitivity_template.fsf
    out_path=/corral-repl/utexas/prestonlab/univ/
elif [ "$type" == "ppi" ]; then
    template=/home1/09123/ofriend/analysis/temple/univ/level1_templates/ppi_first_template.fsf
    out_path=/corral-repl/utexas/prestonlab/univ/ppi
elif [ "$type" == "ppi_inverse" ]; then
    template=/home1/09123/ofriend/analysis/temple/univ/level1_templates/ppi_first_inverse.fsf
    out_path=/corral-repl/utexas/prestonlab/univ/ppi_inverse
fi

mkdir -p $out_path

func_dir=/corral-repl/utexas/prestonlab/temple/sub-"${subject}"/func/

nifti_file1=${func_dir}/sub-"${subject}"_task-collector_run-01_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
# dimensions of functional images
d1=$(fslinfo "$nifti_file1" | awk '$1 == "dim1" {print $2}')
d2=$(fslinfo "$nifti_file1" | awk '$1 == "dim2" {print $2}')
d3=$(fslinfo "$nifti_file1" | awk '$1 == "dim3" {print $2}')

num_vols1=$(fslinfo "$nifti_file1" | awk '$1 == "dim4" {print $2}')
num_vox1=$((num_vols1*d1*d2*d3))

nifti_file2=${func_dir}/sub-"$subject"_task-collector_run-02_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols2=$(fslinfo "$nifti_file2" | awk '$1 == "dim4" {print $2}')
num_vox2=$((num_vols2*d1*d2*d3))

nifti_file3=${func_dir}/sub-"$subject"_task-collector_run-03_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols3=$(fslinfo "$nifti_file3" | awk '$1 == "dim4" {print $2}')
num_vox3=$((num_vols3*d1*d2*d3))

nifti_file4=${func_dir}/sub-"$subject"_task-collector_run-04_space-T1w_desc-preproc_bold_ss_4mm.nii.gz
num_vols4=$(fslinfo "$nifti_file4" | awk '$1 == "dim4" {print $2}')
num_vox4=$((num_vols4*d1*d2*d3))

python edit_first_fsf.py $template $out_path $subject 1 $num_vols1 $num_vox1 $type $roi
python edit_first_fsf.py $template $out_path $subject 2 $num_vols2 $num_vox2 $type $roi
python edit_first_fsf.py $template $out_path $subject 3 $num_vols3 $num_vox3 $type $roi
python edit_first_fsf.py $template $out_path $subject 4 $num_vols4 $num_vox4 $type $roi


