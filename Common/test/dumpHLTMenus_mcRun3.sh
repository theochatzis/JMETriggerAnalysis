#!/bin/bash -e
hltGetConfiguration /dev/CMSSW_12_4_0/GRun \
   --globaltag 124X_mcRun3_2022_realistic_forTSG_menu1p4_v1 \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2022_v1_3_0-d1_xml \
   --input /store/mc/Run3Summer21DRPremix/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2540000/b354245e-d8bc-424d-b527-58815586a6a5.root \
 > tmp.py

edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_12_4_0_GRun_configDump.py
rm -f tmp.py
