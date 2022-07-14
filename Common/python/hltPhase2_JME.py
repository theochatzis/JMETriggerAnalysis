import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiCentral as _puppiCentral, puppiForward as _puppiForward, puppiNoLep as _puppiNoLep
from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets
from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets, ak4PFJetsCHS, ak4PFJetsPuppi
from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJets, ak8PFJetsCHS, ak8PFJetsPuppi
from RecoMET.METProducers.PFClusterMET_cfi import pfClusterMet

def customise_hltPhase2_JME(process):
    ### Guidelines to browse the code below:
    ###  - jet (MET) collections are indicated by comments starting with "## Jets: " ("## MET:")
    ###  - sequences are indicated by comments starting with "## Sequence: "
    ###  - HLT-related collections (sequences) start with "hlt" ("HLT")
    ###  - modifications that are temporary and/or likely to change in a more realistic HLT menu are indicated by "#!!"
    ###    (at the moment, these might simply indicate differences between the current configuration and the one used in the 2018 HLT-Menu)

    #### check if reconstruction sequence exists
    if not hasattr(process, 'reconstruction'):
       raise RuntimeError('reconstruction sequence process.reconstruction not found')

    _particleFlowCands = 'particleFlowTmp'
    if not hasattr(process, _particleFlowCands):
       raise RuntimeError('process has no member named "'+_particleFlowCands+'"')

    #_primaryVertices = 'offlinePrimaryVertices' # changed to : 
    _primaryVertices = 'hltPhase2OfflinePrimaryVertices'
    
    if not hasattr(process, _primaryVertices):
       raise RuntimeError('process has no member named "'+_primaryVertices+'"')

    _primaryVerticesGood = 'goodOfflinePrimaryVertices'

    ## Jets: AK4 Calo
    process.hltAK4CaloJets = process.ak4CaloJets.clone(
      src = 'towerMaker',
      useDeterministicSeed = True,
      doAreaDiskApprox = True,
      doAreaFastjet = False,
      doPUOffsetCorr = False,
      doRhoFastjet = False,
      srcPVs = 'NotUsed',
      doPVCorrection = False,
    )

