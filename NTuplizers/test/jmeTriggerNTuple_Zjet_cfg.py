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

opts.register('useZMuSkim', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'apply the cuts used for producing ZMu skim samples (see DPGAnalysis/Skims/python/ZMuSkim_cff.py in CMSSSW)')

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
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_13_0_0_GRun_configDump_dataZjet import cms, process
  #from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_13_0_0_GRun_configDump import cms, process
  update_jmeCalibs = True
  #from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_13_0_0_GRun_configDump_noCustom import cms, process
  #update_jmeCalibs = False
  #process.hltParticleFlow.calibrationsLabel = ''
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
  #'MC_*AK8Calo*',
  #'HLT_PFJet*_v*',
  #'HLT_AK4PFJet*_v*',
  #'HLT_AK8PFJet*_v*',
  #'HLT_PFHT*_v*',
  #'HLT_PFMET*_PFMHT*_v*',
  #'AlCa_*',
  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*'
  'HLT_PFJet*_v*'
  'HLT_PFMetNoMu*_v*'
]

vetoPaths = [
  #'HLT_*ForPPRef_v*',
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
  # process.pfhcESSource = cms.ESSource('PoolDBESSource',
  #   _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/PFCalibration.db'),
  #   #_CondDB.clone(connect = 'sqlite_file:PFCalibration.db'),
  #   toGet = cms.VPSet(
  #     cms.PSet(
  #       record = cms.string('PFCalibrationRcd'),
  #       tag = cms.string('PFCalibration_CMSSW_13_0_0_HLT_126X_v4_mcRun3_2023'),
  #       label = cms.untracked.string('HLT'),
  #     ),
  #   ),
  # )
  # process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ##ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Run3Winter23Digi_OfflinePFHC.db'),
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
  outputBranchesToBeDropped = cms.vstring(),

  #HepMCProduct = cms.InputTag('generatorSmeared'),
  #GenEventInfoProduct = cms.InputTag('generator'),
  #PileupSummaryInfo = cms.InputTag('addPileupInfo'),

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
    offlinePrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
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
    hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    #hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    #hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

# recoPFClusterJetCollections = cms.PSet(

#   hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
#   hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

#   hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
#   hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
# ),

  recoPFJetCollections = cms.PSet(

    #hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),

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
    hltMuons = cms.InputTag('hltIterL3Muons'), # this collection uses the miniAOD definition muon::isLooseTriggerMuon(reco::Muon)
    offlineMuons = cms.InputTag('muons'), 
  ),

  patMuonCollections = cms.PSet(
    #offlineMuons = cms.InputTag('slimmedMuons')
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
if opts.useZMuSkim:
  # add Zmu skim cuts sequence
  ### HLT filter
  import copy
  from HLTrigger.HLTfilters.hltHighLevel_cfi import *
  from PhysicsTools.PatAlgos.producersLayer1.genericParticleProducer_cfi import patGenericParticles
  from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi import patMuons

  process.ZMuHLTFilter = copy.deepcopy(hltHighLevel)
  process.ZMuHLTFilter.throw = cms.bool(False)
  process.ZMuHLTFilter.HLTPaths = ["HLT_Mu*","HLT_IsoMu*"]

  ### Z -> MuMu candidates
  # Get muons of needed quality for Zs

  ###create a track collection with generic kinematic cuts
  process.looseMuonsForZMuSkim = cms.EDFilter("TrackSelector",
                              src = cms.InputTag("generalTracks"),
                              cut = cms.string('pt > 10 &&  abs(eta)<2.4 &&  (charge!=0)'),
                              filter = cms.bool(True)                                
                              )



  ###cloning the previous collection into a collection of candidates
  process.ConcretelooseMuonsForZMuSkim = cms.EDProducer("ConcreteChargedCandidateProducer",
                                                src = cms.InputTag("looseMuonsForZMuSkim"),
                                                particleType = cms.string("mu+")
                                                )



  ###create iso deposits
  process.tkIsoDepositTk = cms.EDProducer("CandIsoDepositProducer",
                                  src = cms.InputTag("ConcretelooseMuonsForZMuSkim"),
                                  MultipleDepositsFlag = cms.bool(False),
                                  trackType = cms.string('track'),
                                  ExtractorPSet = cms.PSet(
          #MIsoTrackExtractorBlock
          Diff_z = cms.double(0.2),
          inputTrackCollection = cms.InputTag("generalTracks"),
          BeamSpotLabel = cms.InputTag("offlineBeamSpot"),
          ComponentName = cms.string('TrackExtractor'),
          DR_Max = cms.double(0.5),
          Diff_r = cms.double(0.1),
          Chi2Prob_Min = cms.double(-1.0),
          DR_Veto = cms.double(0.01),
          NHits_Min = cms.uint32(0),
          Chi2Ndof_Max = cms.double(1e+64),
          Pt_Min = cms.double(-1.0),
          DepositLabel = cms.untracked.string('tracker'),
          BeamlineOption = cms.string('BeamSpotFromEvent')
          )
                                  )

  ###adding isodeposits to candidate collection
  process.allPatTracks = patGenericParticles.clone(
      src = cms.InputTag("ConcretelooseMuonsForZMuSkim"),
      # isolation configurables
      userIsolation = cms.PSet(
        tracker = cms.PSet(
          veto = cms.double(0.015),
          src = cms.InputTag("tkIsoDepositTk"),
          deltaR = cms.double(0.3),
          #threshold = cms.double(1.5)
        ),
        ),
      isoDeposits = cms.PSet(
          tracker = cms.InputTag("tkIsoDepositTk"),
          ),
      )




  ###create the "probe collection" of isolated tracks 
  process.looseIsoMuonsForZMuSkim = cms.EDFilter("PATGenericParticleSelector",  
                              src = cms.InputTag("allPatTracks"), 
                              cut = cms.string("(userIsolation('pat::TrackIso')/pt)<0.4"),
                              filter = cms.bool(True)
                              )



  ###create the "tag collection" of muon candidate, embedding the relevant infos  
  process.tightMuonsCandidateForZMuSkim = patMuons.clone(
      src = cms.InputTag("muons"),
      embedHighLevelSelection = cms.bool(True), 
  )

  ##apply ~tight muon ID 
  process.tightMuonsForZMuSkim = cms.EDFilter("PATMuonSelector",
                                      src = cms.InputTag("tightMuonsCandidateForZMuSkim"),       
                                      cut = cms.string('(pt > 28) &&  (abs(eta)<2.4) && (isPFMuon>0) && (isGlobalMuon = 1) && (globalTrack().normalizedChi2() < 10) && (globalTrack().hitPattern().numberOfValidMuonHits()>0)&& (numberOfMatchedStations() > 1)&& (innerTrack().hitPattern().numberOfValidPixelHits() > 0)&& (innerTrack().hitPattern().trackerLayersWithMeasurement() > 5) && (abs(dB)<0.2)  && ((isolationR03().sumPt/pt)<0.1)'),
                                      filter = cms.bool(True)                                
                                      )


  # build Z-> MuMu candidates
  process.dimuonsZMuSkim = cms.EDProducer("CandViewShallowCloneCombiner",
                          checkCharge = cms.bool(False),
                          cut = cms.string('(mass > 60) &&  (charge=0) && (abs(daughter(0).vz - daughter(1).vz) < 0.1)'),
                          decay = cms.string("tightMuonsForZMuSkim looseIsoMuonsForZMuSkim")
                          )                                    


  # Z filter
  process.dimuonsFilterZMuSkim = cms.EDFilter("CandViewCountFilter",
                              src = cms.InputTag("dimuonsZMuSkim"),
                              minNumber = cms.uint32(1)
                              )



  process.diMuonSelSeq = cms.Sequence(
                              process.ZMuHLTFilter *
                              process.looseMuonsForZMuSkim *
                              process.ConcretelooseMuonsForZMuSkim *
                              process.tkIsoDepositTk *
                              process.allPatTracks *
                              process.looseIsoMuonsForZMuSkim * 
                              process.tightMuonsCandidateForZMuSkim *
                              process.tightMuonsForZMuSkim *
                              process.dimuonsZMuSkim *
                              process.dimuonsFilterZMuSkim 
  )
  process.diMuonSelPath = cms.Path(process.diMuonSelSeq)
  process.schedule.append(process.diMuonSelPath)

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
    '/store/data/Run2023C/Muon0/RAW-RECO/ZMu-PromptReco-v4/000/367/770/00000/166a8559-ebd1-449d-a065-52fa13ea0f13.root',
    #'/store/mc/Run3Winter23Reco/DYToMuMu_M-20_TuneCP5_13p6TeV-pythia8/GEN-SIM-RECO/GTv4Digi_GTv4_126X_mcRun3_2023_forPU65_v4-v2/2820000/002b36bd-33fd-4bac-b77c-0c918047ec98.root'
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
    #'/store/mc/Run3Winter23Digi/DYToMuMu_M-20_TuneCP5_13p6TeV-pythia8/GEN-SIM-RAW/GTv4Digi_126X_mcRun3_2023_forPU65_v4-v2/2820000/ee1d0637-c9e4-4469-b769-646cc4beb50f.root'
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
