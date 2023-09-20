import os
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

opts.register('rerunPUPPI', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create offline puppi configurations with latest tune note: needs to be updated with developments in puppi')

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

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_75e33',
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
def customisePhase2TrackingPtThresholds(process, ptMin):
  process.CkfBaseTrajectoryFilter_block.minPt = cms.double(ptMin)
  process.HLTIter0Phase2L3FromL1TkMuonGroupedCkfTrajectoryFilterIT.minPt = cms.double(ptMin)
  process.HLTPSetMuonCkfTrajectoryFilter.minPt = cms.double(ptMin)
  process.TrajectoryFilterForConversions.minPt = cms.double(ptMin)
  process.highPtTripletStepTrajectoryFilterBase.minPt = cms.double(ptMin)
  process.highPtTripletStepTrajectoryFilterInOut.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryBuilder.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterBase.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterInOut.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonInitialStepTrajectoryBuilder.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonInitialStepTrajectoryFilter.minPt = cms.double(ptMin)
  process.initialStepTrajectoryFilter.minPt = cms.double(ptMin)
  process.muonSeededTrajectoryFilterForInOut.minPt = cms.double(ptMin)
  process.muonSeededTrajectoryFilterForOutIn.minPt = cms.double(ptMin)
  process.muonSeededTrajectoryFilterForOutInDisplaced.minPt = cms.double(ptMin)
  process.firstStepPrimaryVerticesUnsorted.TkFilterParameters.minPt = cms.double(ptMin)
  process.generalTracks.MinPT = cms.double(ptMin)
  process.highPtTripletStepTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonGeneralTracks.MinPT = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonPixelTrackFilterByKinematics.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonPixelTracksFilter.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonPixelTracksTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.pixelTrackFilterByKinematics.ptMin = cms.double(ptMin)
  process.pixelTracksTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.trackWithVertexRefSelectorBeforeSorting.ptMin = cms.double(ptMin)
  process.unsortedOfflinePrimaryVertices.TkFilterParameters.minPt = cms.double(ptMin)
  return process

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

if opt_reco == 'HLT_TRKv00':
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
  #from JMETriggerAnalysis.Common.configs.HLT_75e33_cfg import cms, process
  # optimal tracking thresholds for MET
  #process = customisePhase2TrackingPtThresholds(process,1.8)
  #process.schedule_().append(process.MC_JME)
  from JMETriggerAnalysis.Common.configs.HLT_75e33_ticlv4_cfg import cms, process
  # Input source
  process.source.inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_hlt*_*_HLT',
        'drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT'
  )


elif opt_reco == 'HLT_75e33_time':
  from JMETriggerAnalysis.Common.configs.HLT_75e33_cfg_time import cms, process

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
from HLTrigger.JetMET.hltSiPixelClusterMultiplicityValueProducer_cfi import hltSiPixelClusterMultiplicityValueProducer as _hltSiPixelClusterMultiplicityValueProducer
from HLTrigger.JetMET.hltSiPhase2TrackerClusterMultiplicityValueProducer_cfi import hltSiPhase2TrackerClusterMultiplicityValueProducer as _hltSiPhase2TrackerClusterMultiplicityValueProducer

from JMETriggerAnalysis.Common.hltTrackMultiplicityValueProducer_cfi import hltTrackMultiplicityValueProducer as _hltTrackMultiplicityValueProducer
from JMETriggerAnalysis.Common.hltVertexMultiplicityValueProducer_cfi import hltVertexMultiplicityValueProducer as _hltVertexMultiplicityValueProducer

#if not hasattr(process, 'hltPixelClustersMultiplicity'):
#  process.hltPixelClustersMultiplicity = _hltSiPixelClusterMultiplicityValueProducer.clone(src = 'siPixelClusters', defaultValue = -1.)

if not hasattr(process, 'hltOuterTrackerClustersMultiplicity'):
  process.hltOuterTrackerClustersMultiplicity = _hltSiPhase2TrackerClusterMultiplicityValueProducer.clone(src = 'siPhase2Clusters', defaultValue = -1.)

process.hltPixelTracksMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'pixelTracks', defaultValue = -1.)
process.hltPixelTracksCleanerMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'pixelTracksCleaner', defaultValue = -1.)
process.hltPixelTracksMergerMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'pixelTracksMerger', defaultValue = -1.)
process.hltTracksMultiplicity = _hltTrackMultiplicityValueProducer.clone(src = 'generalTracks', defaultValue = -1.)

