from CRABClient.UserUtilities import config

sample_name = 'flatPU_Run3126X_CMSSW_13_0_0'

RAW_DSET = '/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter23Digi-FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v1/GEN-SIM-RAW'

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
config.Data.outLFNDirBase = '/store/user/chuh/hlt_runIII_jesc_2023/crab_out/'+sample_name
config.Data.unitsPerJob = 500
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T3_KR_KNU'
config.section_('User')
