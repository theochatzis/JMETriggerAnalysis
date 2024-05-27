#! /usr/bin/env python3

crabSubmitFile = open("SubmitCrabJobsData.sh","w")
crabSubmitFile.write("#!/bin/bash\n")

storeDir = "TriggerObjects"

samples_muons = {
  #2022
  '/Muon/Run2022C-PromptReco-v1/MINIAOD':["Muon0_Run2022CV1","Winter22Run3_RunC_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/Muon/Run2022D-PromptReco-v1/MINIAOD':["Muon0_Run2022DV1","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/Muon/Run2022D-PromptReco-v2/MINIAOD':["Muon0_Run2022DV2","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/Muon/Run2022D-PromptReco-v3/MINIAOD':["Muon0_Run2022DV3","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/Muon/Run2022E-PromptReco-v1/MINIAOD':["Muon0_Run2022EV1","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/Muon/Run2022F-PromptReco-v1/MINIAOD':["Muon0_Run2022FV1","Summer22EEPrompt22_RunF_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/Muon/Run2022G-PromptReco-v1/MINIAOD':["Muon0_Run2022GV1","Summer22EEPrompt22_RunG_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  #2023 Muon0
  '/Muon0/Run2023A-PromptReco-v2/MINIAOD':["Muon0_Run2023AV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023B-PromptReco-v1/MINIAOD':["Muon0_Run2023BV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023C-PromptReco-v1/MINIAOD':["Muon0_Run2023CV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023C-PromptReco-v2/MINIAOD':["Muon0_Run2023CV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023C-PromptReco-v3/MINIAOD':["Muon0_Run2023CV3","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023C-PromptReco-v4/MINIAOD':["Muon0_Run2023CV4","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023D-PromptReco-v1/MINIAOD':["Muon0_Run2023DV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon0/Run2023D-PromptReco-v2/MINIAOD':["Muon0_Run2023DV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2023 Muon1
  '/Muon1/Run2023A-PromptReco-v2/MINIAOD':["Muon1_Run2023AV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023B-PromptReco-v1/MINIAOD':["Muon1_Run2023BV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023C-PromptReco-v1/MINIAOD':["Muon1_Run2023CV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023C-PromptReco-v2/MINIAOD':["Muon1_Run2023CV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023C-PromptReco-v3/MINIAOD':["Muon1_Run2023CV3","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023C-PromptReco-v4/MINIAOD':["Muon1_Run2023CV4","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023D-PromptReco-v1/MINIAOD':["Muon1_Run2023DV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/Muon1/Run2023D-PromptReco-v2/MINIAOD':["Muon1_Run2023DV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2024 Muon0
  '/Muon0/Run2024B-PromptReco-v1/MINIAOD':["Muon0_Run2024B","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  '/Muon0/Run2024C-PromptReco-v1/MINIAOD':["Muon0_Run2024C","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  '/Muon0/Run2024D-PromptReco-v1/MINIAOD':["Muon0_Run2024D","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_378981_380470_Golden.json","140X_dataRun3_Prompt_v2"],
  #2024 Muon1
  '/Muon1/Run2024B-PromptReco-v1/MINIAOD':["Muon1_Run2024B","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  '/Muon1/Run2024C-PromptReco-v1/MINIAOD':["Muon1_Run2024C","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  '/Muon1/Run2024D-PromptReco-v1/MINIAOD':["Muon1_Run2024D","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_378981_380470_Golden.json","140X_dataRun3_Prompt_v2"],
}

samples = {
  #2022
  '/JetMET/Run2022C-PromptReco-v1/MINIAOD':["JetMET0_Run2022CV1","Winter22Run3_RunC_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/JetMET/Run2022D-PromptReco-v1/MINIAOD':["JetMET0_Run2022DV1","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/JetMET/Run2022D-PromptReco-v2/MINIAOD':["JetMET0_Run2022DV2","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/JetMET/Run2022D-PromptReco-v3/MINIAOD':["JetMET0_Run2022DV3","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/JetMET/Run2022E-PromptReco-v1/MINIAOD':["JetMET0_Run2022EV1","Winter22Run3_RunD_V2_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/JetMET/Run2022F-PromptReco-v1/MINIAOD':["JetMET0_Run2022FV1","Summer22EEPrompt22_RunF_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  '/JetMET/Run2022G-PromptReco-v1/MINIAOD':["JetMET0_Run2022GV1","Summer22EEPrompt22_RunG_V1_DATA","Cert_Collisions2022_355100_362760_Golden.json","124X_dataRun3_Prompt_v4"],
  #2023 JetMET0
  '/JetMET0/Run2023A-PromptReco-v2/MINIAOD':["JetMET0_Run2023AV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023B-PromptReco-v1/MINIAOD':["JetMET0_Run2023BV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023C-PromptReco-v1/MINIAOD':["JetMET0_Run2023CV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023C-PromptReco-v2/MINIAOD':["JetMET0_Run2023CV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023C-PromptReco-v3/MINIAOD':["JetMET0_Run2023CV3","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023C-PromptReco-v4/MINIAOD':["JetMET0_Run2023CV4","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023D-PromptReco-v1/MINIAOD':["JetMET0_Run2023DV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2023D-PromptReco-v2/MINIAOD':["JetMET0_Run2023DV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2023 JetMET1
  '/JetMET1/Run2023A-PromptReco-v2/MINIAOD':["JetMET1_Run2023AV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023B-PromptReco-v1/MINIAOD':["JetMET1_Run2023BV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023C-PromptReco-v1/MINIAOD':["JetMET1_Run2023CV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023C-PromptReco-v2/MINIAOD':["JetMET1_Run2023CV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023C-PromptReco-v3/MINIAOD':["JetMET1_Run2023CV3","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023C-PromptReco-v4/MINIAOD':["JetMET1_Run2023CV4","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023D-PromptReco-v1/MINIAOD':["JetMET1_Run2023DV1","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2023D-PromptReco-v2/MINIAOD':["JetMET1_Run2023DV2","Winter23Prompt23_V2_MC","Cert_Collisions2023_366442_370790_Golden.json","130X_dataRun3_Prompt_v2"],
  #2024 JetMET0
  '/JetMET0/Run2024B-PromptReco-v1/MINIAOD':["JetMET0_Run2024B","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2024C-PromptReco-v1/MINIAOD':["JetMET0_Run2024C","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  '/JetMET0/Run2024D-PromptReco-v1/MINIAOD':["JetMET0_Run2024D","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_378981_380470_Golden.json","140X_dataRun3_Prompt_v2"],
  #2024 JetMET1
  '/JetMET1/Run2024B-PromptReco-v1/MINIAOD':["JetMET1_Run2024B","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraB_Golden.json","140X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2024C-PromptReco-v1/MINIAOD':["JetMET1_Run2024C","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_eraC_Golden.json","140X_dataRun3_Prompt_v2"],
  '/JetMET1/Run2024D-PromptReco-v1/MINIAOD':["JetMET1_Run2024D","Summer23BPixPrompt23_V1_MC","Cert_Collisions2024_378981_380470_Golden.json","140X_dataRun3_Prompt_v2"],
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
