import sys
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 300
config.JobType.maxMemoryMB = 2000
config.JobType.psetName = '/afs/cern.ch/work/p/pdas/JMETrigger/run3/test/CMSSW_11_2_0_Patatrack/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = ['PFHC_Run3Winter20_HLT_v01.db','JESC_Run3Winter20_V2_MC.db']
config.JobType.outputFiles = ['out.root']

config.Data.inputDataset = '/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/MINIAODSIM'
config.Data.secondaryInputDataset = '/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2000
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/pdas/'

config.Site.storageSite = 'T2_US_Wisconsin'