#!/bin/bash
#
# Run randomise to test z-statistic images.

if [[ $# -lt 3 ]]; then
    echo "temple_randomise_2sample_new.sh fmriprep_dir comp roi"
    exit 1
fi

fmriprep_dir=$1
comp=$2
roi=$3
source $HOME/analysis/temple/rsa/bin/activate

# temple_randomise_2sample_new.sh $FM AC_symm whole_brain
# temple_randomise_2sample_new.sh $FM AC whole_brain


fslmerge -t ${fmriprep_dir}/searchlight/mni_${comp}/group_zstat_${roi}_${comp}.nii.gz ${fmriprep_dir}/searchlight/mni_${comp}/temple064* ${fmriprep_dir}/searchlight/mni_${comp}/temple070* ${fmriprep_dir}/searchlight/mni_${comp}/temple078* ${fmriprep_dir}/searchlight/mni_${comp}/temple041* ${fmriprep_dir}/searchlight/mni_${comp}/temple084* ${fmriprep_dir}/searchlight/mni_${comp}/temple092* ${fmriprep_dir}/searchlight/mni_${comp}/temple053* ${fmriprep_dir}/searchlight/mni_${comp}/temple065* ${fmriprep_dir}/searchlight/mni_${comp}/temple063* ${fmriprep_dir}/searchlight/mni_${comp}/temple069* ${fmriprep_dir}/searchlight/mni_${comp}/temple034* ${fmriprep_dir}/searchlight/mni_${comp}/temple068* ${fmriprep_dir}/searchlight/mni_${comp}/temple066* ${fmriprep_dir}/searchlight/mni_${comp}/temple060* ${fmriprep_dir}/searchlight/mni_${comp}/temple093* ${fmriprep_dir}/searchlight/mni_${comp}/temple030* ${fmriprep_dir}/searchlight/mni_${comp}/temple051* ${fmriprep_dir}/searchlight/mni_${comp}/temple079* ${fmriprep_dir}/searchlight/mni_${comp}/temple029* ${fmriprep_dir}/searchlight/mni_${comp}/temple036* ${fmriprep_dir}/searchlight/mni_${comp}/temple035* ${fmriprep_dir}/searchlight/mni_${comp}/temple082* ${fmriprep_dir}/searchlight/mni_${comp}/temple033* ${fmriprep_dir}/searchlight/mni_${comp}/temple085* ${fmriprep_dir}/searchlight/mni_${comp}/temple038* ${fmriprep_dir}/searchlight/mni_${comp}/temple042* ${fmriprep_dir}/searchlight/mni_${comp}/temple045* ${fmriprep_dir}/searchlight/mni_${comp}/temple083* ${fmriprep_dir}/searchlight/mni_${comp}/temple032* ${fmriprep_dir}/searchlight/mni_${comp}/temple056* ${fmriprep_dir}/searchlight/mni_${comp}/temple089* ${fmriprep_dir}/searchlight/mni_${comp}/temple072* ${fmriprep_dir}/searchlight/mni_${comp}/temple059* ${fmriprep_dir}/searchlight/mni_${comp}/temple074* ${fmriprep_dir}/searchlight/mni_${comp}/temple075* ${fmriprep_dir}/searchlight/mni_${comp}/temple057* ${fmriprep_dir}/searchlight/mni_${comp}/temple076* ${fmriprep_dir}/searchlight/mni_${comp}/temple058* ${fmriprep_dir}/searchlight/mni_${comp}/temple088* ${fmriprep_dir}/searchlight/mni_${comp}/temple020* ${fmriprep_dir}/searchlight/mni_${comp}/temple087* ${fmriprep_dir}/searchlight/mni_${comp}/temple037* ${fmriprep_dir}/searchlight/mni_${comp}/temple023* ${fmriprep_dir}/searchlight/mni_${comp}/temple019* ${fmriprep_dir}/searchlight/mni_${comp}/temple071* ${fmriprep_dir}/searchlight/mni_${comp}/temple024* ${fmriprep_dir}/searchlight/mni_${comp}/temple025* ${fmriprep_dir}/searchlight/mni_${comp}/temple022* ${fmriprep_dir}/searchlight/mni_${comp}/temple016* ${fmriprep_dir}/searchlight/mni_${comp}/temple073* ${fmriprep_dir}/searchlight/mni_${comp}/temple050* 


randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/group_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/group_zstat_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/new_rand_mats_081324/new_group.mat -t /home1/09123/ofriend/analysis/temple/bin/templates/new_rand_mats_081324/new_group.con -n 5000 -x  --uncorrp

randomise -i ${fmriprep_dir}/searchlight/mni_${comp}/group_zstat_${roi}_${comp}.nii.gz -o ${fmriprep_dir}/searchlight/mni_${comp}/age_param_zstat_randomise_${roi} -d /home1/09123/ofriend/analysis/temple/bin/templates/new_rand_mats_081324/new_age_parametric.mat -t /home1/09123/ofriend/analysis/temple/bin/templates/new_rand_mats_081324/new_age_parametric.con -n 5000 -x  --uncorrp
