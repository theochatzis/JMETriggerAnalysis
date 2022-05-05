#!/bin/bash

OUTDIR=${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs

if [ ! -d ${OUTDIR} ]; then
  printf "%s\n" ">> invalid target directory: ${OUTDIR}"
  exit 1
fi

recos=(
 TRKv06p1_TICL
)

for reco_i in "${recos[@]}"; do
  cmsDriver.py step3 \
    --geometry Extended2026D77 --era Phase2C11I13M9 \
    --conditions auto:phase2_realistic_T21 \
    --processName HLTX \
    --step RAW2DIGI,RECO \
    --eventcontent RECO \
    --datatier RECO \
    --filein /store/relval/CMSSW_12_3_0_pre3/RelValTTbar_14TeV/GEN-SIM-RECO/123X_mcRun4_realistic_v3_2026D77noPU-v1/2580000/1f4f72e0-0933-4e78-818a-1b22db93d8b4.root \
    --mc \
    --nThreads 4 \
    --nStreams 4 \
    --no_exec \
    -n 10 \
    --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
    --customise JMETriggerAnalysis/Common/customizeHLTForPhase2.customise_hltPhase2_scheduleJMETriggers_${reco_i} \
    --python_filename ${OUTDIR}/hltPhase2_${reco_i}_cfg_test.py
done
unset reco_i

unset OUTDIR recos
