from CRABClient.UserUtilities import config

sample_name = 'flatPU_Run3Summer120X_CMSSW_12_4_0_pre3'

RAW_DSET = '/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Summer21DR-FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/GEN-SIM-DIGI-RAW'

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
config.JobType.inputFiles = ['PFCalibration.db']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'Automatic'
config.Data.inputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/chuh/hlt_runIII_jesc_oct/crab_out/'+sample_name
config.Data.unitsPerJob = 2700
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T3_KR_KNU'
config.section_('User')
