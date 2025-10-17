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

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('output', 'L1_output.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### use base configuration file from L1
###
from JMETriggerAnalysis.Common.configs.rerunL1_cfg import cms, process

# EDM Input Files
if opts.inputFiles and opts.secondaryInputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = opts.secondaryInputFiles
elif opts.inputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = []
else:
   process.source.fileNames = [
   #'/store/mc/Phase2Spring24DIGIRECOMiniAOD/DYToLL_M-10To50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200ALCA_pilot_140X_mcRun4_realistic_v4-v1/130000/00969257-fdc7-4748-be48-d21074b28511.root'
   '/store/mc/Phase2Spring24DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_AllTP_140X_mcRun4_realistic_v4-v1/2560000/11d1f6f0-5f03-421e-90c7-b5815197fc85.root'
   #'/store/relval/CMSSW_14_0_6/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_140X_mcRun4_realistic_v3_STD_2026D110_PU-v1/2590000/00042ff4-01a3-48a9-b88e-83412b3a65c6.root'
   #'/store/mc/Phase2Spring23DIGIRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_131X_mcRun4_realistic_v5-v1/30000/01607282-0427-4687-a122-ef0a41220590.root'
   #'/store/mc/PhaseIISpring22DRMiniAOD/QCD_Pt-15To3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_castor_123X_mcRun4_realistic_v11-v1/40000/009871c5-babe-40aa-9e82-7d91f772b3e4.root'
   #'/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/MINIAODSIM/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/f19a93e6-ee91-4f47-81ec-697697c32c66.root'
   ]
   process.source.secondaryFileNames = [
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/00443525-cac0-4db8-85d2-7c9bd9986266.root',
# '/store/relval/CMSSW_13_1_0_pre3/RelValQCD_Pt15To7000_Flat_14/GEN-SIM-DIGI-RAW/PU_131X_mcRun4_realistic_v2_2026D95PU200-v1/00000/fcb028a5-b0f8-47b0-8109-ce7556b7af35.root',
   ]
# max number of events to be processed
process.maxEvents.input = opts.maxEvents
# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)


## update process.GlobalTag.globaltag
if opts.globalTag is not None:
   #raise RuntimeError('command-line argument "globalTag='+opts.globalTag+'" will overwrite process.GlobalTag (previous customizations of it will be lost)')
   #from Configuration.AlCa.GlobalTag import GlobalTag
   #process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')
   process.GlobalTag.globaltag = cms.string(opts.globalTag)

# This is based on process.source.inputCommands of HLT_75e33_D110_cfg.py (Logic: What input isn't needed by the HLT step to be dropped in output of L1)
list_to_be_dropped = [
  'drop *_hlt*_*_HLT',
  'drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT',
  'drop *_hgcalMergeLayerClusters_*_HLT',
  'drop *_particleFlow*_*_HLT',
  'drop *_ak4CaloJet*_*_HLT',
  'drop *_hltEgammaGsfElectron*_*_HLT',
  'drop *_genPU*_*_HLT',
  'drop *_hltEgammaGsfTracks*_*_HLT',
  'drop *_particleFlowBlock*_*_HLT',
  'drop *_particleFlowCluster*_*_HLT',
  'drop *_displaced*_*_RECO',
  'drop *_particleFlowSuperCluster*_*_HLT',
  'drop *_hltHps*_*_HLT',
  'drop *_slimmedCaloJets_*_RECO',
  'drop *_slimmedJPTJets_*_RECO',
  'drop *_gsfTracksOpenConversions_*_RECO',
  'drop *_ctppsProtons_*_RECO',
  'drop *_scalersRawToDigi_*_RECO',
  'drop *_hltL2MuonFromL1TkMuonCandidates_*_HLT',
  'drop *_hltPFMETTypeOne_*_HLT',
  'drop *_hltTauPFJets08Region_*_HLT',
  'drop *_hltPFPuppiJetForBtagEta2p4_*_HLT',
  'drop *_hltAK4*_*_HLT',
  'drop *_pfTICL_*_HLT',
  'drop *_hltAK8*_*_HLT',
  'drop *_hltPFPuppi*_*_HLT',
  'drop *_hlt*Filter_*_HLT',
  'drop *_generalTracks_*_HLT',
  'drop *_hltPhase2PixelTracks_*_HLT',
  'drop *_HGCalRecHit_*_HLT',
  'drop *_ecalBarrelClusterFastTimer_*_HLT',
  'drop *_ticlTrackstersMerge_*_HLT',
  'drop *_prunedTrackingParticles_*_HLT',
  'drop *_ticlTrackstersCLUE3DHigh_*_HLT',
  'drop *_*_MergedMtdTruth*_HLT',
  'drop *_*_MergedTrackTruth_HLT',
  'drop *_*_MergedCaloTruth_HLT',
  'drop *_*_EcalRecHits*_HLT',
  'drop *_g4SimHits_*_SIM',
  'drop *_l1t*_*_HLT',
  'drop *_hltHoreco_*_HLT',
  'drop *_horeco_*_HLT',
  'drop *_hltCaloMET_*_HLT',
  'drop *_hltHtMhtPFPuppiCentralJetsQuadC30MaxEta2p4_*_HLT',
  'drop *_hlt*MuonCandidates_*_HLT',
  'drop *_hltEgammaCandidates*_*_HLT',
  'drop *_hltPhase2PixelVertices_*_HLT',
  'drop *_hlt1PFPuppi*_*_HLT',
  'drop *_hltBTag*_*_HLT',
  'drop *_hltDiMuon*_*_HLT',
  'drop *_hltL3f*_*_HLT',
  'drop *_hltL1*_*_HLT',
  'drop *_towerMaker_*_HLT',
  'drop *_hltHbhereco_*_HLT',
  'drop *_hfprereco_*_HLT',
  'drop *_hltHfreco_*_HLT',
  'drop *_hfreco_*_HLT',
  'drop *_offlinePrimaryVertices_*_HLT',
  'drop *_offlineBeamSpot_*_HLT',
  'drop *_TriggerResults_*_HLT',
  'drop *_TTClusterAssociatorFromPixelDigis_*_HLT',
  'drop *_TTStubAssociatorFromPixelDigis_*_HLT',
  'drop *_TTTrackAssociatorFromPixelDigis_*_HLT',
  'drop *_TTTrackAssociatorFromPixelDigisExtended_*_HLT',
  'drop *_TTStubsFromPhase2TrackerDigis_*_HLT',
  'drop *_TTClustersFromPhase2TrackerDigis_*_HLT',
  'drop *_externalLHEProducer_*_SIM',
  'drop *_randomEngineStateProducer_*_SIM',
  'drop *_hlt2PFPuppi*_*_HLT',
  'drop *_hlt3PFPuppi*_*_HLT',
  'drop *_hlt4PFPuppi*_*_HLT',
  'drop *_hltDouble*_*_HLT',
  'drop *_hltTriple*_*_HLT',
  'drop *_hltCsc2DRecHits_*_HLT',
  'drop *_hltCscSegments_*_HLT',
  'drop *_hltDt4DSegments_*_HLT',
  'drop *_hltRpcRecHits_*_HLT',
  'drop *_*_FTL*_HLT',
  'drop *_caloStage2Digis_*_RECO',
  'drop *_gmtStage2Digis_*_RECO',
  'drop *_slimmedAddPileupInfo_*_RECO',
  'drop *_ctppsLocalTrackLiteProducer_*_RECO',
  'drop *_CSCHaloData_*_RECO',
  'drop *_offlineBeamSpot_*_RECO',
  'drop *_BeamHaloSummary_*_RECO',
  'drop *_TriggerResults_*_RECO',
  'drop *_gtDigis_*_RECO',
  'drop *_gtStage2Digis_*_RECO',
  'drop *_hltL3*_*_HLT',
  'drop *_simKBmtfDigis_*_HLT',
  'drop *_simEmtfShowers_*_HLT',
  'drop *_simOmtfDigis_*_HLT',
  'drop *_simEmtfDigis_*_HLT',
  'drop *_simDtTriggerPrimitiveDigis_*_HLT',
  'drop *_simCscTriggerPrimitiveDigis_*_HLT',
  'drop *_simGtStage2Digis_*_HLT',
  'drop *_simCaloStage2Digis_*_HLT',
  'drop *_simCaloStage2Layer1Digis_*_HLT',
  'drop *_simGmtStage2Digis_*_HLT',
  'drop *_fixedGridRho*_*_RECO',
  'drop *_TriggerResults_*_SIM',
  'drop *_simGmtShowerDigis_*_HLT',
  'drop *_simBmtfDigis_*_HLT',
  'drop *_simMuonGEMPadDigiClusters_*_HLT',
  'drop *_simMuonGEMPadDigis_*_HLT',
  'drop *_hltSingleAK4PFPuppiJet520_*_HLT',
  'drop *_hltTriggerSummaryRAW_*_HLT',
  'drop *_hltTriggerSummaryAOD_*_HLT',
  'drop *_fixedGridRhoFastjetAllTmp_*_HLT',
  'drop *_randomEngineStateProducer_*_HLT',
  'drop *_l1tTOoLLiPProducer*_*_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_uncalibrated_L1TrackTrigger',
  'drop *_*_UncalibratedPhase1L1TJetFromPfCandidates_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_emUncalibrated_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_hcalUncalibrated_L1TrackTrigger',
  'drop *_l1tLayer1*_TK_L1TrackTrigger',
  'drop *_l1tLayer1*_Calo_L1TrackTrigger',
  'drop *_l1tLayer1*_EmCalo_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_hcalUnclustered_L1TrackTrigger',
  'drop *_*_PuppiRegional_L1TrackTrigger',
  'drop *_*_L1TkElePerBoard_L1TrackTrigger',
  'drop *_*_L1TkEmPerBoard_L1TrackTrigger',
  'drop *_l1tLayer1*_PF_L1TrackTrigger',
  'drop *_l1tLayer1*_Puppi_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_ecalCells_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_had_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_egamma_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombinedCalo*_em_L1TrackTrigger',
  'drop *_l1tMETMLProducer_*_L1TrackTrigger',
  'drop *_l1tLayer1*_vec*_L1TrackTrigger',
  'drop *_l1tLayer1*_max*_L1TrackTrigger',
  'drop *_l1tLayer1*_tot*_L1TrackTrigger',
  'drop *_l1tTrackFastJets_*_L1TrackTrigger',
  'drop *_l1tTrackTripletEmulation_*_L1TrackTrigger',
  'drop *_l1tTowerCalibration_*_L1TrackTrigger',
  'drop *_l1tBJetProducerPuppiCorrectedEmulator_*_L1TrackTrigger',
  'drop *_l1tPFClustersFromHGC*_*_L1TrackTrigger',
  'drop *_l1tPFClustersFromCombined*_*_L1TrackTrigger',
  'drop *_l1tPhase2L1CaloEGammaEmulator_*_L1TrackTrigger',
  'drop *_l1tHGCalBackEndLayer1Producer_*_L1TrackTrigger',
  'drop *_l1tHGCalBackEndLayer2Producer_*_L1TrackTrigger',
  'drop *_l1tHGCalEnergySplitTowerProducer_*_L1TrackTrigger',
  'drop *_l1tHGCalTowerProducer_*_L1TrackTrigger',
  'drop *_l1tHGCalEnergySplitTowerMapProducer_*_L1TrackTrigger',
  'drop *_l1tHGCalTowerMapProducer_*_L1TrackTrigger',
  'drop *_l1tPFClustersFromL1EGClusters_*_L1TrackTrigger',
  'drop *_l1tHGCalConcentratorProducer_*_L1TrackTrigger',
  'drop *_l1tHGCalVFEProducer_*_L1TrackTrigger',
  'drop *_TTClusterAssociatorFromPixelDigis_*_L1TrackTrigger',
  'drop *_TTStubAssociatorFromPixelDigis_*_L1TrackTrigger',
  'drop *_l1tBJetProducerPuppi_L1PFBJets_L1TrackTrigger',
  'drop *_l1t*_DecodedTK_L1TrackTrigger',
  'drop *_l1tEGammaClusterEmuProducer_*_L1TrackTrigger',
  'drop *_l1*_L1TkEle_L1TrackTrigger',
  'drop *_l1*_L1TkEm_L1TrackTrigger',
  'drop *_*GEMDigis_*_L1TrackTrigger',
  'drop *_*_L1CaloJetsNoCuts_L1TrackTrigger',
  'drop *_*_GCTJet_L1TrackTrigger',
  'drop *_*GEM*_*_L1TrackTrigger',
  'drop *_gem*_*_L1TrackTrigger',
  'drop *_l1tCaloJet_L1CaloJetCollectionBXV_L1TrackTrigger',
  'drop *_simCaloStage2Digis_*_L1TrackTrigger',
  'drop *_simCaloStage2Layer1Digis_*_L1TrackTrigger',
  'drop *_simBmtfDigis_*_L1TrackTrigger',
  'drop *_simEmtfDigis_*_L1TrackTrigger',
  'drop *_simCscTriggerPrimitiveDigis_*_L1TrackTrigger',
  'drop *_simDtTriggerPrimitiveDigis_*_L1TrackTrigger',
  'drop *_simKBmtfDigis_*_L1TrackTrigger',
  'drop *_simGmtStage2Digis_*_L1TrackTrigger',
  'drop *_simGmtShowerDigis_*_L1TrackTrigger',
  'drop *_simOmtfDigis_*_L1TrackTrigger',
  'drop *_simEmtfShowers_*_L1TrackTrigger',
  'drop *_l1tNNCaloTauEmulator_*_L1TrackTrigger',
  'drop *_l1tLayer1HGCal*_*_L1TrackTrigger',
  'drop *_l1tLayer1HF_*_L1TrackTrigger',
  'drop *_l1tPhase1JetSumsProducer9x9_*_L1TrackTrigger',
  'drop PixelDigiSimLinkedmDetSetVector_simSiPixelDigis_Tracker_HLT',
  'drop PixelDigiSimLinkedmDetSetVector_simSiPixelDigis_Pixel_HLT',
  'drop DetIdHGCSampleHGCDataFramesSorted_simHGCalUnsuppressedDigis_EE_HLT'
]

for outputs_to_be_dropped in list_to_be_dropped:
  process.FEVTDEBUGHLToutput.outputCommands.append(outputs_to_be_dropped)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# Output name
#process.FEVTDEBUGHLToutput.fileName = cms.untracked.string(f'file:{opts.output}')
process.FEVTDEBUGHLToutput.fileName = cms.untracked.string(f'{opts.output}')
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

process.prune()

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())


