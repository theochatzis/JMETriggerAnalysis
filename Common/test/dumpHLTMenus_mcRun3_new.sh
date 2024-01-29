#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_13_3_0/GRun \
   --globaltag auto:phase1_2023_realistic \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --input /store/relval/CMSSW_13_3_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/133X_mcRun3_2023_realistic_v1_Standard_13_3_0_pre4-v1/2590000/4c47f6d7-9938-4c87-b795-ece3aa6d3d22.root \
   --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2023_v1_3_0_xml \
   > hltMC.py


# dump configuration 
edmConfigDump hltMC.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_13_3_0_GRun_configDump.py

#test running it
#cmsRun hltMC.py &> test.log

rm -f hltMC.py


