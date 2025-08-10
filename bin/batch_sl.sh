#!/bin/bash

comp=$1
masktype=$2

source /home1/09123/ofriend/analysis/temple/rsa/bin/activate

for sub in temple016 temple019 temple020 temple024 temple025 temple029 \
temple032 temple033 temple034 temple035 temple036 temple037 temple038 temple041 \
temple042 temple045 temple050 temple051 temple053 temple056 temple057 temple058 \
temple059 temple060 temple063 temple064 temple065 temple066 temple068 temple069 \
temple071 temple072 temple073 temple074 temple075 temple076 temple078 temple079 \
temple082 temple083 temple084 temple085 temple087 temple089 temple088 temple090 \
temple091 temple092 temple093 temple094 temple095 temple096 temple097 temple098 \
temple099 temple103 temple105 temple106 temple107 temple108 temple109 temple110 \
temple111 temple112 temple113 temple114 temple119 temple120 temple123 temple124 \
temple125 temple126  temple128 temple130; do #temple127

  temple_sl_prepost.py $sub $comp $masktype
#  sl_to_mni.sh $sub /scratch/09123/ofriend/temple/new_prepro/derivatives/fmriprep $comp $masktype prepost
done

temple_sl_prepost.py temple023 $comp $masktype --drop_run=6

temple_sl_prepost.py temple030 $comp $masktype --drop_run=6

temple_sl_prepost.py temple070 $comp $masktype --drop_run=3

temple_sl_prepost.py temple116 $comp $masktype --drop_run=5