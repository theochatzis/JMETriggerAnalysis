#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_13_0_0/GRun \
   --globaltag 132X_dataRun3_HLT_v2 \
   --data \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2023_v1_2_0_xml \
   --input /store/data/Run2022G/EphemeralHLTPhysics3/RAW/v1/000/362/720/00000/850a6b3c-6eef-424c-9dad-da1e678188f3.root \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_13_0_0_GRun_configDump_dataZjet.py

#test running it
#cmsRun tmp.py &> test.log

#rm -f tmp.py


