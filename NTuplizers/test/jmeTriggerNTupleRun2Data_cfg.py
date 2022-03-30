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
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_3_0_GRun_data_configDump import cms, process
  update_jmeCalibs = False

elif opts.reco == 'HLT_Run3TRK':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_3_0_GRun_data_configDump import cms, process
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
from JMETriggerAnalysis.Common.customise_hlt import *
#process = addPaths_MC_JMECalo(process)
#process = addPaths_MC_JMEPFCluster(process)
#process = addPaths_MC_JMEPF(process)
#process = addPaths_MC_JMEPFCHS(process)
#process = addPaths_MC_JMEPFPuppi(process)

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:PFHC_Run3Winter21_HLT_V3.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_CMSSW_12_0_1_HLT_120X_mcRun3_2021'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:JESC_Run3Winter21_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

else:
  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:JESC_Run3Winter21_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter21_V2_MC_AK8PFPuppiHLT'),
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
process.schedule.append(process.analysisNTupleEndPath)

###
### updating Phase 0 HCAL thresholds
###

#process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].name = "PFRecHitQTestHCALThresholdVsDepth"
#del process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].threshold

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
    '/store/data/Run2018D/SingleMuon/MINIAOD/12Nov2019_UL2018-v8/270001/0E6F8912-55C4-0B49-A023-B114E200F5E8.root'
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/10668FAD-FE9F-E811-8A1B-FA163EF83AB3.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/3C9E348F-FF9F-E811-A251-FA163E4284DE.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/62EF0CA4-FF9F-E811-A45A-FA163E9B865E.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/6684A9AB-FE9F-E811-82EF-FA163EB0AAB0.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/6A1F12E0-FE9F-E811-A2A3-FA163E88D3BA.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/A296BFC3-FF9F-E811-9E38-FA163E97E87F.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/A85697F8-FF9F-E811-AB11-02163E0164E8.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/B877DB56-FF9F-E811-8D15-FA163E9C4E08.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/295/00000/D0C9A0B3-FF9F-E811-B5FF-FA163ED190E5.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/0670C1C1-9CAC-E811-BBA6-FA163EAFB047.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/24AB5EF3-9CAC-E811-AA5F-FA163E4642C6.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/2622C333-9DAC-E811-BDBA-FA163EBA050E.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/6CC0EDCA-9CAC-E811-B946-FA163E29D9CB.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/96D45A06-9DAC-E811-B3CE-FA163E6B94A5.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/D6850F33-9DAC-E811-BAE4-02163E013A10.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/E4196842-9DAC-E811-976A-FA163E92858C.root',
    '/store/data/Run2018D/SingleMuon/RAW/v1/000/321/975/00000/F0B48CB7-9DAC-E811-94B9-02163E00AF22.root',
  ]

#process.source.eventsToProcess = cms.untracked.VEventRange("325057:61751881")

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
