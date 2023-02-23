import os
import fnmatch

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB

###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

# options to control puppi tuning at different regions
opts.register('puppiParamsHB',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HB region given as [parameter_name]:[parameter_scale] ')

opts.register('puppiParamsHE1',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HE1 region given as [parameter_name]:[parameter_scale] ')

opts.register('puppiParamsHE2',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HE2 region given as [parameter_name]:[parameter_scale] ')

opts.register('puppiParamsHF',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HF region given as [parameter_name]:[parameter_scale] ')

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

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_Run3TRK',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('keepPFPuppi', True,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'keep full collection of PFlow and PFPuppi candidates')
opts.register('useMixedTrk',False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'use  full + pixel tracks in PF')
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
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_4_0_GRun_configDump import cms, process
  update_jmeCalibs = False

elif opts.reco == 'HLT_Run3TRK':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_4_0_GRun_configDump import cms, process
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
  'AlCa_*'
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
#if hasattr(process, 'MessageLogger'):
#  del process.MessageLogger

###
### customisations
###

## customised JME collections
from JMETriggerAnalysis.Common.customise_hlt import *
process = addPaths_MC_JMECalo(process)
process = addPaths_MC_JMEPFCluster(process)
process = addPaths_MC_JMEPF(process)
process = addPaths_MC_JMEPFCHS(process)
#process = addPaths_MC_JMEPFPuppi(process)

puppi_modifications_list = []
for param_change in opts.puppiParamsHB:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HB',parameter_name, parameter_scale])

for param_change in opts.puppiParamsHE1:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HE1',parameter_name, parameter_scale]) 

for param_change in opts.puppiParamsHE2:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HE2',parameter_name, parameter_scale])

for param_change in opts.puppiParamsHF:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HF',parameter_name, parameter_scale])

process = addPaths_MC_JMEPFPuppi(process, puppi_modifications_list)


if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    #_CondDB.clone(connect = 'sqlite_file:PFHC_Run3Winter21_HLT_V3.db'),
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/PFHC_Run3Summer21_MC.db'),
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
    #_CondDB.clone(connect = 'sqlite_file:JESC_Run3Winter21_V2_MC.db'),
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/JESC_Run3Summer21_MC.db'),
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
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      #cms.PSet(
      #  record = cms.string('JetCorrectionsRecord'),
      #  tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFPuppiHLT'),
      #  label = cms.untracked.string('AK4PFPuppiHLT'),
      #),
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
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK8PFHLT'),#!!
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

  # -- adding fast puppi jecs separately
  
  process.puppijescESSource = cms.ESSource('PoolDBESSource', # Nominal, Offline, FixedDist
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/JESCorrections/test/jescs_tuneV1/DBfile/Run3Summer21_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Summer21_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
    ),
  )
  process.puppijescESPrefer = cms.ESPrefer('PoolDBESSource', 'puppijescESSource')
  
else:
  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter21_V2_MC.db'),
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

## ECAL UL calibrations
process.GlobalTag.toGet = cms.VPSet(
 cms.PSet(record = cms.string("EcalLaserAlphasRcd"),
 tag = cms.string("EcalLaserAlphas_UL_Run1_Run2_2018_lastIOV_movedTo1"),
 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
 ),
 cms.PSet(record = cms.string("EcalIntercalibConstantsRcd"),
 tag = cms.string("EcalIntercalibConstants_UL_Run1_Run2_2018_lastIOV_movedTo1"),
 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
 ),)

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
    #offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
    
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    hltVerticesPF = cms.InputTag('hltVerticesPF'),
    #offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    #hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    #hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    #hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    #hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    #hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
    #hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

    #hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
    #hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
  ),

  recoPFJetCollections = cms.PSet(

    #hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

    #hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    #hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    #hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    #hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    #hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    #hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    #hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    #hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    #hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
  ),

  patJetCollections = cms.PSet(

    #offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    #offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    #offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(

    #hltCaloMET = cms.InputTag('hltMet'),
    #hltCaloMETTypeOne = cms.InputTag('hltCaloMETTypeOne'),
  ),

  recoPFClusterMETCollections = cms.PSet(

    #hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
    #hltPFClusterMETTypeOne = cms.InputTag('hltPFClusterMETTypeOne'),
  ),

  recoPFMETCollections = cms.PSet(

    #hltPFMET = cms.InputTag('hltPFMETProducer'),
    hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),

    #hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    #hltPFCHSMETTypeOne = cms.InputTag('hltPFCHSMETTypeOne'),

    #hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
    hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    #offlinePFMET = cms.InputTag('slimmedMETs'),
    #offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),
)

if opts.keepPFPuppi:
  #process.offlinePFPuppi.puppiDiagnostics = True
  process.hltPFPuppi.puppiDiagnostics = True
  process.JMETriggerNTuple.vdoubles = cms.PSet(
    #offlinePFPuppi_PuppiWeights = cms.InputTag('offlinePFPuppi:PuppiWeights'),
    #offlinePFPuppi_PuppiRawAlphas = cms.InputTag('offlinePFPuppi:PuppiRawAlphas'),
    #offlinePFPuppi_PuppiAlphas = cms.InputTag('offlinePFPuppi:PuppiAlphas'),
    #offlinePFPuppi_PuppiAlphasMed = cms.InputTag('offlinePFPuppi:PuppiAlphasMed'),
    #offlinePFPuppi_PuppiAlphasRms = cms.InputTag('offlinePFPuppi:PuppiAlphasRms'),
    #hltPFPuppi_PuppiWeights = cms.InputTag('hltPFPuppi:PuppiWeights'),
    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms')
  )
  process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet(
    hltParticleFlow = cms.InputTag('hltParticleFlow'),
    hltPFPuppi = cms.InputTag('hltPFPuppi'),
    #offlineParticleFlow = cms.InputTag('particleFlow'),
    #offlinePFPuppi = cms.InputTag('offlinePFPuppi'),
  )

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.append(process.analysisNTupleEndPath)

###
### updating Phase 0 HCAL thresholds
###

#process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].name = "PFRecHitQTestHCALThresholdVsDepth"
#del process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].threshold

###
### Customisation for "mixed" tracking (full + pixel tracks in PF) 
###
if opts.useMixedTrk:
  from HLTrigger.Configuration.customizeHLTforMixedPF import customizeHLTForMixedPF
  process = customizeHLTForMixedPF(process)

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
if opts.globalTag is not None:
   #from Configuration.AlCa.GlobalTag import GlobalTag
   #process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')
   process.GlobalTag.globaltag = cms.string(opts.globalTag)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
 #'/store/mc/Run3Winter21DRMiniAOD/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v1/270000/01a06ce0-a218-423f-a576-587debd69c63.root',
 #"/store/mc/RunIISummer16DR80/NeutrinoGun_E_10GeV/AODSIM/FlatPU0to75TuneCUETP8M4_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000/104F26EB-3B0B-E711-8750-A0369FC5EEF4.root"
 #"/store/mc/RunIIAutumn18DR/SingleNeutrinoGun/GEN-SIM-DIGI-RAW/PUPoissonAve85_102X_upgrade2018_realistic_v15_ext5-v1/100000/3D6B0068-DC22-4143-8DDE-5A68D48FCA4A.root"
 #'/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/003cee26-b0ed-4491-a301-f3261420b157.root'
 
 # test PU-only
 #'/store/mc/Run3Summer21DRPremix/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/SNB_120X_mcRun3_2021_realistic_v6-v2/2540000/000f4b8d-d64a-473d-9c30-acc77e148637.root'
 #'/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/AODSIM/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520000/00362d0b-f7a4-426b-ba2c-e91c2cd2b792.root'
 # test QCD
 # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/MINIAODSIM/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/1fb87340-34b4-4c8a-a049-33192b21d54b.root' 
 # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/AODSIM/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820000/01e4d447-2f4a-4ad0-bbc2-a8324f18ea2a.root'
 
 # '/store/mc/Run3Summer21MiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/MINIAODSIM/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v5-v1/30000/76dfad7c-52eb-4207-96cf-e74c5c6509d0.root'

 #  '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/0d8a6361-5115-49d3-86a4-4dbeca2e2fd6.root'
 '/store/mc/Run3Summer22DR/QCD_Pt-15To7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_castor_124X_mcRun3_2022_realistic_v12-v1/2810000/00323e70-75e6-4098-8cbc-31c69a451d8c.root'
 # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/70007/98c44c2f-d5b4-49b3-a2bf-a709898dd8cd.root' 
  
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    # test PU-only
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520001/9154d5a7-8d1e-40a5-8ff2-0ec12515c390.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/02141377-fef1-4fa1-86f1-9bbae0927d07.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/033d4a7f-4731-4838-b680-40756a41974a.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/03e84645-9aff-4988-ad68-6eb8a1a8d03c.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/17c4f5c4-80ab-4191-95d3-8809e7cee970.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/2602ec39-bfc0-43e7-a72d-d237111342e4.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/32441529-91fb-4b95-ae01-c28a27a9a22e.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/4a417aa4-fce3-4632-886e-fb8a6ec853be.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/4e8a3050-fff4-4292-9eb5-91f48f902cb9.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/65529587-a211-479b-b804-71360ca2a63a.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/80e28bfa-b264-4b52-ac42-1c7b7dca6f0e.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/81e9ae8c-d7f8-4517-9dbe-7ebc868d41f2.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/8cd48b79-77e7-40f3-9c9b-43c8c71a7406.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/8d7a88df-727c-4e98-9d26-4483a7fdb595.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/9923a456-6773-4ea0-b82c-0bcafc94267c.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/b5e84669-cffe-4a7d-b437-65067597c1fa.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/ccbfffab-2c68-4574-a220-cb7dfee2d4b3.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/d2419e1a-97e4-49fa-9bf8-f6fa281dbd19.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/f40e56eb-6589-4c03-99c5-5b40d082888d.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/f9051a3a-670b-4b30-aac0-feee81e9dc06.root',
    # '/store/mc/Run3Winter22DR/SingleNeutrino_E-10-gun/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_SNB_122X_mcRun3_2021_realistic_v9-v2/2520005/f9a3c6a9-6c81-46d9-952e-12438e946239.root',
    
    # test QCD
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820000/a6db45f3-aac7-4123-b48f-021db13fe79c.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820000/bc364d75-61b7-47bc-87a8-54091ce8f0aa.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820001/0e728e38-ff2b-4087-95c3-758e322cdb6e.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820001/f05ad893-993f-4160-939f-3606967070df.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820003/0cf7acea-001f-42b9-b157-222543d86266.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820003/5ce782ce-e5dc-4a2b-952a-02dbc3cf0c7f.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820003/9b91cdb4-a430-4251-b409-f07dfb6e93bc.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820004/1c70a5f5-df2a-4eb3-8abe-91de54b8971a.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820004/8838f488-ed2f-4c3a-b122-6cfe75f55607.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820004/88fc5934-8f30-4af5-827a-a1e075228fff.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820004/a5e064b1-000a-469e-8c7d-221b11c085c5.root',
    # '/store/mc/Run3Winter22DR/QCD_Pt15to7000_TuneCP5_13p6TeV-pythia8/GEN-SIM-DIGI-RAW/L1TPU0to99FEVT_castor_122X_mcRun3_2021_realistic_v9-v2/2820004/d5b09519-335d-4012-bb36-2c155c063c5c.root'

#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/0f6dd686-c85f-4c55-b207-cdd1646f7d1a.root',
#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/45cc05fe-c6ea-42b2-84cf-e6e4af83c1a5.root',
#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/571695d2-0e3e-45dc-95b8-5b4881bf0356.root',
#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/5835fbc1-66f6-4372-a450-83002f5068a3.root',
#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/6fde9068-2ec2-4ead-bca4-5df23c7c6a01.root',
#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/ddc677fc-592d-4c43-ba41-fbf3d127902e.root',
#  '/store/mc/Run3Winter22GS/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/GEN-SIM/122X_mcRun3_2021_realistic_v9-v2/40003/ed761382-1713-4bca-bebc-0a0be2c04417.root'

      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/08f9d5ad-7a1c-4440-ac2f-f71c84d6f525.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/0bd11d4d-1967-4973-80ad-0b962d2669c5.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/0e0481b5-1c39-4eda-a1de-0e2254f52a9c.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/2045ffa9-fbd3-4153-bc38-207b607304cb.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/236704cf-462c-47ec-a8b3-6147ff0f4be9.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/23dc9f4b-488c-4f9b-82dd-9c982a7cd449.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/2c2c1b8c-3378-44da-87e5-bd3b4f948d22.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/4fea1664-d8db-43bd-bfad-cd94126424d3.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/5556d434-1dd5-434a-bccd-a0bc5f277152.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/5561b0cb-fe04-4c02-881f-295e558c5444.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/5f8f1d6d-6210-42ab-b8ee-0b00aacdd8e1.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/600ff5f5-716d-49b5-b728-f8376f84ceb0.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/6742997d-3d24-4deb-8365-61b6abc87ca4.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/6cbfb800-3d15-488a-954f-0feb585d37a5.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/755bff65-36b9-4172-ac83-f4e2685b53b4.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/87b78df9-1cf3-4ab7-806e-58f748112d2f.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/991c0347-412d-43eb-b219-b28af01e067f.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/ac7addf7-cbd6-434b-b8b3-8f56407deecd.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/ae75c926-22a1-4d3e-b0b0-7fc2a67c9fb5.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/b259fb57-968d-4aef-b27d-c2fc03aaea27.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/b5799868-5a40-48f3-83ca-b6f59d666565.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/c0640f64-da4d-49b0-87f5-e25f02277eef.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/c1ae0140-d077-4d40-a895-87852244210f.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/ce4c3976-70d7-4d77-aa43-dfeb2eb32f4f.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/ce6ebc04-d829-42d8-88f6-9a7259809f79.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/cf182551-397e-424f-aa9b-190e1003ec38.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/d34ff4b3-ce41-47f7-8f83-9ddcd95122c3.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/d428f27f-2d2f-4e46-a005-92a7f4199fd7.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/d6f2e27b-c502-4fcd-812d-a96280814cca.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/f2bf3602-f0d9-4ddc-9503-e1deefa9a8d8.root',
      # '/store/mc/Run3Winter21DRMiniAOD/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_112X_mcRun3_2021_realistic_v16-v2/120000/fff0e03b-c95e-41b9-b72e-fa6f163d6308.root'
    #########
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/5a423664-f0f4-432a-9573-601f608ffd61.root',
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/76845592-a3ca-4ba0-88d6-62a7783903d7.root',
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/a825d603-efb0-4ec8-aa97-64c1d1668be4.root',
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/00169f6c-2bd0-4419-9de0-f9dff5f6e909.root',
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/4489ddce-a7e0-4a36-b924-7ec6de3b6bab.root',
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/b66444c2-1e9e-4f10-8f75-6e9099fa7d6e.root',
    # '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/d73315f5-4981-4a87-a48d-465ab24e203e.root',
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
   #print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('-------------------------------')
