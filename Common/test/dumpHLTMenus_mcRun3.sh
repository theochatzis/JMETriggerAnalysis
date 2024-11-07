#!/bin/bash -e

   hltGetConfiguration /dev/CMSSW_14_0_0/GRun \
   --globaltag auto:phase1_2024_realistic \
   --mc \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --input /store/mc/Run3Winter24Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v8-v2/80000/dc984f7f-2e54-48c4-8950-5daa848b6db9.root \
   --eras Run3_2024 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_3_0_xml \
   --path MC_*,HLTriggerF*,Status*,HLT_PFJet*,HLT_PFHT*,HLT_PFMET*_PFMHT*_IDTight_v* \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_14_0_0_GRun_configDump.py

#test running it
#cmsRun tmp.py &> test.log

rm -f tmp.py


