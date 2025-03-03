from CRABClient.UserUtilities import config
config = config()

# inDS = '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIISummer19UL18RECO-NoPU_106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM'
inDS = '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIISummer19UL18RECO-FlatPU0to70_106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM'
# inDS = '/QCD_Pt-15to7000_TuneCP5_Flat_13TeV_pythia8/RunIISummer19UL18RECO-EpsilonPU_pilot_106X_upgrade2018_realistic_v11_L1v1-v2/AODSIM'
requestName = 'JetMETAnalysis_2018UL_FlatPU0to70'
FILESPERJOB = 1
PUBLISHDATANAME = '20200608'

########

config.General.requestName = requestName

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'run_JRA_cfg.py'
# config.JobType.allowUndistributedCMSSW = True
#config.JobType.inputFiles = ['']

config.section_("Data")
config.Data.inputDataset = inDS
config.General.requestName = config.Data.inputDataset.split('/')[2]
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

# config.Data.splitting = 'FileBased'
# config.Data.unitsPerJob = FILESPERJOB
config.Data.publication = True
config.Data.outputDatasetTag = config.General.requestName + '_' + PUBLISHDATANAME
# config.Data.ignoreLocality = True

config.Data.outLFNDirBase = '/store/user/clange/'
config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
