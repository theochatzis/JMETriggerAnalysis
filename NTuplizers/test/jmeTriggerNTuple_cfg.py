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
if opts.reco == 'HLT_GRun_oldJECs':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_GRun_V6_configDump import cms, process
  update_jmeCalibs = False

elif opts.reco == 'HLT_GRun':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_GRun_V6_configDump import cms, process
  update_jmeCalibs = True

elif opts.reco == 'HLT_Run3TRK':
  # (a) Run-3 tracking: standard
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_GRun_V6_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTforRun3Tracking import customizeHLTforRun3Tracking
  process = customizeHLTforRun3Tracking(process)
  update_jmeCalibs = True

elif opts.reco == 'HLT_Run3TRKWithPU':
  # (b) Run-3 tracking: all pixel vertices
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_0_0_GRun_V6_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTforRun3Tracking import customizeHLTforRun3TrackingAllPixelVertices
  process = customizeHLTforRun3TrackingAllPixelVertices(process)
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
from JMETriggerAnalysis.Common.customise_hlt import *
process = addPaths_MC_JMECalo(process)
process = addPaths_MC_JMEPFCluster(process)
process = addPaths_MC_JMEPF(process)
process = addPaths_MC_JMEPFCHS(process)
process = addPaths_MC_JMEPFPuppi(process)

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/PFHC_Run3Winter20_HLT_v01.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_HLT_mcRun3_2021'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

else:
  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

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

    hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
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
#process.HLTSchedule.extend([process.analysisNTupleEndPath])

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
process.options.numberOfThreads = max(opts.numThreads, 1)
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
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/MINIAODSIM/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/6301c6f9-4a1e-4f02-b347-24e1b4fffc4d.root',
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/05c52296-cc48-4c07-8444-ed00163e44de.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/3ff8e3ec-96fa-473f-983f-9ee459e86d78.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/542f0211-dfc1-4e89-ac84-47c52688bbfa.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/5d27fe9e-5b60-4ea0-8d1b-44e89ddfe507.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/7521d027-4025-49b7-b1ca-889bf218cf1b.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/758a7152-f8a2-4b75-a9af-d4ede7652055.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/775ea69b-f775-4770-9296-9bdae1be2071.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/7c66868f-b11d-4370-b41c-fe7390c3d2ec.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/7edfc0d5-ac5c-438d-bdaa-aa29351c0e65.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/820593bf-73ef-4b4c-98fd-6a895e630b5c.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/84b3d55b-15d0-4308-8791-cb66b7dafd98.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/8536e1ab-486c-460d-b011-fab6170d8698.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/95b2308c-c711-4671-a615-7f476d1c1779.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/96e4753e-b7c6-4719-88b6-587746e174fd.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/9d5387b6-95aa-4bf9-875a-448980a9498a.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/9e485a22-d50f-464f-9970-88ce46e54304.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/afece741-d685-4b27-9bb2-3c36fd080a78.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/b1954d9b-4bc4-4a2b-9e71-69dca2b9a2cc.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/b874a551-b3d9-4e0a-9d15-95e3d645b66e.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/c42288ef-9559-473a-bd36-c3179f05b672.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/d63f6e2b-fd37-4cc2-8eaa-73af44940543.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/d97540c2-5633-47c8-93f8-4abddc7b2161.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/dcfea6cc-a311-41a9-90ea-50059d38a4af.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/df2087cf-4c88-4fca-a355-f6f31296be6b.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/e2e1b9c5-c17b-4336-b1b6-114c1546cc21.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/e453b174-aeb0-467b-a48f-318c24284e05.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/ebaa9a01-c262-4d42-a9e0-48fe38ca2c49.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/f1583bdd-59bb-4e1c-be6d-d3be494d92dc.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/f9a009e7-ec07-4b88-bb34-4a16d85ab686.root',
    '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/280000/fce25a40-c545-43a0-bc7c-66e67a501b62.root',
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
