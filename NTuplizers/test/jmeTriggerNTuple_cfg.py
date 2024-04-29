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
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_3_0_GRun_configDump import cms, process
  update_jmeCalibs = False

elif opts.reco == 'HLT_Run3TRK':
  #from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_4_0_GRun_postEE_configDump import cms, process
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_13_0_0_GRun_configDump import cms, process
  #from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_13_0_0_GRun_doubletRecovery_configDump import cms, process
  update_jmeCalibs = True
  #process.GlobalTag.globaltag = cms.string('126X_mcRun3_2023_forPU65_v7')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT
  # Test option to skip forward PFHC application (after eta = 2.5)
  #process.hltParticleFlow.skipForwardCalibrations = cms.bool(True)
  #from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_13_0_0_GRun_configDump_noCustom import cms, process

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
  #'HLT_PFJet*_v*',
  #'HLT_AK4PFJet*_v*',
  #'HLT_AK8PFJet*_v*',
  #'HLT_PFHT*_v*',
  #'HLT_PFMET*_PFMHT*_v*',
  #'AlCa_*',
  #'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*'
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

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/PFCalibration.db'),
    #_CondDB.clone(connect = 'sqlite_file:PFCalibration.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_CMSSW_13_0_0_HLT_126X_v6_mcRun3_2023'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ##ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Run3Winter23Digi_OfflinePFHC.db'),
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Run3Winter23Digi_OfflinePFHC_skipFwd.db'),
    #_CondDB.clone(connect = 'sqlite_file:Run3Winter23Digi.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter23Digi_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter23Digi_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter23Digi_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter23Digi_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

