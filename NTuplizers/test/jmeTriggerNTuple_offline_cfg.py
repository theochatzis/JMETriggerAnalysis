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

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('addTimingDQM', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'print results of FastTimerService, and produce corresponding DQM output file')

#opts.register('globalTag', None,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.string,
#              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'offline_reco',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('onlyTriggerResultsInNTuple', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'store only the trigger-results booleans in the output NTuple')

opts.register('trkdqm', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'added monitoring histograms for selected Track collections')

opts.register('pvdqm', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'added monitoring histograms for selected Vertex collections (partly, to separate output files)')

opts.register('pfdqm', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'added monitoring histograms for selected PF-Candidates')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### base configuration file
###

# customisation to change min-pT threshold of tracks in HLT reco
"""
def customisePhase2TrackingPtThresholds(process, ptMin):
  process.CkfBaseTrajectoryFilter_block.minPt = ptMin
  process.HLTIter0Phase2L3FromL1TkMuonGroupedCkfTrajectoryFilterIT.minPt = ptMin
  process.HLTPSetMuonCkfTrajectoryFilter.minPt = ptMin
  process.TrajectoryFilterForConversions.minPt = ptMin
  process.highPtTripletStepTrajectoryFilterBase.minPt = ptMin
  process.highPtTripletStepTrajectoryFilterInOut.minPt = ptMin
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryBuilder.minPt = ptMin
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterBase.minPt = ptMin
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterInOut.minPt = ptMin
  process.hltPhase2L3MuonInitialStepTrajectoryBuilder.minPt = ptMin
  process.hltPhase2L3MuonInitialStepTrajectoryFilter.minPt = ptMin
  process.initialStepTrajectoryFilter.minPt = ptMin
  process.muonSeededTrajectoryFilterForInOut.minPt = ptMin
  process.muonSeededTrajectoryFilterForOutIn.minPt = ptMin
  process.muonSeededTrajectoryFilterForOutInDisplaced.minPt = ptMin
  process.firstStepPrimaryVerticesUnsorted.TkFilterParameters.minPt = ptMin
  process.generalTracks.MinPT = ptMin
  process.highPtTripletStepTrackingRegions.RegionPSet.ptMin = ptMin
  process.hltPhase2L3MuonGeneralTracks.MinPT = ptMin
  process.hltPhase2L3MuonHighPtTripletStepTrackingRegions.RegionPSet.ptMin = ptMin
  process.hltPhase2L3MuonPixelTrackFilterByKinematics.ptMin = ptMin
  process.hltPhase2L3MuonPixelTracksFilter.ptMin = ptMin
  process.hltPhase2L3MuonPixelTracksTrackingRegions.RegionPSet.ptMin = ptMin
  process.pixelTrackFilterByKinematics.ptMin = ptMin
  process.pixelTracksTrackingRegions.RegionPSet.ptMin = ptMin
  process.trackWithVertexRefSelectorBeforeSorting.ptMin = ptMin
  process.unsortedOfflinePrimaryVertices.TkFilterParameters.minPt = ptMin
  return process
"""

# customisation to change min-E threshold of HGCal clusters in HLT reco
def customisePhase2HGCalClusterEnergyThresholds(process, eMin):
  process.hgcalLayerClusters.plugin.ecut = eMin
  return process

def loadProcess_HLT_75e33_TrkPtX_HGCEnX(thrScalingFactor_trk, thrScalingFactor_hgc):
  from JMETriggerAnalysis.Common.configs.HLT_75e33_TrkAndHGCalThresholdsTest_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process = customisePhase2TrackingPtThresholds(process, 0.9 * thrScalingFactor_trk)
  process = customisePhase2HGCalClusterEnergyThresholds(process, 3.0 * thrScalingFactor_hgc)
  return cms, process

# flag: skim original collection of generalTracks (only tracks associated to first N pixel vertices)
opt_skimTracks = False

opt_reco = opts.reco
if opt_reco.endswith('_skimmedTracks'):
  opt_reco = opt_reco[:-len('_skimmedTracks')]
  opt_skimTracks = True

if opt_reco == 'offline_reco':
  from JMETriggerAnalysis.Common.configs.offline_cfg_test import cms, process

elif opt_reco == 'HLT_TRKv00':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv00_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_TICL_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv02':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv02_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_TICL_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv06':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv06_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_TICL_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv06p1':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv06p1_TICL':
  #from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_TICL_cfg import cms, process
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_TICL_cfg_test import cms, process
  #process.schedule_().append(process.MC_JME)
  #process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv06p3':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p3_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv06p3_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p3_TICL_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv07p2':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv07p2_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_TRKv07p2_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv07p2_TICL_cfg import cms, process
  process.schedule_().append(process.MC_JME)
  process.schedule_().append(process.MC_JME_Others)

elif opt_reco == 'HLT_75e33':
  from HLTrigger.Phase2.HLT_75e33_cfg import cms, process
  process.schedule_().append(process.MC_JME)