process.hltPixelVerticesMultiplicity = _hltVertexMultiplicityValueProducer.clone(src = 'pixelVertices', defaultValue = -1.)
process.hltPrimaryVerticesMultiplicity = _hltVertexMultiplicityValueProducer.clone(src = 'goodOfflinePrimaryVertices', defaultValue = -1.)
process.offlinePrimaryVerticesMultiplicity = _hltVertexMultiplicityValueProducer.clone(src = 'offlineSlimmedPrimaryVertices', defaultValue = -1.)

# removed because of non existing HLTrigger.mcStitching anymore which contained a stitchingWeight_cfi
# must do this to work :
#mkdir -p HLTrigger
#git clone https://github.com/veelken/mcStitching.git HLTrigger/mcStitching
#from JMETriggerAnalysis.NTuplizers.qcdWeightProducer import qcdWeightProducer
#process.qcdWeightPU140 = qcdWeightProducer(BXFrequency = 30. * 1e6, PU = 140.)
#process.qcdWeightPU200 = qcdWeightProducer(BXFrequency = 30. * 1e6, PU = 200.)

process.jmeTriggerNTupleInputsSeq = cms.Sequence(
  #  process.siPixelClusters
  #+ process.hltPixelClustersMultiplicity
    process.hltOuterTrackerClustersMultiplicity
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

process.jmeTriggerNTupleInputsPath = cms.Path(process.jmeTriggerNTupleInputsSeq)
process.schedule_().append(process.jmeTriggerNTupleInputsPath)

ak4jets_stringCut = '' #'pt > 20'
ak8jets_stringCut = '' #'pt > 80'



## add offline puppi ------------------------------------------------------------

if opts.rerunPUPPI:
  #from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep
  from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi as _ak4PFJetsPuppi
  
  
  #process.offlinePFPuppi = _puppi.clone(
  #  candName = 'packedPFCandidates',
  #  vertexName = cms.InputTag("offlineSlimmedPrimaryVertices4D")
  #)
  
  
  process.offlinePFPuppi = cms.EDProducer("PuppiProducer",
      DeltaZCut = cms.double(0.1),
      DeltaZCutForChargedFromPUVtxs = cms.double(0.2),
      EtaMaxCharged = cms.double(99999),
      EtaMaxPhotons = cms.double(2.5),
      EtaMinUseDeltaZ = cms.double(4.0),
      MinPuppiWeight = cms.double(0.01),
      NumOfPUVtxsForCharged = cms.uint32(2),
      PUProxyValue = cms.InputTag(""),
      PtMaxCharged = cms.double(20.0),
      PtMaxNeutrals = cms.double(200),
      PtMaxNeutralsStartSlope = cms.double(20.0),
      PtMaxPhotons = cms.double(-1),
      UseDeltaZCut = cms.bool(True),
      UseDeltaZCutForPileup = cms.bool(False),
      UseFromPVLooseTight = cms.bool(False),
      algos = cms.VPSet(
          cms.PSet(
              etaMin = cms.vdouble(0.,  2.5),
              etaMax = cms.vdouble(2.5, 3.5),
              ptMin  = cms.vdouble(0.,  0.), #Normally 0
              MinNeutralPt   = cms.vdouble(0.2, 0.2),
              MinNeutralPtSlope   = cms.vdouble(0.015, 0.030),
              RMSEtaSF = cms.vdouble(1.0, 1.0),
              MedEtaSF = cms.vdouble(1.0, 1.0),
              EtaMaxExtrap = cms.double(2.0),
              puppiAlgos = cms.VPSet(cms.PSet(
                  algoId = cms.int32(5),
                  applyLowPUCorr = cms.bool(True),
                  combOpt = cms.int32(0),
                  cone = cms.double(0.4),
                  rmsPtMin = cms.double(0.1),
                  rmsScaleFactor = cms.double(1.0),
                  useCharged = cms.bool(True)
              ))
          ),
          cms.PSet(
              etaMin = cms.vdouble( 3.5),
              etaMax = cms.vdouble(10.0),
              ptMin = cms.vdouble( 0.), #Normally 0
              MinNeutralPt = cms.vdouble( 2.0),
              MinNeutralPtSlope = cms.vdouble(0.08),
              RMSEtaSF = cms.vdouble(1.0 ),
              MedEtaSF = cms.vdouble(0.75),
              EtaMaxExtrap = cms.double( 2.0),
              puppiAlgos = cms.VPSet(cms.PSet(
                  algoId = cms.int32(5),
                  applyLowPUCorr = cms.bool(True),
                  combOpt = cms.int32(0),
                  cone = cms.double(0.4),
                  rmsPtMin = cms.double(0.5),
                  rmsScaleFactor = cms.double(1.0),
                  useCharged = cms.bool(False)
              ))
          )
      ),
      applyCHS = cms.bool(True),
      candName = cms.InputTag("packedPFCandidates"), # can use also "particleFlow" (see also the jet definition bellow)
      clonePackedCands = cms.bool(False),
      invertPuppi = cms.bool(False),
      mightGet = cms.optional.untracked.vstring,
      puppiDiagnostics = cms.bool(False),
      puppiNoLep = cms.bool(False),
      useExistingWeights = cms.bool(False),
      useExp = cms.bool(False),
      usePUProxyValue = cms.bool(False),
      useVertexAssociation = cms.bool(False),
      vertexAssociation = cms.InputTag(""),
      vertexAssociationQuality = cms.int32(0),
      vertexName = cms.InputTag("offlineSlimmedPrimaryVertices"),
      #vertexName = cms.InputTag("offlineSlimmedPrimaryVertices4D"),
      vtxNdofCut = cms.int32(4),
      vtxZCut = cms.double(24)
  )
  


  #process.offlineAK4PFPuppiJets  = _ak4PFJetsPuppi.clone( 
  #    src = "particleFlow", # if use the "particleFlow" (the default in the _ak4PFJetsPuppi) then error if the file doesnt have it
  #    applyWeight = True,
  #    srcWeights = cms.InputTag("offlinePFPuppi")
  #)


  process.offlineAK4PFPuppiJets  = _ak4PFJetsPuppi.clone(
      src = "offlinePFPuppi",
      applyWeight = cms.bool(False) # don't apply weight, to avoid applying weight 2 times
  )

  
  ## JECs
  # -- L1 -- 
  process.offlineAK4PFPuppiJetCorrectorL1 = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("fixedGridRhoFastjetAllTmp")
  )

  # -- L2L3 -- 
  process.offlineAK4PFPuppiJetCorrectorL2 = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L2Relative')
  )
  process.offlineAK4PFPuppiJetCorrectorL3 = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFPuppi'),
    level = cms.string('L3Absolute')
  )

  process.offlineAK4PFPuppiJetCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("offlineAK4PFPuppiJetCorrectorL1", "offlineAK4PFPuppiJetCorrectorL2", "offlineAK4PFPuppiJetCorrectorL3")
  )

  process.offlineAK4PFPuppiJetsCorrected = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("offlineAK4PFPuppiJetCorrector"),
    src = cms.InputTag("offlineAK4PFPuppiJets")
  )

  process.offlinePFPuppiSequence = cms.Sequence(
    # calculate particles weights with puppi
    process.offlinePFPuppi
    # make jets with puppi particles
    + process.offlineAK4PFPuppiJets
    # add corrections for the jets
    + process.offlineAK4PFPuppiJetCorrectorL1
    + process.offlineAK4PFPuppiJetCorrectorL2
    + process.offlineAK4PFPuppiJetCorrectorL3
    + process.offlineAK4PFPuppiJetCorrector
    + process.offlineAK4PFPuppiJetsCorrected
  )

  process.offlinePFPuppiPath = cms.Path(
    process.offlinePFPuppiSequence
  )

  process.schedule_().append(process.offlinePFPuppiPath)
