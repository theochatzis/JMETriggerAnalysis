import os
import fnmatch
import csv 

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

opts.register('offlineJecs', 'Summer22EEPrompt22_RunG_V1_DATA',#'Winter23Prompt23_RunA_V1_DATA',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', '130X_dataRun3_Prompt_v2',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')
opts.register('reco', 'default',
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
### Process
###

import FWCore.ParameterSet.Config as cms
process = cms.Process('MYANALYSIS')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')


update_jmeCalibs = True

###
### PoolSource (EDM input)
###
process.source = cms.Source('PoolSource',
  fileNames = cms.untracked.vstring(opts.inputFiles),
  secondaryFileNames = cms.untracked.vstring(opts.secondaryInputFiles),
  # number of events to be skipped
  skipEvents = cms.untracked.uint32(opts.skipEvents)
)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

###
### EDM Options
###
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(opts.maxEvents))

process.options = cms.untracked.PSet(
  # show cmsRun summary at job completion
  wantSummary = cms.untracked.bool(opts.wantSummary),
  # multi-threading settings
  numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1),
  numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1),
)

###
### Global Tag
###
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if opts.globalTag is not None:
   from Configuration.AlCa.GlobalTag import GlobalTag
   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')
else:
   raise RuntimeError('failed to specify name of the GlobalTag (use "globalTag=XYZ")')

###
### TFileService
###
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

## Jets processing

if update_jmeCalibs:
  process.offlinejescESSource = cms.ESSource('PoolDBESSource',
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Winter23Prompt23_RunA_V1_DATA.db'),
    _CondDB.clone(connect = 'sqlite_file:'+opts.offlineJecs+'.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_'+opts.offlineJecs+'_AK4PFPuppi'),
        label = cms.untracked.string('AK4PFPuppi'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_'+opts.offlineJecs+'_AK8PFPuppi'),
        label = cms.untracked.string('AK8PFPuppi'),
      ),
    ),
  )
  process.offlinejescESPrefer = cms.ESPrefer('PoolDBESSource', 'offlinejescESSource')


###
### Customized objects modules
###

## Muons
from JMETriggerAnalysis.NTuplizers.userMuons_cff import userMuons
process, userMuonsCollection = userMuons(process)

## Jets
from JMETriggerAnalysis.NTuplizers.userJets_cff import userJets
process, userJetsAK4PFPuppiCollection = userJets(process)


## Update MET corrections based on new userJetsAK4PFPuppiCollection
# link for recommendations : https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETUncertaintyPrescription
## The three lines below should always be included

# from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
# from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
# makePuppiesFromMiniAOD( process, True );

# runMetCorAndUncFromMiniAOD(process,
#                            isData=True,
#                            metType="Puppi",
#                            postfix="Puppi",
#                            jetFlavor="AK4PFPuppi",
#                            )


