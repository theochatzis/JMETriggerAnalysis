#! /usr/bin/env python3

crabSubmitFile = open("SubmitCrabJobsData.sh","w")
crabSubmitFile.write("#!/bin/bash\n")

storeDir = "TriggerObjects"

samples_muons = {
  #2022
  'Muon0_Run2022CV1':["/Muon/Run2022C-22Sep2023-v1/MINIAOD","Summer22_22Sep2023_RunCD_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_v2"],
  'Muon0_Run2022DV1':["/Muon/Run2022D-22Sep2023-v1/MINIAOD","Summer22_22Sep2023_RunCD_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_v2"],
  'Muon0_Run2022EV1':["/Muon/Run2022E-22Sep2023-v1/MINIAOD","Summer22EE_22Sep2023_RunE_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_v2"],
  'Muon0_Run2022FV1':["/Muon/Run2022F-22Sep2023-v2/MINIAOD","Summer22EE_22Sep2023_RunF_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_PromptAnalysis_v1"],
  'Muon0_Run2022GV1':["/Muon/Run2022G-22Sep2023-v1/MINIAOD","Summer22EE_22Sep2023_RunG_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_PromptAnalysis_v1"],
  #2023 Muon0
  #'/Muon0/Run2023A-PromptReco-v2/MINIAOD':["Muon0_Run2023AV2","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  #'Muon0_Run2023BV1':["/Muon0/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon0_Run2023CV1':["/Muon0/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon0_Run2023CV2':["/Muon0/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon0_Run2023CV3':["/Muon0/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon0_Run2023CV4':["/Muon0/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon0_Run2023DV1':["/Muon0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","132X_dataRun3_Prompt_v4"],
  'Muon0_Run2023DV2':["/Muon0/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  #2023 Muon1
  #'/Muon1/Run2023A-PromptReco-v2/MINIAOD':["Muon1_Run2023AV2","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  #'Muon1_Run2023BV1':["/Muon1/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon1_Run2023CV1':["/Muon1/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon1_Run2023CV2':["/Muon1/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon1_Run2023CV3':["/Muon1/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon1_Run2023CV4':["/Muon1/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'Muon1_Run2023DV1':["/Muon0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  'Muon0_Run2023DV2':["/Muon0/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  'Muon1_Run2023EV1':["/Muon/Run2023E-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  #2024 Muon0
  #'Muon0_Run2024BV1':["/Muon0/Run2024B-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024CV1':["/Muon0/Run2024C-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024DV1':["/Muon0/Run2024D-PromptReco-v1/MINIAOD","Summer24Prompt24_RunDnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024EV1':["/Muon0/Run2024E-PromptReco-v1/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024EV2':["/Muon0/Run2024E-PromptReco-v2/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon0_Run2024FV1':["/Muon0/Run2024F-PromptReco-v1/MINIAOD","Summer24Prompt24_RunFnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'Muon0_Run2024GV1':["/Muon0/Run2024G-PromptReco-v1/MINIAOD","Summer24Prompt24_RunGnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'Muon0_Run2024HV1':["/Muon0/Run2024H-PromptReco-v1/MINIAOD","Summer24Prompt24_RunHnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'Muon0_Run2024IV1':["/Muon0/Run2024I-PromptReco-v1/MINIAOD","Summer24Prompt24_RunInib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  #2024 Muon1
  #'Muon1_Run2024BV1':["/Muon1/Run2024B-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024CV1':["/Muon1/Run2024C-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024DV1':["/Muon1/Run2024D-PromptReco-v1/MINIAOD","Summer24Prompt24_RunDnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024EV1':["/Muon1/Run2024E-PromptReco-v1/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024EV2':["/Muon1/Run2024E-PromptReco-v2/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'Muon1_Run2024FV1':["/Muon1/Run2024F-PromptReco-v1/MINIAOD","Summer24Prompt24_RunFnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'Muon1_Run2024GV1':["/Muon1/Run2024G-PromptReco-v1/MINIAOD","Summer24Prompt24_RunGnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'Muon1_Run2024HV1':["/Muon1/Run2024H-PromptReco-v1/MINIAOD","Summer24Prompt24_RunHnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'Muon1_Run2024IV1':["/Muon1/Run2024I-PromptReco-v1/MINIAOD","Summer24Prompt24_RunInib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  
  #2025 Muon0
  #'Muon0_Run2025B':["/Muon0/Run2025B-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'Muon0_Run2025CV1':["/Muon0/Run2025C-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'Muon0_Run2025CV2':["/Muon0/Run2025C-PromptReco-v2/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'Muon0_Run2025DV1':["/Muon0/Run2025D-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  #2025 Muon1
  #'Muon1_Run2025B':["/Muon1/Run2025B-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'Muon1_Run2025CV1':["/Muon1/Run2025C-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'Muon1_Run2025CV2':["/Muon1/Run2025C-PromptReco-v2/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'Muon1_Run2025DV1':["/Muon0/Run2025D-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
}

samples = {
  #2022
  'JetMET0_Run2022CV1':["/JetMET/Run2022C-22Sep2023-v1/MINIAOD","Summer22_22Sep2023_RunCD_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_v2"],
  'JetMET0_Run2022DV1':["/JetMET/Run2022D-22Sep2023-v1/MINIAOD","Summer22_22Sep2023_RunCD_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_v2"],
  'JetMET0_Run2022EV1':["/JetMET/Run2022E-22Sep2023-v1/MINIAOD","Summer22EE_22Sep2023_RunE_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_v2"],
  'JetMET0_Run2022FV1':["/JetMET/Run2022F-22Sep2023-v2/MINIAOD","Summer22EE_22Sep2023_RunF_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_PromptAnalysis_v1"],
  'JetMET0_Run2022GV1':["/JetMET/Run2022G-22Sep2023-v2/MINIAOD","Summer22EE_22Sep2023_RunG_V3_DATA","Collisions22/Cert_Collisions2022_355100_362760_Golden.json","130X_dataRun3_PromptAnalysis_v1"],
  #2023 JetMET0
  #'/JetMET0/Run2023A-PromptReco-v2/MINIAOD':["JetMET0_Run2023AV2","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  #'JetMET0_Run2023BV1':["/JetMET0/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET0_Run2023CV1':["/JetMET0/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET0_Run2023CV2':["/JetMET0/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET0_Run2023CV3':["/JetMET0/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET0_Run2023CV4':["/JetMET0/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET0_Run2023DV1':["/JetMET0/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  'JetMET0_Run2023DV2':["/JetMET0/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  #2023 JetMET1
  #'/JetMET1/Run2023A-PromptReco-v2/MINIAOD':["JetMET1_Run2023AV2","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  #'JetMET1_Run2023BV1':["/JetMET1/Run2023B-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET1_Run2023CV1':["/JetMET1/Run2023C-PromptReco-v1/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET1_Run2023CV2':["/JetMET1/Run2023C-PromptReco-v2/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET1_Run2023CV3':["/JetMET1/Run2023C-PromptReco-v3/MINIAOD","Summer23Prompt23_RunCv123_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET1_Run2023CV4':["/JetMET1/Run2023C-PromptReco-v4/MINIAOD","Summer23Prompt23_RunCv4_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v3"],
  'JetMET1_Run2023DV1':["/JetMET1/Run2023D-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  'JetMET1_Run2023DV2':["/JetMET1/Run2023D-PromptReco-v2/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  'JetMET1_Run2023EV1':["/JetMET/Run2023E-PromptReco-v1/MINIAOD","Summer23BPixPrompt23_RunD_V3_DATA","Collisions23/Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v4"],
  #2024 JetMET0
  #'JetMET0_Run2024BV1':["/JetMET0/Run2024B-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024CV1':["/JetMET0/Run2024C-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024DV1':["/JetMET0/Run2024D-PromptReco-v1/MINIAOD","Summer24Prompt24_RunDnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024EV1':["/JetMET0/Run2024E-PromptReco-v1/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024EV2':["/JetMET0/Run2024E-PromptReco-v2/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET0_Run2024FV1':["/JetMET0/Run2024F-PromptReco-v1/MINIAOD","Summer24Prompt24_RunFnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'JetMET0_Run2024GV1':["/JetMET0/Run2024G-PromptReco-v1/MINIAOD","Summer24Prompt24_RunGnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'JetMET0_Run2024HV1':["/JetMET0/Run2024H-PromptReco-v1/MINIAOD","Summer24Prompt24_RunHnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'JetMET0_Run2024IV1':["/JetMET0/Run2024I-PromptReco-v1/MINIAOD","Summer24Prompt24_RunInib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  
  #2024 JetMET1
  #'JetMET1_Run2024BV1':["/JetMET1/Run2024B-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024CV1':["/JetMET1/Run2024C-PromptReco-v1/MINIAOD","Summer24Prompt24_RunCnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024DV1':["/JetMET1/Run2024D-PromptReco-v1/MINIAOD","Summer24Prompt24_RunDnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024EV1':["/JetMET1/Run2024E-PromptReco-v1/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024EV2':["/JetMET1/Run2024E-PromptReco-v2/MINIAOD","Summer24Prompt24_RunEnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v2"],
  'JetMET1_Run2024FV1':["/JetMET1/Run2024F-PromptReco-v1/MINIAOD","Summer24Prompt24_RunFnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'JetMET1_Run2024GV1':["/JetMET1/Run2024G-PromptReco-v1/MINIAOD","Summer24Prompt24_RunGnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'JetMET1_Run2024HV1':["/JetMET1/Run2024H-PromptReco-v1/MINIAOD","Summer24Prompt24_RunHnib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  'JetMET1_Run2024IV1':["/JetMET1/Run2024I-PromptReco-v1/MINIAOD","Summer24Prompt24_RunInib1_V1_DATA","Collisions24/Cert_Collisions2024_378981_386951_Golden.json","140X_dataRun3_Prompt_v4"],
  
  #2025 JetMET0
  #'JetMET0_Run2025B':["/JetMET0/Run2025B-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'JetMET0_Run2025CV1':["/JetMET0/Run2025C-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'JetMET0_Run2025CV2':["/JetMET0/Run2025C-PromptReco-v2/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'JetMET0_Run2025D':["/JetMET0/Run2025D-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  #2025 JetMET1
  #'JetMET1_Run2025B':["/JetMET1/Run2025B-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'JetMET1_Run2025CV1':["/JetMET1/Run2025C-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'JetMET1_Run2025CV2':["/JetMET1/Run2025C-PromptReco-v2/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
  'JetMET1_Run2025DV1':["/JetMET0/Run2025D-PromptReco-v1/MINIAOD","","Collisions25/DCSOnly_JSONS/dailyDCSOnlyJSON/Collisions25_13p6TeV_Latest.json","150X_dataRun3_Prompt_v1"],
}

def main():
  for sample, sample_attributes in samples.items():
    name=sample_attributes[0]
    jecsName=sample_attributes[1]
    lumiJSON=sample_attributes[2]
    globalTag=sample_attributes[3]

    print("Creating file: "+name)

    crabSubmitFile.write("rm -rf crab_"+name+"\n")
    crabSubmitFile.write("crab submit -c crab3_"+name+".py\n")

    file = open("crab3_"+name+".py","w")
    file.write("import sys\n")
    file.write("from CRABClient.UserUtilities import config\n")
    file.write("config = config()")
    file.write("\n")
    file.write("store_dir = \'"+storeDir+"\'\n")
    file.write("sample_name = \'"+name+"\'\n")
    file.write("\n")
    file.write("input_file_dir = \'/afs/cern.ch/work/t/tchatzis/private/run3_2023/CMSSW_13_0_7_patch1/src/JMETriggerAnalysis/NTuplizers/test/\'\n")
    file.write("\n")
    file.write("config.section_(\'General\')\n")
    file.write("config.General.requestName = sample_name\n")
    file.write("config.General.transferOutputs = True\n")
    file.write("config.General.transferLogs = False\n")
    file.write("\n")
    file.write("config.section_(\'JobType\')\n")
    file.write("config.JobType.pluginName = \'Analysis\'\n")
    file.write("config.JobType.maxMemoryMB = 2500\n")
    file.write("config.JobType.psetName = input_file_dir+\'jmeTriggerNTuple2023Data_miniAOD_testObjects_cfg.py\'\n")
    file.write("config.JobType.pyCfgParams = [\'offlineJecs="+jecsName+"\',\'globalTag="+globalTag+"\']\n")
    file.write("config.JobType.allowUndistributedCMSSW = True\n")
    file.write("config.JobType.inputFiles = [input_file_dir+\'"+jecsName+".db\']\n")
    file.write("\n")
    file.write("config.section_(\'Data\')\n")
    file.write("config.Data.publication = False\n")
    file.write("config.Data.ignoreLocality = False\n")
    file.write("config.Data.inputDataset = \'"+sample+"\'\n")
    file.write("config.Data.splitting = \'Automatic\'\n")
    file.write("config.Data.unitsPerJob = 200\n")
    file.write("config.Data.totalUnits = -1\n")
    file.write("\n")
    file.write("config.Data.lumiMask = input_file_dir+\'"+lumiJSON+"\'\n")
    file.write("config.Data.outLFNDirBase = \'/store/user/tchatzis/\'+store_dir+\'/\'+sample_name\n")
    file.write("\n")
    file.write("config.section_(\'Site\')\n")
    file.write("config.Site.storageSite = \'T3_CH_CERNBOX\'\n")
    file.close()

  crabSubmitFile.close()

if __name__=="__main__":
  main()
