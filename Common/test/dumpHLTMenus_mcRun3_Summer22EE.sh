#!/bin/bash -e
hltGetConfiguration /dev/CMSSW_12_4_0/GRun \
   --globaltag auto:phase1_2022_realistic_postEE \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2022_v1_4_0-d1_xml \
   --input /store/mc/Run3Summer22EEDR/TT_TuneCP5_13p6TeV-powheg-pythia8/GEN-SIM-RAW/Poisson70KeepRAW_124X_mcRun3_2022_realistic_postEE_v1-v1/2820000/9d9729c8-b83e-4714-8c6c-56aeca948934.root \
 > tmp.py

edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_12_4_0_GRun_postEE_configDump.py
rm -f tmp.py
