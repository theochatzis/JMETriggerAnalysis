import sys
from CRABClient.UserUtilities import config
config = config()

store_dir = 'testCRAB'
sample_name = 'QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8'

input_file_dir = '/afs/cern.ch/work/t/tchatzis/private/run3puppi_test_new/testTrk/CMSSW_12_4_12/src/JMETriggerAnalysis/NTuplizers/test/'

config.General.requestName = 'QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8_test2'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 120 # minutes
config.JobType.psetName = input_file_dir+'jmeTriggerNTuple_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = [input_file_dir+'PFHC_Run3Summer21_MC.db',input_file_dir+'JESC_Run3Summer21_MC.db',input_file_dir+'puppiJECs.db']

config.Data.inputDataset = '/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/Run3Summer22MiniAODv3-FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/MINIAODSIM'
config.Data.secondaryInputDataset = '/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/Run3Summer22DR-FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/GEN-SIM-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 10
config.Data.totalUnits = 1000
config.Data.outLFNDirBase = '/store/user/tchatzis/'+store_dir+'/'+sample_name
config.Data.publication = False

config.Site.storageSite = 'T3_CH_CERNBOX'

