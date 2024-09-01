#!/bin/bash

#add L1 emulator
#run simplified menu
cmsDriver.py Phase2 -s HLT:75e33 --processName=HLTX \
--conditions auto:phase2_realistic_T33 \
--geometry Extended2026D110 \
--era Phase2C17I13M9 \
--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 \
--eventcontent FEVTDEBUGHLT \
--filein=/store/relval/CMSSW_14_0_6/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_140X_mcRun4_realistic_v3_STD_2026D110_PU-v1/2590000/00042ff4-01a3-48a9-b88e-83412b3a65c6.root \
-n 100 --nThreads 1 --no_exec

edmConfigDump Phase2_HLT.py > HLT_75e33_D110_cfg.py

#add: process.MessageLogger.HLTrigReport = cms.untracked.PSet()

#Run with:
#cmsRun HLT_75e33_cfg.py &> test.log
