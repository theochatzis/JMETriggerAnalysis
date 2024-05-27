#!/bin/bash -e

# Taken from SWGuideGlobalHLT page : https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGlobalHLT

hltGetConfiguration /dev/CMSSW_14_0_0/GRun \
   --globaltag 140X_dataRun3_HLT_for2024TSGStudies_v1 \
   --data \
   --unprescale \
   --output minimal \
   --max-events 10 \
   --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_2_0_xml \
   --input /store/data/Run2023D/EphemeralHLTPhysics0/RAW/v1/000/370/293/00000/2ef73d2a-1fb7-4dac-9961-149525f9e887.root \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_14_0_0_GRun_configDump_data.py

#test running it
#cmsRun tmp.py &> test.log

rm -f tmp.py