# else:
#   ## ES modules for HLT JECs
#   process.jescESSource = cms.ESSource('PoolDBESSource',
#     _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/JESC_Run3Winter23Digi.db'),
#     toGet = cms.VPSet(
#       cms.PSet(
#         record = cms.string('JetCorrectionsRecord'),
#         tag = cms.string('JetCorrectorParametersCollection_Run3Winter23Digi_AK4PFHLT'),#!!
#         label = cms.untracked.string('AK4PFchsHLT'),
#       ),
#       cms.PSet(
#         record = cms.string('JetCorrectionsRecord'),
#         tag = cms.string('JetCorrectorParametersCollection_Run3Winter23Digi_AK8PFHLT'),#!!
#         label = cms.untracked.string('AK8PFchsHLT'),
#       ),
#     ),
#   )
#   process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')


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
  outputBranchesToBeDropped = cms.vstring(
  'hltAK4PFJets_jetArea',
  'hltAK4PFJets_jesc',
  'hltAK4PFJets_numberOfDaughters',
  'hltAK4PFJets_chargedHadronEnergyFraction',
  'hltAK4PFJets_neutralHadronEnergyFraction',
  'hltAK4PFJets_photonEnergyFraction',
  'hltAK4PFJets_muonEnergyFraction',
  'hltAK4PFJets_electronEnergyFraction',
  'hltAK4PFJets_chargedHadronMultiplicity',
  'hltAK4PFJets_neutralHadronMultiplicity',
  'hltAK4PFJets_photonMultiplicity',
  'hltAK4PFJets_muonMultiplicity',
  'hltAK4PFJets_electronMultiplicity',

  'hltAK4PFJetsCorrected_jetArea',
  'hltAK4PFJetsCorrected_jesc',
  'hltAK4PFJetsCorrected_numberOfDaughters',
  'hltAK4PFJetsCorrected_chargedHadronEnergyFraction',
  'hltAK4PFJetsCorrected_neutralHadronEnergyFraction',
  'hltAK4PFJetsCorrected_photonEnergyFraction',
  'hltAK4PFJetsCorrected_muonEnergyFraction',
  'hltAK4PFJetsCorrected_electronEnergyFraction',
  'hltAK4PFJetsCorrected_chargedHadronMultiplicity',
  'hltAK4PFJetsCorrected_neutralHadronMultiplicity',
  'hltAK4PFJetsCorrected_photonMultiplicity',
  'hltAK4PFJetsCorrected_muonMultiplicity',
  'hltAK4PFJetsCorrected_electronMultiplicity',

  'hltAK4CaloJets_jetArea',
  'hltAK4CaloJets_jesc',
  'hltAK4CaloJets_numberOfDaughters',
  'hltAK4CaloJets_chargedHadronEnergyFraction',
  'hltAK4CaloJets_neutralHadronEnergyFraction',
  'hltAK4CaloJets_photonEnergyFraction',
  'hltAK4CaloJets_muonEnergyFraction',
  'hltAK4CaloJets_electronEnergyFraction',
  'hltAK4CaloJets_chargedHadronMultiplicity',
  'hltAK4CaloJets_neutralHadronMultiplicity',
  'hltAK4CaloJets_photonMultiplicity',
  'hltAK4CaloJets_muonMultiplicity',
  'hltAK4CaloJets_electronMultiplicity',

  'hltAK4CaloJetsCorrected_jetArea',
  'hltAK4CaloJetsCorrected_jesc',
  'hltAK4CaloJetsCorrected_numberOfDaughters',
  'hltAK4CaloJetsCorrected_chargedHadronEnergyFraction',
  'hltAK4CaloJetsCorrected_neutralHadronEnergyFraction',
  'hltAK4CaloJetsCorrected_photonEnergyFraction',
  'hltAK4CaloJetsCorrected_muonEnergyFraction',
  'hltAK4CaloJetsCorrected_electronEnergyFraction',
  'hltAK4CaloJetsCorrected_chargedHadronMultiplicity',
  'hltAK4CaloJetsCorrected_neutralHadronMultiplicity',
  'hltAK4CaloJetsCorrected_photonMultiplicity',
  'hltAK4CaloJetsCorrected_muonMultiplicity',
  'hltAK4CaloJetsCorrected_electronMultiplicity',

  'hltAK8PFJets_jetArea',
  'hltAK8PFJets_jesc',
  'hltAK8PFJets_numberOfDaughters',
  'hltAK8PFJets_chargedHadronEnergyFraction',
  'hltAK8PFJets_neutralHadronEnergyFraction',
  'hltAK8PFJets_photonEnergyFraction',
  'hltAK8PFJets_muonEnergyFraction',
  'hltAK8PFJets_electronEnergyFraction',
  'hltAK8PFJets_chargedHadronMultiplicity',
  'hltAK8PFJets_neutralHadronMultiplicity',
  'hltAK8PFJets_photonMultiplicity',
  'hltAK8PFJets_muonMultiplicity',
  'hltAK8PFJets_electronMultiplicity',

  'hltAK8PFJetsCorrected_jetArea',
  'hltAK8PFJetsCorrected_jesc',
  'hltAK8PFJetsCorrected_numberOfDaughters',
  'hltAK8PFJetsCorrected_chargedHadronEnergyFraction',
  'hltAK8PFJetsCorrected_neutralHadronEnergyFraction',
  'hltAK8PFJetsCorrected_photonEnergyFraction',
  'hltAK8PFJetsCorrected_muonEnergyFraction',
  'hltAK8PFJetsCorrected_electronEnergyFraction',
  'hltAK8PFJetsCorrected_chargedHadronMultiplicity',
  'hltAK8PFJetsCorrected_neutralHadronMultiplicity',
  'hltAK8PFJetsCorrected_photonMultiplicity',
  'hltAK8PFJetsCorrected_muonMultiplicity',
  'hltAK8PFJetsCorrected_electronMultiplicity',

  'hltAK8CaloJets_jetArea',
  'hltAK8CaloJets_jesc',
  'hltAK8CaloJets_numberOfDaughters',
  'hltAK8CaloJets_chargedHadronEnergyFraction',
  'hltAK8CaloJets_neutralHadronEnergyFraction',
  'hltAK8CaloJets_photonEnergyFraction',
  'hltAK8CaloJets_muonEnergyFraction',
  'hltAK8CaloJets_electronEnergyFraction',
  'hltAK8CaloJets_chargedHadronMultiplicity',
  'hltAK8CaloJets_neutralHadronMultiplicity',
  'hltAK8CaloJets_photonMultiplicity',
  'hltAK8CaloJets_muonMultiplicity',
  'hltAK8CaloJets_electronMultiplicity',

  'hltAK8CaloJetsCorrected_jetArea',
  'hltAK8CaloJetsCorrected_jesc',
  'hltAK8CaloJetsCorrected_numberOfDaughters',
  'hltAK8CaloJetsCorrected_chargedHadronEnergyFraction',
  'hltAK8CaloJetsCorrected_neutralHadronEnergyFraction',
  'hltAK8CaloJetsCorrected_photonEnergyFraction',
  'hltAK8CaloJetsCorrected_muonEnergyFraction',
  'hltAK8CaloJetsCorrected_electronEnergyFraction',
  'hltAK8CaloJetsCorrected_chargedHadronMultiplicity',
  'hltAK8CaloJetsCorrected_neutralHadronMultiplicity',
  'hltAK8CaloJetsCorrected_photonMultiplicity',
  'hltAK8CaloJetsCorrected_muonMultiplicity',
  'hltAK8CaloJetsCorrected_electronMultiplicity',

  'offlineAK4PFPuppiJets_jetArea',
  'offlineAK4PFPuppiJets_jesc',
  'offlineAK4PFPuppiJets_numberOfDaughters',
  'offlineAK4PFPuppiJets_chargedHadronEnergyFraction',
  'offlineAK4PFPuppiJets_neutralHadronEnergyFraction',
  'offlineAK4PFPuppiJets_photonEnergyFraction',
  'offlineAK4PFPuppiJets_muonEnergyFraction',
  'offlineAK4PFPuppiJets_electronEnergyFraction',
  'offlineAK4PFPuppiJets_chargedHadronMultiplicity',
  'offlineAK4PFPuppiJets_neutralHadronMultiplicity',
  'offlineAK4PFPuppiJets_photonMultiplicity',
  'offlineAK4PFPuppiJets_muonMultiplicity',
  'offlineAK4PFPuppiJets_electronMultiplicity',

  'ak4GenJetsNoNu_jetArea',
  'ak4GenJetsNoNu_jesc',
  'ak4GenJetsNoNu_numberOfDaughters',
  'ak4GenJetsNoNu_chargedHadronEnergyFraction',
  'ak4GenJetsNoNu_neutralHadronEnergyFraction',
  'ak4GenJetsNoNu_photonEnergyFraction',
  'ak4GenJetsNoNu_muonEnergyFraction',
  'ak4GenJetsNoNu_electronEnergyFraction',
  'ak4GenJetsNoNu_chargedHadronMultiplicity',
  'ak4GenJetsNoNu_neutralHadronMultiplicity',
  'ak4GenJetsNoNu_photonMultiplicity',
  'ak4GenJetsNoNu_muonMultiplicity',
  'ak4GenJetsNoNu_electronMultiplicity',

  'ak8GenJetsNoNu_jetArea',
  'ak8GenJetsNoNu_jesc',
  'ak8GenJetsNoNu_numberOfDaughters',
  'ak8GenJetsNoNu_chargedHadronEnergyFraction',
  'ak8GenJetsNoNu_neutralHadronEnergyFraction',
  'ak8GenJetsNoNu_photonEnergyFraction',
  'ak8GenJetsNoNu_muonEnergyFraction',
  'ak8GenJetsNoNu_electronEnergyFraction',
  'ak8GenJetsNoNu_chargedHadronMultiplicity',
  'ak8GenJetsNoNu_neutralHadronMultiplicity',
  'ak8GenJetsNoNu_photonMultiplicity',
  'ak8GenJetsNoNu_muonMultiplicity',
  'ak8GenJetsNoNu_electronMultiplicity',
  ),

  HepMCProduct = cms.InputTag('generatorSmeared'),
  GenEventInfoProduct = cms.InputTag('generator'),
  PileupSummaryInfo = cms.InputTag('addPileupInfo'),

  doubles = cms.PSet(

    #hltFixedGridRhoFastjetAllCalo = cms.InputTag('hltFixedGridRhoFastjetAllCalo'),
    #hltFixedGridRhoFastjetAllPFCluster = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    hltFixedGridRhoFastjetAll = cms.InputTag('hltFixedGridRhoFastjetAll'),
    #offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    #hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('hltPixelVertices'),
    #hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    #hltVerticesPF = cms.InputTag('hltVerticesPF'),
    #offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
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

# recoPFClusterJetCollections = cms.PSet(

#   hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
#   hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

#   hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
#   hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
# ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
    #offlineAK4PFPuppiJets = cms.InputTag('ak4PFJetsPuppi'),
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

    #offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    #offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    #offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    #genMETCalo = cms.InputTag('genMetCalo::HLT'),
    #genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(

    #hltCaloMET = cms.InputTag('hltMet'),
    #hltCaloMETTypeOne = cms.InputTag('hltCaloMETTypeOne'),
  ),

