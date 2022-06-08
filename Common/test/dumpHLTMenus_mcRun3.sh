#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_12_3_0/GRun \
 --full \
 --offline \
 --mc --unprescale \
 --process HLTX \
 --globaltag auto:phase1_2021_realistic \
 --input /store/mc/Run3Summer21DRPremix/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2540000/b354245e-d8bc-424d-b527-58815586a6a5.root \
 --max-events 10 \
 --eras Run3 \
 --l1-emulator FullMC --l1 L1Menu_Collisions2022_v1_0_0_xml \
 > tmp.py

edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_12_3_0_GRun_configDump.py
rm -f tmp.py
