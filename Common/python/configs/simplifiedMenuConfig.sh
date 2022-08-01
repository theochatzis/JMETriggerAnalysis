#!/bin/bash

# run simplified menu
cmsDriver.py Phase2 -s HLT:75e33 --processName=HLTX \
--conditions auto:phase2_realistic_T21 \
--geometry Extended2026D88 \
--era Phase2C17I13M9 \
--eventcontent FEVTDEBUGHLT \
--filein=/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-RECO/123X_mcRun4_realistic_v11_2026D88noPU-v1/2580000/4cb86d46-f780-4ce7-94df-9e0039e1953b.root \
-n 100 --nThreads 1 --no_exec

# important:
#please use the following fragment to fix the aging scenario in your configuration:
#from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000
#process = customise_aging_1000(process) 
#
# then run:
#cmsConfigDump Phase2_HLT.py > HLT_75e33_cfg.py
# (the HLT_75e33_cfg will be used in the NTuplizers/test/jmeTriggerNTuple_cfg.py to create the NTuple for your studies)