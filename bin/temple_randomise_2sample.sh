#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 1 ]]; then
    echo "temple_randomise.sh fmriprep_dir"
    exit 1
fi

fmriprep_dir=$1
comp=$2
roi=$3
source $HOME/analysis/temple/rsa/bin/activate

#19, 20, 22, 23, 25, 37, 57, 58, 59, 74, 72, 16, 24, 50, 56, 73, 71, 76
#fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_ten_mni_zstat_${roi}_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple019* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple020* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple022* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple025* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple037* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple057* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple059* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple074* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple072* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple016* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple024* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple050* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple056* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple073* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple071* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple058* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple076* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple023* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple029* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple051*  ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple033* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple035* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple060* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple036* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple032* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple045* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple038* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple063* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple042* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple030*

#fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_sev_mni_zstat_${roi}_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple019* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple020* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple022* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple025* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple037* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple057* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple059* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple074* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple072* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple016* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple024* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple050* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple056* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple073* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple071* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple058* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple076* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple023* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple041* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple064* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple034* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple065* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple066* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple053* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple068* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple070*


#10-12s
# 29, 51, 30, 33, 35, 60, 36, 32, 45, 38, 42, 63
#fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/ten_sev_mni_zstat_${roi}_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple029* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple051*  ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple033* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple035* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple060* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple036* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple032* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple045* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple038* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple063* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple042* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple030* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple041* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple064* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple034* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple065* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple066* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple053* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple068* ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/temple070*


randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_ten_mni_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_over_ten_${comp}_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/adult_ten.mat -t /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/adult_ten.con -n 5000 -x  --uncorrp

#randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_ten_mni_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/ten_over_adult_${comp}_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/10_ad_des.mat -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/ten_sev_mni_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/ten_sev_${comp}_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/ten_sev.mat -t /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/ten_sev.con -n 5000 -x  --uncorrp

#randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/ten_sev_mni_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/sev_over_ten_${comp}_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/7_10_des.mat -t /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/ad_sev.con -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_sev_mni_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_over_sev_${comp}_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/adult_sev.mat -t /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/adult_sev.con -n 5000 -x  --uncorrp

#randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/adult_sev_mni_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/${roi}/sev_over_adult_${comp}_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/rand_d_mats/7_ad_des.mat -n 5000 -x  --uncorrp


