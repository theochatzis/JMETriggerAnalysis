## MC Run-3
#cmsrel CMSSW_11_1_0_pre7 && cd CMSSW_11_1_0_pre7/src && cmsenv
#git cms-merge-topic missirol:devel_debugCorrectedJetProducer

hltGetConfiguration /dev/CMSSW_11_1_0/GRun/V7 \
  --globaltag 110X_mcRun3_2021_realistic_v6 \
  --process HLT2 --full --offline --mc \
  --input /store/mc/Run3Winter20DRPremixMiniAOD/GluGluToHHTo4B_node_SM_TuneCP5_14TeV-madgraph-pythia8/GEN-SIM-RAW/110X_mcRun3_2021_realistic_v6-v2/250000/904FDC0F-6179-7E44-9988-C20E997EFFA8.root \
  --paths HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v3 \
  --prescale none --output none --max-events 100 --type GRun > hlt_mc.py

## Data 2018
#cmsrel CMSSW_10_2_18 && cd CMSSW_10_2_18/src && cmsenv

hltGetConfiguration /online/collisions/2018/2e34/v3.6/HLT \
  --globaltag 101X_dataRun2_HLT_v7 --data --process HLT2 --full --offline \
  --type GRun --path HLTriggerFirstPath,HLT_PFHT330PT30_QuadPFJet_75_60_45_40_v9,HLTriggerFinalPath,HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v3,HLTAnalyzerEndpath \
  --timing --prescale none --max-events 30000 --output none > hlt_data.py
