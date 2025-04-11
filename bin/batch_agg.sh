#!/bin/bash

comps=$1


source /home1/09123/ofriend/analysis/temple/rsa/bin/activate


#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AB hip_subfields --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#${comps} searchlight_contrast --agg_file

#aggregate_integration.py symmetry /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#${comps} searchlight_contrast --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#BC hip_subfields --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#BC lat_hip_subregions --agg_file
#
#aggregate_integration.py both /corral-repl/utexas/prestonlab/temple/integration_prepost \
#AB lat_hip_subregions --agg_file

for sub in temple016 temple019 temple020 temple022 temple024 temple025 temple029 \
temple032 temple033 temple034 temple035 temple036 temple037 temple038 temple041 \
temple042 temple045 temple050 temple051 temple053 temple056 temple057 temple058 \
temple059 temple060 temple063 temple064 temple065 temple066 temple068 temple069 \
temple071 temple072 temple073 temple074 temple075 temple076 temple078 temple079 \
temple082 temple083 temple084 temple085 temple087 temple089 temple088 temple090 \
temple091 temple092 temple093 temple094 temple095 temple096 temple097 temple098 \
temple099 temple103 temple105 temple106 temple107 temple108 temple109 temple110 \
temple111 temple112 temple113 temple114 temple115 temple117 temple119 temple120 \
temple121 temple122 temple123 temple124 temple125; do

  temple_sl_prepost.py ${sub} AC_weak gm
  sl_to_mni.sh ${sub} /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AC_weak b_gray_func prepost
#  /home1/09123/ofriend/analysis/temple/bin/run_descriptives/tsnr_by_roi.sh /corral-repl/utexas/prestonlab/temple/ ${sub} lat_hip_subregions


done

temple_sl_prepost.py temple023 AC_weak gm --drop_run=6
sl_to_mni.sh temple023 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AC_weak b_gray_func prepost
temple_sl_prepost.py temple030 AC_weak gm --drop_run=6
sl_to_mni.sh temple030 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AC_weak b_gray_func prepost
temple_sl_prepost.py temple070 AC_weak gm --drop_run=3
sl_to_mni.sh temple070 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AC_weak b_gray_func prepost
temple_sl_prepost.py temple116 AC_weak gm --drop_run=5
sl_to_mni.sh temple116 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AC_weak b_gray_func prepost



for sub in temple016 temple019 temple020 temple022 temple024 temple025 temple029 \
temple032 temple033 temple034 temple035 temple036 temple037 temple038 temple041 \
temple042 temple045 temple050 temple051 temple053 temple056 temple057 temple058 \
temple059 temple060 temple063 temple064 temple065 temple066 temple068 temple069 \
temple071 temple072 temple073 temple074 temple075 temple076 temple078 temple079 \
temple082 temple083 temple084 temple085 temple087 temple089 temple088 temple090 \
temple091 temple092 temple093 temple094 temple095 temple096 temple097 temple098 \
temple099 temple103 temple105 temple106 temple107 temple108 temple109 temple110 \
temple111 temple112 temple113 temple114 temple115 temple117 temple119 temple120 \
temple121 temple122 temple123 temple124 temple125; do

  temple_sl_prepost.py ${sub} AB gm
  sl_to_mni.sh ${sub} /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AB b_gray_func prepost
#  /home1/09123/ofriend/analysis/temple/bin/run_descriptives/tsnr_by_roi.sh /corral-repl/utexas/prestonlab/temple/ ${sub} lat_hip_subregions


done

temple_sl_prepost.py temple023 AB gm --drop_run=6
sl_to_mni.sh temple023 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AB b_gray_func prepost
temple_sl_prepost.py temple030 AB gm --drop_run=6
sl_to_mni.sh temple030 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AB b_gray_func prepost
temple_sl_prepost.py temple070 AB gm --drop_run=3
sl_to_mni.sh temple070 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AB b_gray_func prepost
temple_sl_prepost.py temple116 AB gm --drop_run=5
sl_to_mni.sh temple116 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ AB b_gray_func prepost



for sub in temple016 temple019 temple020 temple022 temple024 temple025 temple029 \
temple032 temple033 temple034 temple035 temple036 temple037 temple038 temple041 \
temple042 temple045 temple050 temple051 temple053 temple056 temple057 temple058 \
temple059 temple060 temple063 temple064 temple065 temple066 temple068 temple069 \
temple071 temple072 temple073 temple074 temple075 temple076 temple078 temple079 \
temple082 temple083 temple084 temple085 temple087 temple089 temple088 temple090 \
temple091 temple092 temple093 temple094 temple095 temple096 temple097 temple098 \
temple099 temple103 temple105 temple106 temple107 temple108 temple109 temple110 \
temple111 temple112 temple113 temple114 temple115 temple117 temple119 temple120 \
temple121 temple122 temple123 temple124 temple125; do

  temple_sl_prepost.py ${sub} ABC gm
  sl_to_mni.sh ${sub} /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ ABC b_gray_func prepost
#  /home1/09123/ofriend/analysis/temple/bin/run_descriptives/tsnr_by_roi.sh /corral-repl/utexas/prestonlab/temple/ ${sub} lat_hip_subregions


done

temple_sl_prepost.py temple023 ABC gm --drop_run=6
sl_to_mni.sh temple023 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ ABC b_gray_func prepost
temple_sl_prepost.py temple030 ABC gm --drop_run=6
sl_to_mni.sh temple030 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ ABC b_gray_func prepost
temple_sl_prepost.py temple070 ABC gm --drop_run=3
sl_to_mni.sh temple070 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ ABC b_gray_func prepost
temple_sl_prepost.py temple116 ABC gm --drop_run=5
sl_to_mni.sh temple116 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/ ABC b_gray_func prepost

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AB b_ifg_subregions --agg_file

#aggregate_integration.py both /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep/integration_prepost \
#AC b_ifg_subregions --agg_file


