import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.pfPileUp_cfi import pfPileUp as _pfPileUp

from CommonTools.ParticleFlow.TopProjectors.pfNoPileUp_cfi import pfNoPileUp as _pfNoPileUp
from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep
#from CommonTools.RecoAlgos.primaryVertexAssociation_cfi import primaryVertexAssociation

from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets as _ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi as _ak4PFJetsPuppi, ak4PFJetsCHS as _ak4PFJetsCHS
from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsPuppi as _ak8PFJetsPuppi, ak8PFJetsCHS as _ak8PFJetsCHS

from RecoParticleFlow.PFProducer.particleFlowTmpPtrs_cfi import particleFlowTmpPtrs as _particleFlowTmpPtrs


def addPaths_MC_JMECalo(process):
    process.hltPreMCJMECalo = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    ## MET Type-1
    process.hltCaloMETCorrection = cms.EDProducer('CaloJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4CaloCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4CaloCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4CaloFastJetCorrector'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      src = cms.InputTag('hltAK4CaloJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltCaloMETTypeOne = cms.EDProducer('CorrectedCaloMETProducer',
      src = cms.InputTag('hltMet'),
      srcCorrections = cms.VInputTag('hltCaloMETCorrection:type1'),
    )

    ## Path
    process.MC_JMECalo_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMECalo
      ## AK{4,8} Jets
      + process.HLTAK4CaloJetsSequence
      + process.HLTAK8CaloJetsSequence
      ## MET
      + process.hltMet
      ## MET Type-1
      + process.hltCaloMETCorrection
      + process.hltCaloMETTypeOne
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_JMECalo_v1)

    return process

