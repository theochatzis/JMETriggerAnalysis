from CRABClient.UserUtilities import config

sample_name = 'noPU_runIII_autoWInFile_take5'

RAW_DSET = '/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/Run3Winter20DRMiniAOD-NoPU_110X_mcRun3_2021_realistic_v6_ext1-v1/GEN-SIM-RAW'

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
#config.JobType.maxJobRuntimeMin = 2480
config.JobType.maxMemoryMB = 4000
#config.JobType.inputFiles = ['/afs/cern.ch/user/t/tomei/public/L1TObjScaling.db']
config.JobType.inputFiles = ['PFHC_Run3Winter20_HLT_v01.db']
#config.JobType.inputFiles = []
config.JobType.allowUndistributedCMSSW = True
#config.JobType.numCores = 4

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'Automatic'
# SPS don't need secondary dataset I think? 
#config.Data.inputDataset = MIN_DSET
#config.Data.secondaryInputDataset = RAW_DSET
config.Data.inputDataset = RAW_DSET
config.Data.outLFNDirBase = '/store/user/saparede/hlt_runIII_jec_v1/crab_out/'+sample_name
config.Data.unitsPerJob = 2700
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T2_BE_IIHE'
if config.Data.ignoreLocality:
   config.Site.whitelist = ['T2_CH_CERN', 'T2_DE_*']

config.section_('User')

