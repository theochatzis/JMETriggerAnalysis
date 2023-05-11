import os
import fnmatch

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB

###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

#opts.register('globalTag', None,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.string,
#              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_Run3TRK',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('keepPFPuppi', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'keep full collection of PFlow and PFPuppi candidates')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

#opts.register('printSummaries', False,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.bool,
#              'show summaries from HLT services')

opts.parseArguments()

###
### HLT configuration
###
if opts.reco == 'HLT_oldJECs':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_4_0_GRun_postEE_configDump import cms, process
  update_jmeCalibs = False

elif opts.reco == 'HLT_Run3TRK':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_4_0_GRun_postEE_configDump import cms, process
#  from HLTrigger.Configuration.customizeHLTforRun3 import customizeHLTforRun3Tracking
#  process = customizeHLTforRun3Tracking(process)
  update_jmeCalibs = True

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print('> removed cms.OutputModule:', _modname)

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print('> removed cms.EndPath:', _modname)

# remove selected cms.Path objects from HLT config-dump
print('-'*108)
print('{:<99} | {:<4} |'.format('cms.Path', 'keep'))
print('-'*108)

# list of patterns to determine paths to keep
keepPaths = [
  'MC_*Jets*',
  'MC_*MET*',
  'MC_*AK8Calo*',
  'HLT_PFJet*_v*',
  'HLT_AK4PFJet*_v*',
  'HLT_AK8PFJet*_v*',
  'HLT_PFHT*_v*',
  'HLT_PFMET*_PFMHT*_v*',
]

vetoPaths = [
  'HLT_*ForPPRef_v*',
]

# list of paths that are kept
listOfPaths = []

for _modname in sorted(process.paths_()):
    _keepPath = False
    for _tmpPatt in keepPaths:
      _keepPath = fnmatch.fnmatch(_modname, _tmpPatt)
      if _keepPath: break

    if _keepPath:
      for _tmpPatt in vetoPaths:
        if fnmatch.fnmatch(_modname, _tmpPatt):
          _keepPath = False
          break

    if _keepPath:
      print('{:<99} | {:<4} |'.format(_modname, '+'))
      listOfPaths.append(_modname)
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print('{:<99} | {:<4} |'.format(_modname, ''))
print('-'*108)

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

# remove MessageLogger
if hasattr(process, 'MessageLogger'):
  del process.MessageLogger

###
### customisations
###

## customised JME collections
# from JMETriggerAnalysis.Common.customise_hlt import *
# process = addPaths_MC_JMECalo(process)
# process = addPaths_MC_JMEPFCluster(process)
# process = addPaths_MC_JMEPF(process)
# process = addPaths_MC_JMEPFCHS(process)
# process = addPaths_MC_JMEPFPuppi(process)

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:PFHC_Run3Summer21_MC.db'),
    

    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_CMSSW_12_4_0_pre3_HLT_112X_mcRun3_2022'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:JESC_Run3Summer21_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFchsHLT'),
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFchsHLT'),
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

else:
  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:JESC_Run3Summer21_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFchsHLT'),
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFcshHLT'),
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

# ## ECAL UL calibrations
# process.GlobalTag.toGet = cms.VPSet(
#  cms.PSet(record = cms.string("EcalLaserAlphasRcd"),
#  tag = cms.string("EcalLaserAlphas_UL_Run1_Run2_2018_lastIOV_movedTo1"),
#  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
#  ),
#  cms.PSet(record = cms.string("EcalIntercalibConstantsRcd"),
#  tag = cms.string("EcalIntercalibConstants_UL_Run1_Run2_2018_lastIOV_movedTo1"),
#  connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
#  ),)

## Output NTuple
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',
  TTreeName = cms.string('Events'),
  TriggerResults = cms.InputTag('TriggerResults'),
  TriggerResultsFilterOR = cms.vstring(),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(
    sorted(list(set([(_tmp[:_tmp.rfind('_v')] if '_v' in _tmp else _tmp) for _tmp in listOfPaths])))
  ),
  outputBranchesToBeDropped = cms.vstring(),

  HepMCProduct = cms.InputTag('generatorSmeared'),
  GenEventInfoProduct = cms.InputTag('generator'),
  PileupSummaryInfo = cms.InputTag('addPileupInfo'),

  doubles = cms.PSet(

    hltFixedGridRhoFastjetAllCalo = cms.InputTag('hltFixedGridRhoFastjetAllCalo'),
    hltFixedGridRhoFastjetAllPFCluster = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    hltFixedGridRhoFastjetAll = cms.InputTag('hltFixedGridRhoFastjetAll'),
    offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPF = cms.InputTag('hltVerticesPF'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
    hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

    hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
    hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

    #hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    #hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    #hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    #hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    #hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    #hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    #hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    #hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(

    hltCaloMET = cms.InputTag('hltMet'),
    hltCaloMETTypeOne = cms.InputTag('hltCaloMETTypeOne'),
  ),

  recoPFClusterMETCollections = cms.PSet(

    hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
    hltPFClusterMETTypeOne = cms.InputTag('hltPFClusterMETTypeOne'),
  ),

  recoPFMETCollections = cms.PSet(

    hltPFMET = cms.InputTag('hltPFMETProducer'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),

    hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    hltPFCHSMETTypeOne = cms.InputTag('hltPFCHSMETTypeOne'),

    hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
    hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),
)

