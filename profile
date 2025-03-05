#!/bin/bash

#script directory
source /home1/09123/ofriend/.bashrc

module load freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
module load ants

# study name and directory
export STUDY=temple
export SRCDIR=$HOME/analysis/temple
export STUDYDIR=$STOCKYARD2/ls6/temple
export BATCHDIR=$STOCKYARD2/ls6/temple/batch/launchscripts
export FS=$SCRATCH/temple/new_prepro/derivatives/fmriprep/sourcedata/freesurfer
export FM=$SCRATCH/temple/new_prepro/derivatives/fmriprep
export CORR=/corral-repl/utexas/prestonlab/temple
# add analysis scripts to path
export PATH=$PATH:$SRCDIR/bin
export STUDYDIR=$STOCKYARD2/ls6/temple
. $STOCKYARD2/ls6/tempenv/bin/activate
export ASHS_ROOT=/work/09123/ofriend/ls6/ashs/ashs-fastashs_beta

# change color to differentiate from wr when working
echo -e "\033]11;#084f00\007"

# subjects
export SKY_SUBS=temple_016:temple_019:temple_020:temple_022:temple_023:temple_024:temple_025:temple_029:temple_030:temple_032:temple_033:temple_034:temple_035:temple_036:temple_037:temple_038:temple_041:temple_042:temple_045:temple_050:temple_051:temple_053
export SKYBIDS=temple016:temple019:temple020:temple022:temple023:temple024:temple025:temple029:temple030:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053
export num_sky=22




sub_ids=temple_016:temple_019:temple_020:temple_022:temple_023:temple_024:temple_025:temple_029:temple_030:temple_032:temple_033:temple_034:temple_035:temple_036:temple_037:temple_038:temple_041:temple_042:temple_045:temple_050:temple_051:temple_053:temple_056:temple_057:temple_058:temple_059:temple_060:temple_063:temple_064:temple_065:temple_066:temple_068:temple_070:temple_071:temple_072:temple_073:temple_074:temple_076

# for work without sub 16
export TEMPSUBS=temple076:temple019:temple020:temple022:temple023:temple024:temple025:temple029:temple030:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple070:temple071:temple072:temple073:temple074:temple075:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple092:temple093

export SUBS=temple016:temple019:temple020:temple022:temple023:temple024:temple025:temple029:temple030:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple070:temple071:temple072:temple073:temple074:temple075:temple076:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple090:temple091:temple092:temple093:temple094:temple095:temple096:temple097:temple098:temple099:temple103:temple105:temple106:temple107:temple108:temple109:temple110:temple111:temple112:temple113:temple114:temple115:temple116:temple119:temple120
export num_SUBS=74

export SUBS_ND=temple016:temple019:temple020:temple022:temple024:temple025:temple029:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple071:temple072:temple073:temple074:temple075:temple076:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple090:temple091:temple092:temple093:temple094:temple095:temple096:temple097:temple098:temple099:temple103:temple105:temple106:temple107:temple108:temple109:temple110:temple111:temple112:temple113:temple114:temple119:temple120
export num_ND=69

export COLL_SUBS=temple016:temple019:temple020:temple022:temple023:temple024:temple025:temple029:temple030:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple071:temple072:temple073:temple074:temple075:temple076:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple092:temple093
