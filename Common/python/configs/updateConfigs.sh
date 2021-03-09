#!/bin/bash

OUTDIR=${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs

if [ ! -d ${OUTDIR} ]; then
  printf "%s\n" ">> invalid target directory: ${OUTDIR}"
  exit 1
fi

recos=(
 TRKv00
 TRKv00_TICL
 TRKv02
 TRKv02_TICL
 TRKv06
 TRKv06_TICL
 TRKv06p1
 TRKv06p1_TICL
 TRKv07p2
 TRKv07p2_TICL
)

for reco_i in "${recos[@]}"; do
  cmsDriver.py step3 \
    --geometry Extended2026D49 --era Phase2C9 \
    --conditions 111X_mcRun4_realistic_T15_v5 \
    --processName HLTX \
    --step RAW2DIGI,RECO \
    --eventcontent RECO \
    --datatier RECO \
    --filein /store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/280000/015FB6F1-59B4-304C-B540-2392A983A97D.root \
    --mc \
    --nThreads 4 \
    --nStreams 4 \
    --no_exec \
    -n 10 \
    --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
    --customise JMETriggerAnalysis/Common/customizeHLTForPhase2.customise_hltPhase2_scheduleJMETriggers_${reco_i} \
    --python_filename ${OUTDIR}/hltPhase2_${reco_i}_cfg.py
done
unset reco_i

unset OUTDIR recos
