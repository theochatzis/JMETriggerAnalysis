from WMCore.Configuration import Configuration

sample_name = 'submit_test_flatPU_runIII'

#
RAW_DSET = '/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-FlatPU0to80_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW'

config = Configuration()

config.section_('General')
config.General.requestName = 'jmeTriggerNTuple_'+sample_name
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jescJRA_cfg.py'
config.JobType.pyCfgParams = ['output='+sample_name+'.root','maxEvents=100000']
config.JobType.maxJobRuntimeMin = 2480
config.JobType.maxMemoryMB = 2000
#config.JobType.inputFiles = ['/afs/cern.ch/user/t/tomei/public/L1TObjScaling.db']
config.JobType.inputFiles = []
config.JobType.allowUndistributedCMSSW = True
#config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'EventAwareLumiBased'
# SPS don't need secondary dataset I think? 
#config.Data.inputDataset = MIN_DSET
#config.Data.secondaryInputDataset = RAW_DSET
config.Data.inputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/saparede/hlt_runIII_jec_v1/crab_out/'+sample_name
config.Data.unitsPerJob = 100
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T2_BE_IIHE'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')
