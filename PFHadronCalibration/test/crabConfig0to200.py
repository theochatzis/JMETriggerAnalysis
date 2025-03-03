import CRABClient
from CRABClient.UserUtilities import config

config = config()

config.section_("General")
config.General.requestName   = 'SinglePion_E_2to200_PFHadCalib_run3_2023'
#config.General.requestName   = 'SinglePion_E_200to500_PFHadCalib_run3_2023'
config.General.transferLogs = False
config.General.workArea = 'SinglePion'

config.section_("JobType")
config.JobType.pluginName  = 'Analysis'
# Name of the CMSSW configuration file
config.JobType.psetName    = 'pfHadCalibNTuple_cfg.py'
config.JobType.outputFiles = ['pfHCNTuple.root']
#config.JobType.numCores = 4
#config.JobType.inputFiles    = ['/d3/scratch/cghuh3811/CMSSW_9_2_14/src/PFHCalib/PFHadHLT/python/HLT_BX25_Feb17_MC.db']
#config.JobType.inputFiles    = ['/afs/cern.ch/work/m/missirol/public/phase2/JESC/PhaseIIFall17_V5b_MC.db']
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxMemoryMB = 2000

config.section_("Data")
# This string determines the primary dataset of the newly-produced outputs.
# For instance, this dataset will be named /CrabTestSingleMu/something/USER
#config.Data.inputDataset = ''
config.Data.inputDataset = '/SinglePionGun_E0p2to200/Run3Winter23Digi-NoPUGTv4_126X_mcRun3_2023_forPU65_v4-v2/GEN-SIM-RAW'
#config.Data.inputDataset = '/SinglePionGun_E200to500/Run3Winter23Digi-NoPUGTv4_126X_mcRun3_2023_forPU65_v4-v2/GEN-SIM-RAW'
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 180
config.Data.totalUnits = -1
#config.Data.splitting = 'FileBased'
#config.Data.unitsPerJob = 500
#config.Data.totalUnits = 6429
config.Data.publication = False
#config.Data.allowNonValidInputDataset = True

config.Data.outLFNDirBase = '/store/user/chuh/PFHadCalib_2023/SinglePionE_2_200_v6_run3_13_0_0'
#config.Data.outLFNDirBase = '/store/user/chuh/PFHadCalib_2023/SinglePionE_200_500_run3_v6_13_0_0'
#config.Data.useParent = True
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Cert_271036-284044_13TeV_PromptReco_Collisions16_JSON_NoL1T.txt'

# This string is used to construct the output dataset name
#config.Data.publishDataName = 'CRAB3-tutorial'

#config.Data.publication = True
#config.Data.publishDBS = 'phys03'
#config.Data.outputDatasetTag = 'SingleMuon_Run2016H_theNEWjec'

config.section_("Site")
#config.Site.whitelist = ['T2_CH_CERN']
config.Site.storageSite = 'T3_KR_KNU'
#config.Site.blacklist = ['T1_US_FNAL','T2_UK_London_Brunel']