def addPaths_MC_JMEPFCluster(process):
    process.hltPreMCJMEPFCluster = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.HLTParticleFlowClusterSequence = cms.Sequence(
        process.HLTDoFullUnpackingEgammaEcalWithoutPreshowerSequence
      + process.HLTDoLocalHcalSequence
      + process.HLTPreshowerSequence
      + process.hltParticleFlowRecHitECALUnseeded
      + process.hltParticleFlowRecHitHBHE
      + process.hltParticleFlowRecHitHF
      + process.hltParticleFlowRecHitPSUnseeded
      + process.hltParticleFlowClusterECALUncorrectedUnseeded
      + process.hltParticleFlowClusterPSUnseeded
      + process.hltParticleFlowClusterECALUnseeded
      + process.hltParticleFlowClusterHBHE
      + process.hltParticleFlowClusterHCAL
      + process.hltParticleFlowClusterHF
    )

    process.hltParticleFlowClusterRefsECALUnseeded = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterECALUnseeded'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefsHCAL = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterHCAL'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefsHF = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('hltParticleFlowClusterHF'),
      particleType = cms.string('pi+')
    )

    process.hltParticleFlowClusterRefs = cms.EDProducer('PFClusterRefCandidateMerger',
      src = cms.VInputTag(
        'hltParticleFlowClusterRefsECALUnseeded',
        'hltParticleFlowClusterRefsHCAL',
        'hltParticleFlowClusterRefsHF',
      )
    )

    process.HLTParticleFlowClusterRefsSequence = cms.Sequence(
        process.hltParticleFlowClusterRefsECALUnseeded
      + process.hltParticleFlowClusterRefsHCAL
      + process.hltParticleFlowClusterRefsHF
      + process.hltParticleFlowClusterRefs
    )

    ## AK4 Jets
    process.hltFixedGridRhoFastjetAllPFCluster = cms.EDProducer('FixedGridRhoProducerFastjet',
      gridSpacing = cms.double(0.55),
      maxRapidity = cms.double(5.0),
      pfCandidatesTag = cms.InputTag('hltParticleFlowClusterRefs'),
    )

    process.hltAK4PFClusterJets = _ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doAreaDiskApprox = True,
      doPVCorrection = False,
    )

    process.hltAK4PFClusterJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK4PFClusterHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    )

    process.hltAK4PFClusterJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFClusterHLT'),
      level = cms.string('L2Relative'),
    )

    process.hltAK4PFClusterJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFClusterHLT'),
      level = cms.string('L3Absolute'),
    )

    process.hltAK4PFClusterJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFClusterJetCorrectorL1',
        'hltAK4PFClusterJetCorrectorL2',
        'hltAK4PFClusterJetCorrectorL3',
      ),
    )

    process.hltAK4PFClusterJetsCorrected = cms.EDProducer('CorrectedPFClusterJetProducer',
      src = cms.InputTag('hltAK4PFClusterJets'),
      correctors = cms.VInputTag('hltAK4PFClusterJetCorrector'),
    )

    ## AK8 Jets
    process.hltAK8PFClusterJets = _ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doAreaDiskApprox = True,
      doPVCorrection = False,
      rParam = 0.8,
    )

    process.hltAK8PFClusterJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK8PFClusterHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    )

    process.hltAK8PFClusterJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFClusterHLT'),
      level = cms.string('L2Relative'),
    )

    process.hltAK8PFClusterJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFClusterHLT'),
      level = cms.string('L3Absolute'),
    )

    process.hltAK8PFClusterJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFClusterJetCorrectorL1',
        'hltAK8PFClusterJetCorrectorL2',
        'hltAK8PFClusterJetCorrectorL3',
      ),
    )

    process.hltAK8PFClusterJetsCorrected = cms.EDProducer('CorrectedPFClusterJetProducer',
      src = cms.InputTag('hltAK8PFClusterJets'),
      correctors = cms.VInputTag('hltAK8PFClusterJetCorrector'),
    )

    ## MET
    process.hltPFClusterMET = cms.EDProducer('PFClusterMETProducer',
      src = cms.InputTag('hltParticleFlowClusterRefs'),
      globalThreshold = cms.double(0.0),
      alias = cms.string(''),
    )

    ## MET Type-1
    process.hltPFClusterMETCorrection = cms.EDProducer('PFClusterJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4PFClusterJetCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4PFClusterJetCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4PFClusterJetCorrectorL1'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      src = cms.InputTag('hltAK4PFClusterJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltPFClusterMETTypeOne = cms.EDProducer('CorrectedPFClusterMETProducer',
      src = cms.InputTag('hltPFClusterMET'),
      srcCorrections = cms.VInputTag('hltPFClusterMETCorrection:type1'),
    )

    process.hltPFClusterJMESequence = cms.Sequence(
      ## AK4 Jets
        process.hltAK4PFClusterJets
      + process.hltFixedGridRhoFastjetAllPFCluster
      + process.hltAK4PFClusterJetCorrectorL1
      + process.hltAK4PFClusterJetCorrectorL2
      + process.hltAK4PFClusterJetCorrectorL3
      + process.hltAK4PFClusterJetCorrector
      + process.hltAK4PFClusterJetsCorrected
      ## AK8 Jets
      + process.hltAK8PFClusterJets
      + process.hltAK8PFClusterJetCorrectorL1
      + process.hltAK8PFClusterJetCorrectorL2
      + process.hltAK8PFClusterJetCorrectorL3
      + process.hltAK8PFClusterJetCorrector
      + process.hltAK8PFClusterJetsCorrected
      ## MET
      + process.hltPFClusterMET
      ## MET Type-1
      + process.hltPFClusterMETCorrection
      + process.hltPFClusterMETTypeOne
    )

    process.MC_JMEPFCluster_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPFCluster
      + process.HLTParticleFlowClusterSequence
      + process.HLTParticleFlowClusterRefsSequence
      + process.hltPFClusterJMESequence
      + process.HLTEndSequence
    )

    if process.schedule_():
      process.schedule_().append(process.MC_JMEPFCluster_v1)

    return process

def addPaths_MC_JMEPF(process):
    process.hltPreMCJMEPF = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    ## Path
    process.MC_JMEPF_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPF
      + process.HLTAK4PFJetsSequence
      + process.hltPFMETProducer
      ## MET Type-1
      + process.hltcorrPFMETTypeOne
      + process.hltPFMETTypeOne
      + process.HLTEndSequence
    )

    if process.schedule_():
       process.schedule_().append(process.MC_JMEPF_v1)

    return process

