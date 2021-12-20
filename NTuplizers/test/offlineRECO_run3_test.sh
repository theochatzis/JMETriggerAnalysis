#!/bin/bash

cmsDriver.py step3 \
  --era Run3 \
  --conditions auto:phase1_2021_realistic \
  --processName RECO2 \
  --step RAW2DIGI,RECO \
  --eventcontent RECO \
  --datatier RECO \
  --customise HLTrigger.Timer.python.FastTimer.customise_timer_service_print \
  --nThreads 1 \
  --nStreams 1 \
  --mc \
  --filein file:mc/Run3Winter20DRMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/240000/54077295-ED36-6046-8D6F-F17EE87C63DD.root \
  --fileout offlineRECO_run3_output.root \
  --python_filename offlineRECO_run3_cfg.py \
  -n 100
