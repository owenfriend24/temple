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
#fslmerge -t ${fmriprep_dir}/searchlight/mni_ABC/adult_mni_zstat_hip.nii.gz ${fmriprep_dir}/searchlight/mni_ABC/temple019* ${fmriprep_dir}/searchlight/mni_ABC/temple020* ${fmriprep_dir}/searchlight/mni_ABC/temple022* ${fmriprep_dir}/searchlight/mni_ABC/temple025* ${fmriprep_dir}/searchlight/mni_ABC/temple037* ${fmriprep_dir}/searchlight/mni_ABC/temple057* ${fmriprep_dir}/searchlight/mni_ABC/temple059* ${fmriprep_dir}/searchlight/mni_ABC/temple074* ${fmriprep_dir}/searchlight/mni_ABC/temple072* ${fmriprep_dir}/searchlight/mni_ABC/temple016* ${fmriprep_dir}/searchlight/mni_ABC/temple024* ${fmriprep_dir}/searchlight/mni_ABC/temple050* ${fmriprep_dir}/searchlight/mni_ABC/temple056* ${fmriprep_dir}/searchlight/mni_ABC/temple073* ${fmriprep_dir}/searchlight/mni_ABC/temple071* ${fmriprep_dir}/searchlight/mni_ABC/temple058* ${fmriprep_dir}/searchlight/mni_ABC/temple076* 

#${fmriprep_dir}/searchlight/mni_ABC/temple023*

#fslmerge -t ${fmriprep_dir}/searchlight/mni_AC/adult_mni_zstat_hip.nii.gz ${fmriprep_dir}/searchlight/mni_AC/temple019* ${fmriprep_dir}/searchlight/mni_AC/temple020* ${fmriprep_dir}/searchlight/mni_AC/temple022* ${fmriprep_dir}/searchlight/mni_AC/temple025* ${fmriprep_dir}/searchlight/mni_AC/temple037* ${fmriprep_dir}/searchlight/mni_AC/temple057* ${fmriprep_dir}/searchlight/mni_AC/temple059* ${fmriprep_dir}/searchlight/mni_AC/temple074* ${fmriprep_dir}/searchlight/mni_AC/temple072* ${fmriprep_dir}/searchlight/mni_AC/temple016* ${fmriprep_dir}/searchlight/mni_AC/temple024* ${fmriprep_dir}/searchlight/mni_AC/temple050* ${fmriprep_dir}/searchlight/mni_AC/temple056* ${fmriprep_dir}/searchlight/mni_AC/temple073* ${fmriprep_dir}/searchlight/mni_AC/temple071* ${fmriprep_dir}/searchlight/mni_AC/temple058* ${fmriprep_dir}/searchlight/mni_AC/temple076*

#${fmriprep_dir}/searchlight/mni_AC/temple023*

#10-12s
# 29, 51, 30, 33, 35, 60, 36, 32, 45, 38, 42, 63
#fslmerge -t ${fmriprep_dir}/searchlight/mni_ABC/tentwe_mni_zstat_hip.nii.gz ${fmriprep_dir}/searchlight/mni_ABC/temple029* ${fmriprep_dir}/searchlight/mni_ABC/temple051*  ${fmriprep_dir}/searchlight/mni_ABC/temple033* ${fmriprep_dir}/searchlight/mni_ABC/temple035* ${fmriprep_dir}/searchlight/mni_ABC/temple060* ${fmriprep_dir}/searchlight/mni_ABC/temple036* ${fmriprep_dir}/searchlight/mni_ABC/temple032* ${fmriprep_dir}/searchlight/mni_ABC/temple045* ${fmriprep_dir}/searchlight/mni_ABC/temple038* ${fmriprep_dir}/searchlight/mni_ABC/temple063* ${fmriprep_dir}/searchlight/mni_ABC/temple042*

#${fmriprep_dir}/searchlight/mni_ABC/temple030*

#fslmerge -t ${fmriprep_dir}/searchlight/mni_AC/tentwe_mni_zstat_hip.nii.gz ${fmriprep_dir}/searchlight/mni_AC/temple029* ${fmriprep_dir}/searchlight/mni_AC/temple051* ${fmriprep_dir}/searchlight/mni_AC/temple033* ${fmriprep_dir}/searchlight/mni_AC/temple035* ${fmriprep_dir}/searchlight/mni_AC/temple060* ${fmriprep_dir}/searchlight/mni_AC/temple036* ${fmriprep_dir}/searchlight/mni_AC/temple032* ${fmriprep_dir}/searchlight/mni_AC/temple045* ${fmriprep_dir}/searchlight/mni_AC/temple038* ${fmriprep_dir}/searchlight/mni_AC/temple063* ${fmriprep_dir}/searchlight/mni_AC/temple042*
#7-9s

#${fmriprep_dir}/searchlight/mni_ABC/temple030*

# 41, 64, 70, 34, 65, 66, 53, 68
#fslmerge -t ${fmriprep_dir}/searchlight/mni_ABC/sevni_mni_zstat_hip.nii.gz ${fmriprep_dir}/searchlight/mni_ABC/temple041* ${fmriprep_dir}/searchlight/mni_ABC/temple064* ${fmriprep_dir}/searchlight/mni_ABC/temple034* ${fmriprep_dir}/searchlight/mni_ABC/temple065* ${fmriprep_dir}/searchlight/mni_ABC/temple066* ${fmriprep_dir}/searchlight/mni_ABC/temple053* ${fmriprep_dir}/searchlight/mni_ABC/temple068*

#${fmriprep_dir}/searchlight/mni_ABC/temple070*

#fslmerge -t ${fmriprep_dir}/searchlight/mni_AC/sevni_mni_zstat_hip.nii.gz ${fmriprep_dir}/searchlight/mni_AC/temple041* ${fmriprep_dir}/searchlight/mni_AC/temple064* ${fmriprep_dir}/searchlight/mni_AC/temple034* ${fmriprep_dir}/searchlight/mni_AC/temple065* ${fmriprep_dir}/searchlight/mni_AC/temple066* ${fmriprep_dir}/searchlight/mni_AC/temple053* ${fmriprep_dir}/searchlight/mni_AC/temple068*

#${fmriprep_dir}/searchlight/mni_AC/temple070* 

#randomise -i ${fmriprep_dir}/searchlight/mni_ABC/adult_mni_zstat_hip.nii.gz -o ${fmriprep_dir}/searchlight/mni_ABC/adult_ABC_randomise_hip -1 -m $WORK/wr/mni_rois/b_hip.nii.gz -n 5000 -x  --uncorrp

#randomise -i ${fmriprep_dir}/searchlight/mni_AC/adult_mni_zstat_hip.nii.gz -o ${fmriprep_dir}/searchlight/mni_AC/adult_AC_randomise_hip -1 -m $WORK/wr/mni_rois/b_hip.nii.gz -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_ABC/tentwe_mni_zstat_hip.nii.gz -o ${fmriprep_dir}/searchlight/mni_ABC/tentwe_ABC_randomise_hip -1 -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_AC/tentwe_mni_zstat_hip.nii.gz -o ${fmriprep_dir}/searchlight/mni_AC/tentwe_AC_randomise_hip -1 -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_ABC/sevni_mni_zstat_hip.nii.gz -o ${fmriprep_dir}/searchlight/mni_ABC/sevni_ABC_randomise_hip -1 -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_AC/sevni_mni_zstat_hip.nii.gz -o ${fmriprep_dir}/searchlight/mni_AC/sevni_AC_randomise_hip -1 -n 5000 -x  --uncorrp