elif opt_reco == 'HLT_75e33_TrkPtX1p00_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.00, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX1p25_HGCEnX1p25': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.25, 1.25)
elif opt_reco == 'HLT_75e33_TrkPtX1p50_HGCEnX1p50': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.50, 1.50)
elif opt_reco == 'HLT_75e33_TrkPtX1p75_HGCEnX1p75': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.75, 1.75)
elif opt_reco == 'HLT_75e33_TrkPtX2p00_HGCEnX2p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(2.00, 2.00)
elif opt_reco == 'HLT_75e33_TrkPtX1p50_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.50, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX2p00_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(2.00, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX1p00_HGCEnX1p50': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.00, 1.50)
elif opt_reco == 'HLT_75e33_TrkPtX1p00_HGCEnX2p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.00, 2.00)
elif opt_reco == 'HLT_75e33_TrkPtX9p99_HGCEnX9p99': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(9.99, 9.99)
elif opt_reco == 'HLT_75e33_TrkPtX9p99_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(9.99, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX1p00_HGCEnX9p99': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(1.00, 9.99)

elif opt_reco == 'HLT_75e33_TrkPtX2p50_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(2.50, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX3p00_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(3.00, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX3p50_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(3.50, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX4p00_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(4.00, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX5p00_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(5.00, 1.00)
elif opt_reco == 'HLT_75e33_TrkPtX6p00_HGCEnX1p00': cms, process = loadProcess_HLT_75e33_TrkPtX_HGCEnX(6.00, 1.00)

else:
  raise RuntimeError('invalid argument for option "reco": "'+opt_reco+'"')

###
### analysis sequence
###

## JMETrigger NTuple
#from HLTrigger.JetMET.hltSiPixelClusterMultiplicityValueProducer_cfi import hltSiPixelClusterMultiplicityValueProducer as _hltSiPixelClusterMultiplicityValueProducer
#from HLTrigger.JetMET.hltSiPhase2TrackerClusterMultiplicityValueProducer_cfi import hltSiPhase2TrackerClusterMultiplicityValueProducer as _hltSiPhase2TrackerClusterMultiplicityValueProducer

#from JMETriggerAnalysis.Common.hltTrackMultiplicityValueProducer_cfi import hltTrackMultiplicityValueProducer as _hltTrackMultiplicityValueProducer
#from JMETriggerAnalysis.Common.hltVertexMultiplicityValueProducer_cfi import hltVertexMultiplicityValueProducer as _hltVertexMultiplicityValueProducer

#if not hasattr(process, 'hltPixelClustersMultiplicity'):
#  process.hltPixelClustersMultiplicity = _hltSiPixelClusterMultiplicityValueProducer.clone(src = 'siPixelClusters', defaultValue = -1.)

#if not hasattr(process, 'hltOuterTrackerClustersMultiplicity'):
#  process.hltOuterTrackerClustersMultiplicity = _hltSiPhase2TrackerClusterMultiplicityValueProducer.clone(src = 'siPhase2Clusters', defaultValue = -1.)

#process.hltPixelTracksMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'pixelTracks', defaultValue = -1.)
##process.hltPixelTracksCleanerMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'pixelTracksCleaner', defaultValue = -1.)
#process.hltPixelTracksMergerMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'pixelTracksMerger', defaultValue = -1.)
#process.hltTracksMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'generalTracks', defaultValue = -1.)

#process.hltPixelVerticesMultiplicity = _hltVertexMultiplicityValueProducer.clone(src = 'pixelVertices', defaultValue = -1.)
#process.hltPrimaryVerticesMultiplicity = _hltVertexMultiplicityValueProducer.clone(src = 'offlinePrimaryVertices', defaultValue = -1.)
#process.offlinePrimaryVerticesMultiplicity = _hltVertexMultiplicityValueProducer.clone(src = 'offlineSlimmedPrimaryVertices', defaultValue = -1.)

# removed because of non existing HLTrigger.mcStitching anymore which contained a stitchingWeight_cfi
# must do this to work :
#mkdir -p HLTrigger
#git clone https://github.com/veelken/mcStitching.git HLTrigger/mcStitching
#from JMETriggerAnalysis.NTuplizers.qcdWeightProducer import qcdWeightProducer
#process.qcdWeightPU140 = qcdWeightProducer(BXFrequency = 30. * 1e6, PU = 140.)
#process.qcdWeightPU200 = qcdWeightProducer(BXFrequency = 30. * 1e6, PU = 200.)
"""
process.jmeTriggerNTupleInputsSeq = cms.Sequence(
    process.hltPixelClustersMultiplicity
  + process.hltOuterTrackerClustersMultiplicity
  + process.hltPixelTracksMultiplicity
  + process.hltPixelTracksCleanerMultiplicity
  + process.hltPixelTracksMergerMultiplicity
  + process.hltTracksMultiplicity
  + process.hltPixelVerticesMultiplicity
  + process.hltPrimaryVerticesMultiplicity
  + process.offlinePrimaryVerticesMultiplicity
  #+ process.qcdWeightPU140 # see above mcStitching
  #+ process.qcdWeightPU200
)
"""


#process.jmeTriggerNTupleInputsPath = cms.Path(process.jmeTriggerNTuple_cfg.py)
#process.schedule_().append(process.jmeTriggerNTupleInputsPath)



