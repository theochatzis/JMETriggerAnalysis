#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_13_0_0/GRun \
   --globaltag 126X_mcRun3_2023_forPU65_v7 \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --input /store/mc/Run3Winter23Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1_ext1-v2/40002/cbcb2b23-174a-4e7f-a385-152d9c5c5b87.root \
   --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2023_v1_2_0_xml \
   > hltMC.py

cmsRun hltMC.py &> hltMC.log

# dump configuration 
edmConfigDump hltMC.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_13_0_0_GRun_configDump.py

#test running it
#cmsRun hltMC.py &> test.log

rm -f hltMC.py


