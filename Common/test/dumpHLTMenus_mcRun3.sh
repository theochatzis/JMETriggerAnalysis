#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_15_0_0/GRun \
   --globaltag 142X_mcRun3_2025_realistic_v7 \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --input /store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/0174bea8-1bb2-442c-ab23-c0864b50a3a0.root \
   --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_3_0_xml \
   --path MC_*,HLTriggerF*,Status*,HLT_PFJet*,HLT_PFHT*,HLT_PFMET*_PFMHT*_IDTight_v* \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_15_0_0_GRun_configDump.py

#test running it
#cmsRun tmp.py &> test.log

rm -f tmp.py