ak4jets_stringCut = '' #'pt > 20'
ak8jets_stringCut = '' #'pt > 80'

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple_offline',

  TTreeName = cms.string('Events'),

  
  TriggerResults = cms.InputTag('TriggerResults'),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(
    'MC_JME',
    'L1T_SinglePFPuppiJet200off',
    'HLT_AK4PFJet520',
    'HLT_AK4PFCHSJet520',
    'HLT_AK4PFPuppiJet520',
    'L1T_PFPuppiHT450off',
    'HLT_PFPuppiHT1070',
    'L1T_PFPuppiMET200off',
    'L1T_PFPuppiMET245off',
    'HLT_PFMET250',
    'HLT_PFCHSMET250',
    'HLT_PFPuppiMET250',
    'HLT_PFPuppiMET140',
    'HLT_PFPuppiMET140_PFPuppiMHT140',
    'HLT_PFPuppiMET140_PFPuppiMHT140_PFPuppiHT60',
    'HLT_PFPuppiMETTypeOne140_PFPuppiMHT140',
  ),
  

  fillCollectionConditions = cms.PSet(),

  HepMCProduct = cms.InputTag('generatorSmeared'),
  GenEventInfoProduct = cms.InputTag('generator'),
  PileupSummaryInfo = cms.InputTag('addPileupInfo'),

  doubles = cms.PSet(
    
    #qcdWeightPU140 = cms.InputTag('qcdWeightPU140'),
    #qcdWeightPU200 = cms.InputTag('qcdWeightPU200'),
    
    #fixedGridRhoFastjetAllTmp = cms.InputTag('fixedGridRhoFastjetAllTmp'),
    #offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),
    #hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
    #hltOuterTrackerClustersMultiplicity = cms.InputTag('hltOuterTrackerClustersMultiplicity'),
    #hltPixelTracksMultiplicity = cms.InputTag('hltPixelTracksMultiplicity'),
    #hltPixelTracksCleanerMultiplicity = cms.InputTag('hltPixelTracksCleanerMultiplicity'),
    #hltPixelTracksMergerMultiplicity = cms.InputTag('hltPixelTracksMergerMultiplicity'),
    #hltTracksMultiplicity = cms.InputTag('hltTracksMultiplicity'),
    #hltPixelVerticesMultiplicity = cms.InputTag('hltPixelVerticesMultiplicity'),
    #hltPrimaryVerticesMultiplicity = cms.InputTag('hltPrimaryVerticesMultiplicity'),
    #offlinePrimaryVerticesMultiplicity = cms.InputTag('offlinePrimaryVerticesMultiplicity'),
    
  ),

  vdoubles = cms.PSet(

#    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
#    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
#    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
#    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms'),
  ),

  recoVertexCollections = cms.PSet(

   #hltPixelVertices = cms.InputTag('pixelVertices'),
   #hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
   offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
   offlineSlimmedPrimaryVertices4D = cms.InputTag('offlineSlimmedPrimaryVertices4D'),
  ),

#  l1tPFCandidateCollections = cms.PSet(

#   l1tPFPuppi = cms.InputTag('l1pfCandidates', 'Puppi'),
 # ),

#  recoPFCandidateCollections = cms.PSet(

