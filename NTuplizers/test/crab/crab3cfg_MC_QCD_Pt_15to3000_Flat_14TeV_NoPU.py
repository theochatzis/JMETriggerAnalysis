from WMCore.Configuration import Configuration

store_dir = 'jme_trigger/jmeTriggerNtuples/Phase2/trackingV2/v04/191229'
sample_name = 'QCD_Pt_15to3000_Flat_14TeV_NoPU'

MIN_DSET = '/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/PhaseIITDRSpring19MiniAOD-NoPU_castor_106X_upgrade2023_realistic_v3-v2/MINIAODSIM'
RAW_DSET = '/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/PhaseIITDRSpring19DR-NoPU_castor_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW'

config = Configuration()

config.section_('General')
config.General.requestName = 'jmeTriggerNTuple_'+sample_name
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jmeTriggerNTuple_cfg.py'
config.JobType.inputFiles = []
config.JobType.pyCfgParams = ['output='+sample_name+'.root']
config.JobType.maxJobRuntimeMin = 2880
config.JobType.maxMemoryMB = 4000
#config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = True
config.Data.splitting = 'EventAwareLumiBased'
config.Data.inputDataset = MIN_DSET
config.Data.secondaryInputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/missirol/'+store_dir+'/'+sample_name
config.Data.unitsPerJob = 100
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T2_DE_DESY'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')
