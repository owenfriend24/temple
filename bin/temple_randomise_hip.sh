#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "temple_randomise.sh fmriprep_dir"
    exit 1
fi

fmriprep_dir=$1
comp=$2
source $HOME/analysis/temple/rsa/bin/activate

#19, 20, 22, 23, 25, 37, 57, 58, 59, 74, 72, 16, 24, 50, 56, 73, 71, 76
fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/adult_mni_zstat_b_hip_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple019* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple020* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple022* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple025* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple037* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple057* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple059* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple074* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple072* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple016* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple024* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple050* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple056* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple073* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple071* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple058* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple076* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple023*


#10-12s
# 29, 51, 30, 33, 35, 60, 36, 32, 45, 38, 42, 63
fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/tentwe_mni_zstat_b_hip_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple029* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple051*  ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple033* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple035* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple060* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple036* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple032* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple045* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple038* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple063* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple042* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple030*

# 41, 64, 70, 34, 65, 66, 53, 68
fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/sevni_mni_zstat_b_hip_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple041* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple064* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple034* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple065* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple066* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple053* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple068* ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/temple070*


randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/adult_mni_zstat_b_hip_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/adult_${comp}_randomise_b_hip -1 -n 5000 -x  --uncorrp


randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/tentwe_mni_zstat_b_hip_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/tentwe_${comp}_randomise_b_hip -1 -n 5000 -x  --uncorrp


randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/sevni_mni_zstat_b_hip_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/b_hip/sevni_${comp}_randomise_b_hip -1 -n 5000 -x  --uncorrp



