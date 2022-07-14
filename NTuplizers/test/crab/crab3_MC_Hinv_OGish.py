import sys
from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'VBF_HToInvisible_OGsetup_lessMemlessTime'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 200
config.JobType.numCores = 8
config.JobType.maxMemoryMB = 8000
config.JobType.psetName = '/afs/cern.ch/work/s/saparede/private/jet_stuff/hlt_runIII_jescs_jul22/CMSSW_12_4_0_pre3/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = ['PFCalibration.db','Run3Summer21_MC.db']
config.JobType.outputFiles = ['out.root']

config.Data.inputDataset = '/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Summer21MiniAOD-120X_mcRun3_2021_realistic_v5-v2/MINIAODSIM'
config.Data.secondaryInputDataset = '/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/Run3Summer21DRPremix-120X_mcRun3_2021_realistic_v6-v2/GEN-SIM-DIGI-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2000
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/group/phys_jetmet/saparede/runIII_hlt_jec/validation'

config.Site.storageSite = 'T2_CH_CERN'

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']

