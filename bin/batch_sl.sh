#!/bin/bash

comp=$1
masktype=$2

source /home1/09123/ofriend/analysis/temple/rsa/bin/activate

for sub in temple016 temple019 temple020 temple022 temple024 temple025 temple029 temple030 temple032 temple033 temple034 temple035 temple036 temple037 temple038 temple041 temple042 temple045 temple050 temple051 temple053 temple056 temple057 temple058 temple059 temple060 temple063 temple064 temple065 temple066 temple068 temple069 temple070 temple071 temple072 temple073 temple074 temple075 temple076 temple078 temple079 temple082 temple083 temple084 temple085 temple087 temple089 temple088 temple090 temple091 temple092 temple093 temple094 temple095 temple096 temple097 temple098 temple099 temple103 temple105 temple106 temple107 temple108 temple109 temple110 temple111 temple112 temple113 temple114 temple115 temple116 temple117 temple119 temple120 temple121 temple122 temple123 temple124 temple125 temple126 temple127 temple128 temple129 temple130 temple131 temple132 temple133 temple135 temple136; do

  temple_sl_prepost.py $sub $comp gm
  temple_sl_prepost.py $sub $comp hippocampus

  sl_to_mni.sh $sub /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep $comp b_gray_func prepost
  sl_to_mni.sh $sub /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep $comp b_hip prepost

done

temple_sl_prepost.py temple023 $comp gm --drop_run=6
temple_sl_prepost.py temple023 $comp hippocampus --drop_run=6
sl_to_mni.sh temple023 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep $comp b_gray_func prepost
sl_to_mni.sh temple023 /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep $comp b_hip prepost