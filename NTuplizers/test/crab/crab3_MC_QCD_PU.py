import sys
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8'
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

config.Data.inputDataset = '/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter23MiniAOD-FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v2/MINIAODSIM'
config.Data.secondaryInputDataset = '/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter23Digi-FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v1/GEN-SIM-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1000
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/chuh/hlt_runIII_jesc_2023/validation'

config.Site.storageSite = 'T3_KR_KNU'

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
