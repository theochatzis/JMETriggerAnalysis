#!/bin/bash

#add L1 emulator
#run simplified menu
cmsDriver.py Phase2 -s HLT:75e33 --processName=HLTX \
--conditions auto:phase2_realistic_T21 \
--geometry Extended2026D88 \
--era Phase2C17I13M9 \
--eventcontent FEVTDEBUGHLT \
--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 \
--filein=/store/relval/CMSSW_13_1_0_pre3/RelValTTbar_14TeV/GEN-SIM-RECO/131X_mcRun4_realistic_v2_2026D95noPU-v1/00000/23d1df90-bf0e-4277-bcc9-02da47a5e493.root \
-n 1000 --nThreads 1 --no_exec

edmConfigDump Phase2_HLT.py > HLT_75e33_cfg.py

#add: process.MessageLogger.HLTrigReport = cms.untracked.PSet()

#Run with:
#cmsRun HLT_75e33_cfg.py &> test.log