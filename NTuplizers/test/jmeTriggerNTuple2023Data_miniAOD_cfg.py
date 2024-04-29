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

opts.register('offlineJecs', 'Summer22EEPrompt22_RunG_V1_DATA',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', '124X_dataRun3_Prompt_v4',
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
  print('Using the offline corrections:'+opts.offlineJecs+'.db')
  
  process.offlinejescESSource = cms.ESSource('PoolDBESSource',
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

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple_MiniAOD',
  TTreeName = cms.string('Events'),
  createSkim = cms.untracked.bool(True), # applies selection of events based on collections jets,met,muons etc bellow - Note: could add typesOfSelections based on target e.f. 'WmunuJet'
  createTriggerQuantities = cms.untracked.bool(True), # creates branches needed for trigger efficiencies like leadingJetPt, HT, MET based on the collections bellow
  jets = cms.InputTag(userJetsAK4PFPuppiCollection),
  muons = cms.InputTag(userMuonsCollection),
  pfmet = cms.InputTag("slimmedMETs"),
  met = cms.InputTag("slimmedMETsPuppi"),
  #met = cms.InputTag("slimmedMETsPuppi","","MYANALYSIS"),
  vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  metFilterBitsTag = cms.InputTag("TriggerResults::RECO"),
  TriggerResults = cms.InputTag('TriggerResults::HLT'),
  TriggerResultsFilterOR = cms.vstring(
   'HLT_IsoMu27'
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
    'HLT_PFJet60',
    'HLT_PFJet80',
    'HLT_PFJet140',
    'HLT_PFJet320',
    'HLT_PFJet500',
    # Forward
    'HLT_PFJetFwd60',
    'HLT_PFJetFwd80',
    'HLT_PFJetFwd140',
    'HLT_PFJetFwd320',
    'HLT_PFJetFwd500',
    # HT
    'HLT_PFHT180',
    'HLT_PFHT350',
    'HLT_PFHT510',
    'HLT_PFHT780',
    'HLT_PFHT1050',
    # MET MHT
    'HLT_PFMET120_PFMHT120_IDTight',
    'HLT_PFMET140_PFMHT140_IDTight',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight',
    'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF',
    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight',
    'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_FilterHF',
    # MET Only
    'HLT_PFMET200_BeamHaloCleaned',
    'HLT_PFMET200_NotCleaned',
    'HLT_PFMET250_NotCleaned',
    'HLT_PFMET300_NotCleaned',
    # muon
    'HLT_IsoMu27', 
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
 # + process.puppiMETSequence
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
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/362/00000/f6126759-0090-43f1-9746-f012d665b19d.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/f1fab25b-6734-4232-bcfb-df1a3fd28430.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/cdda2acc-8897-4329-96d5-a1372a8ab02e.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/c8fead6d-2e7b-4414-ab7d-fb6ac52c9546.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/b0efdfb3-bb9e-4178-9956-4b96af48770d.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/de81f779-9b70-4c72-b1f1-f9faba4c4ccd.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/4c9d8a9b-de70-4f03-a81a-3f05556950af.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/b984bb52-600e-464e-af82-92fef286cfaf.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/9df68e29-f2a4-4cb2-988a-aa32c3809909.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/9b552bb2-61e4-4af4-9aab-28897a9664bc.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/44fc47e6-395a-4531-ad9d-f290b4c14a91.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/9ad2d965-86c1-4749-afde-a8c5876c7e8c.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/d4fbe6ae-b0b0-4078-9695-341f2b96a174.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/9a328385-4470-4eb7-9721-0ed0ae487b94.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/a347f629-8b11-4915-9b9c-98b83e4233a2.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/a18f6455-f4ae-4e26-8647-d51927c32275.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/aab82770-f276-47b5-aa13-35df56f49570.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/569d9f8c-8e1a-437c-8dc7-9041e090c1d5.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/e88ad1bb-1704-415a-8e64-45a06e247cad.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/3c26805b-9c44-456b-a681-a91da08ddcbc.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/fc489de5-8ee5-4924-b040-43cffa50c985.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/69130ed7-e113-4760-9bb9-2df8e33fced7.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/a2ac4fcb-3f93-4df3-81fb-678de21aacf3.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/c274772f-cee1-403b-9f0e-95d453e609d2.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/b0f21195-257e-491c-adca-6773e25ba3e8.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/a1215fc3-efb9-4f92-9cdb-7f01662082eb.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/5ff0a12c-0195-4f84-af60-77074ed70b1e.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/e9d98c6f-a63a-42da-aa15-4b28c5b18695.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/977f4f87-b018-49dd-91a0-bd304d07f1fa.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/ce7e9b17-f92e-44e1-9026-77e7f0f98a79.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/82d00650-1bd5-4165-8cd2-19b76c7d9d52.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/3fb97e96-fa9f-4c0a-84d6-cd19ccab9e1c.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/ad6e2587-eb4c-4c39-a720-d125ca61eb48.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/52449ef5-7756-4175-80fc-fb8f4fb7a2f7.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/c20ba8e6-8f48-45fb-9a36-c4050cb78fad.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/e2230052-fbaf-4059-97ae-08c3a3c7b521.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/e59e15f7-aeb0-46e7-9e96-ce71864576df.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/70c45489-4ca5-4be0-86e9-82d66aacb718.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/69a6be53-29b0-47aa-929b-2265b25c8331.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/f90c1d94-b18c-419c-a5e5-f6ba1ada4f58.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/35b4ceb5-9373-4704-9f89-a1d093742440.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/54da72d8-6a61-46a4-966e-8b2b12690446.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/463988c7-9886-4d1d-8134-31e794074b42.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/dbe986df-c4ff-47b4-ac7d-1abac13e1d83.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/dd759187-7d0a-4a3f-8169-1fce3b642684.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/b3607850-8095-4216-8ef4-fcad5535df31.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/ce236b7f-b2da-4eb0-aea5-2a0158f3ef87.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/696/00000/33a684d9-f13e-4f88-b48f-bf5db2c1e41c.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/526b5c68-4540-4489-b0c2-93f524414258.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/b8451b45-8025-4f1f-b55d-df25658b5da2.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/29748a30-0b45-4fbd-813c-eb0c4c3adb24.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/acf72a67-f869-4126-ab19-7d48ca12edfa.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/c0ccc71c-efed-4f72-ad4f-0fbd23b732c0.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/a383e51d-c0cd-4718-b3de-afed4480ca70.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/5834db0b-05b9-42cc-b19d-19cd1d326d72.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/794ed236-c7b8-411d-b959-adc95fc2185f.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/a81a9e30-c063-4b7c-9ab1-ccad6dded790.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/728/00000/6c58e996-2e47-467b-bd4c-0cef65a996c4.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/207344eb-8d16-492f-a3a7-2143fab59c65.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/2b918976-c43d-4c71-b279-cfa118a29edb.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/7d7ccf88-5752-45e4-84e2-1c18f2a414ea.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/f848a794-d2ad-4227-aef3-b39c77c28b29.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/c1623bbc-0599-4631-ab18-02412c47e7a6.root',
  '/store/data/Run2022G/Muon/MINIAOD/PromptReco-v1/000/362/720/00000/136f028d-2b63-49e4-b3a4-2ea04bf86fc7.root',

    #'/store/data/Run2023B/Muon0/RAW/v1/000/366/895/00000/8c846177-ca3d-4c0f-a602-b401cb32b041.root'

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