#    ## Jets: AK8 Calo
#    process.hltAK8CaloJets = process.hltAK4CaloJets.clone(rParam = 0.8)

    ## Sequence: Calo Jets
    process.HLTCaloJetsReconstruction = cms.Sequence(
      process.hltAK4CaloJets
    )

    ## MET: Calo
    process.hltCaloMET = cms.EDProducer("CaloMETProducer",
      alias = cms.string('RawCaloMET'),
      calculateSignificance = cms.bool(False),
      globalThreshold = cms.double(0.3),
      noHF = cms.bool(False),
      src = cms.InputTag("towerMaker") #!! hltTowerMakerForAll
    )

    ## Sequence: Calo MET
    process.HLTCaloMETReconstruction = cms.Sequence(
      process.hltCaloMET
    )

    ## Jets: AK4 PFClusters
    process.load('RecoJets.JetProducers.PFClustersForJets_cff')

    # add PFClusters from HGCal
    process.pfClusterRefsForJetsHGCAL = cms.EDProducer('PFClusterRefCandidateProducer',
      src = cms.InputTag('particleFlowClusterHGCal'),
      particleType = cms.string('pi+'),
    )
    process.pfClusterRefsForJets_stepTask.add(process.pfClusterRefsForJetsHGCAL)
    process.pfClusterRefsForJets.src += ['pfClusterRefsForJetsHGCAL']

    process.hltAK4PFClusterJets = ak4PFClusterJets.clone(
      doPVCorrection = False,
      srcPVs = 'NotUsed',
    )

    ## Jets: AK8 PFClusters
    process.hltAK8PFClusterJets = process.hltAK4PFClusterJets.clone(rParam = 0.8)

    ## MET: PFClusters
    process.hltPFClusterMET = cms.EDProducer("PFClusterMETProducer",
      src = cms.InputTag('pfClusterRefsForJets'),
      alias = cms.string('pfClusterMet'),
      globalThreshold = cms.double(0.0)
    )

    ## Sequence: PFClusterJets and PFClusterMET
    process.HLTPFClusterJMEReconstruction = cms.Sequence(
        process.pfClusterRefsForJets_step
      + process.hltAK4PFClusterJets
      + process.hltAK8PFClusterJets
      + process.hltPFClusterMET
    )

    ## Jets: AK4 PF
    process.hltAK4PFJets = ak4PFJets.clone(
      src = _particleFlowCands,
#     jetPtMin = 10.,
    )
    process.hltAK4PFJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK4PFJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK4PFJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PF' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK4PFJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFJetCorrectorL1',
        'hltAK4PFJetCorrectorL2',
        'hltAK4PFJetCorrectorL3',
      )
    )
    process.hltAK4PFJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK4PFJets' ),
      correctors = cms.VInputTag( 'hltAK4PFJetCorrector' ),
    )

    ## Sequence: AK4 PF Jets
    process.HLTAK4PFJetsReconstruction = cms.Sequence(
        process.hltAK4PFJets
      + process.hltAK4PFJetCorrectorL1
      + process.hltAK4PFJetCorrectorL2
      + process.hltAK4PFJetCorrectorL3
      + process.hltAK4PFJetCorrector
      + process.hltAK4PFJetsCorrected
    )

    ## Jets: AK8 PF
    process.hltAK8PFJets = ak8PFJets.clone(
      src = _particleFlowCands,
#     jetPtMin = 80.,
    )
    process.hltAK8PFJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK8PFJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK8PFJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PF' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK8PFJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFJetCorrectorL1',
        'hltAK8PFJetCorrectorL2',
        'hltAK8PFJetCorrectorL3',
      )
    )
    process.hltAK8PFJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK8PFJets' ),
      correctors = cms.VInputTag( 'hltAK8PFJetCorrector' ),
    )

    ## Sequence: AK8 PF Jets
    process.HLTAK8PFJetsReconstruction = cms.Sequence(
        process.hltAK8PFJets
      + process.hltAK8PFJetCorrectorL1
      + process.hltAK8PFJetCorrectorL2
      + process.hltAK8PFJetCorrectorL3
      + process.hltAK8PFJetCorrector
      + process.hltAK8PFJetsCorrected
    )

    ## Jets: AK4 PF+CHS
    process.hltAK4PFCHSJets = ak4PFJetsCHS.clone(
#     jetPtMin = 10.,
    )

    process.hltAK4PFCHSJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK4PFCHSJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK4PFCHSJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFchs' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK4PFCHSJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFCHSJetCorrectorL1',
        'hltAK4PFCHSJetCorrectorL2',
        'hltAK4PFCHSJetCorrectorL3',
      )
    )
    process.hltAK4PFCHSJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK4PFCHSJets' ),
      correctors = cms.VInputTag( 'hltAK4PFCHSJetCorrector' ),
    )

    ## Jets: AK8 PF+CHS
    process.hltAK8PFCHSJets = ak8PFJetsCHS.clone(
#     jetPtMin = 80.,
    )

    process.hltAK8PFCHSJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK8PFCHSJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK8PFCHSJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFchs' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK8PFCHSJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK8PFCHSJetCorrectorL1',
        'hltAK8PFCHSJetCorrectorL2',
        'hltAK8PFCHSJetCorrectorL3',
      )
    )
    process.hltAK8PFCHSJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK8PFCHSJets' ),
      correctors = cms.VInputTag( 'hltAK8PFCHSJetCorrector' ),
    )

    ## Sequence: PF+CHS Jets, AK4 and AK8
    process.particleFlowPtrs.src = _particleFlowCands

    process.goodOfflinePrimaryVertices.src = _primaryVertices

    process.HLTPFJetsCHSReconstruction = cms.Sequence(
        process.particleFlowPtrs
      + process.goodOfflinePrimaryVertices
      + process.pfPileUpJME
      + process.pfNoPileUpJME
      + process.hltAK4PFCHSJets
      + process.hltAK4PFCHSJetCorrectorL1
      + process.hltAK4PFCHSJetCorrectorL2
      + process.hltAK4PFCHSJetCorrectorL3
      + process.hltAK4PFCHSJetCorrector
      + process.hltAK4PFCHSJetsCorrected
      + process.hltAK8PFCHSJets
      + process.hltAK8PFCHSJetCorrectorL1
      + process.hltAK8PFCHSJetCorrectorL2
      + process.hltAK8PFCHSJetCorrectorL3
      + process.hltAK8PFCHSJetCorrector
      + process.hltAK8PFCHSJetsCorrected
    )

    ## MET: PF Raw
    process.hltPFMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( _particleFlowCands ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False ),
    )

    ## MET: PF Type-1
    _jescLabelForPFMETTypeOne = 'AK4PFchs'
    _jetsForPFMETTypeOne = 'hltAK4PFCHSJets'

    process.hltPFMETJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltPFMETJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L2Relative' )
    )
    process.hltPFMETJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( _jescLabelForPFMETTypeOne ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltPFMETJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag( 'hltPFMETJetCorrectorL1','hltPFMETJetCorrectorL2','hltPFMETJetCorrectorL3' )
    )
    process.hltPFMETTypeOneCorrector = cms.EDProducer( 'PFJetMETcorrInputProducer',
      src = cms.InputTag( _jetsForPFMETTypeOne ),
      type1JetPtThreshold = cms.double( 30. ),
      skipEMfractionThreshold = cms.double( 0.9 ),
      skipEM = cms.bool( True ),
      jetCorrLabelRes = cms.InputTag( 'hltPFMETJetCorrector' ),
      offsetCorrLabel = cms.InputTag( 'hltPFMETJetCorrectorL1' ),
      skipMuons = cms.bool( True ),
      skipMuonSelection = cms.string( 'isGlobalMuon | isStandAloneMuon' ),
      jetCorrEtaMax = cms.double( 9.9 ),
      jetCorrLabel = cms.InputTag( 'hltPFMETJetCorrector' ),
    )
    process.hltPFMETTypeOne = cms.EDProducer( 'CorrectedPFMETProducer',
      src = cms.InputTag( 'hltPFMET' ),
      srcCorrections = cms.VInputTag( 'hltPFMETTypeOneCorrector:type1' )
    )

    ## Sequence: MET PF, Raw and Type-1
    process.HLTPFMETsReconstruction = cms.Sequence(
        process.hltPFMET
      + process.hltPFMETJetCorrectorL1
      + process.hltPFMETJetCorrectorL2
      + process.hltPFMETJetCorrectorL3
      + process.hltPFMETJetCorrector
      + process.hltPFMETTypeOneCorrector
      + process.hltPFMETTypeOne
    )

    ## MET: CHS
    process.hltParticleFlowCHS = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
      src = process.hltAK4PFCHSJets.src,
    )
    process.hltPFCHSMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( 'hltParticleFlowCHS' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False ),
    )

    ## Sequence: MET CHS
    process.HLTPFCHSMETReconstruction = cms.Sequence(
        process.hltParticleFlowCHS
      + process.hltPFCHSMET
    )

    ## MET: SoftKiller
    process.hltParticleFlowSoftKiller = cms.EDProducer('SoftKillerProducer',
      PFCandidates = cms.InputTag( _particleFlowCands ),
      Rho_EtaMax = cms.double( 5.0 ),
      rParam = cms.double( 0.4 )
    )
    process.hltPFSoftKillerMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( 'hltParticleFlowSoftKiller' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False )
    )

    ## Sequence: MET SoftKiller
    process.HLTPFSoftKillerMETReconstruction = cms.Sequence(
        process.hltParticleFlowSoftKiller
      + process.hltPFSoftKillerMET
    )

    ## Jets: PFPuppi AK4
    process.hltPFPuppi = _puppi.clone(
      candName = _particleFlowCands,
      vertexName = _primaryVerticesGood,
#      PtMaxCharged = 20.,
#      EtaMinUseDeltaZ = 4.0,
#      PtMaxNeutralsStartSlope = 20.,
#      NumOfPUVtxsForCharged = 2,
#      puppiDiagnostics = False,
    )