if opts.keepPFPuppi:
  process.hltPFPuppi.puppiDiagnostics = True
  process.JMETriggerNTuple.vdoubles = cms.PSet(
    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms'),
  )
  process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet(
    hltParticleFlow = cms.InputTag('hltParticleFlow'),
    hltPFPuppi = cms.InputTag('hltPFPuppi'),
  )

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.append(process.analysisNTupleEndPath)

###
### updating Phase 0 HCAL thresholds
###

# process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].name = "PFRecHitQTestHCALThresholdVsDepth"
# del process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].threshold

#if opts.printSummaries:
#   process.FastTimerService.printEventSummary = False
#   process.FastTimerService.printRunSummary = False
#   process.FastTimerService.printJobSummary = True
#   process.ThroughputService.printEventSummary = False

###
### standard options
###

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 8)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

## update process.GlobalTag.globaltag
#if opts.globalTag is not None:
#   from Configuration.AlCa.GlobalTag import GlobalTag
#   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
  '/store/mc/Run3Summer22MiniAODv3/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/0345b123-6141-4707-8f96-d17170654938.root'
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/11962fa4-129d-4ad0-8bc8-8ffb631fb034.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/1bcabf5d-ec1c-46f4-88cd-746bb14a05b5.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/29c2f2f6-61ad-4e1b-8ecc-021a0d02a86e.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/2c4aabb4-423b-4c61-b1b6-64f47d1b5711.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/46131606-30ec-4229-90d9-67504a5e7bbf.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/4a5f31d3-a0e6-4c15-b1c8-93a2002fa94d.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/4def2ecd-261a-4afc-9e8e-cc6ca17206c7.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/81bdc368-2f48-4d58-b4a0-2c1970028417.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/8eb28a05-dcc7-47eb-837b-a88bb26fa2a9.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/980e3228-116c-4e1e-817c-998fef4c36de.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/9cbdda6f-a994-43ea-8e98-0e7b75ed3e96.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/9f2a9e0f-ac30-4b14-bf71-1334b86323f7.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/bad149a7-b885-4e8b-95f2-4fd6a292d9ef.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/c5208e50-10ce-471b-891a-a005a0a23af9.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/c5a5a118-ae74-4139-9566-5f454b320b37.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/c8997caa-88a2-4493-87ef-e31897cba3db.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/02866b1a-22c5-43e9-a5c1-5ac174227dab.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/083de72f-375a-4310-b286-6d072ed29199.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/099d5c8f-f23c-4a3a-ba79-0d2bbd92e089.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/1d9ad32b-a287-4f26-8e28-0c5d1fa9bd7a.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/2b3c2453-26b8-4460-96f9-0193579e37ac.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/4b653df4-7ca0-4a0b-8727-4eec4543e8da.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/553d86c8-0e45-4e24-b7e6-91add3cd9a35.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/5b552d2a-1479-41b7-be0e-f6680984a593.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/78bc9f4a-8e86-4175-966b-2d19754635a2.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/827278d4-7841-4bfb-bbda-b75866a76a6e.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/8df29cee-0bfa-4cc8-87d3-f8dbe1fbc718.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/b7c9d294-d936-464e-9c22-26f665fa9d0d.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/baa9f5da-98a4-4c3a-bd54-8e4b085e2252.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/cb95288a-1f37-42ea-977b-33a71832184e.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/d132cd0c-465e-40db-be91-8dd34726ce24.root',
    '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810003/e6c0bddb-63d1-43d6-a094-148a1769b211.root',
  ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# printouts
if opts.verbosity > 0:
   print('--- jmeTriggerNTuple_cfg.py ---')
   print('')
   print('option: output =', opts.output)
   print('option: reco =', opts.reco)
   print('option: dumpPython =', opts.dumpPython)
   print('')
   print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('-------------------------------')