def addPaths_MC_JMEPFCHS(process):

    process.hltPreMCJMEPFCHS = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltParticleFlowPtrs = _particleFlowTmpPtrs.clone(src = 'hltParticleFlow')

    process.hltPFPileUpJME = _pfPileUp.clone(
      PFCandidates = 'hltParticleFlowPtrs',
      Vertices = 'hltVerticesPF',
      checkClosestZVertex = False,
      useVertexAssociation = False,
    )

    process.hltPFNoPileUpJME = _pfNoPileUp.clone(
      topCollection = 'hltPFPileUpJME',
      bottomCollection = 'hltParticleFlowPtrs',
    )

    process.HLTPFCHSSequence = cms.Sequence(
        process.HLTPreAK4PFJetsRecoSequence
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
      + process.hltParticleFlowPtrs
      + process.hltVerticesPF
      + process.hltPFPileUpJME
      + process.hltPFNoPileUpJME
    )

    ## AK4
    process.hltAK4PFCHSJets = _ak4PFJetsCHS.clone(src = 'hltPFNoPileUpJME')

    process.hltAK4PFCHSJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK4PFchsHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK4PFCHSJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFchsHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK4PFCHSJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFchsHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK4PFCHSJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFCHSJetCorrectorL1',
        'hltAK4PFCHSJetCorrectorL2',
        'hltAK4PFCHSJetCorrectorL3',
      ),
    )

    process.hltAK4PFCHSJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK4PFCHSJets'),
      correctors = cms.VInputTag('hltAK4PFCHSJetCorrector'),
    )

    process.HLTAK4PFCHSJetsSequence = cms.Sequence(
        process.hltAK4PFCHSJets
      + process.hltAK4PFCHSJetCorrectorL1
      + process.hltAK4PFCHSJetCorrectorL2
      + process.hltAK4PFCHSJetCorrectorL3
      + process.hltAK4PFCHSJetCorrector
      + process.hltAK4PFCHSJetsCorrected
    )

    ## AK8
    process.hltAK8PFCHSJets = _ak8PFJetsCHS.clone(src = 'hltPFNoPileUpJME')

    process.hltAK8PFCHSJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK8PFchsHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK8PFCHSJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFchsHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK8PFCHSJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFchsHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK8PFCHSJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFCHSJetCorrectorL1',
        'hltAK8PFCHSJetCorrectorL2',
        'hltAK8PFCHSJetCorrectorL3',
      ),
    )

    process.hltAK8PFCHSJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK8PFCHSJets'),
      correctors = cms.VInputTag('hltAK8PFCHSJetCorrector'),
    )

    process.HLTAK8PFCHSJetsSequence = cms.Sequence(
        process.hltAK8PFCHSJets
      + process.hltAK8PFCHSJetCorrectorL1
      + process.hltAK8PFCHSJetCorrectorL2
      + process.hltAK8PFCHSJetCorrectorL3
      + process.hltAK8PFCHSJetCorrector
      + process.hltAK8PFCHSJetsCorrected
    )

    ## MET
    process.hltParticleFlowCHS = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
      src = process.hltAK4PFCHSJets.src,
    )

    process.hltPFCHSMET = cms.EDProducer('PFMETProducer',
      src = cms.InputTag('hltParticleFlowCHS'),
      globalThreshold = cms.double(0.0),
      calculateSignificance = cms.bool(False),
    )

    ## MET Type-1
    process.hltPFCHSMETCorrection = cms.EDProducer('PFJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4PFCHSJetCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4PFCHSJetCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4PFCHSJetCorrectorL1'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      skipMuonSelection = cms.string('isGlobalMuon | isStandAloneMuon'),
      skipMuons = cms.bool(True),
      src = cms.InputTag('hltAK4PFCHSJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltPFCHSMETTypeOne = cms.EDProducer('CorrectedPFMETProducer',
      src = cms.InputTag('hltPFCHSMET'),
      srcCorrections = cms.VInputTag('hltPFCHSMETCorrection:type1'),
    )

    ## Sequence: MET CHS
    process.HLTPFCHSMETSequence = cms.Sequence(
        process.hltParticleFlowCHS
      + process.hltPFCHSMET
      + process.hltPFCHSMETCorrection
      + process.hltPFCHSMETTypeOne
    )

    ## Path
    process.MC_JMEPFCHS_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPFCHS
      + process.HLTPFCHSSequence
      + process.HLTAK4PFCHSJetsSequence
      + process.HLTAK8PFCHSJetsSequence
      + process.HLTPFCHSMETSequence
      + process.HLTEndSequence
    )

    if process.schedule_():
      process.schedule_().append(process.MC_JMEPFCHS_v1)

    return process

