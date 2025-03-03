import sys
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 300
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 9000
config.JobType.psetName = '/afs/cern.ch/work/c/chuh/JESC/CMSSW_13_0_0/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = ['PFCalibration.db','Run3Winter23Digi.db']
config.JobType.outputFiles = ['out.root']

config.Data.inputDataset = '/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Winter23MiniAOD-126X_mcRun3_2023_forPU65_v1-v2/MINIAODSIM'
config.Data.secondaryInputDataset = '/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/Run3Winter23Digi-126X_mcRun3_2023_forPU65_v1-v2/GEN-SIM-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 500
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/chuh/hlt_runIII_jesc_2023/validation'

config.Site.storageSite = 'T3_KR_KNU'

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
