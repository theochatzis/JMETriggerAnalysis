#!/bin/bash -e
hltGetConfiguration /dev/CMSSW_12_4_0/GRun \
   --globaltag 124X_mcRun3_2022_realistic_v12 \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2022_v1_4_0-d1_xml \
   --input /store/mc/Run3Summer22DRPremix/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/124X_mcRun3_2022_realistic_v12-v3/2810000/0021d9ee-25de-4f09-a7ee-a55cf3fa1175.root \
 > tmp.py

edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_12_4_0_GRun_configDump.py
rm -f tmp.py