def addPaths_MC_JMEPFPuppi(process,listOfPaths):

    process.hltPreMCJMEPFPuppi = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltPixelClustersMultiplicity = cms.EDProducer("HLTSiPixelClusterMultiplicityValueProducer",
        defaultValue = cms.double(-1.0),
        mightGet = cms.optional.untracked.vstring,
        src = cms.InputTag("siPixelClusters")
    )

    process.hltPFPuppi = cms.EDProducer("PuppiProducer",
        DeltaZCut = cms.double(0.3),
        DeltaZCutForChargedFromPUVtxs = cms.double(0.2),
        EtaMaxCharged = cms.double(99999),
        EtaMaxPhotons = cms.double(2.5),
        EtaMinUseDeltaZ = cms.double(0.0),
        MinPuppiWeight = cms.double(0.01),
        NumOfPUVtxsForCharged = cms.uint32(2),
        PUProxyValue = cms.InputTag("hltPixelClustersMultiplicity"),
        PtMaxCharged = cms.double(20.0),
        PtMaxNeutrals = cms.double(200),
        PtMaxNeutralsStartSlope = cms.double(20.0),
        PtMaxPhotons = cms.double(-1),
        UseDeltaZCut = cms.bool(True),
        UseDeltaZCutForPileup = cms.bool(True),
        UseFromPVLooseTight = cms.bool(False),
        algos = cms.VPSet(
            cms.PSet(
                EtaMaxExtrap = cms.double(2.0),
                MedEtaSF = cms.vdouble(1.0, 1.0),
                MinNeutralPt = cms.vdouble(0.2, 0.2),
                MinNeutralPtSlope = cms.vdouble(1.62e-05, 1.62e-05),
                RMSEtaSF = cms.vdouble(1.0, 1.0),
                etaMax = cms.vdouble(1.3, 2.5),
                etaMin = cms.vdouble(0.0, 1.3),
                ptMin = cms.vdouble(0.0, 0.0),
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
                EtaMaxExtrap = cms.double(2.0),
                MedEtaSF = cms.vdouble(1.1, 1.05),
                MinNeutralPt = cms.vdouble(1.7, 2.0),
                MinNeutralPtSlope = cms.vdouble(0.0008640000000000001, 0.00027),
                RMSEtaSF = cms.vdouble(1.3, 0.4),
                etaMax = cms.vdouble(3.0, 10.0),
                etaMin = cms.vdouble(2.5, 3.0),
                ptMin = cms.vdouble(0.0, 0.0),
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
        candName = cms.InputTag("hltParticleFlow"),
        clonePackedCands = cms.bool(False),
        invertPuppi = cms.bool(False),
        mightGet = cms.optional.untracked.vstring,
        puppiDiagnostics = cms.bool(False),
        puppiNoLep = cms.bool(False),
        useExistingWeights = cms.bool(False),
        useExp = cms.bool(False),
        usePUProxyValue = cms.bool(True),
        useVertexAssociation = cms.bool(False),
        vertexAssociation = cms.InputTag(""),
        vertexAssociationQuality = cms.int32(0),
        vertexName = cms.InputTag("hltVerticesPF"),
        vtxNdofCut = cms.int32(4),
        vtxZCut = cms.double(24)
    )


    process.HLTPFPuppiSequence = cms.Sequence(
        process.HLTPreAK4PFJetsRecoSequence
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
      + process.hltVerticesPF
      + process.hltPixelClustersMultiplicity
      + process.hltPFPuppi
    )

    ## AK4
    process.hltAK4PFPuppiJets = _ak4PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

    process.hltAK4PFPuppiJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK4PFPuppiHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK4PFPuppiJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFPuppiHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK4PFPuppiJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK4PFPuppiHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK4PFPuppiJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFPuppiJetCorrectorL1',
        'hltAK4PFPuppiJetCorrectorL2',
        'hltAK4PFPuppiJetCorrectorL3',
      ),
    )

    process.hltAK4PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK4PFPuppiJets'),
      correctors = cms.VInputTag('hltAK4PFPuppiJetCorrector'),
    )

    process.HLTAK4PFPuppiJetsSequence = cms.Sequence(
        process.hltAK4PFPuppiJets
      + process.hltAK4PFPuppiJetCorrectorL1
      + process.hltAK4PFPuppiJetCorrectorL2
      + process.hltAK4PFPuppiJetCorrectorL3
      + process.hltAK4PFPuppiJetCorrector
      + process.hltAK4PFPuppiJetsCorrected
    )

    ## AK8
    process.hltAK8PFPuppiJets = _ak8PFJetsPuppi.clone(
      src = 'hltParticleFlow',
      srcWeights = 'hltPFPuppi',
      applyWeight = True,
    )

    process.hltAK8PFPuppiJetCorrectorL1 = cms.EDProducer('L1FastjetCorrectorProducer',
      algorithm = cms.string('AK8PFPuppiHLT'),
      level = cms.string('L1FastJet'),
      srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    )

    process.hltAK8PFPuppiJetCorrectorL2 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFPuppiHLT'),
      level = cms.string('L2Relative')
    )

    process.hltAK8PFPuppiJetCorrectorL3 = cms.EDProducer('LXXXCorrectorProducer',
      algorithm = cms.string('AK8PFPuppiHLT'),
      level = cms.string('L3Absolute')
    )

    process.hltAK8PFPuppiJetCorrector = cms.EDProducer('ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFPuppiJetCorrectorL1',
        'hltAK8PFPuppiJetCorrectorL2',
        'hltAK8PFPuppiJetCorrectorL3',
      ),
    )

    process.hltAK8PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag('hltAK8PFPuppiJets'),
      correctors = cms.VInputTag('hltAK8PFPuppiJetCorrector'),
    )

    process.HLTAK8PFPuppiJetsSequence = cms.Sequence(
        process.hltAK8PFPuppiJets
      + process.hltAK8PFPuppiJetCorrectorL1
      + process.hltAK8PFPuppiJetCorrectorL2
      + process.hltAK8PFPuppiJetCorrectorL3
      + process.hltAK8PFPuppiJetCorrector
      + process.hltAK8PFPuppiJetsCorrected
    )

    ## MET
    process.hltPFPuppiNoLep = cms.EDProducer("PuppiProducer",
        DeltaZCut = cms.double(0.3),
        DeltaZCutForChargedFromPUVtxs = cms.double(0.2),
        EtaMaxCharged = cms.double(99999),
        EtaMaxPhotons = cms.double(2.5),
        EtaMinUseDeltaZ = cms.double(0.0),
        MinPuppiWeight = cms.double(0.01),
        NumOfPUVtxsForCharged = cms.uint32(2),
        PUProxyValue = cms.InputTag("hltPixelClustersMultiplicity"),
        PtMaxCharged = cms.double(20.0),
        PtMaxNeutrals = cms.double(200),
        PtMaxNeutralsStartSlope = cms.double(20.0),
        PtMaxPhotons = cms.double(-1),
        UseDeltaZCut = cms.bool(True),
        UseDeltaZCutForPileup = cms.bool(True),
        UseFromPVLooseTight = cms.bool(False),
        algos = cms.VPSet(
            cms.PSet(
                EtaMaxExtrap = cms.double(2.0),
                MedEtaSF = cms.vdouble(1.0, 1.0),
                MinNeutralPt = cms.vdouble(0.2, 0.2),
                MinNeutralPtSlope = cms.vdouble(1.62e-05, 1.62e-05),
                RMSEtaSF = cms.vdouble(1.0, 1.0),
                etaMax = cms.vdouble(1.3, 2.5),
                etaMin = cms.vdouble(0.0, 1.3),
                ptMin = cms.vdouble(0.0, 0.0),
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
                EtaMaxExtrap = cms.double(2.0),
                MedEtaSF = cms.vdouble(1.1, 1.05),
                MinNeutralPt = cms.vdouble(1.7, 2.0),
                MinNeutralPtSlope = cms.vdouble(0.0008640000000000001, 0.00027),
                RMSEtaSF = cms.vdouble(1.3, 0.4),
                etaMax = cms.vdouble(3.0, 10.0),
                etaMin = cms.vdouble(2.5, 3.0),
                ptMin = cms.vdouble(0.0, 0.0),
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
        candName = cms.InputTag("hltParticleFlow"),
        clonePackedCands = cms.bool(False),
        invertPuppi = cms.bool(False),
        mightGet = cms.optional.untracked.vstring,
        puppiDiagnostics = cms.bool(False),
        puppiNoLep = cms.bool(True),
        useExistingWeights = cms.bool(False),
        useExp = cms.bool(False),
        usePUProxyValue = cms.bool(True),
        useVertexAssociation = cms.bool(False),
        vertexAssociation = cms.InputTag(""),
        vertexAssociationQuality = cms.int32(0),
        vertexName = cms.InputTag("hltVerticesPF"),
        vtxNdofCut = cms.int32(4),
        vtxZCut = cms.double(24)
    )

    process.hltPFPuppiMET = cms.EDProducer('PFMETProducer',
      alias = cms.string(''),
      applyWeight = cms.bool(True),
      calculateSignificance = cms.bool(False),
      globalThreshold = cms.double(0.0),
      parameters = cms.PSet(),
      src = cms.InputTag('hltParticleFlow'),
      srcWeights = cms.InputTag('hltPFPuppiNoLep'),
    )

    ## MET Type-1
    process.hltPFPuppiMETCorrection = cms.EDProducer('PFJetMETcorrInputProducer',
      jetCorrEtaMax = cms.double(9.9),
      jetCorrLabel = cms.InputTag('hltAK4PFPuppiJetCorrector'),
      jetCorrLabelRes = cms.InputTag('hltAK4PFPuppiJetCorrector'),
      offsetCorrLabel = cms.InputTag('hltAK4PFPuppiJetCorrectorL1'),
      skipEM = cms.bool(True),
      skipEMfractionThreshold = cms.double(0.9),
      skipMuonSelection = cms.string('isGlobalMuon | isStandAloneMuon'),
      skipMuons = cms.bool(True),
      src = cms.InputTag('hltAK4PFPuppiJets'),
      type1JetPtThreshold = cms.double(30.0),
    )

    process.hltPFPuppiMETTypeOne = cms.EDProducer('CorrectedPFMETProducer',
      src = cms.InputTag('hltPFPuppiMET'),
      srcCorrections = cms.VInputTag('hltPFPuppiMETCorrection:type1'),
    )

    process.HLTPFPuppiMETSequence = cms.Sequence(
        process.hltPFPuppiNoLep
      + process.hltPFPuppiMET
      + process.hltPFPuppiMETCorrection
      + process.hltPFPuppiMETTypeOne
    )

    ## Paths

    # Reconstruction path
    process.MC_JMEPFPuppi_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCJMEPFPuppi
      + process.HLTPFPuppiSequence
      + process.HLTAK4PFPuppiJetsSequence
      + process.HLTAK8PFPuppiJetsSequence
      + process.HLTPFPuppiMETSequence
      + process.HLTEndSequence
    )

    #### HLT paths development area
    # example customization for creating HLT_PFPuppiJet40_v1 path
    ## HLT_PFPuppiJet40_v1
    process.hltPrePFPuppiJet40 = cms.EDFilter("HLTPrescaler",
        L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
        offset = cms.uint32(0)
    )

    process.hltPFPuppiJetsCorrectedMatchedToCaloJets10 = cms.EDProducer("HLTPFJetsMatchedToFilteredCaloJetsProducer",
        maxDeltaR = cms.double(0.5),
        src = cms.InputTag("hltAK4PFPuppiJetsCorrected"),
        triggerJetsFilter = cms.InputTag("hltSingleCaloJet10"),
        triggerJetsType = cms.int32(85)
    )

    process.hltSinglePFPuppiJet40 = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(5.0),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(1),
        MinPt = cms.double(40.0),
        inputTag = cms.InputTag("hltPFPuppiJetsCorrectedMatchedToCaloJets10"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(85)
    )


    process.HLT_PFPuppiJet40_v1 = cms.Path(
        process.SimL1Emulator
      + process.HLTBeginSequence 
      + process.hltL1sZeroBias                # L1 seed
      + process.hltPrePFPuppiJet40            # prescale filter
      + process.HLTAK4CaloJetsSequence        # produce calo jets
      + process.hltSingleCaloJet10            # filter calos > 10 GeV (for matching - see later)  
      + process.HLTPFPuppiSequence            # produce pf particles and puppi weights
      + process.HLTAK4PFPuppiJetsSequence     # make AK4 jets reconstruction using puppi weights + calibrations
      + process.hltPFPuppiJetsCorrectedMatchedToCaloJets10  # match puppi to calo jets with dR<0.5 
      + process.hltSinglePFPuppiJet40              # filter puppi jets with pT>40GeV
      + process.HLTEndSequence
    )
    
    ## adding paths in "trigger menu"
    # modify this list of names with any new path
    newPathNames = [
       'HLT_PFPuppiJet40_v1'
    ] 
    
    # Adds the paths in the menu
    for pathName in newPathNames:
       process.datasets.JetMET += cms.vstring(pathName)
       process.datasets.OnlineMonitor += cms.vstring(pathName)
       process.hltDatasetJetMET.triggerConditions += cms.vstring(pathName)
       process.hltDatasetOnlineMonitor.triggerConditions += cms.vstring(pathName + ' / 3')
       listOfPaths.append(pathName)
       
    # append new paths to schedule
    if process.schedule_():
      process.schedule_().append(process.MC_JMEPFPuppi_v1)
      process.schedule_().append(process.HLT_PFPuppiJet40_v1)

    return [process,listOfPaths]
