import CRABClient
from CRABClient.UserUtilities import config

#sample_name = 'noPU_Run3Winter21_E2to500_take7'

#RAW_DSET = '/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Winter21DRMiniAOD-FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/GEN-SIM-DIGI-RAW'

config = config()

config.section_('General')
#config.General.requestName = 'jmeTriggerNTuple_'+sample_name
#config.General.requestName   = 'QCD_pT_15to7000_PU0to80_jmeTrigger_run3_2022'
config.General.requestName   = 'QCD_pT_15to7000_NoPU_jmeTrigger_run3_2022'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = 'jescJRA_cfg.py'
#config.JobType.pyCfgParams = ['output='+sample_name+'.root']
config.JobType.pyCfgParams = ['output=jmeTriggerNTuple.root']
config.JobType.maxMemoryMB = 2500
config.JobType.inputFiles    = ['PFHC_Run3Winter21_HLT_V3.db']
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'Automatic'
#config.Data.inputDataset = RAW_DSET
#config.Data.outLFNDirBase = '/store/user/saparede/hlt_runIII_jesc_oct/crab_out/'+sample_name
#config.Data.inputDataset = '/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Summer21DR-FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/GEN-SIM-DIGI-RAW'
config.Data.inputDataset = '/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/Run3Summer21DR-NoPUFEVT_castor_120X_mcRun3_2021_realistic_v6-v1/GEN-SIM-DIGI-RAW'
#config.Data.outLFNDirBase = '/store/user/chuh/jmeTrigger_2022/QCD_pT15_7000_PU0to80_run3_12_3_0_pre4'
config.Data.outLFNDirBase = '/store/user/chuh/jmeTrigger_2022/QCD_pT15_7000_NoPU_run3_12_3_0_pre4'
config.Data.unitsPerJob = 500
#config.Data.unitsPerJob = 2700
config.Data.totalUnits = -1

config.section_("Site")
config.Site.storageSite = 'T3_KR_KNU'
#config.section_('User')