# recoPFClusterMETCollections = cms.PSet(

#   hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
#   hltPFClusterMETTypeOne = cms.InputTag('hltPFClusterMETTypeOne'),
# ),

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
    #offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  recoMuonCollections = cms.PSet(
    #hltMuons = cms.InputTag('hltIterL3Muons'), # this collection uses the miniAOD definition muon::isLooseTriggerMuon(reco::Muon)
  )
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
    '/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2550000/000b8f39-b147-44c0-a2cb-a048abe5786c.root'
    #'/store/mc/Run3Winter23MiniAOD/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v2/2540000/10e9c9ff-b431-42c5-a1ec-e3143eafee20.root',
    #'/store/mc/Run3Winter23Digi/DYToMuMu_M-20_TuneCP5_13p6TeV-pythia8/GEN-SIM-RAW/GTv4Digi_126X_mcRun3_2023_forPU65_v4-v2/2820000/0070321e-e4e6-4769-900f-0c0ad3831215.root'
    #'/store/mc/Run3Winter23MiniAOD/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/126X_mcRun3_2023_forPU65_v1-v2/2550000/19e43825-6b8e-426e-9cca-e23cf318737c.root',
    #'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/033373ea-6628-4bd0-b0ce-a35145622552.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/1b0db43a-d38e-4e8b-8ad5-a2b255a54445.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/6259374b-6865-4dd4-9414-25e393cb30ae.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/8aae5414-96dc-414b-b277-e3da177b5fd6.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/1b62be66-8f21-4c37-ada8-0e9094b754c3.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/9292ed8b-e6e9-4e25-9ca2-bea39913b662.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/7f0077e6-e6f7-45bb-8d09-688fbe898716.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/33ca1f69-b3b2-4f6c-8505-66d405c7dc85.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/0379f27a-2c28-4e23-9d1f-beb1fbae45dd.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/216d41af-b3b1-4669-b496-682e7eefd6cb.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/6ef59234-3b07-49e4-96b3-03b499901f22.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/755f6116-2539-4d13-89cd-874fe989d755.root',
#'/store/mc/Run3Summer23DR/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to70_castor_130X_mcRun3_2023_realistic_v14-v1/2560003/6137a5b1-f72c-4fd0-93e5-2f2eaa238dc0.root',

  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    #'/store/mc/Run3Winter23Digi/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_126X_mcRun3_2023_forPU65_v1-v1/2560000/00d203d8-3ef3-4ca2-884d-a6b2f3bfbb6e.root',
    #
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/f61dc979-f42d-443f-8a1f-587b3353b109.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/e465ec59-571a-4dd5-b429-93b2b55f643b.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/f90d178a-8997-43ca-b9c9-edc49b733fcb.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/572aa6f8-a7a2-4db2-b332-5729c37ba743.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/5d2ccf3f-7f9f-4237-b210-a48c838dfa6a.root',
    # '/store/mc/Run3Winter23Digi/VBFHToInvisible_M-125_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/126X_mcRun3_2023_forPU65_v1-v2/40000/b17347c9-536a-4b06-9a68-f8199e76ddf2.root',
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
