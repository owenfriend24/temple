#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "temple_randomise.sh fmriprep_dir"
    exit 1
fi

fmriprep_dir=$1
source $HOME/analysis/temple/rsa/bin/activate

#19, 20, 22, 23, 25, 37, 57, 58, 59, 74, 72, 16, 24, 50, 56, 73, 71, 76
fslmerge -t ${fmriprep_dir}/searchlight/mni_AB/adult_mni_zstat_wb/nii.gz ${fmriprep_dir}/searchlight/mni_AB/wb/temple019* ${fmriprep_dir}/searchlight/mni_AB/wb/temple020* ${fmriprep_dir}/searchlight/mni_AB/wb/temple022* ${fmriprep_dir}/searchlight/mni_AB/wb/temple025* ${fmriprep_dir}/searchlight/mni_AB/wb/temple037* ${fmriprep_dir}/searchlight/mni_AB/wb/temple057* ${fmriprep_dir}/searchlight/mni_AB/wb/temple059* ${fmriprep_dir}/searchlight/mni_AB/wb/temple074* ${fmriprep_dir}/searchlight/mni_AB/wb/temple072* ${fmriprep_dir}/searchlight/mni_AB/wb/temple016* ${fmriprep_dir}/searchlight/mni_AB/wb/temple024* ${fmriprep_dir}/searchlight/mni_AB/wb/temple050* ${fmriprep_dir}/searchlight/mni_AB/wb/temple056* ${fmriprep_dir}/searchlight/mni_AB/wb/temple073* ${fmriprep_dir}/searchlight/mni_AB/wb/temple071* ${fmriprep_dir}/searchlight/mni_AB/wb/temple058* ${fmriprep_dir}/searchlight/mni_AB/wb/temple076* ${fmriprep_dir}/searchlight/mni_AB/wb/temple023*


#10-12s
# 29, 51, 30, 33, 35, 60, 36, 32, 45, 38, 42, 63
fslmerge -t ${fmriprep_dir}/searchlight/mni_AB/tentwe_mni_zstat_wb.nii.gz ${fmriprep_dir}/searchlight/mni_AB/wb/temple029* ${fmriprep_dir}/searchlight/mni_AB/wb/temple051*  ${fmriprep_dir}/searchlight/mni_AB/wb/temple033* ${fmriprep_dir}/searchlight/mni_AB/wb/temple035* ${fmriprep_dir}/searchlight/mni_AB/wb/temple060* ${fmriprep_dir}/searchlight/mni_AB/wb/temple036* ${fmriprep_dir}/searchlight/mni_AB/wb/temple032* ${fmriprep_dir}/searchlight/mni_AB/wb/temple045* ${fmriprep_dir}/searchlight/mni_AB/wb/temple038* ${fmriprep_dir}/searchlight/mni_AB/wb/temple063* ${fmriprep_dir}/searchlight/mni_AB/wb/temple042* ${fmriprep_dir}/searchlight/mni_AB/wb/temple030*

# 41, 64, 70, 34, 65, 66, 53, 68
fslmerge -t ${fmriprep_dir}/searchlight/mni_AB/sevni_mni_zstat_wb.nii.gz ${fmriprep_dir}/searchlight/mni_AB/wb/temple041* ${fmriprep_dir}/searchlight/mni_AB/wb/temple064* ${fmriprep_dir}/searchlight/mni_AB/wb/temple034* ${fmriprep_dir}/searchlight/mni_AB/wb/temple065* ${fmriprep_dir}/searchlight/mni_AB/wb/temple066* ${fmriprep_dir}/searchlight/mni_AB/wb/temple053* ${fmriprep_dir}/searchlight/mni_AB/wb/temple068* ${fmriprep_dir}/searchlight/mni_AB/wb/temple070*

randomise -i ${fmriprep_dir}/searchlight/mni_AB/wb/adult_mni_zstat_wb.nii.gz -o ${fmriprep_dir}/searchlight/mni_AB/wb/adult_ABC_randomise_hip -1 -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_AB/wb/tentwe_mni_zstat_wb.nii.gz -o ${fmriprep_dir}/searchlight/mni_AB/wb/tentwe_ABC_randomise_hip -1 -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_AB/wb/sevni_mni_zstat_wb.nii.gz -o ${fmriprep_dir}/searchlight/mni_AB/wb/sevni_ABC_randomise_hip -1 -n 5000 -x  --uncorrp