## ------------------------------------------------------------------------------




## ---- updated JECs from local db file ------------------------------------------
process.jescESSource = cms.ESSource('PoolDBESSource',
  _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Phase2Spring23ticlv4_MC.db'),
  toGet = cms.VPSet(
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Phase2Spring23ticlv4_MC_AK4PFPuppiHLT'),
      label = cms.untracked.string('AK4PFPuppi'),
    ),
  ),
)
process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')
# ---------------------------------------------------------------------------------
"""
# add analyzer for MTD timing checks
process.MtdTracksValidation = cms.EDProducer('MtdTracksValidation',
  #folder = cms.string('MTDvalidation'),
  inputTagG = cms.InputTag('generalTracks'),
  inputTagT = cms.InputTag('generalTracksWithMTD'),
  inputTagV = cms.InputTag('offlinePrimaryVertices4D'),
  inputTagH = cms.InputTag('generatorSmeared'),
  tmtd = cms.InputTag('generalTracksWithMTD:generalTracktmtd'),
  sigmatmtd = cms.InputTag('generalTracksWithMTD:generalTracksigmatmtd'),
  t0Src = cms.InputTag('generalTracksWithMTD:generalTrackt0'),
  sigmat0Src = cms.InputTag('generalTracksWithMTD:generalTracksigmat0'),
  trackAssocSrc = cms.InputTag('generalTracksWithMTD:generalTrackassoc'),
  pathLengthSrc = cms.InputTag('generalTracksWithMTD:generalTrackPathLength'),
  t0SafePID = cms.InputTag('generalTracksTOFPIDProducer:t0safe'),
  sigmat0SafePID = cms.InputTag('generalTracksTOFPIDProducer:sigmat0safe'),
  sigmat0PID = cms.InputTag('generalTracksTOFPIDProducer:sigmat0'),
  t0PID = cms.InputTag('generalTracksTOFPIDProducer:t0'),
  trackMVAQual = cms.InputTag('generalTracksMtdTrackQualityMVA:mtdQualMVA'),
  trackMinimumPt = cms.double(0.7),
  #trackMaximumBtlEta = cms.double(1.5),
  #trackMinimumEtlEta = cms.double(1.6),
  #trackMaximumEtlEta = cms.double(3.)
  
)

process.mtdvalidationEndPath = cms.EndPath(process.MtdTracksValidation)
process.schedule_().extend([process.mtdvalidationEndPath])

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    #dataset = cms.untracked.PSet(
    #    dataTier = cms.untracked.string('DQMIO'),
    #    filterName = cms.untracked.string('')
    #),
    fileName = cms.untracked.string('file:step3_inDQM.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

process.DQMoutput_step = cms.EndPath( process.DQMoutput )

"""
# JME Trigger NTuple analyzer
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),
  

  TriggerResultsCollections = cms.vstring(
    'MC_JME',
    'HLT_AK4PFPuppiJet520',
    'HLT_PFPuppiHT1070',
    'HLT_PFPuppiMETTypeOne140_PFPuppiMHT140',
    #'L1T_SinglePFPuppiJet200off',
    #'HLT_AK4PFJet520',
    #'HLT_AK4PFCHSJet520',
    #'HLT_AK4PFPuppiJet520',
    #'L1T_PFPuppiHT450off',
    #'HLT_PFPuppiHT1070',
    #'L1T_PFPuppiMET200off',
    #'L1T_PFPuppiMET245off',
    #'HLT_PFMET250',
    #'HLT_PFCHSMET250',
    #'HLT_PFPuppiMET250',
    #'HLT_PFPuppiMET140',
    #'HLT_PFPuppiMET140_PFPuppiMHT140',
    #'HLT_PFPuppiMET140_PFPuppiMHT140_PFPuppiHT60',
    #'HLT_PFPuppiMETTypeOne140_PFPuppiMHT140',
  ),

  fillCollectionConditions = cms.PSet(),

  HepMCProduct = cms.InputTag('generatorSmeared'),
  GenEventInfoProduct = cms.InputTag('generator'),
  PileupSummaryInfo = cms.InputTag('addPileupInfo'),
  
  doubles = cms.PSet(

    #qcdWeightPU140 = cms.InputTag('qcdWeightPU140'),
    #qcdWeightPU200 = cms.InputTag('qcdWeightPU200'),

    fixedGridRhoFastjetAllTmp = cms.InputTag('fixedGridRhoFastjetAllTmp'),
    offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),
    #hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
    hltOuterTrackerClustersMultiplicity = cms.InputTag('hltOuterTrackerClustersMultiplicity'),
    hltPixelTracksMultiplicity = cms.InputTag('hltPixelTracksMultiplicity'),
    hltPixelTracksCleanerMultiplicity = cms.InputTag('hltPixelTracksCleanerMultiplicity'),
    hltPixelTracksMergerMultiplicity = cms.InputTag('hltPixelTracksMergerMultiplicity'),
    hltTracksMultiplicity = cms.InputTag('hltTracksMultiplicity'),
    hltPixelVerticesMultiplicity = cms.InputTag('hltPixelVerticesMultiplicity'),
    hltPrimaryVerticesMultiplicity = cms.InputTag('hltPrimaryVerticesMultiplicity'),
    offlinePrimaryVerticesMultiplicity = cms.InputTag('offlinePrimaryVerticesMultiplicity'),
  ),

  vdoubles = cms.PSet(

#    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
#    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
#    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
#    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms'),
  ),

  recoVertexCollections = cms.PSet(

#    hltPixelVertices = cms.InputTag('pixelVertices'),
#    hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
#    hltPrimaryVertices4D = cms.InputTag('goodOfflinePrimaryVertices4D'),
#    hltUnsortedPrimaryVertices4D = cms.InputTag('unsortedOfflinePrimaryVertices4D'),
#    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
    offlineSlimmedPrimaryVertices4D = cms.InputTag('offlineSlimmedPrimaryVertices4D'),

  ),

  l1tPFCandidateCollections = cms.PSet(

#   l1tPFPuppi = cms.InputTag('l1pfCandidates', 'Puppi'),
  ),

  recoPFCandidateCollections = cms.PSet(

#    hltPFSim = cms.InputTag('simPFProducer'),
#    hltPFTICL = cms.InputTag('pfTICL'),
#     hltParticleFlow = cms.InputTag('particleFlowTmp'),
#     hltParticleFlowBarrel = cms.InputTag('particleFlowTmpBarrel'), # all PF without the pfTICL (that means + forward > 3.0 etas)
#     hltPfTICL = cms.InputTag('pfTICL'), # HGCal particles 1.5 < |eta| < 3.0
#    hltPFPuppi = cms.InputTag('hltPFPuppi'),
#    hltPFPuppiNoLep = cms.InputTag('hltPFPuppiNoLep'),
  ),

  patPackedCandidateCollections = cms.PSet(

#    offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),
  patPackedGenParticleCollections = cms.PSet(
     ##genParticles = cms.InputTag("packedGenParticles")
  ),

  recoGenJetCollections = cms.PSet(
    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
    #ak4GenJets = cms.InputTag('slimmedGenJets')
  ),

  l1tPFJetCollections = cms.PSet(

#   l1tAK4CaloJetsCorrected = cms.InputTag('ak4PFL1CaloCorrected'),
#   l1tAK4PFJetsCorrected = cms.InputTag('ak4PFL1PFCorrected'),
#   l1tAK4PFPuppiJetsCorrected = cms.InputTag('ak4PFL1PuppiCorrected'),
  ),

  recoCaloJetCollections = cms.PSet(

#    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
#    hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),

#    l1tSlwPFPuppiJets = cms.InputTag('l1tSlwPFPuppiJets', 'UncalibratedPhase1L1TJetFromPfCandidates'),
#    l1tSlwPFPuppiJetsCorrected = cms.InputTag('l1tSlwPFPuppiJetsCorrected', 'Phase1L1TJetFromPfCandidates'),
  ),

  recoPFClusterJetCollections = cms.PSet(

#   hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
#   hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
  ),

  recoPFJetCollections = cms.PSet(

#    l1tAK4CaloJets = cms.InputTag('ak4PFL1Calo'),
#    l1tAK4PFJets = cms.InputTag('ak4PFL1PF'),
#    l1tAK4PFPuppiJets = cms.InputTag('ak4PFL1Puppi'),

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
##    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
#    hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
#    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
#    hltAK8PFJets = hltAK4PFCHSJets('hltAK4PFCHSJets'),
##    hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),
#    hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),
    hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),
#    hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
#    hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),
#     offlineAK4PFPuppiJets = cms.InputTag('offlineAK4PFPuppiJets'), # with rerunPUPPI option
#     offlineAK4PFPuppiJetsCorrected = cms.InputTag('offlineAK4PFPuppiJetsCorrected') # with rerunPUPPI option
  ),

  patJetCollections = cms.PSet(

#    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
#    offlineAK4PFPuppiJetsCorrectedPAT = cms.InputTag('slimmedJetsPuppi'),
    
#    offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    #genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoMETCollections = cms.PSet(

    #l1tPFPuppiHT = cms.InputTag('l1tPFPuppiHT'),
    #hltPFPuppiHT = cms.InputTag('hltPFPuppiHT'),
    #hltPFPuppiMHT = cms.InputTag('hltPFPuppiMHT'),
  ),

  recoCaloMETCollections = cms.PSet(

    hltCaloMET = cms.InputTag('hltCaloMET'),
  ),

  recoPFClusterMETCollections = cms.PSet(

#   hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
  ),

  recoPFMETCollections = cms.PSet(

    #l1tCaloMET = cms.InputTag('l1PFMetCalo'),
    #l1tPFMET = cms.InputTag('l1PFMetPF'),
    #l1tPFPuppiMET = cms.InputTag('l1PFMetPuppi'),

    hltPFMET = cms.InputTag('hltPFMET'),
    #hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
    #hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    #hltPFSoftKillerMET = cms.InputTag('hltPFSoftKillerMET'),
    hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
    hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
    #hltPFPuppiMETv0 = cms.InputTag('hltPFPuppiMETv0'),
  ),

  patMETCollections = cms.PSet(

    #offlinePFMET = cms.InputTag('slimmedMETs'),
    #offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(

#   offlineIsolatedMuons = cms.InputTag('userIsolatedMuons'),
  ),

  patElectronCollections = cms.PSet(

#   offlineIsolatedElectrons = cms.InputTag('userIsolatedElectrons'),
  ),

  stringCutObjectSelectors = cms.PSet(
    # GEN
    ak4GenJetsNoNu = cms.string(''),
    ak8GenJetsNoNu = cms.string(''),

    # L1T AK4
    l1tAK4CaloJets = cms.string(ak4jets_stringCut),
    l1tAK4PFJets = cms.string(ak4jets_stringCut),
    l1tAK4PFPuppiJets = cms.string(ak4jets_stringCut),
    l1tSlwPFPuppiJets = cms.string(ak4jets_stringCut),

    l1tAK4CaloJetsCorrected = cms.string(ak4jets_stringCut),
    l1tAK4PFJetsCorrected = cms.string(ak4jets_stringCut),
    l1tAK4PFPuppiJetsCorrected = cms.string(ak4jets_stringCut),
    l1tSlwPFPuppiJetsCorrected = cms.string(ak4jets_stringCut),

    # HLT AK4
    hltAK4CaloJets = cms.string(ak4jets_stringCut),
    hltAK4PFClusterJets = cms.string(ak4jets_stringCut),
    hltAK4PFJets = cms.string(ak4jets_stringCut),
    hltAK4PFJetsCorrected = cms.string(ak4jets_stringCut),
    hltAK4PFCHSJetsCorrected = cms.string(ak4jets_stringCut),
    hltAK4PFPuppiJetsCorrected = cms.string(ak4jets_stringCut),

    # HLT AK8
    hltAK8CaloJets = cms.string(ak8jets_stringCut),
    hltAK8PFClusterJets = cms.string(ak8jets_stringCut),
    hltAK8PFJetsCorrected = cms.string(ak8jets_stringCut),
    hltAK8PFCHSJetsCorrected = cms.string(ak8jets_stringCut),
    hltAK8PFPuppiJetsCorrected = cms.string(ak8jets_stringCut),

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
if opts.onlyTriggerResultsInNTuple:
   # reset input collections
   process.JMETriggerNTuple.doubles = cms.PSet()
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet()
   process.JMETriggerNTuple.l1tPFCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.patPackedCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.patPackedGenParticleCollections = cms.PSet()
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
   #process.JMETriggerNTuple.patMuonCollections = cms.PSet()
   #process.JMETriggerNTuple.patElectronCollections = cms.PSet()

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
if opts.globalTag is not None:
   #raise RuntimeError('command-line argument "globalTag='+opts.globalTag+'" will overwrite process.GlobalTag (previous customizations of it will be lost)')
   #from Configuration.AlCa.GlobalTag import GlobalTag
   #process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')
   process.GlobalTag.globaltag = cms.string('123X_mcRun4_realistic_v10')

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
   #process.VertexHistograms_hltTrimmedPixelVertices = vertexHistogrammer.clone(src = 'trimmedPixelVertices')
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

      #if hasattr(process, 'pixelVertices') or hasattr(process, 'trimmedPixelVertices'):
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

         #for _tmp in ['pixelVertices', 'trimmedPixelVertices']:
         #  if hasattr(process, _tmp):
         #    process.pvAnalyzer1.vertexRecoCollections += [_tmp]
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
   '/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_131X_mcRun4_realistic_v5-v1/30000/01607282-0427-4687-a122-ef0a41220590.root'
   #'/store/mc/PhaseIISpring22DRMiniAOD/QCD_Pt-15To3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_castor_123X_mcRun4_realistic_v11-v1/40000/009871c5-babe-40aa-9e82-7d91f772b3e4.root'
   #'/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/MINIAODSIM/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f19a93e6-ee91-4f47-81ec-697697c32c66.root'
   ]
   process.source.secondaryFileNames = [
#    '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/00443525-cac0-4db8-85d2-7c9bd9986266.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/013bf05c-abbb-4b82-b393-c29ce84fdc97.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/02fdb8df-d984-421e-9c6b-94d1c743c61f.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/060959ba-f5f3-4b2c-911c-76efd9e73a35.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/09ab53f4-9bc1-4b73-a38d-dcfb193012c3.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0ae62707-82c9-425b-9552-537dcd9b397b.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0b2d0e88-42ca-4dd6-a195-b301239f540a.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0b31af83-26a3-4e97-b9c1-9471ddd4226f.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0bf0f1d6-f2a7-4686-9aa1-d5d2bd53f282.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0d5cd91c-bd79-4897-9d95-0e8c5e0158fa.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0de4c09a-41c5-4901-a1ad-a3ce97f398ed.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0f8c1dfe-2668-41e4-8654-4ba3cd9cdf16.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/0fc9131f-888a-444c-a9d6-9d800f00cd87.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/11a93a57-8d9d-4be0-a01c-0827f675804c.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/12281f17-ab50-4fa5-b970-9ba48122e594.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/12491ea1-7bcd-48b6-b119-2f3a48b0516b.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/156d76ae-7b08-4ef7-a72f-fe44f906c484.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/1623118f-ccfd-49b2-b681-736e661a5b6d.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/1c94f897-8bb2-4b60-80bb-fe860ecd3e90.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/1d1b1dcc-4cf4-412c-855d-41c595e96406.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/1d1ffe67-f619-4bb6-be9a-2b53d2b3c40b.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/21a15b91-28be-402d-8eb1-cce6c44b9a17.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/2361c3b6-49b6-4d56-8ae2-be67a878cebc.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/26a6f030-a337-4ec9-a0f4-f077364bee03.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/2dbfdcc5-10a3-47d8-902f-0bd6ae1d1f4a.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/2ed65e8a-278b-4cc2-8d30-8aae156fe244.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/32ccfada-70b1-4e82-881b-0519a768663d.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/335bb1e3-7dbe-4167-b2cc-bd5f6028c5df.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/34da0045-d547-4823-a343-4a00bc348f84.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/37934f59-b84f-4886-aa1d-405590027c06.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/3af53417-c311-4816-bb2f-c8d1647105d2.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/3ce439f2-dff5-466e-a1bf-79b14c4607f1.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/3e7364d7-5d89-4169-a919-2754c0d18b9d.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/43e9a3b9-7195-4e3d-b30f-bd60b1bc1703.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/47b1ce5f-1025-4bae-9fcc-575f3bd5fa78.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/49cb0ff5-8392-442f-a05c-32c4d947e29b.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/4a17be90-04f8-4b8d-bca7-fa7fa70a3ae5.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/4adc21a4-3b52-4f2a-bb92-78ea425b3584.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/4dd5e854-604d-4016-b592-686b29685a78.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/50c7f1a6-56a2-4daa-90b2-4f5767fe1280.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/511ef2cd-7425-41f4-9bae-6d3dbbb3c3b9.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5249919b-211f-433b-8c20-e610886240c6.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5307199a-27aa-4fd6-b7a3-2c9b021c4087.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/53c4b46c-9115-40ec-9939-ba6f2cb8bd34.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/53d647f3-d9a4-4409-ba0f-521013594159.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5938cee1-aecc-475d-ac26-52a45251eab1.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5b6a3774-b75d-4278-a7bd-1e673ae9e535.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5d0cf845-cfb2-46b5-8233-b4491be002f9.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5dbc5222-245e-429c-801b-4600453618b2.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/5e445349-072e-4cb5-823e-9e35dc43ab23.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/63828e51-9d6b-41fd-9a17-0e39ff9b03e5.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/64011be5-97b0-4493-9ac8-f777851c6a42.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/643f6b67-4214-45a9-bfd1-e4f797c7b4d5.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/64d86c7f-69fc-4444-8195-2d5160eff403.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/659cfb19-738c-403c-856c-3c38efa76a90.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/6604f58e-0a70-4733-b74a-fca521585e70.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/67ec3f06-1037-4a3a-897d-0c7b73df5b4f.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/69f28e4e-02b3-43bd-998a-ac0ea517a4da.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/6a2bb32c-9cfe-44b2-9ae8-3aab902a5204.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/6d374471-d08c-4e1b-8ecf-fed77697ab85.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/6db9699b-70ff-488a-91b3-2ff8887192e7.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/7055ab48-2ff5-432c-ace2-d94e21f99a58.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/71ba703e-5b16-4e9b-a861-d9e2d05ffb8d.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/71c9c5ac-6ede-48ec-ab2f-29327f933ae1.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/749243ea-2e1c-41c4-898e-acf291bff4cf.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/7543706a-1934-48d8-8718-1a1fae38d4e5.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/769516d0-e665-4268-a0dd-d92d77d662bd.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/78ab1b4b-cb13-481c-92b6-680489bca30d.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/7a9b1ef3-0d9a-4fb4-afe4-ccdf2f52e9f6.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/7c09b6bd-86e7-470e-89e1-e81d052595e3.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/7fd02a16-60b8-4b86-a391-eb0c2d156867.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/80ea9382-8976-4c48-a830-82c6711786b9.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/85b3148c-d0c1-4073-94d1-5fe8ed50e59a.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/85c4fa3f-9e29-41c5-a559-d37720847994.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/86b09132-8c7a-425d-bbc3-bc675c8c4f89.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/8817a775-44ae-408b-978f-8e69ccb8d268.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/91877670-c33d-4d86-92fe-5583765f3411.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/93546b74-7b4c-49ac-9378-a0677a2282da.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/93b44053-ac5f-437b-b8e9-77939d4e633c.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/940073ff-0623-4f83-9985-a19f18a3d077.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/96b16739-6fa5-41e5-9478-f265dd8c821b.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/9719436e-fe01-49e7-a114-414e122ed014.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/9a442d27-597d-478c-848c-d99267cba1c6.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/9ae5d7ac-ced6-41fc-93c8-45e1fa067069.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/9e8266c5-c941-4e43-b364-51df932f2320.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/a6f90af7-7fdd-44a9-b79d-c9672b8b8383.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/a892bbaf-1a67-470c-b26c-d76300bba203.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/ab1a2f7c-c3d0-44bc-acce-50344adcf534.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/ab99b6da-ae3a-4ab4-b099-559048c29798.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/af96600e-d030-46bc-b968-741fac836f05.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/b0bd699d-b944-4bc7-b07a-ee0107c08c02.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/b3f5ad50-0ee9-413b-a85f-3a9e0c4492c0.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/b45c2435-1ebc-4992-98aa-f71fb264d73a.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/b575b4a1-4324-4d71-b79d-ef3a365b96bf.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/b8ac7f77-b188-435b-a9bc-a2c2f30ab650.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/b93b8ed1-4b88-4fe3-9890-3af6721bdf34.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/bc690c45-8849-4591-b4f7-b31718b1c9bd.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/bddb9e8e-a7f4-48ed-bf5c-d5ede48e1e8e.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/beb6731e-a1ea-4e3a-aee8-0b163eaf2be9.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/bee72856-636b-4377-9900-78835f850313.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/bfa1b70e-03f5-40be-9579-7873202a3569.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c2006dfd-8e41-4985-bd3f-9a49d3cd124e.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c2d41091-c578-4166-ba33-a586daf79752.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c51423a6-2d74-44fc-a99e-c45279d20a3c.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c51704c8-f79a-4578-a264-7de91ce96098.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c544cdb2-1b7a-4158-a470-d8eebce53a78.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c6cfc0e7-7815-47e4-b68b-e69c20267a7b.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/c788361c-0e03-4b71-aadf-a39a8ce5e746.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/cad71800-588a-47b9-bafd-4cc59ec9dfd8.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/ccdc92e9-b961-4509-88f8-feb7bfcd435c.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/ce516553-31c9-4cc2-867c-244713559a04.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d1a0ec24-fcb9-4c24-a971-0c31720f5782.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d3c9e3d2-9e71-4879-8f34-75f2cf99bead.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d3e1b6b7-49b5-43dc-ac5d-1724570680b0.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d501eb5b-388b-4dea-a18a-d65a8857f6eb.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d7fe9c2b-6a08-4ef3-ad75-488197b9e2c8.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d90a2e96-f516-442a-b2f8-642b432c8437.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d910d8a2-7b38-43e2-8324-57cfbb2e7d34.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d99f29a4-1bc2-4135-a5af-d3e0da02389c.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d9d4ea7d-a721-4599-9f2c-6865a972d261.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/d9f631ae-95ad-4012-8c55-568732fdeee7.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/da157822-28d4-409d-a26a-1027e81af894.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/ddc0a92d-5475-4c2b-a3f8-7611a4e208f8.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/e70166ac-7e30-490d-ab12-1727304ba11e.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/e83be913-381b-48d3-b01d-6135fc2fa5b7.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/ebb86259-48b2-4758-bd59-1b2a43950400.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f0faa9bd-157d-4005-9635-63a92e8f1e68.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f13143cc-ad17-4762-acbd-a89fc74ab2d7.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f2a659eb-0eee-4b64-84a8-426bb3fff12a.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f40a821f-9f08-4673-a4bb-73894d366a22.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f5d71938-e5b1-4f94-9492-87325915e7ac.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f753fdd3-693e-4eb2-95f7-4f6a064bf22d.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f815b4c8-4627-4794-8b19-533e328e632f.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/fc31bf63-e9f1-473d-a070-5b75a3937b35.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/fcb028a5-b0f8-47b0-8109-ce7556b7af35.root',
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
     hltPixelVertices = cms.InputTag('pixelVertices'),
     hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
     hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
     offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
   )

   process.JMETriggerNTuple.outputBranchesToBeDropped += [
     'hltPixelVertices_isFake',
     'hltPixelVertices_chi2',
     'hltPixelVertices_ndof',

     'hltTrimmedPixelVertices_isFake',
     'hltTrimmedPixelVertices_chi2',
     'hltTrimmedPixelVertices_ndof',
   ]

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
