import FWCore.ParameterSet.Config as cms

from CommonTools.ParticleFlow.pfPileUp_cfi import pfPileUp as _pfPileUp

from CommonTools.ParticleFlow.TopProjectors.pfNoPileUp_cfi import pfNoPileUp as _pfNoPileUp
from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep
#from CommonTools.RecoAlgos.primaryVertexAssociation_cfi import primaryVertexAssociation

from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets as _ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi as _ak4PFJetsPuppi, ak4PFJetsCHS as _ak4PFJetsCHS
from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsPuppi as _ak8PFJetsPuppi, ak8PFJetsCHS as _ak8PFJetsCHS

from RecoParticleFlow.PFProducer.particleFlowTmpPtrs_cfi import particleFlowTmpPtrs as _particleFlowTmpPtrs

from JMETriggerAnalysis.Common.multiplicityValueProducerFromNestedCollectionEdmNewDetSetVectorSiPixelClusterDouble_cfi\
 import multiplicityValueProducerFromNestedCollectionEdmNewDetSetVectorSiPixelClusterDouble as _nSiPixelClusters

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

def addPaths_MC_JMEPFPuppi(process, change_params_list=[]):

    process.hltPreMCJMEPFPuppi = cms.EDFilter('HLTPrescaler',
      L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
      offset = cms.uint32(0)
    )

    process.hltPixelClustersMultiplicity = _nSiPixelClusters.clone(src = 'hltSiPixelClusters', defaultValue = -1.)
    
    ## add offline puppi
    #process.offlinePFPuppi = _puppi.clone(
    #  #candName = 'packedPFCandidates',
    #  #vertexName = 'offlineSlimmedPrimaryVertices',
    #  #useExistingWeights = False
    #  useVertexAssociation=False
    #)

    #process.OfflinePFPuppiSequence = cms.Sequence(
    #  process.offlinePFPuppi
    #)

    process.hltPFPuppi = _puppi.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltPixelVertices',
      UseDeltaZCut = True,
      EtaMinUseDeltaZ = 0.0,
      DeltaZCut = 0.3,
      #UseFromPVLooseTight = True,
      vtxNdofCut = 4,
      vtxZCut=24,
      #vertexName = 'hltVerticesPF',
      #usePUProxyValue = True,
      #PUProxyValue = 'hltPixelClustersMultiplicity',
      #NumOfPUVtxsForCharged = 0,
      useVertexAssociation = False,
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
    process.hltPFPuppiNoLep = _puppiNoLep.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltPixelVertices',
      UseDeltaZCut = True,
      EtaMinUseDeltaZ = 0.0,
      DeltaZCut = 0.3,
      #UseFromPVLooseTight = True,
      vtxNdofCut = 4,
      vtxZCut=24,
      #vertexName = 'hltVerticesPF',
      #usePUProxyValue = True,
      #PUProxyValue = 'hltPixelClustersMultiplicity',
      #NumOfPUVtxsForCharged = 0,
      useVertexAssociation = False,
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

    ## Modifications to PUPPI parameters
    for mod_i in [process.hltPFPuppi, process.hltPFPuppiNoLep]:
      for algo_idx in range(len(mod_i.algos)):
        if len(mod_i.algos[algo_idx].MinNeutralPt) != len(mod_i.algos[algo_idx].MinNeutralPtSlope):
          raise RuntimeError('instance of PuppiProducer is misconfigured:\n\n'+str(mod_i)+' = '+mod_i.dumpPython())

        #for algoReg_idx in range(len(mod_i.algos[algo_idx].MinNeutralPt)):
        #  mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] += 2.56 * mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx]
        #  mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] *= 0.00271
        #  ## for checks without any cut at neutrals pT i.e. MinNeutralPt==0 and MinNeutralPtSlope==0
        #  #mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] = 0.0
        #  #mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] = 0.0
          
      # changes per specific region
      regions_dict={ 'HB':[0,0], 'HE1':[0,1], 'HE2':[1,0], 'HF':[1,1]}
      for change in change_params_list:
        if change[1]=='MinNeutralPt':
          mod_i.algos[regions_dict[change[0]][0]].MinNeutralPt[regions_dict[change[0]][1]] *= float(change[2])
        elif change[1]=='MinNeutralPtSlope':
          mod_i.algos[regions_dict[change[0]][0]].MinNeutralPtSlope[regions_dict[change[0]][1]] *= float(change[2])
        elif change[1]=='RMSEtaSF':
          mod_i.algos[regions_dict[change[0]][0]].RMSEtaSF[regions_dict[change[0]][1]] *= float(change[2])
        elif change[1]=='MedEtaSF':
          mod_i.algos[regions_dict[change[0]][0]].MedEtaSF[regions_dict[change[0]][1]] *= float(change[2])
        else: 
          continue

    ## Path
    #+ process.OfflinePFPuppiSequence # calculate the offline puppi PF first
    process.MC_JMEPFPuppi_v1 = cms.Path(
        process.HLTBeginSequence
      #+ process.OfflinePFPuppiSequence # calculate the offline puppi PF first
      + process.hltPreMCJMEPFPuppi
      + process.HLTPFPuppiSequence
      + process.HLTAK4PFPuppiJetsSequence
      + process.HLTAK8PFPuppiJetsSequence
      + process.HLTPFPuppiMETSequence
      + process.HLTEndSequence
    )

    if process.schedule_():
      process.schedule_().append(process.MC_JMEPFPuppi_v1)

    return process
