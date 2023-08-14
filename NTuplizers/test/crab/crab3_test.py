import sys
from CRABClient.UserUtilities import config
config = config()

store_dir = 'samples2023'
sample_name = 'data_withBPix_fixOption5'

input_file_dir = '/afs/cern.ch/work/t/tchatzis/private/run3_2023/CMSSW_13_0_7_patch1/src/JMETriggerAnalysis/NTuplizers/test/'

config.General.requestName = sample_name
config.General.transferOutputs = True
config.General.transferLogs = True


config.JobType.allowUndistributedCMSSW = True
#config.JobType.maxJobRuntimeMin = 300 # minutes
#config.JobType.numCores = 8
#config.JobType.maxMemoryMB = 9000
config.JobType.psetName = input_file_dir+'jmeTriggerNTuple2023Data_compare_cfg.py'
config.JobType.pluginName = 'Analysis'
#config.JobType.inputFiles = [input_file_dir+'PFCalibration.db',input_file_dir+'Run3Winter23Digi.db',input_file_dir+'Winter23Prompt23_RunA_V1_DATA.db']
#config.Data.inputDataset = '/Muon0/Run2023C-PromptReco-v4/MINIAOD'
#config.Data.secondaryInputDataset = '/Muon0/Run2023C-v1/RAW'
config.Data.inputDataset = '/Muon0/Run2023D-PromptReco-v1/MINIAOD'
config.Data.secondaryInputDataset = '/Muon0/Run2023D-v1/RAW'
#config.Data.runRange = '367765-999999'
#config.Data.lumiMask = input_file_dir+'pickevents.json'
config.Data.splitting = 'Automatic'
#config.Data.unitsPerJob = 10
#config.Data.totalUnits = 1000
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.unitsPerJob = 50000
config.Data.totalUnits = 10000000
config.Data.outLFNDirBase = '/store/user/tchatzis/'+store_dir+'/'+sample_name
config.Data.publication = False

config.Site.storageSite = 'T3_CH_CERNBOX'

