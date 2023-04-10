#!/bin/bash -e

hltGetConfiguration /dev/CMSSW_13_0_0/GRun \
   --globaltag 126X_mcRun3_2023_forPU65_v3 \
   --full \
   --offline \
   --mc \
   --unprescale \
   --process HLTX \
   --output minimal \
   --max-events 10 \
   --input /store/mc/Run3Winter23Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1_ext1-v2/40002/cbcb2b23-174a-4e7f-a385-152d9c5c5b87.root \
   --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2023_v1_0_0_xml \
   --path MC_*,HLTriggerF*,Status*,HLT_PFJet60_v*,HLT_PFJet140_v*,HLT_PFJet320_v*,HLT_PFJet500_v*,HLT_PFHT780_v*,HLT_PFHT890_v*,HLT_PFHT1050_v*,HLT_PFMET120_PFMHT120_IDTight_v*,HLT_PFMET140_PFMHT140_IDTight_v*,HLT_PFMETTypeOne140_PFMHT140_IDTight_v* \
   --customise HLTrigger/Configuration/customizeHLTFor2023.customizeHLTFor2023_v3_fromCondDb \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_13_0_0_GRun_configDump.py

#test running it
#cmsRun tmp.py &> test.log

rm -f tmp.py


