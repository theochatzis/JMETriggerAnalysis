#!/bin/bash -e

# option5: /users/vmastrap/doubletRecovery23/trkWithDoubletRecovery/V6
# option3: /users/vmastrap/doubletRecovery23/trkWithDoubletRecovery/V3
#hltGetConfiguration /dev/CMSSW_13_0_0/GRun \
hltGetConfiguration /dev/CMSSW_13_0_0/GRun \
   --globaltag 130X_dataRun3_HLT_v2 \
   --data \
   --unprescale \
   --output minimal \
   --max-events 100 \
   --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2023_v1_2_0_xml \
   --path HLTriggerF*,Status*,HLT_PFJet60_v*,HLT_PFJet140_v*,HLT_PFJet320_v*,HLT_PFJet500_v*,HLT_PFHT780_v*,HLT_PFHT890_v*,HLT_PFHT1050_v*,HLT_PFMET120_PFMHT120_IDTight_v*,HLT_PFMET140_PFMHT140_IDTight_v*,HLT_PFMETTypeOne140_PFMHT140_IDTight_v*,HLT_IsoMu27_v* \
   --input /store/data/Run2022G/EphemeralHLTPhysics3/RAW/v1/000/362/720/00000/850a6b3c-6eef-424c-9dad-da1e678188f3.root \
   > tmp.py

# dump configuration 
edmConfigDump tmp.py > "${CMSSW_BASE}"/src/JMETriggerAnalysis/Common/python/configs/HLT_dev_CMSSW_13_0_0_GRun_configDump_data_compare.py

#test running it
#cmsRun tmp.py &> test.log

#rm -f tmp.py