## Output NTuple
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple_MiniAOD_testObjects',
  TTreeName = cms.string('Events'),
  createSkim = cms.untracked.bool(True), # applies selection of events based on collections jets,met,muons etc bellow - Note: could add typesOfSelections based on target e.f. 'WmunuJet'
  isMuonDataset = cms.untracked.bool(False), # use this only for muon dataset to apply the muons criteria in selection
  createTriggerQuantities = cms.untracked.bool(True), # creates branches needed for trigger efficiencies like leadingJetPt, HT, MET based on the collections bellow
  jets = cms.InputTag(userJetsAK4PFPuppiCollection),
  muons = cms.InputTag(userMuonsCollection),
  #met = cms.InputTag("slimmedMETsPuppi","","MYANALYSIS"),
  met = cms.InputTag("slimmedMETsPuppi"),
  vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  metFilterBitsTag = cms.InputTag("TriggerResults::RECO"),
  TriggerResults = cms.InputTag('TriggerResults::HLT'),
  TriggerObjects = cms.InputTag('slimmedPatTrigger'),
  TriggerResultsFilterOR = cms.vstring(
    #'HLT_IsoMu27'
    'HLT_PFJet40',
    'HLT_PFJet60',
    'HLT_PFJet80',
    'HLT_PFJet110',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500',
  ),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(
    # # Single jet 
    # 'HLT_PFJet60',
    # 'HLT_PFJet80',
    # 'HLT_PFJet140',
    # 'HLT_PFJet320',
    # 'HLT_PFJet500',
    # # Forward
    # 'HLT_PFJetFwd60',
    # 'HLT_PFJetFwd80',
    # 'HLT_PFJetFwd140',
    # 'HLT_PFJetFwd320',
    # 'HLT_PFJetFwd500',
    # # HT
    # 'HLT_PFHT180',
    # 'HLT_PFHT350',
    # 'HLT_PFHT510',
    # 'HLT_PFHT780',
    # 'HLT_PFHT1050',
    # # MET
    # 'HLT_PFMET120_PFMHT120_IDTight',
    # 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
    # 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF',
    # # muon
    # 'HLT_IsoMu27',
    'HLT_PFJet40',
    'HLT_PFJet60',
    'HLT_PFJet80',
    'HLT_PFJet110',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500',
  ),
  TriggerResultsCollectionsForObjects = cms.vstring(
    'HLT_PFJet40',
    'HLT_PFJet60',
    'HLT_PFJet80',
    'HLT_PFJet110',
    'HLT_PFJet140',
    'HLT_PFJet200',
    'HLT_PFJet260',
    'HLT_PFJet320',
    'HLT_PFJet400',
    'HLT_PFJet450',
    'HLT_PFJet500',
  ),
  outputBranchesToBeDropped = cms.vstring(
     'offlineAK4PFPuppiJetsCorrected_jesc',
     'offlineAK4PFPuppiJetsCorrected_jetArea',
     'offlineAK4PFPuppiJetsCorrected_numberOfDaughters',
     'offlineAK4PFPuppiJetsCorrected_chargedHadronEnergyFraction',
     'offlineAK4PFPuppiJetsCorrected_neutralHadronEnergyFraction',
     'offlineAK4PFPuppiJetsCorrected_electronEnergyFraction',
     'offlineAK4PFPuppiJetsCorrected_photonEnergyFraction',
     'offlineAK4PFPuppiJetsCorrected_muonEnergyFraction',
     'offlineAK4PFPuppiJetsCorrected_chargedHadronMultiplicity',
     'offlineAK4PFPuppiJetsCorrected_neutralHadronMultiplicity',
     'offlineAK4PFPuppiJetsCorrected_electronMultiplicity',
     'offlineAK4PFPuppiJetsCorrected_photonMultiplicity',
     'offlineAK4PFPuppiJetsCorrected_muonMultiplicity',

     'offlinePFPuppiMET_Type1XY_pt',
     'offlinePFPuppiMET_Type1XY_phi',
     'offlinePFPuppiMET_Type1XY_sumEt',
     'offlinePFPuppiMET_NeutralEMFraction',
     'offlinePFPuppiMET_NeutralHadEtFraction',
     'offlinePFPuppiMET_ChargedEMEtFraction',
     'offlinePFPuppiMET_ChargedEMEtFraction',
     'offlinePFPuppiMET_MuonEtFraction',

     'offlineMuons_mass',
     'offlineMuons_vx',
     'offlineMuons_vy',
     'offlineMuons_vz',
     
  ),

  #HepMCProduct = cms.InputTag('generatorSmeared'),
  #GenEventInfoProduct = cms.InputTag('generator'),
  #PileupSummaryInfo = cms.InputTag('addPileupInfo'),
  bools = cms.PSet(),  # add bools container to use it for TriggerResults
  
  doubles = cms.PSet(

    #hltFixedGridRhoFastjetAllCalo = cms.InputTag('hltFixedGridRhoFastjetAllCalo'),
    #hltFixedGridRhoFastjetAllPFCluster = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    #hltFixedGridRhoFastjetAll = cms.InputTag('hltFixedGridRhoFastjetAll'),
    
    #offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    #hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    #hltPixelVertices = cms.InputTag('hltPixelVertices'),
    #hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    #hltVerticesPF = cms.InputTag('hltVerticesPF'),
    #offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
  ),

  recoGenJetCollections = cms.PSet(

    #ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    #ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
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
    #hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

    #hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    #hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    #hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    #hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    #hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    #hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    #hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    #hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    #hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    #hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),

  ),

  patJetCollections = cms.PSet(
    #offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    #offlineAK4PFPuppiJetsCorrected = cms.InputTag(userJetsAK4PFPuppiCollection), # instead of slimmedJetsPuppi 
  ),

  recoGenMETCollections = cms.PSet(
    #genMETCalo = cms.InputTag('genMetCalo::HLT'),
    #genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),
  # recoMETCollections = cms.PSet (
  #   hltCaloHT = cms.InputTag('hltHtMhtJet30'),
  #   hltPFHT = cms.InputTag('hltPFHTJet30')
  # ),
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
    #hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),

    #hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    #hltPFCHSMETTypeOne = cms.InputTag('hltPFCHSMETTypeOne'),

    #hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
    #hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    #offlinePFMET = cms.InputTag('slimmedMETs'),
    ##offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(
    ##offlineMuons = cms.InputTag(userMuonsCollection)
  )
)