#    process.hltPFPuppi.algos[0].etaMin[0] = -0.01

    process.hltAK4PFPuppiJets = ak4PFJetsPuppi.clone(
      src = _particleFlowCands,
      applyWeight = True,
      srcWeights = 'hltPFPuppi',
#     jetPtMin = 10.,
    )
    process.hltAK4PFPuppiJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK4PFPuppiHLT' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK4PFPuppiJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFPuppiHLT' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK4PFPuppiJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK4PFPuppiHLT' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK4PFPuppiJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
      correctors = cms.VInputTag(
        'hltAK4PFPuppiJetCorrectorL1',
        'hltAK4PFPuppiJetCorrectorL2',
        'hltAK4PFPuppiJetCorrectorL3',
      )
    )
    process.hltAK4PFPuppiJetsCorrected = cms.EDProducer('CorrectedPFJetProducer',
      src = cms.InputTag( 'hltAK4PFPuppiJets' ),
      correctors = cms.VInputTag( 'hltAK4PFPuppiJetCorrector' ),
    )

    ## Jets: PFPuppi AK8
    process.hltAK8PFPuppiJets = ak8PFJetsPuppi.clone(
      src = _particleFlowCands,
      applyWeight = True,
      srcWeights = 'hltPFPuppi',
#     jetPtMin = 80.,
    )
    process.hltAK8PFPuppiJetCorrectorL1 = cms.EDProducer( 'L1FastjetCorrectorProducer',
      srcRho = cms.InputTag( 'fixedGridRhoFastjetAllTmp' ),
      algorithm = cms.string( 'AK8PFPuppiHLT' ),
      level = cms.string( 'L1FastJet' )
    )
    process.hltAK8PFPuppiJetCorrectorL2 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFPuppiHLT' ),
      level = cms.string( 'L2Relative' )
    )
    process.hltAK8PFPuppiJetCorrectorL3 = cms.EDProducer( 'LXXXCorrectorProducer',
      algorithm = cms.string( 'AK8PFPuppiHLT' ),
      level = cms.string( 'L3Absolute' )
    )
    process.hltAK8PFPuppiJetCorrector = cms.EDProducer( 'ChainedJetCorrectorProducer',
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

    ## MET: PFPuppi Raw

    # PFPuppi candidates for MET
    process.hltPFPuppiNoLep = _puppiNoLep.clone(
      candName = _particleFlowCands,
      vertexName = _primaryVerticesGood,
#      PtMaxCharged = 20.,
#      EtaMinUseDeltaZ = 4.0,
#      PtMaxNeutralsStartSlope = 20.,
#      NumOfPUVtxsForCharged = 2,
#      puppiDiagnostics = False,
    )
#    process.hltPFPuppiNoLep.algos[0].etaMin[0] = -0.01

    process.hltPFPuppiMETv0 = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( _particleFlowCands ),
      applyWeight = cms.bool( True ),
      srcWeights = cms.InputTag( 'hltPFPuppi' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False ),
    )

    process.hltPFPuppiMET = cms.EDProducer( 'PFMETProducer',
      src = cms.InputTag( _particleFlowCands ),
      applyWeight = cms.bool( True ),
      srcWeights = cms.InputTag( 'hltPFPuppiNoLep' ),
      globalThreshold = cms.double( 0.0 ),
      calculateSignificance = cms.bool( False ),
    )

    ## MET: PFPuppi Type-1
    process.hltPFPuppiMETTypeOneCorrector = cms.EDProducer( 'PFJetMETcorrInputProducer',
      src = cms.InputTag( 'hltAK4PFPuppiJets' ),
      type1JetPtThreshold = cms.double( 30. ),
      skipEMfractionThreshold = cms.double( 0.9 ),
      skipEM = cms.bool( True ),
      jetCorrLabelRes = cms.InputTag( 'hltAK4PFPuppiJetCorrector' ),
      offsetCorrLabel = cms.InputTag( 'hltAK4PFPuppiJetCorrectorL1' ),
      skipMuons = cms.bool( True ),
      skipMuonSelection = cms.string( 'isGlobalMuon | isStandAloneMuon' ),
      jetCorrEtaMax = cms.double( 9.9 ),
      jetCorrLabel = cms.InputTag( 'hltAK4PFPuppiJetCorrector' )
    )
    process.hltPFPuppiMETTypeOne = cms.EDProducer( 'CorrectedPFMETProducer',
      src = cms.InputTag( 'hltPFPuppiMET' ),
      srcCorrections = cms.VInputTag( 'hltPFPuppiMETTypeOneCorrector:type1' )
    )

    ## Sequence: PFPuppi Jets and MET
    process.HLTPFPuppiJMEReconstruction = cms.Sequence(
        process.goodOfflinePrimaryVertices
      + process.hltPFPuppiNoLep
      + process.hltPFPuppiMET
      + process.hltPFPuppi
      + process.hltPFPuppiMETv0
      + process.hltAK4PFPuppiJets
      + process.hltAK4PFPuppiJetCorrectorL1
      + process.hltAK4PFPuppiJetCorrectorL2
      + process.hltAK4PFPuppiJetCorrectorL3
      + process.hltAK4PFPuppiJetCorrector
      + process.hltAK4PFPuppiJetsCorrected
      + process.hltPFPuppiMETTypeOneCorrector
      + process.hltPFPuppiMETTypeOne
      + process.hltAK8PFPuppiJets
      + process.hltAK8PFPuppiJetCorrectorL1
      + process.hltAK8PFPuppiJetCorrectorL2
      + process.hltAK8PFPuppiJetCorrectorL3
      + process.hltAK8PFPuppiJetCorrector
      + process.hltAK8PFPuppiJetsCorrected
    )

    return process
