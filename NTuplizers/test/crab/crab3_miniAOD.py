import sys
from CRABClient.UserUtilities import config
config = config()

store_dir = 'CoffteaNTuples'
sample_name = 'Muon0_Run2023Cv1'

input_file_dir = '/afs/cern.ch/work/t/tchatzis/private/run3_2023/CMSSW_13_0_7_patch1/src/JMETriggerAnalysis/NTuplizers/test/'

config.section_('General')
config.General.requestName = sample_name
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 2500
config.JobType.psetName = input_file_dir+'jmeTriggerNTuple2023Data_miniAOD_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.inputDataset = '/Muon0/Run2023C-PromptReco-v1/MINIAOD'
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 200
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/tchatzis/'+store_dir+'/'+sample_name

config.section_('Site')
config.Site.storageSite = 'T3_CH_CERNBOX'