## Trigger Flags

## Note: Issue when there are more than one L1 paths 
# --> need to fix the producer so it can handle this case - will put to skip it initially and show always zero 
# Could improve it by seeing finding out how to check if the relation is OR/AND between L1 seeds and get the outcome of operation
# or if not possible can add more than one L1seed and make this a vector.

process.triggerFlagsTask = cms.Task()

hltPathsWithTriggerFlags = [
  # Single jet 
    # 'HLT_PFJet60',
    # 'HLT_PFJet80',
    # 'HLT_PFJet140',
    # 'HLT_PFJet320',
    # 'HLT_PFJet500',
    # # Forward
    # 'HLT_PFJetFwd60',
    # 'HLT_PFJetFwd80',
    # 'HLT_PFJetFwd140',
    # 'HLT_PFJetFwd320',
    # 'HLT_PFJetFwd500',
    # # HT
    # 'HLT_PFHT180',
    # 'HLT_PFHT350',
    # 'HLT_PFHT510',
    # 'HLT_PFHT780',
    # 'HLT_PFHT1050',
    # # MET MHT
    # 'HLT_PFMET120_PFMHT120_IDTight',
    # 'HLT_PFMET140_PFMHT140_IDTight',
    # 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
    # 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF',
    # 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
    # 'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_FilterHF',
    # # MET Only
    # 'HLT_PFMET200_BeamHaloCleaned',
    # 'HLT_PFMET200_NotCleaned',
    # 'HLT_PFMET250_NotCleaned',
    # 'HLT_PFMET300_NotCleaned',
    # muon
    #'HLT_IsoMu27', 
]

from JMETriggerAnalysis.NTuplizers.TriggerFlagsPrescalesProducer_cfi import TriggerFlagsPrescalesProducer

