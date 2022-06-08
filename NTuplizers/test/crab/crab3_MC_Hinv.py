import sys
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'VBF_HToInvisible_M125_TuneCUETP8M1_14TeV_powheg_pythia8'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 300
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 9000
config.JobType.psetName = '/afs/cern.ch/work/p/pdas/JMETrigger/run3/test/CMSSW_12_3_0_pre6/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = ['PFHC_Run3Winter21_HLT_V3.db','JESC_Run3Winter21_V2_MC.db']
config.JobType.outputFiles = ['out.root']

config.Data.inputDataset = '/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Summer21MiniAOD-120X_mcRun3_2021_realistic_v5-v2/MINIAODSIM'
config.Data.secondaryInputDataset = '/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Summer21DRPremix-120X_mcRun3_2021_realistic_v6-v2/GEN-SIM-DIGI-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1000
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/group/phys_jetmet/pdas'

config.Site.storageSite = 'T2_CH_CERN'

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

