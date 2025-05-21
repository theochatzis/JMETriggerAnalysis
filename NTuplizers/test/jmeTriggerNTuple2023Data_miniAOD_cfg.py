import os
import fnmatch
import csv 
import re 

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

opts.register('isMuonData', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'set to True if you want to run on Muon dataset for miniAOD analysis')

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

opts.register('offlineJecs', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', '140X_dataRun3_Prompt_v2',
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


update_jmeCalibs = False

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

if opts.offlineJecs is not None:
  print('Using the offline corrections:'+opts.offlineJecs+'.db')
  
  process.offlinejescESSource = cms.ESSource('PoolDBESSource',
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Winter23Prompt23_RunA_V1_DATA.db'),
    #_CondDB.clone(connect = 'sqlite_file:Winter23Prompt23_RunA_V1_DATA.db'),
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

#--- Updating offline JECs 
  from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
  #Load JECs
  jecLevels = ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual']
  jecToUse = cms.vstring(jecLevels)
  updateJetCollection(
      process,
      jetSource=cms.InputTag("slimmedJetsPuppi"),  #Input PAT jet collection
      labelName="AK4PFPuppi",  #Label for the updated jet collection - will become patJetCorrFactors[labelName]
      jetCorrections=("AK4PFPuppi", jecToUse, "None"),  #JECs to be applied
  )

  updateJetCollection(
      process,
      jetSource=cms.InputTag("slimmedJetsAK8"),  #Input PAT jet collection
      labelName="AK8PFPuppi",  #Label for the updated jet collection - will become patJetCorrFactors[labelName]
      jetCorrections=("AK8PFPuppi", jecToUse, "None"),  #JECs to be applied
  )

  process.jecSequence = cms.Sequence(process.patJetCorrFactorsAK4PFPuppi * process.updatedPatJetsAK4PFPuppi * process.patJetCorrFactorsAK8PFPuppi * process.updatedPatJetsAK8PFPuppi)
  process.offlineJecPath = cms.Path(process.jecSequence)
  process.schedule.append(process.offlineJecPath)

###
### Customized objects modules
###

## Muons
from JMETriggerAnalysis.NTuplizers.userMuons_cff import userMuons
process, userMuonsCollection = userMuons(process)

## Electrons
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



## 
# here you can add paths that you want your events to pass
# this is changing based on the selection of dataset. If muonic use IsoMu27 otherwirse using all single jet,dijet triggers. 
# Note : the search for paths existing could become more automated to be searched with wildcards. e.g. HLT_(Di)PFJet+_v*
pathsForDataSelection = []

if opts.isMuonData:
   pathsForDataSelection = ['HLT_IsoMu27']
else:
  pathsForDataSelection = [
      # Single jet triggers
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
      'HLT_PFJet550',
      # Dijet and HF Dijet triggers
      'HLT_DiPFJetAve40',
      'HLT_DiPFJetAve60',
      'HLT_DiPFJetAve80',
      'HLT_DiPFJetAve140',
      'HLT_DiPFJetAve200',
      'HLT_DiPFJetAve260',
      'HLT_DiPFJetAve320',
      'HLT_DiPFJetAve400',
      'HLT_DiPFJetAve500',
      'HLT_DiPFJetAve60_HFJEC',
      'HLT_DiPFJetAve80_HFJEC',
      'HLT_DiPFJetAve100_HFJEC',
      'HLT_DiPFJetAve160_HFJEC',
      'HLT_DiPFJetAve220_HFJEC',
      'HLT_DiPFJetAve260_HFJEC',
      'HLT_DiPFJetAve300_HFJEC',
  ]



## Output NTuple
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple_MiniAOD',
  TTreeName = cms.string('Events'),
  createSkim = cms.untracked.bool(True), # applies selection of events based on collections jets,met,muons etc bellow - Note: will create dijet skim unless the isMuonDataset is used.
  isMuonDataset = cms.untracked.bool(opts.isMuonData), # use this only for muon dataset to apply the muons criteria in selection
  createTriggerQuantities = cms.untracked.bool(True), # creates branches with trigger objects and if also one wants (from the boolean bellow) offline quantities to monitor
  createOfflineQuantities = cms.untracked.bool(False),
  jets = cms.InputTag(userJetsAK4PFPuppiCollection),
  muons = cms.InputTag(userMuonsCollection),
  pfmet = cms.InputTag("slimmedMETs"),
  met = cms.InputTag("slimmedMETsPuppi"),
  #met = cms.InputTag("slimmedMETsPuppi","","MYANALYSIS"),
  vertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  metFilterBitsTag = cms.InputTag("TriggerResults::RECO"),
  TriggerResults = cms.InputTag('TriggerResults::HLT'),
  TriggerObjects = cms.InputTag('slimmedPatTrigger'),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(),
  TriggerResultsFilterOR = cms.vstring(pathsForDataSelection),
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
    'offlinePFPuppiMET_ChargedHadEtFraction',
    'offlinePFPuppiMET_Type6EtFraction',
    'offlinePFPuppiMET_Type7EtFraction',

    'offlinePFMET_Type1XY_pt',
    'offlinePFMET_Type1XY_phi',
    'offlinePFMET_Type1XY_sumEt',
    'offlinePFMET_NeutralEMFraction',
    'offlinePFMET_NeutralHadEtFraction',
    'offlinePFMET_ChargedEMEtFraction',
    'offlinePFMET_ChargedEMEtFraction',
    'offlinePFMET_MuonEtFraction',
    'offlinePFMET_ChargedHadEtFraction',
    'offlinePFMET_Type6EtFraction',
    'offlinePFMET_Type7EtFraction',

    'offlineMuons_mass',
    'offlineMuons_vx',
    'offlineMuons_vy',
    'offlineMuons_vz',

    'offlinePrimaryVertices_x',
    'offlinePrimaryVertices_y',
    'offlinePrimaryVertices_xError',
    'offlinePrimaryVertices_yError',
    'offlinePrimaryVertices_zError',
    'offlinePrimaryVertices_tracksSize',
    'offlinePrimaryVertices_isFake',
    'offlinePrimaryVertices_chi2',
    'offlinePrimaryVertices_ndof',
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
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
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
    offlineAK4PFPuppiJetsCorrected = cms.InputTag(userJetsAK4PFPuppiCollection), # instead of slimmedJetsPuppi 
    #offlineAK4PFPuppiJetsCorrected = cms.InputTag('updatedPatJetsAK4PFPuppi'),
    #offlineAK8PFPuppiJetsCorrected = cms.InputTag('updatedPatJetsAK8PFPuppi'),
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

    offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(
    offlineMuons = cms.InputTag(userMuonsCollection)
  )
)



## Trigger Flags

## Note: Issue when there are more than one L1 paths 
# --> need to fix the producer so it can handle this case - will put to skip it initially and show always zero 
# Could improve it by seeing finding out how to check if the relation is OR/AND between L1 seeds and get the outcome of operation
# or if not possible can add more than one L1seed and make this a vector.


# helper function for extracting the path threshold
# path_name is the string input of path name without the version (e.g. HLT_PFJet500 --> will output 500)
def extract_threshold(path_name):
    # Use regular expression to find the first sequence of digits
    match = re.search(r'\d+', path_name)
    if match:
        return int(match.group())
    else:
        return None

process.triggerFlagsTask = cms.Task()

from JMETriggerAnalysis.NTuplizers.TriggerFlagsPrescalesProducer_cfi import TriggerFlagsPrescalesProducer

if not opts.isMuonData:
    
    # Lists of paths to monitor using emulator method with JetMET dataset
    hltPathsWithTriggerFlags = [
      # the triggers go as : ["Numerator_name","Denominator_name"]
      # Single jet
      ['HLT_PFJet60','HLT_PFJet40'],
      ['HLT_PFJet140','HLT_PFJet60'],
      ['HLT_PFJet320','HLT_PFJet140'],
      ['HLT_PFJet500','HLT_PFJet320'],
      # Forward
      ['HLT_PFJetFwd60','HLT_PFJetFwd40'],
      ['HLT_PFJetFwd140','HLT_PFJetFwd60'],
      ['HLT_PFJetFwd320','HLT_PFJetFwd140'],
      ['HLT_PFJetFwd500','HLT_PFJetFwd320'],
      # HT
      ['HLT_PFHT370','HLT_PFHT180'],
      ['HLT_PFHT780','HLT_PFHT370'],
      ['HLT_PFHT1050','HLT_PFHT780'],

    ]
  
    for _hltPathUnv in hltPathsWithTriggerFlags:
        
        _triggerFlagsModName = 'triggerFlags'+_hltPathUnv[0].replace('_','')

        # In case you use useEmulationFromDenominator = True, instead of the triggerBit decision you get the emulated decision, which is found as follows:
        # 1) You take the HLT object from a reference trigger (denominator) which is the previous threshold
        # 2) You require the L1 seed to be accepted --> Emulated efficiency is "HLT Efficiency" not "L1+HLT Efficiency"
        # 3) As trigger decision you define Object_pt > trigger threshold
        # in case of emulation method the denominator decision also gets the L1 to be accepted always.

        setattr(process, _triggerFlagsModName, TriggerFlagsPrescalesProducer.clone(
          triggerResults = 'TriggerResults::HLT',
          ignorePathVersion = True,
          pathName = _hltPathUnv[0],
          denominatorPathName = _hltPathUnv[1],
          # options used for emulator method
          useEmulationFromDenominator = True,
          triggerObjects = cms.InputTag('slimmedPatTrigger'),
          emulatedThreshold = cms.double(extract_threshold(_hltPathUnv[0])),
        ))
        process.triggerFlagsTask.add(getattr(process, _triggerFlagsModName))
        #setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_L1TSeedAccept', cms.InputTag(_triggerFlagsModName+':L1TSeedAccept')) # L1 Seed decision
        setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_HLTPathAccept', cms.InputTag(_triggerFlagsModName+':HLTPathAccept')) # Trigger bit decision or emulated decision from denominator Trigger Object
        setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_HLTDenominatorPathAccept', cms.InputTag(_triggerFlagsModName+':HLTDenPathAccept'))

        # other available infos:
        # setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_L1TSeedPrescaledOrMasked', cms.InputTag(_triggerFlagsModName+':L1TSeedPrescaledOrMasked')) #  is the L1 seed prescaled in the event? 
        #setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_HLTPathPrescaled', cms.InputTag(_triggerFlagsModName+':HLTPathPrescaled')) #  is the path prescaled in the event? 
        #setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_L1TSeedInitialDecision', cms.InputTag(_triggerFlagsModName+':L1TSeedInitialDecision')) # initial L1 decision --> note : L1 fist decides then keeps from prescale 1/N events (deterministic prescaling)
        #setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_L1TSeedFinalDecision', cms.InputTag(_triggerFlagsModName+':L1TSeedFinalDecision')) # final L1 decision

else:
    # Lists of paths to monitor using emulator method with Muon dataset. This is using the orthogonal method.
    hltPathsWithTriggerFlags = [
      # the triggers go as : ["Numerator_name","Denominator_name"]
      # muon
      ['HLT_IsoMu27','HLT_IsoMu27'],
      # Lowest unprescaled Single Jet
      ['HLT_PFJet500','HLT_IsoMu27'],
      # HT
      # Lowest unprescaled HT
      ['HLT_PFHT1050','HLT_IsoMu27'],
      # MET MHT
      ['HLT_PFMET120_PFMHT120_IDTight','HLT_IsoMu27'],
      ['HLT_PFMET130_PFMHT130_IDTight','HLT_IsoMu27'],
      ['HLT_PFMET140_PFMHT140_IDTight','HLT_IsoMu27'],
      ['HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_FilterHF','HLT_IsoMu27'],
      ['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight','HLT_IsoMu27'],
      ['HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF','HLT_IsoMu27'],
      ['HLT_PFMETNoMu140_PFMHTNoMu140_IDTight','HLT_IsoMu27'],
      ['HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_FilterHF','HLT_IsoMu27'],
      # MET Only
      ['HLT_PFMET200_BeamHaloCleaned','HLT_IsoMu27'],
      ['HLT_PFMET200_NotCleaned','HLT_IsoMu27'],
      #['HLT_PFMET250_NotCleaned','HLT_IsoMu27'],
      ['HLT_PFMET300_NotCleaned','HLT_IsoMu27'],
    ]
    for _hltPathUnv in hltPathsWithTriggerFlags:
      _triggerFlagsModName = 'triggerFlags'+_hltPathUnv[0].replace('_','')
      setattr(process, _triggerFlagsModName, TriggerFlagsPrescalesProducer.clone(
        triggerResults = 'TriggerResults::HLT',
        ignorePathVersion = True,
        pathName = _hltPathUnv[0],
        denominatorPathName = 'HLT_IsoMu27',
        # options used for emulator method
        useEmulationFromDenominator = False,
        triggerObjects = cms.InputTag('slimmedPatTrigger'),
        emulatedThreshold = cms.double(extract_threshold(_hltPathUnv[0])),
      ))
      process.triggerFlagsTask.add(getattr(process, _triggerFlagsModName))

      # in the 
      #setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_L1TSeedAccept', cms.InputTag(_triggerFlagsModName+':L1TSeedAccept'))
      setattr(process.JMETriggerNTuple.bools, _hltPathUnv[0]+'_HLTPathAccept', cms.InputTag(_triggerFlagsModName+':HLTPathAccept'))
    

process.triggerFlagsSeq = cms.Sequence(process.triggerFlagsTask)

#process.fullPatMetSequencePuppi = cms.Sequence(process.fullPatMetTaskPuppi)

process.analysisCollectionsPath = cms.Path(
  process.userMuonsSequence
  + process.userJetsSeq
  #+ process.puppiMETSequence # for MET corrections
  #+ process.fullPatMetSequencePuppi  # for MET corrections
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

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
     
      # #"/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/f3854db9-8328-4591-b2e2-8a0cd34031fc.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/2a41298a-f240-421d-92a3-665f0a00a9da.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/90a54148-7f8b-40f3-ac77-e240a82b95d2.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/aea24369-2a7e-44c1-a476-8255ceeef295.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/fb66836e-3ee5-4995-9dc4-44357914dbf1.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/bc3bc8ef-e2af-4dcd-8e95-8bc0e5c98096.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/3e04bb3f-daf7-460d-9b91-eb20d9d5150c.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/71c228bb-fa00-4ab6-a257-88cf7a79b605.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/626/00000/20ce0b17-7996-466a-8b21-a1cb8106306e.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/2d683ffe-08fb-4d32-a1a8-03b849ffdbca.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/6a8b664d-57e7-42f5-bb16-ddad315c5ffb.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/569c8b9d-fb67-4932-bcb7-36928521a897.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/680be2a4-426f-4adb-8087-c24ce8fdf4bd.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/064338f3-6d48-4057-9791-4817d31044b2.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/627/00000/aa078748-9f12-4449-8c6f-8f46e260c33a.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/567/00000/24961d49-a692-4127-9f31-6c8f743fb0ac.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/567/00000/d0012944-3bfe-4635-966b-0d5df201f6e8.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/567/00000/7727ca8e-af85-4b14-95ad-7f08feaafe72.root",
      # "/store/data/Run2024D/JetMET1/MINIAOD/PromptReco-v1/000/380/620/00000/6fb8c3d9-625d-4af7-be14-b62858bfb066.root",
    
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/945/00000/106b7dab-0466-436c-9bbc-fc5d775c2b0b.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/945/00000/16f7a7a8-ed8b-47fd-99ef-af5d1ae192e0.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/947/00000/d878fa5e-9428-4561-a505-32146cd83aaf.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/945/00000/ffafb0c2-2e05-499f-9b9d-922be3d67a70.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/947/00000/bdb42e3e-422b-4ca9-9945-411e62a1b60c.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/945/00000/ffdb4e66-03e8-48eb-a665-40286a7cb70d.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/945/00000/f98c4569-1324-4370-9f8f-655fb69e2384.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/947/00000/fefcd741-9eb9-4cbe-a447-1e071322d54a.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/945/00000/618d3936-bdef-4c01-a631-0d62af74abc8.root",
    "/store/data/Run2024D/Muon1/MINIAOD/PromptReco-v1/000/380/947/00000/f1ba24bf-eae6-4d47-a014-f0119ea43801.root",
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
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