for _hltPathUnv in hltPathsWithTriggerFlags:
    _triggerFlagsModName = 'triggerFlags'+_hltPathUnv.replace('_','')
    setattr(process, _triggerFlagsModName, TriggerFlagsPrescalesProducer.clone(
      triggerResults = 'TriggerResults::HLT',
      ignorePathVersion = True,
      pathName = _hltPathUnv,
      denominatorPathName = 'HLT_IsoMu27'
    ))
    process.triggerFlagsTask.add(getattr(process, _triggerFlagsModName))
    setattr(process.JMETriggerNTuple.bools, _hltPathUnv+'_L1TSeedAccept', cms.InputTag(_triggerFlagsModName+':L1TSeedAccept'))
    #setattr(process.JMETriggerNTuple.bools, _hltPathUnv+'_L1TSeedPrescaledOrMasked', cms.InputTag(_triggerFlagsModName+':L1TSeedPrescaledOrMasked'))
    setattr(process.JMETriggerNTuple.bools, _hltPathUnv+'_HLTPathPrescaled', cms.InputTag(_triggerFlagsModName+':HLTPathPrescaled'))
    setattr(process.JMETriggerNTuple.bools, _hltPathUnv+'_HLTPathAccept', cms.InputTag(_triggerFlagsModName+':HLTPathAccept'))
    #setattr(process.JMETriggerNTuple.bools, _hltPathUnv+'_L1TSeedInitialDecision', cms.InputTag(_triggerFlagsModName+':L1TSeedInitialDecision'))
    #setattr(process.JMETriggerNTuple.bools, _hltPathUnv+'_L1TSeedFinalDecision', cms.InputTag(_triggerFlagsModName+':L1TSeedFinalDecision'))
    setattr(process.JMETriggerNTuple.doubles, _hltPathUnv+'_HLTPathPrescaleWeight', cms.InputTag(_triggerFlagsModName+':HLTPathPrescaleWeight'))

process.triggerFlagsSeq = cms.Sequence(process.triggerFlagsTask)

#process.fullPatMetSequencePuppi = cms.Sequence(process.fullPatMetTaskPuppi)

process.analysisCollectionsPath = cms.Path(
  process.userMuonsSequence
  + process.userJetsSeq
  #+ process.puppiMETSequence
  #+ process.fullPatMetSequencePuppi
  + process.triggerFlagsSeq
  + process.JMETriggerNTuple
)

###
### standard options
###

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = opts.numThreads
process.options.numberOfStreams = opts.numStreams

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
  '/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/1bccb908-c5ed-4dee-bc39-fb1b68069599.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/bfeecef1-d8dc-478c-80a5-50123a343749.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/82140a8e-bbc0-4330-ae70-58f7d7da443d.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/b1dbeb6f-a995-4db0-b006-9ec0c874f1e0.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/cd076e86-ef64-4ffa-9748-6f52f2c1f0c4.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/f167e073-7e7b-4c07-ad56-4e0d6d71967d.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/728/00000/35fc54b4-1142-4db5-aca0-8f578ffb5921.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/6a0cc43a-448d-499b-8a61-4b15d519bb36.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/85587726-582d-4235-905d-4b6ad64ce26c.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/740a5901-9158-4d7e-9164-ce47b5b078ba.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/ccdb52fb-6a43-4252-a8e9-e8c42999996c.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/688b49d4-da8a-41b9-879c-c7455f28abc4.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/b6f44306-f7f7-4d32-aa08-9457eba480dc.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/d2f4c8aa-e0be-4ed5-aa52-8ceca70d5f61.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/0316a653-a245-43f9-9505-5ec13ef2bcb9.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/1e48080d-9a47-499b-a0ff-2a3fa29aa77b.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/ac789515-8e47-4a3b-8f83-258e08f25f95.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/323902eb-1dd9-437f-8571-a48bb0af416d.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/59ad835e-7686-4865-b8aa-ecdc77394bae.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/95b110b7-4e37-46da-935b-82b4c044750a.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/71cb2997-785d-43fa-b9f0-c7052b797007.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/5a00cadb-f3db-45cb-9075-22ce371c14e0.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/6aa47b01-53fd-4e95-bef8-b418bfa1a2fd.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/015d1ed1-21aa-4eaf-a74c-a6170cf2c6a5.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/4f568f24-f37e-4265-8923-455ea5edcd60.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/63efa9a0-d544-4b84-bf6f-f0895436a3ec.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/728/00000/c77919b4-93e7-4233-ba8f-a9b88d6d462a.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/7380ba5e-9843-4678-967f-7f81f273bb9b.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/e40eda0f-09ce-45ff-8fb7-159bebecc809.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/0b0aa818-8d68-4f18-a981-ca5e398f5c63.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/b2e55b8f-ce43-4a43-a24f-246023cdbac5.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/728/00000/02e59ecd-fac8-498b-9098-ae71e44ea9e7.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/bdbf5ebe-bfae-4369-88c6-ab1bcff3607a.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/d023286d-9372-497d-b97a-23f345521d87.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/cd1d3873-ca77-4760-92fa-30350fe22632.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/788b38bd-a12a-44af-b8c2-b33aa76b8779.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/44c3d3d5-08cc-4f0e-ad41-61fb7c1eba59.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/c1ee9433-4c60-4d63-8a0b-5ed422893d23.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/728/00000/b46fe44b-d1cb-494a-b331-7ec834962501.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/61671f9a-a10f-4993-877a-ed014593b8e9.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/708a53ac-f7f6-4bcc-b502-636477183c3b.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/63606f88-2af5-4b62-9094-f4fd24b8eaec.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/f35a62d4-cdb5-41f0-9ac1-0eeea305b54c.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/0795bec4-a9f2-4bfa-bb8d-9f1cb68443c0.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/0012a271-26ab-4e78-9c23-b05ad459fcba.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/9d14a4b6-8b4c-4f6b-98a8-34b3f1545128.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/2912cf44-bfa6-4e22-bc65-3ce6d181e064.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/da7b215e-9047-4c21-a8bf-56942a26897d.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/2bce5c14-e40b-4583-a7ab-95c4c1d12990.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/3d990964-6f20-4b0f-b0fc-4e53c25de3a2.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/1c50f4f3-05f6-4677-8a20-a5a6a017488d.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/97a8e02d-e3b7-4512-9923-54f1e76d958c.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/b3bb2142-78d5-4dcd-9b4b-9d7edd1108b8.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/720/00000/e9795742-a8a7-4a80-a310-62e153bbf0a3.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/728/00000/296e4b31-8ee4-44cb-9ec2-390e2ea0bb5b.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/696/00000/1430e07f-614c-4ded-9c39-e3e0ac9efda7.root',