#    hltPFSim = cms.InputTag('simPFProducer'),
#    hltPFTICL = cms.InputTag('pfTICL'),
#    hltParticleFlow = cms.InputTag('particleFlowTmp'),
#    hltPFPuppi = cms.InputTag('hltPFPuppi'),
#    hltPFPuppiNoLep = cms.InputTag('hltPFPuppiNoLep'),
#  ),

  patPackedCandidateCollections = cms.PSet(

    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(
    ak4GenJets = cms.InputTag('slimmedGenJets'), 
    #ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    #ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

#  l1tPFJetCollections = cms.PSet(

#   l1tAK4CaloJetsCorrected = cms.InputTag('ak4PFL1CaloCorrected'),
#   l1tAK4PFJetsCorrected = cms.InputTag('ak4PFL1PFCorrected'),
#    l1tAK4PFPuppiJetsCorrected = cms.InputTag('ak4PFL1PuppiCorrected'),
#  ),

#  recoCaloJetCollections = cms.PSet(

#    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
#    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),

#    l1tSlwPFPuppiJets = cms.InputTag('l1tSlwPFPuppiJets', 'UncalibratedPhase1L1TJetFromPfCandidates'),
#    l1tSlwPFPuppiJetsCorrected = cms.InputTag('l1tSlwPFPuppiJetsCorrected', 'Phase1L1TJetFromPfCandidates'),
#  ),

#  recoPFClusterJetCollections = cms.PSet(

#   hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
#   hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
#  ),

 # recoPFJetCollections = cms.PSet(

#    l1tAK4CaloJets = cms.InputTag('ak4PFL1Calo'),
#    l1tAK4PFJets = cms.InputTag('ak4PFL1PF'),
#    l1tAK4PFPuppiJets = cms.InputTag('ak4PFL1Puppi'),

#    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
#    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
#    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
#    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
#    hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),
#    hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),
#    hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
#    hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),
#    hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
#    hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
#  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    #offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

#  recoGenMETCollections = cms.PSet(

#    genMETCalo = cms.InputTag('genMetCalo::HLT'),
#    genMETTrue = cms.InputTag('genMetTrue::HLT'),
#  ),

 # recoMETCollections = cms.PSet(

 #   l1tPFPuppiHT = cms.InputTag('l1tPFPuppiHT'),
 #   hltPFPuppiHT = cms.InputTag('hltPFPuppiHT'),
 #   hltPFPuppiMHT = cms.InputTag('hltPFPuppiMHT'),
 # ),

 # recoCaloMETCollections = cms.PSet(

 #   hltCaloMET = cms.InputTag('hltCaloMET'),
 # ),

 # recoPFClusterMETCollections = cms.PSet(

#   hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
 # ),

 # recoPFMETCollections = cms.PSet(

 #   l1tCaloMET = cms.InputTag('l1PFMetCalo'),
 #   l1tPFMET = cms.InputTag('l1PFMetPF'),
 #   l1tPFPuppiMET = cms.InputTag('l1PFMetPuppi'),

 #   hltPFMET = cms.InputTag('hltPFMET'),
 #   hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
 #   hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
 #   hltPFSoftKillerMET = cms.InputTag('hltPFSoftKillerMET'),
 #   hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
 #   hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
 #   hltPFPuppiMETv0 = cms.InputTag('hltPFPuppiMETv0'),
 # ),

  patMETCollections = cms.PSet(

    offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

#  patMuonCollections = cms.PSet(

#   offlineIsolatedMuons = cms.InputTag('userIsolatedMuons'),
#  ),

#  patElectronCollections = cms.PSet(

#   offlineIsolatedElectrons = cms.InputTag('userIsolatedElectrons'),
#  ),

  stringCutObjectSelectors = cms.PSet(
    # GEN
    ak4GenJetsNoNu = cms.string(''),
    ak8GenJetsNoNu = cms.string(''),

    # L1T AK4
#    l1tAK4CaloJets = cms.string(ak4jets_stringCut),
#    l1tAK4PFJets = cms.string(ak4jets_stringCut),
#    l1tAK4PFPuppiJets = cms.string(ak4jets_stringCut),
#    l1tSlwPFPuppiJets = cms.string(ak4jets_stringCut),

#    l1tAK4CaloJetsCorrected = cms.string(ak4jets_stringCut),
#    l1tAK4PFJetsCorrected = cms.string(ak4jets_stringCut),
#    l1tAK4PFPuppiJetsCorrected = cms.string(ak4jets_stringCut),
#    l1tSlwPFPuppiJetsCorrected = cms.string(ak4jets_stringCut),

    # HLT AK4
#    hltAK4CaloJets = cms.string(ak4jets_stringCut),
#    hltAK4PFClusterJets = cms.string(ak4jets_stringCut),
#    hltAK4PFJets = cms.string(ak4jets_stringCut),
#    hltAK4PFJetsCorrected = cms.string(ak4jets_stringCut),
#    hltAK4PFCHSJetsCorrected = cms.string(ak4jets_stringCut),
#    hltAK4PFPuppiJetsCorrected = cms.string(ak4jets_stringCut),

    # HLT AK8
#    hltAK8CaloJets = cms.string(ak8jets_stringCut),
#    hltAK8PFClusterJets = cms.string(ak8jets_stringCut),
#    hltAK8PFJetsCorrected = cms.string(ak8jets_stringCut),
#    hltAK8PFCHSJetsCorrected = cms.string(ak8jets_stringCut),
#    hltAK8PFPuppiJetsCorrected = cms.string(ak8jets_stringCut),

    # Offline
    offlineAK4PFCHSJetsCorrected = cms.string(ak4jets_stringCut),
    offlineAK4PFPuppiJetsCorrected = cms.string(ak4jets_stringCut),
    offlineAK8PFPuppiJetsCorrected = cms.string(ak8jets_stringCut),
  ),

 outputBranchesToBeDropped = cms.vstring(

    'genMETCalo_MuonEtFraction',
    'genMETCalo_InvisibleEtFraction',
  ),
)

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule_().extend([process.analysisNTupleEndPath])

#process.schedule_().remove(process.MC_JME)
#process.schedule_().remove(process.jmeTriggerNTupleInputsPath)
#process.schedule_().remove(process.analysisNTupleEndPath)
#
#process.setSchedule_(cms.Schedule(
#  process.l1tReconstructionPath,
#  process.HLT_AK4PFPuppiJet520,
#  process.HLT_PFPuppiHT1070,
#  process.HLT_PFPuppiMET140_PFPuppiMHT140,
#))

# JMETriggerNTuple: save only TriggerResults
"""
if opts.onlyTriggerResultsInNTuple:
   # reset input collections
   process.JMETriggerNTuple.doubles = cms.PSet()
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet()
   process.JMETriggerNTuple.l1tPFCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.patPackedCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.recoGenJetCollections = cms.PSet()
   process.JMETriggerNTuple.l1tPFJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoCaloJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFClusterJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFJetCollections = cms.PSet()
   process.JMETriggerNTuple.patJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoGenMETCollections = cms.PSet()
   process.JMETriggerNTuple.recoCaloMETCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFClusterMETCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFMETCollections = cms.PSet()
   process.JMETriggerNTuple.patMETCollections = cms.PSet()
   process.JMETriggerNTuple.patMuonCollections = cms.PSet()
   process.JMETriggerNTuple.patElectronCollections = cms.PSet()
"""
# FastTimerService
if opts.addTimingDQM:
   from HLTrigger.Timer.FastTimer import customise_timer_service, customise_timer_service_print
   process = customise_timer_service(process)
   process = customise_timer_service_print(process)
   import os
   process.dqmOutput.fileName = os.path.splitext(opts.output)[0]+'_DQM.root'
   process.FastTimerService.dqmTimeRange            = 20000.
   process.FastTimerService.dqmTimeResolution       =    10.
   process.FastTimerService.dqmPathTimeRange        = 10000.
   process.FastTimerService.dqmPathTimeResolution   =     5.
   process.FastTimerService.dqmModuleTimeRange      =  1000.
   process.FastTimerService.dqmModuleTimeResolution =     1.

## update process.GlobalTag.globaltag
#if opts.globalTag is not None:
#   raise RuntimeError('command-line argument "globalTag='+opts.globalTag+'" will overwrite process.GlobalTag (previous customizations of it will be lost)')
#   from Configuration.AlCa.GlobalTag import GlobalTag
#   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 1)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JMETriggerNTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

"""
# Tracking Monitoring
if opts.trkdqm > 0:

   if opt_reco in ['HLT_TRKv00', 'HLT_TRKv00_TICL', 'HLT_TRKv02', 'HLT_TRKv02_TICL']:
      process.reconstruction_pixelTrackingOnly_step = cms.Path(process.reconstruction_pixelTrackingOnly)
      process.schedule_().extend([process.reconstruction_pixelTrackingOnly_step])

   from JMETriggerAnalysis.Common.trackHistogrammer_cfi import trackHistogrammer
   process.TrackHistograms_hltPixelTracks = trackHistogrammer.clone(src = 'pixelTracks')
   process.TrackHistograms_hltInitialStepTracks = trackHistogrammer.clone(src = 'initialStepTracks')
   process.TrackHistograms_hltGeneralTracks = trackHistogrammer.clone(src = 'generalTracks')

   process.trkMonitoringSeq = cms.Sequence(
       process.TrackHistograms_hltPixelTracks
     + process.TrackHistograms_hltInitialStepTracks
     + process.TrackHistograms_hltGeneralTracks
   )

   if opt_skimTracks:
      process.TrackHistograms_hltGeneralTracksOriginal = trackHistogrammer.clone(src = 'generalTracksOriginal')
      process.trkMonitoringSeq += process.TrackHistograms_hltGeneralTracksOriginal

   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)
   process.schedule_().extend([process.trkMonitoringEndPath])

# Vertexing monitoring
if opts.pvdqm > 0:

   from JMETriggerAnalysis.Common.vertexHistogrammer_cfi import vertexHistogrammer
   process.VertexHistograms_hltPixelVertices = vertexHistogrammer.clone(src = 'pixelVertices')
   process.VertexHistograms_hltTrimmedPixelVertices = vertexHistogrammer.clone(src = 'trimmedPixelVertices')
   process.VertexHistograms_hltPrimaryVertices = vertexHistogrammer.clone(src = 'offlinePrimaryVertices')
   process.VertexHistograms_offlinePrimaryVertices = vertexHistogrammer.clone(src = 'offlineSlimmedPrimaryVertices')

   process.pvMonitoringSeq = cms.Sequence(
       process.VertexHistograms_hltPixelVertices
     + process.VertexHistograms_hltTrimmedPixelVertices
     + process.VertexHistograms_hltPrimaryVertices
     + process.VertexHistograms_offlinePrimaryVertices
   )

   if opts.pvdqm > 1:

      if not hasattr(process, 'tpClusterProducer'):
         from SimTracker.TrackerHitAssociation.tpClusterProducer_cfi import tpClusterProducer as _tpClusterProducer
         process.tpClusterProducer = _tpClusterProducer.clone()

      from SimTracker.TrackAssociatorProducers.quickTrackAssociatorByHits_cfi import quickTrackAssociatorByHits as _quickTrackAssociatorByHits
      process.quickTrackAssociatorByHits = _quickTrackAssociatorByHits.clone()

      from SimTracker.TrackAssociation.trackingParticleRecoTrackAsssociation_cfi import trackingParticleRecoTrackAsssociation as _trackingParticleRecoTrackAsssociation
      process.trackingParticleRecoTrackAsssociation = _trackingParticleRecoTrackAsssociation.clone()

      process.trackingParticlePixelTrackAssociation = cms.EDProducer('TrackAssociatorEDProducer',
        associator = cms.InputTag('quickTrackAssociatorByHits'),
        ignoremissingtrackcollection = cms.untracked.bool(False),
        label_tp = cms.InputTag('mix', 'MergedTrackTruth'),
        label_tr = cms.InputTag('pixelTracks')
      )

      process.trkTruthInfoSeq = cms.Sequence(
          process.tpClusterProducer
        + process.quickTrackAssociatorByHits
        + process.trackingParticleRecoTrackAsssociation
        + process.trackingParticlePixelTrackAssociation
      )

      process.trkTruthInfoPath = cms.Path(process.trkTruthInfoSeq)
      process.schedule_().extend([process.trkTruthInfoPath])

      if hasattr(process, 'pixelVertices') or hasattr(process, 'trimmedPixelVertices'):
         process.pvAnalyzer1 = cms.EDAnalyzer('PrimaryVertexAnalyzer4PU',
           info = cms.untracked.string(opts.reco),
           f4D = cms.untracked.bool(False),
           beamSpot = cms.InputTag('offlineBeamSpot'),
           simG4 = cms.InputTag('g4SimHits'),
           outputFile = cms.untracked.string('pv_hltPixelVertices.root'),
           verbose = cms.untracked.bool(False),
           veryverbose = cms.untracked.bool(False),
           recoTrackProducer = cms.untracked.string('pixelTracks'),
           minNDOF = cms.untracked.double(-1),
           zmatch = cms.untracked.double(0.05),
           autodump = cms.untracked.int32(0),
           nDump = cms.untracked.int32(0),
           nDumpTracks = cms.untracked.int32(0),
           RECO = cms.untracked.bool(False),
           track_timing = cms.untracked.bool(True),
           TkFilterParameters = cms.PSet(
             maxD0Error = cms.double(999.0),
             maxD0Significance = cms.double(999.0),
             maxDzError = cms.double(999.0),
             maxEta = cms.double(4.0),
             maxNormalizedChi2 = cms.double(999.0),
             minPixelLayersWithHits = cms.int32(2),
             minPt = cms.double(1.0),
             minSiliconLayersWithHits = cms.int32(-1),
             trackQuality = cms.string('any')
           ),
           trackingParticleCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
           trackingVertexCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
           trackAssociatorMap = cms.untracked.InputTag('trackingParticlePixelTrackAssociation'),
           TrackTimesLabel = cms.untracked.InputTag('tofPID4DnoPID:t0safe'), # as opposed to 'tofPID:t0safe'
           TrackTimeResosLabel = cms.untracked.InputTag('tofPID4DnoPID:sigmat0safe'),
           vertexAssociator = cms.untracked.InputTag(''),
           useVertexFilter = cms.untracked.bool(False),
           compareCollections = cms.untracked.int32(0),
           vertexRecoCollections = cms.VInputTag(),
         )

         for _tmp in ['pixelVertices', 'trimmedPixelVertices']:
           if hasattr(process, _tmp):
             process.pvAnalyzer1.vertexRecoCollections += [_tmp]

         process.pvMonitoringSeq += process.pvAnalyzer1

      if hasattr(process, 'offlinePrimaryVertices'):
         process.pvAnalyzer2 = cms.EDAnalyzer('PrimaryVertexAnalyzer4PU',
           info = cms.untracked.string(opts.reco),
           f4D = cms.untracked.bool(False),
           beamSpot = cms.InputTag('offlineBeamSpot'),
           simG4 = cms.InputTag('g4SimHits'),
           outputFile = cms.untracked.string('pv_hltPrimaryVertices.root'),
           verbose = cms.untracked.bool(False),
           veryverbose = cms.untracked.bool(False),
           recoTrackProducer = cms.untracked.string('generalTracks'),
           minNDOF = cms.untracked.double(4.0),
           zmatch = cms.untracked.double(0.05),
           autodump = cms.untracked.int32(0),
           nDump = cms.untracked.int32(0),
           nDumpTracks = cms.untracked.int32(0),
           RECO = cms.untracked.bool(False),
           track_timing = cms.untracked.bool(True),
           TkFilterParameters = cms.PSet(
             maxD0Error = cms.double(1.0),
             maxD0Significance = cms.double(4.0),
             maxDzError = cms.double(1.0),
             maxEta = cms.double(4.0),
             maxNormalizedChi2 = cms.double(10.0),
             minPixelLayersWithHits = cms.int32(2),
             minPt = cms.double(0.0),
             minSiliconLayersWithHits = cms.int32(5),
             trackQuality = cms.string('any')
           ),
           trackingParticleCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
           trackingVertexCollection = cms.untracked.InputTag('mix', 'MergedTrackTruth'),
           trackAssociatorMap = cms.untracked.InputTag('trackingParticleRecoTrackAsssociation'),
           TrackTimesLabel = cms.untracked.InputTag('tofPID4DnoPID:t0safe'),  # as opposed to 'tofPID:t0safe'
           TrackTimeResosLabel = cms.untracked.InputTag('tofPID4DnoPID:sigmat0safe'),
           vertexAssociator = cms.untracked.InputTag(''),
           useVertexFilter = cms.untracked.bool(False),
           compareCollections = cms.untracked.int32(0),
           vertexRecoCollections = cms.VInputTag(
             'offlinePrimaryVertices',
           ),
         )
         process.pvMonitoringSeq += process.pvAnalyzer2

   process.pvMonitoringEndPath = cms.EndPath(process.pvMonitoringSeq)
   process.schedule_().extend([process.pvMonitoringEndPath])

# ParticleFlow Monitoring
if opts.pfdqm > 0:

   from JMETriggerAnalysis.Common.pfCandidateHistogrammerRecoPFCandidate_cfi import pfCandidateHistogrammerRecoPFCandidate
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate
   from JMETriggerAnalysis.Common.leafCandidateHistogrammer_cfi import leafCandidateHistogrammer

   _candTags = [
     ('_offlineParticleFlow', 'packedPFCandidates', '', pfCandidateHistogrammerPatPackedCandidate),
     ('_hltParticleFlow', 'particleFlowTmp', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPFPuppi', 'hltPFPuppi', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
     ('_l1tParticleFlow', 'l1pfCandidates:PF', '', leafCandidateHistogrammer),
     ('_l1tPFPuppi', 'l1pfCandidates:Puppi', '(pt > 0)', leafCandidateHistogrammer),
   ]

   if 'TICL' in opt_reco:
      _candTags += [
        ('_pfTICL', 'pfTICL', '', pfCandidateHistogrammerRecoPFCandidate),
      ]
   else:
      _candTags += [
        ('_simPFProducer', 'simPFProducer', '', pfCandidateHistogrammerRecoPFCandidate),
      ]

   if opts.pfdqm > 2:
      _tmpCandTags = []
      for _tmp in _candTags:
          _tmpCandTags += [(_tmp[0]+'_2GeV', _tmp[1], '(pt > 2.)', _tmp[3])]
      _candTags += _tmpCandTags
      del _tmpCandTags

   _regTags = [
     ['', ''],
     ['_HB'   , '(0.0<=abs(eta) && abs(eta)<1.5)'],
     ['_HGCal', '(1.5<=abs(eta) && abs(eta)<3.0)'],
     ['_HF'   , '(3.0<=abs(eta) && abs(eta)<5.0)'],
   ]

   _pidTags = [['', '']]
   if opts.pfdqm > 1:
      _pidTags += [
        ['_h', '(abs(pdgId) == 211)'],
        ['_e', '(abs(pdgId) == 11)'],
        ['_mu', '(abs(pdgId) == 13)'],
        ['_gamma', '(abs(pdgId) == 22)'],
        ['_h0', '(abs(pdgId) == 130)'],
      ]

   process.pfMonitoringSeq = cms.Sequence()
   for _candTag in _candTags:
     for _regTag in _regTags:
       for _pidTag in _pidTags:
         _modName = 'PFCandidateHistograms'+_candTag[0]+_regTag[0]+_pidTag[0]
         setattr(process, _modName, _candTag[3].clone(
           src = _candTag[1],
           cut = ' && '.join([_tmp for _tmp in [_candTag[2], _regTag[1], _pidTag[1]] if _tmp]),
         ))
         process.pfMonitoringSeq += getattr(process, _modName)

   process.pfMonitoringEndPath = cms.EndPath(process.pfMonitoringSeq)
   process.schedule_().extend([process.pfMonitoringEndPath])
"""
# MessageLogger
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     # scram b USER_CXXFLAGS="-DEDM_ML_DEBUG"
     debugModules = cms.untracked.vstring(
       'JMETriggerNTuple',
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
   )

   if opt_skimTracks:
      process.MessageLogger.debugModules += [
        'hltTrimmedPixelVertices',
        'generalTracks',
      ]

# EDM Input Files
if opts.inputFiles and opts.secondaryInputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = opts.secondaryInputFiles
elif opts.inputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = []
else:
   process.source.fileNames = [
#    '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/280000/007CCF38-CBE4-6B4D-A97A-580FA0CA0850.root',
#    '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/VBF_HToInvisible_M125_14TeV_powheg_pythia8_TuneCP5/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/FC63C96F-0685-B846-BD3C-F60F85AFFB4B.root',
#    '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/FEVT/PU200_castor_111X_mcRun4_realistic_T15_v1-v1/100000/005010D5-6DF5-5E4A-89A3-30FEE02E40F8.root'
#     '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/FEVT/PU200_castor_111X_mcRun4_realistic_T15_v1-v1/100000/005010D5-6DF5-5E4A-89A3-30FEE02E40F8.root'
#    '/store/group/phys_egamma/sobhatta/egamma_timing_studies/samples/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_Phase2HLTTDRWinter20DIGI-PU200_castor_110X_mcRun4_realistic_v3-v2_GEN-SIM-DIGI-RAW_2021-12-06_23-04-36/output_1.root'

      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/MINIAODSIM/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/c354eb33-0710-4697-959d-6ae6ffa27946.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/MINIAODSIM/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/fc9599f3-9048-4d21-9dac-6f5b609dd197.root'
   
   ]
   process.source.secondaryFileNames = [

  
   
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/03a1db66-fb19-4832-8825-f98f0a6122c1.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/06b322e5-89de-4d9f-967a-a4843fff6eba.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/1049741a-5b18-4bd7-925a-543324c86499.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/7282fafb-31e8-4072-af96-402e7a889c9a.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/7b600534-2724-4c34-a970-903f5675f135.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/87b1cb2c-39d8-46d5-9f5d-36bead06ad6c.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/8ea05f50-b5ef-47b5-a9a9-6b79752cd4bc.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/b2136d4b-7bb9-4674-9cf5-689757fbdff6.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/d6f15a85-a6e8-4366-9826-34836a28f4d4.root',
     '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/f8c1743e-94af-4707-a02f-be1b74001178.root',
    
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/039041cd-52ec-4b41-9e2c-28a4ca1e61ed.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/0442828e-6d38-4310-a2ce-d2f667c09a7f.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/0a037338-984c-4d66-952f-fbe8fe2cf2b2.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/0a884b3d-e426-427f-8bdb-ff7624beccca.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/13d3b4d7-c86f-4780-9287-d5efb42bda93.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/18e07719-4814-4520-8e6f-4aabab47c7b3.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/1aed794c-c8bd-4b76-b124-d3d7d5049a38.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/1c069818-c881-4346-bdc5-63cffb006a45.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/205595b3-dc74-4d83-9d6a-d02266feb5a3.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/2214afa9-eb0f-4f1c-b823-dfb93fb924bc.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/22a33b17-a02e-400a-a258-924382fe3c67.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/2383d7d6-7407-484f-9990-0f12a5c77d68.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/238aeeae-6092-4032-91d0-934c9d08bfbe.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/2e37c407-ccf9-4504-9bc0-89a0e50f3209.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/2e6b544f-81d5-4bd1-817a-c2637816885d.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/30b2d988-4ccd-4e64-a4ac-06e1459d0bdb.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/343a23ef-5e39-4f8c-ba08-15b2497297e2.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/40118641-715e-453b-9c31-6777a5d89ee4.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/462784a3-846e-43a7-94d5-0a3b1e749bc9.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/478bf469-c706-4f66-aa71-a43ddf091e17.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/48b194ba-778c-4889-a4d8-e465109896cf.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/495f2b84-956d-4cff-beca-1d5e0818708d.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/499002d7-f766-4861-b5ba-99f775918817.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/4e58d57a-1bcf-4714-b1e3-d65d9d90fa9e.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/517014f3-b3ae-402d-b082-06c9355493e3.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/5457e825-e1c0-4979-893d-e26ad9f2930f.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/56296e80-466d-4183-a3bf-d567c2716e3d.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/573c459e-86db-45c4-8b32-b7f03a76b166.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/5bcf7505-f567-4eac-ae18-4f76935dd41b.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/5ea5fc60-09fe-4d37-9b23-62048f2df4c5.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/623ba5f3-4460-4a6e-9dce-2cef02466b37.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/65b6d821-4186-4d7a-b01b-3606a3f707ee.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/6d3c20cf-da20-42ee-89b7-9b0cac16d13f.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/6ed8f895-f630-4d8e-9583-cd0e50532fe3.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/7697d99c-0848-4395-ae1d-074d34ead9de.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/77aa3fe0-215f-479b-bb3e-7b27f289d5b3.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/78c8c089-f24f-465a-bb37-f7219aa7df10.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/792feeb1-d396-4218-ac8b-1ea09bf97954.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/79a9f21a-0341-48d2-8abd-76886816dc18.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/7ca2e4ea-7fac-424f-b4b4-24a8fe5e67b2.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/836688e1-4c3b-4230-8fda-6ee11b890959.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/930d9511-3c19-4156-8e75-22675cc6ce65.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/986dadc2-5049-40c7-b72c-855b12a3e619.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/98b7a168-0bc4-4732-bd6b-88ef590120cd.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/9941d8c9-5c3b-4863-a09a-b1f5b1d131dc.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/a0a56b97-4f64-42c3-ba43-6ec0aea443c5.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/a1ed42e7-6951-47a2-92fe-2401162e2816.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/a4e79aff-e70e-4baa-8078-cfe8229ac7df.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/a5bf9208-741b-4617-9667-96903acb0f5d.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/a7f0d689-b473-4053-90dd-726b65cc37d7.root',
     
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/a8265c3b-6152-4990-921d-1dc5e434cc57.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/aa91ee5d-4a1d-4dd8-bf2d-668f18997c3c.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/ab833fcf-da09-4d8e-bced-2878f217fe78.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/b194dd86-83b3-41f0-ac69-4546c22148f4.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/b30ef822-d4f1-4f48-ad00-c2d76528a559.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/b37e3fce-0bd8-48cc-9b57-89a07c610170.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/b91857b5-dbb0-4dcb-a270-a05e241b3ba4.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/bac48dfb-ee94-48cc-915f-328ca9dcd018.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/bb9a6c34-d191-40a3-bcd9-08293f33ae64.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/c30a2fea-2c2d-4c24-a8c7-e1987b85c8a9.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/d15ad300-95b0-4119-8f8b-0f7ed200462e.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/d4628ac1-6cf0-4840-a0c1-3b93229dd56d.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/d8990030-0d73-4d65-b2c3-33d07e7782af.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/dc94ff32-095d-4fce-8062-682e43ce0e12.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/e0ac0e3d-50dc-4857-8846-4666797678c9.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/e379bd14-e854-4d28-adc8-2eb8334a60c4.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/e4556ed6-9470-49ba-b39b-21eddcf96374.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/e5e7259c-4c40-40a4-81ee-555ecb666b6f.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/e8faa6ef-a3fa-4431-9762-a7f560aaab80.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/ee972580-25a0-42d1-ae42-6e34a2c40ae5.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/f08a0f99-47a0-4e14-a7ed-4c611115c227.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/f35fc008-8994-4861-a1a6-9dbdce66253a.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/f50e4a7b-cf2b-48bb-a708-ce8f96c21611.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/f6f52cb7-bff5-4444-baa7-354bd6f27732.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/f9554f37-0ba1-4c7f-995b-b96651d2c26e.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/fa87955f-5470-4b12-a386-22e5cde24ec5.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/fd9723d1-30ef-41c5-9595-a652e3546071.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/fea37e62-371e-46be-80aa-ef1e69f8e70a.root',
      '/store/relval/CMSSW_12_4_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_123X_mcRun4_realistic_v11_2026D88PU200-v1/2580000/ff0e3e6e-31ce-417f-bb6f-7b06d507b275.root'
   ]

# skimming of tracks
if opt_skimTracks:

   from JMETriggerAnalysis.Common.hltPhase2_skimmedTracks import customize_hltPhase2_skimmedTracks
   process = customize_hltPhase2_skimmedTracks(process)

#   # modify PV inputs of PFPuppi collections
#   process.puppiNoLep.vertexName = process.generalTracks.vertices
#   process.hltPFPuppi.vertexName = process.generalTracks.vertices

   # add PV collections to JMETriggerNTuple
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet(
  #   hltPixelVertices = cms.InputTag('pixelVertices'),
 #    hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
     offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
     offlineSlimmedPrimaryVertices4D = cms.InputTag('offlineSlimmedPrimaryVertices4D'),
   )

 #  process.JMETriggerNTuple.outputBranchesToBeDropped += [
 #    'hltPixelVertices_isFake',
 #    'hltPixelVertices_chi2',
 #    'hltPixelVertices_ndof',

 #    'hltTrimmedPixelVertices_isFake',
 #    'hltTrimmedPixelVertices_chi2',
 #    'hltTrimmedPixelVertices_ndof',
 #  ]

process.prune()

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
if opts.verbosity > 0:
   print('--- jmeTriggerNTuple_cfg.py ---')
   print('')
   print('option: output =', opts.output)
   print('option: reco =', opts.reco, '(skimTracks = '+str(opt_skimTracks)+')')
   print('option: trkdqm =', opts.trkdqm)
   print('option: pfdqm =', opts.pfdqm)
   print('option: dumpPython =', opts.dumpPython)
   print('')
   print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('-------------------------------')
