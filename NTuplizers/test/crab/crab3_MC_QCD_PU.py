import sys
from CRABClient.UserUtilities import config
config = config()

#config.General.workArea = 'OldJEC_Run3TRK_test'
config.General.requestName = 'QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 300
config.JobType.maxMemoryMB = 2000
config.JobType.psetName = '/afs/cern.ch/work/p/pdas/JMETrigger/run3/test/CMSSW_12_2_0_pre2/src/JMETriggerAnalysis/NTuplizers/test/jmeTriggerNTuple_cfg.py'
config.JobType.pluginName = 'Analysis'
config.JobType.inputFiles = ['PFHC_Run3Winter21_HLT_V3.db','JESC_Run3Winter21_V2_MC.db']
config.JobType.outputFiles = ['out.root']

config.Data.inputDataset = '/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Winter21DRMiniAOD-FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/MINIAODSIM'
config.Data.secondaryInputDataset = '/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Winter21DRMiniAOD-FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/GEN-SIM-DIGI-RAW'
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2000
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/group/phys_jetmet/pdas'

config.Site.storageSite = 'T2_CH_CERN'
config.Site.blacklist = ['T2_US_Purdue']

config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