'/store/data/Run2022G/JetMET/MINIAOD/PromptReco-v1/000/362/728/00000/b5466c6d-1efd-4565-a0c8-72992ea16555.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/da798809-3997-4a4f-b50a-07788935c868.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/268994f7-0591-4d94-86cb-fd48d5f729b3.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/687996a1-f59c-4450-b2e1-dfe7800481d1.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/0f88760a-eb7d-43c8-b38d-0974daaad680.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/afb372e4-50d4-4489-b925-5954d381ec2a.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/01d2fcc6-4deb-49f7-90cc-938dc0796e3d.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/74518823-c2c5-4bdb-a06b-e8f9115a3c32.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/05d25cb4-0554-4106-bd9e-5681fe4d8efb.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/19e78f99-6eb2-417f-acf5-e041ea5b96f8.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/44452017-a9a0-4372-90d8-321ad5750df9.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/2bf0121f-79f4-48d1-9964-560afda815be.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/d21e0a86-5f6b-4605-8977-cd940eaf15c7.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/ad903315-95b9-4ba9-b5ac-3664316af8be.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/f19dddec-100a-4c5a-b03f-39195814527a.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/9aecb4ee-2318-480c-8bca-c537860c3620.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/950733a0-c8cf-4370-9233-226644f61158.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/fa7c5262-1282-459e-b19b-cfd314f95bc7.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/671f0630-5051-4e82-b3d8-8ea46155b11b.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/b05c18bd-c37a-4703-8746-16164d342571.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/18222f62-ec83-47d0-99e1-73e66647fff0.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/7d3ddcb0-b513-4468-b4eb-77754a6725e9.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/c4b6822c-58d4-4505-9ed7-cb26bc665712.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/5e50a787-a286-42bf-815d-89fcf47548db.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/9b6c0e6c-1fa0-4c24-a676-07d29aa56360.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/5ccb6baf-4eb5-4755-a83f-f28b88cd1bd6.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/28688604-a1f0-45c3-b955-157fda9f8b30.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/bd0c4bd6-188d-4786-820f-8fa3bfa7f0ae.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/b0f5b515-7893-4a25-8328-ca6ff5e7cc32.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/bd1565ec-bb5a-40a5-904d-afb1a5134340.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/7947a466-51f6-452b-83cf-9469005d86b0.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/ceb072a1-2396-48f5-90a4-edb05264ce14.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/66bb139d-fb28-48b0-ac2e-18fba3962a25.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/d6184c5c-2fcb-4c38-85f7-31dd6973b18e.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/c012738c-e197-48b6-ad6e-39697e931962.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/7899daef-e3a4-463c-8e10-dc673e83af49.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/2388086f-3093-4997-8e60-10d7ac5bdcb7.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/579/00000/5108e28d-4930-4b1c-9860-4f343fd0dc8b.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/b0be8947-a2a0-4545-ab9b-e244c413aab7.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/de149fbc-f219-4c09-a4db-558269f4e67e.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/999a2bf6-01cc-4e0f-8a46-6455f2890afa.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/4a2cc580-d2d5-47bf-8de5-f703e785192e.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/e34d3349-1d67-4556-a627-16fba741612b.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/6a71ff04-b99d-4654-a418-0c5082ba06f7.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/0f4a98b4-a1d1-4963-bd4f-7149f4fd4674.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/adc459f5-158a-4ed3-8aba-93043cee1fa7.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/b212e4dd-fd06-407d-8f99-b10a5531e118.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/07ba4522-974c-4d81-b530-2fab1870519e.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/ff524a79-1170-4b49-8e6b-ce9bdfb3ba1d.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/d4100351-759e-4635-ad65-84e4d176fb1b.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/8b6cc7f2-286f-45fa-815f-7e9007f55fed.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/52e82069-ba3d-4522-b1c6-afa8228a7f82.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/bb94889f-5208-4a0a-988c-a42a6384b87e.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/d12c9e2e-4820-48f2-848a-64593eebc116.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/89a922f4-8a07-4332-b734-a3759b3d234c.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/8e8e4a42-9a6f-4d53-a69d-b9e277f2b275.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/f2211a36-e640-4428-950f-9a9ebdf1e606.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/5452c2f3-fa89-4463-87b6-c92e2a3cc7ba.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/eb15eaf7-0661-408a-a52c-44e1597cbf78.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/bf89aff0-b9b9-4d23-bf67-8ae4acb3abdd.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/93c5b06b-61b4-41f0-ba50-bc89cf281334.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/d36eaa3a-3b98-4ed4-b387-088500283e92.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/cd977b72-98f1-4c92-a0fe-be8514e96954.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/db27a6f8-eab0-4e3b-8ad2-166c1bf68a3e.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/b7995244-187f-4ad2-aed3-b99049f84a59.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/c531c9ec-92b9-4380-8b23-a0c3b20f3d0b.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/a9a3e166-4896-4470-8d19-3464367848ac.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/abe2a7cd-1984-4409-bec1-8318a77f8a38.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/d5ad0e89-1b95-4aad-8843-88bc3bef7077.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/9307342c-fead-4def-98a7-ad8766fca2bb.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/6bf1dd7b-0bd5-4d7a-ab67-e9023c76536b.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/522/00000/a236d43c-8525-44a3-8ece-90ba66ad6cf2.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/560/00000/46e36cdf-a5de-43c5-972b-b13b0ec8fc42.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/497/00000/dfa2abfc-1c28-44ad-92a0-3fcee26f6af0.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/e3268026-083a-4d8d-a81b-ca3278813d81.root',
  # '/store/data/Run2023D/JetMET0/MINIAOD/PromptReco-v1/000/370/580/00000/6fadd799-69a0-4578-9b1a-06d8b7878401.root',
]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    #'/store/data/Run2022G/Muon/RAW/v1/000/362/362/00000/fe383907-a8c5-4f53-80a8-d11efe8b0d9e.root'
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
