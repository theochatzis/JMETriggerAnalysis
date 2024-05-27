import sys
from CRABClient.UserUtilities import config
config = config()

store_dir = 'samples2023'
sample_name = 'hf_before_muon'

input_file_dir = '/afs/cern.ch/work/t/tchatzis/private/run3_2024/2024_datataking/CMSSW_14_0_6_MULTIARCHS/src/JMETriggerAnalysis/NTuplizers/test'

config.General.requestName = 'hf_before_muon'
config.General.transferOutputs = True
config.General.transferLogs = True


config.JobType.allowUndistributedCMSSW = True
#config.JobType.maxJobRuntimeMin = 120 # minutes
#config.JobType.numCores = 8
#config.JobType.maxMemoryMB = 9000
config.JobType.psetName = input_file_dir+'jmeTriggerNTuple2023Data_miniAOD_cfg.py'
config.JobType.pluginName = 'Analysis'
#config.JobType.inputFiles = [input_file_dir+'PFCalibration.db',input_file_dir+'Run3Winter23Digi.db',input_file_dir+'Winter23Prompt23_RunA_V1_DATA.db']
config.Data.inputDataset = '/Muon0/Run2024D-PromptReco-v1/MINIAOD'
config.JobType.pyCfgParams = ['globalTag=140X_dataRun3_Prompt_v2','isMuonData=True']
#config.Data.secondaryInputDataset = '/JetMET1/Run2023C-v1/RAW'
config.Data.runRange = '380647-380648'
#config.Data.lumiMask = input_file_dir+'pickevents.json'
#config.Data.splitting = 'LumiBased'
#config.Data.unitsPerJob = 10
#config.Data.totalUnits = 1000
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 200
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/tchatzis/'+store_dir+'/'+sample_name
config.Data.publication = False

config.Site.storageSite = 'T3_CH_CERNBOX'

