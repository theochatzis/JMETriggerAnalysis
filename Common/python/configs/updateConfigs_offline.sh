#!/bin/bash

OUTDIR=${CMSSW_BASE}/src/JMETriggerAnalysis/Common/python/configs


cmsDriver.py step3 \
  --geometry Extended2026D88 --era Phase2C17I13M9 \
  --conditions auto:phase2_realistic_T21 \
  --processName HLTX \
  --step RAW2DIGI,RECO \
  --eventcontent RECO \
  --datatier RECO \
  --filein /store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-RECO/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/01b3b6fd-4e69-4d27-ad97-d889c9ca1f54.root \
  --mc \
  --nThreads 4 \
  --nStreams 4 \
  --no_exec \
  -n 10 \
  --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
  --customise_commands 'process.prune()\n' \
  --python_filename ${OUTDIR}/offline_cfg_test.py

