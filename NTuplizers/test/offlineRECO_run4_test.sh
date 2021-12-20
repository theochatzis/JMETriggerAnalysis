#!/bin/bash

cmsDriver.py step3 \
  --geometry Extended2026D49 --era Phase2C9 \
  --conditions auto:phase2_realistic_T15 \
  --processName RECO2 \
  --step RAW2DIGI,RECO \
  --eventcontent RECO \
  --datatier RECO \
  --customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000,Configuration/DataProcessing/Utils.addMonitoring \
  --customise HLTrigger.Timer.python.FastTimer.customise_timer_service_print \
  --nThreads 1 \
  --nStreams 1 \
  --mc \
  --filein file:mc/Phase2HLTTDRWinter20DIGI/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_castor_110X_mcRun4_realistic_v3-v2/10000/F07F04A4-F675-7D48-9851-B937CD164E2F.root \
  --fileout offlineRECO_run4_output.root \
  --python_filename offlineRECO_run4_cfg.py \
  -n 100
