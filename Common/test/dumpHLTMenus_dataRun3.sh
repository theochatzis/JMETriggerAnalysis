#!/bin/bash -e

# Taken from SWGuideGlobalHLT page : https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT
hltGetConfiguration /dev/CMSSW_15_0_0/GRun \
   --globaltag 150X_dataRun3_HLT_v1 \
   --data \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_2_0_xml \
   --input /store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/250/00000/745d08f7-3834-4757-8f58-5294a13f13ae.root \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_15_0_0_GRun_configDump_data.py

#test running it
#cmsRun tmp.py &> test.log

rm -f tmp.py


