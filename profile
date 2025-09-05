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


export SUBS=temple016:temple019:temple020:temple022:temple023:temple024:temple025:temple029:temple030:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple070:temple071:temple072:temple073:temple074:temple075:temple076:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple090:temple091:temple092:temple093:temple094:temple095:temple096:temple097:temple098:temple099:temple103:temple105:temple106:temple107:temple108:temple109:temple110:temple111:temple112:temple113:temple114:temple115:temple116:temple117:temple119:temple120:temple121:temple122:temple123:temple124:temple125:temple126:temple127:temple128:temple129:temple130:temple132
export num_SUBS=86

# to easily call all subs in a for loop
IFS=':' read -ra TEMPLE_SUBS <<< "$SUBS"
export SUB_LIST="${TEMPLE_SUBS[@]}"

export SUBS_nodrop=temple016:temple019:temple020:temple022:temple024:temple025:temple029:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple071:temple072:temple073:temple074:temple075:temple076:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple090:temple091:temple092:temple093:temple094:temple095:temple096:temple097:temple098:temple099:temple103:temple105:temple106:temple107:temple108:temple109:temple110:temple111:temple112:temple113:temple114:temple115:temple117:temple119:temple120:temple121:temple122:temple123:temple124:temple125
export num_SUBS_nodrop=76


export SUBS_ND=temple016:temple019:temple020:temple022:temple024:temple025:temple029:temple032:temple033:temple034:temple035:temple036:temple037:temple038:temple041:temple042:temple045:temple050:temple051:temple053:temple056:temple057:temple058:temple059:temple060:temple063:temple064:temple065:temple066:temple068:temple069:temple071:temple072:temple073:temple074:temple075:temple076:temple078:temple079:temple082:temple083:temple084:temple085:temple087:temple089:temple088:temple090:temple091:temple092:temple093:temple094:temple095:temple096:temple097:temple098:temple099:temple103:temple105:temple106:temple107:temple108:temple109:temple110:temple111:temple112:temple113:temple114:temple119:temple120
export num_ND=69

export gm_extent=115
export hip_extent=15


export MOSHI_SUBS=moshiGO_201:moshiGO_202:moshiGO_203:moshiGO_208:moshiGO_211:moshiGO_212:moshiGO_213:moshiGO_220:moshiGO_221:moshiGO_222:moshiGO_223:moshiGO_224:moshiGO_226:moshiGO_228:moshiGO_229:moshiGO_230:moshiGO_231:moshiGO_232:moshiGO_235:moshiGO_238:moshiGO_239:moshiGO_240:moshiGO_241:moshiGO_243:moshiGO_246:moshiGO_247:moshiGO_248:moshiGO_249:moshiGO_250:moshiGO_251:moshiGO_252:moshiGO_253:moshiGO_255:moshiGO_258:moshiGO_259:moshiGO_260:moshiGO_261:moshiGO_262:moshiGO_266:moshiGO_268:moshiGO_270:moshiGO_271:moshiGO_273:moshiGO_277:moshiGO_278:moshiGO_279:moshiGO_280:moshiGO_281:moshiGO_282:moshiGO_284:moshiGO_285:moshiGO_289:moshiGO_291:moshiGO_292:moshiGO_293:moshiGO_294:moshiGO_297:moshiGO_298:moshiGO_302:moshiGO_304:moshiGO_305:moshiGO_306:moshiGO_308:moshiGO_310:moshiGO_312:moshiGO_313:moshiGO_314:moshiGO_315:moshiGO_316:moshiGO_320:moshiGO_321:moshiGO_322:moshiGO_323:moshiGO_324:moshiGO_327:moshiGO_329:moshiGO_331:moshiGO_333:moshiGO_334:moshiGO_336:moshiGO_339:moshiGO_341:moshiGO_343:moshiGO_345:moshiGO_350:moshiGO_351
export MOSHI_DROP=moshiGO_222:moshiGO_211:moshiGO_351:moshiGO_298:moshiGO_226:moshiGO_323:moshiGO_341:moshiGO_229:moshiGO_279:moshiGO_282:moshiGO_350:moshiGO_212:moshiGO_240:moshiGO_262:moshiGO_297:moshiGO_280:moshiGO_329:moshiGO_253:moshiGO_268:moshiGO_221:moshiGO_343:moshiGO_273:moshiGO_324:moshiGO_239:moshiGO_247:moshiGO_220:moshiGO_243:moshiGO_281:moshiGO_251:moshiGO_322:moshiGO_327:moshiGO_314:moshiGO_336:moshiGO_250:moshiGO_310:moshiGO_308:moshiGO_331:moshiGO_339:moshiGO_320:moshiGO_246:moshiGO_208:moshiGO_249:moshiGO_313:moshiGO_315:moshiGO_333:moshiGO_201:moshiGO_266:moshiGO_238:moshiGO_258:moshiGO_231:moshiGO_304:moshiGO_259:moshiGO_261:moshiGO_284:moshiGO_305:moshiGO_312:moshiGO_224:moshiGO_291:moshiGO_223:moshiGO_235:moshiGO_202:moshiGO_306:moshiGO_293:moshiGO_260:moshiGO_292:moshiGO_203:moshiGO_271:moshiGO_252:moshiGO_270:moshiGO_228:moshiGO_232:moshiGO_302

export MV_SUBS=temple056:temple057:temple058:temple059:temple060:temple061:temple063:temple064:temple065:temple066:temple068:temple069:temple070:temple071:temple072:temple073:temple074:temple075:temple076:temple079:temple082:temple083:temple084:temple085:temple087:temple088:temple089:temple090:temple091:temple092:temple093:temple094:temple095:temple096:temple097:temple098:temple099:temple103:temple105:temple106:temple107:temple108:temple109:temple110:temple111:temple112:temple113:temple114:temple115:temple116:temple120:temple122:temple124:temple117:temple119:temple121:temple123:temple125:temple126:temple128:temple129:temple130:temple132
export num_MV=63

# to easily call all subs in a for loop
IFS=':' read -ra TEMPLE_SUBS <<< "$MV_SUBS"
export MV_LIST="${TEMPLE_SUBS[@]}"