from WMCore.Configuration import Configuration

store_dir = 'Phase2_JECS'
sample_name = 'QCD_Pt_15to3000_Flat_14TeV_PU200'

#MIN_DSET = '/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/PhaseIITDRSpring19MiniAOD-PU200_castor_106X_upgrade2023_realistic_v3-v2/MINIAODSIM'
#RAW_DSET = '/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/PhaseIITDRSpring19DR-PU200_castor_106X_upgrade2023_realistic_v3-v2/GEN-SIM-DIGI-RAW'
MIN_DSET = '/QCD_Pt-15To3000_TuneCP5_Flat_14TeV-pythia8/PhaseIISpring22DRMiniAOD-PU200_castor_123X_mcRun4_realistic_v11-v1/GEN-SIM-DIGI-RAW-MINIAOD'

config = Configuration()

config.section_('General')
config.General.requestName = 'JRA_'+sample_name
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jescJRA_cfg.py'
config.JobType.inputFiles = []
config.JobType.pyCfgParams = ['output='+sample_name+'.root']
config.JobType.maxJobRuntimeMin = 2700
#config.JobType.maxMemoryMB = 2000
#config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'EventAwareLumiBased'
config.Data.inputDataset = MIN_DSET
#config.Data.secondaryInputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/tchatzis/'+store_dir+'/'+sample_name
config.Data.unitsPerJob = 50
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T3_CH_CERNBOX'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')
