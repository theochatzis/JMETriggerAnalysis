#!/bin/bash

#add L1 emulator
#run simplified menu
cmsDriver.py Phase2 -s L1P2GT,HLT:75e33 --processName=HLTX \
--conditions auto:phase2_realistic_T33 \
--geometry Extended2026D110 \
--era Phase2C17I13M9 \
--eventcontent FEVTDEBUGHLT \
--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 \
--filein /store/mc/Phase2Spring24DIGIRECOMiniAOD/DYToLL_M-10To50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200ALCA_pilot_140X_mcRun4_realistic_v4-v1/130000/00969257-fdc7-4748-be48-d21074b28511.root \
--inputCommands='keep *, drop *_hlt*_*_HLT, drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT' \
-n 1 --nThreads 1 --no_output

edmConfigDump Phase2_L1P2GT_HLT.py > HLT_75e33_D110_cfg.py

#add: process.MessageLogger.HLTrigReport = cms.untracked.PSet()

#Run with:
#cmsRun HLT_75e33_cfg.py &> test.log
