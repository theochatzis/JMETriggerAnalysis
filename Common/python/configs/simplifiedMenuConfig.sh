#!/bin/bash

#add L1 emulator
#run simplified menu
cmsDriver.py Phase2 -s HLT:75e33 --processName=HLTX \
--conditions auto:phase2_realistic_T21 \
--geometry Extended2026D95 \
--era Phase2C17I13M9 \
--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 \
--eventcontent FEVTDEBUGHLT \
--filein=/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_131X_mcRun4_realistic_v5-v1/30000/01607282-0427-4687-a122-ef0a41220590.root \
-n 100 --nThreads 1 --no_exec

#edmConfigDump Phase2_HLT.py > HLT_75e33_ticlv3_cfg.py

#add: process.MessageLogger.HLTrigReport = cms.untracked.PSet()

#Run with:
#cmsRun HLT_75e33_cfg.py &> test.log
