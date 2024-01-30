from CRABClient.UserUtilities import config, getUsernameFromCRIC

#sample_name = 'QCD_EpsPUGTv6HCAL_126X_withForwardPFHCs'
sample_name = 'QCD_NoPU_133X'

#RAW_DSET = '/QCD_PT-15to7000_TuneCP5_Flat2022_13p6TeV_pythia8/Run3Winter23Digi-EpsPUGTv6HCAL_126X_mcRun3_2023_forPU65_v6_withHCALResCor_ext1-v2/GEN-SIM-RAW'
RAW_DSET = '/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter24Digi-NoPU_133X_mcRun3_2024_realistic_v9-v3/GEN-SIM-RAW'

config = config()

config.section_('General')
config.General.requestName = 'jmeTriggerNTuple_'+sample_name
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jescJRA_cfg.py'
config.JobType.inputFiles = []
config.JobType.pyCfgParams = ['output='+sample_name+'.root']
config.JobType.maxMemoryMB = 2500
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'Automatic'
config.Data.inputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/%s/nanopost/hlt_run3_JECs/%s'%(getUsernameFromCRIC(),sample_name)
config.Data.unitsPerJob = 200
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T3_CH_CERNBOX'
config.section_('User')
