def customisedHLTProcess(keyword):

    if keyword == 'HLT':
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process

    elif keyword == 'HLT_trkIter2GlobalPtSeed0p9':
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process
       from JMETriggerAnalysis.Common.configs.customise_HLT_trkIter2Global import customise_HLT_trkIter2Global
       process = customise_HLT_trkIter2Global(process, ptMin = 0.9)

    elif keyword == 'HLT_trkIter2RegionalPtSeed0p9':
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process
       process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 0.9

    elif keyword == 'HLT_trkIter2RegionalPtSeed2p0':
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process
       process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 2.0

    elif keyword == 'HLT_trkIter2RegionalPtSeed5p0':
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process
       process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 5.0

    elif keyword == 'HLT_trkIter2RegionalPtSeed10p0':
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process
       process.hltIter2PFlowPixelTrackingRegions.RegionPSet.ptMin = 10.0

    elif keyword.startswith('HLT_singleTrkIterWithPatatrack_v01'):
       from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_1_0_GRun_V11_configDump import cms, process

       from HLTrigger.Configuration.customizeHLTforPatatrack import customise_for_Patatrack_on_cpu
       process = customise_for_Patatrack_on_cpu(process)

       from JMETriggerAnalysis.Common.customise_hltTRK_singleIteration import customise_hltTRK_singleIteration
       process = customise_hltTRK_singleIteration(process)

       if keyword.endswith('_pixVtxFrac0p00'):
          process.hltTrimmedPixelVertices.fractionSumPt2 = -1.
          process.hltTrimmedPixelVertices.minSumPt2 = -1.
       elif keyword.endswith('_pixVtxFrac0p01'):
          process.hltTrimmedPixelVertices.fractionSumPt2 = 0.01
       elif keyword.endswith('_pixVtxFrac0p10'):
          process.hltTrimmedPixelVertices.fractionSumPt2 = 0.10
       elif keyword.endswith('_pixVtxFrac0p30'):
          process.hltTrimmedPixelVertices.fractionSumPt2 = 0.30
       else:
          raise RuntimeError('invalid argument for option "keyword": "'+keyword+'"')

       ## enforce sorting of Pixel Vertices
       process.hltUnsortedPixelVertices = process.hltPixelVertices.clone()

       process.hltPixelVertices = cms.EDProducer('PixelVerticesSelector',

         src = cms.InputTag('hltUnsortedPixelVertices'),

         minSumPt2 = cms.double( -1. ),
         minSumPt2FractionWrtMax = cms.double( -1. ),

         # criterion to rank pixel vertices
         # (utilizes PVClusterComparer to compute
         # the vertex SumPt2 f.o.m. using a sub-set of tracks)
         ranker = cms.PSet(
           refToPSet_ = cms.string('HLTPSetPvClusterComparerForIT')
         ),

         # retain only first N vertices
         maxNVertices = cms.int32( -1 ),
       )

       process.HLTRecopixelvertexingSequence.insert(
         process.HLTRecopixelvertexingSequence.index(process.hltPixelVertices),
         process.hltUnsortedPixelVertices
       )

       ## modules
       process.hltParticleFlowNoMu = cms.EDFilter('GenericPFCandidateSelector',
         src = cms.InputTag('hltParticleFlow'),
         cut = cms.string('particleId != 3'),
       )

       process.hltPFMETNoMuProducer = cms.EDProducer('PFMETProducer',
         alias = cms.string('pfMetNoMu'),
         calculateSignificance = cms.bool(False),
         globalThreshold = cms.double(0.0),
         src = cms.InputTag('hltParticleFlowNoMu')
       )

#       ## add path: MC_AK4PFJets_v1
#       process.hltPreMCAK4PFJets = cms.EDFilter('HLTPrescaler',
#         L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
#         offset = cms.uint32(0)
#       )
#    
#       process.hltAK4PFJetCollection20Filter = cms.EDFilter('HLT1PFJet',
#         MaxEta = cms.double(3.0),
#         MaxMass = cms.double(-1.0),
#         MinE = cms.double(-1.0),
#         MinEta = cms.double(-1.0),
#         MinMass = cms.double(-1.0),
#         MinN = cms.int32(1),
#         MinPt = cms.double(20.0),
#         inputTag = cms.InputTag('hltAK4PFJetsCorrected'),
#         saveTags = cms.bool(True),
#         triggerType = cms.int32(85)
#       )
#    
#       process.MC_AK4PFJets_v1 = cms.Path(
#           process.HLTBeginSequence
#         + process.hltPreMCAK4PFJets
#         + process.HLTAK4PFJetsSequence
#         + process.hltAK4PFJetCollection20Filter
#         + process.HLTEndSequence
#       )
    
#       ## add path: MC_AK8PFJets_v1
#       process.hltPreMCAK8PFJets = process.hltPreMCAK4PFJets.clone()
#    
#       from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJets
#       process.hltAK8PFJets = ak8PFJets.clone(
#         src = 'hltParticleFlow',
#       )
#    
#       process.hltAK8PFL1Corrector = cms.EDProducer('L1FastjetCorrectorProducer', algorithm = cms.string('AK8PFHLT'), level = cms.string('L1FastJet'), srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'))
#       process.hltAK8PFL2Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK8PFHLT'), level = cms.string('L2Relative'))
#       process.hltAK8PFL3Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK8PFHLT'), level = cms.string('L3Absolute'))
#       process.hltAK8PFCorrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK8PFL1Corrector','hltAK8PFL2Corrector','hltAK8PFL3Corrector'))
#       process.hltAK8PFJetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK8PFJets'), correctors = cms.VInputTag('hltAK8PFCorrector'))
#    
#       # add place-holder sequence here (redefined below)
#       process.HLTParticleFlowJMESequence = cms.Sequence()
#    
#       process.HLTAK8PFJetsSequence = cms.Sequence(
#           process.HLTParticleFlowJMESequence
#         + process.hltAK8PFJets
#         + process.hltFixedGridRhoFastjetAll
#         + process.hltAK8PFL1Corrector
#         + process.hltAK8PFL2Corrector
#         + process.hltAK8PFL3Corrector
#         + process.hltAK8PFCorrector
#         + process.hltAK8PFJetsCorrected
#       )
#    
#       process.hltAK8PFJetsCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
#         inputTag = 'hltAK8PFJetsCorrected'
#       )
#    
#       process.MC_AK8PFJets_v1 = cms.Path(
#           process.HLTBeginSequence
#         + process.hltPreMCAK8PFJets
#         + process.HLTAK8PFJetsSequence
#         + process.hltAK8PFJetsCollection20Filter
#         + process.HLTEndSequence
#       )
    
       ## add path: MC_PFMETNoMu_v1
       process.hltPreMCPFMET = cms.EDFilter('HLTPrescaler',
         L1GtReadoutRecordTag = cms.InputTag('hltGtStage2Digis'),
         offset = cms.uint32(0)
       )
    
       process.hltPFMETOpenFilter = cms.EDFilter('HLT1PFMET',
         MaxEta = cms.double(-1.0),
         MaxMass = cms.double(-1.0),
         MinE = cms.double(-1.0),
         MinEta = cms.double(-1.0),
         MinMass = cms.double(-1.0),
         MinN = cms.int32(1),
         MinPt = cms.double(-1.0),
         inputTag = cms.InputTag('hltPFMETProducer'),
         saveTags = cms.bool(True),
         triggerType = cms.int32(87)
       )
    
       process.MC_PFMET_v1 = cms.Path(
           process.HLTBeginSequence
         + process.hltPreMCPFMET
         + process.HLTAK4PFJetsSequence
         + process.hltPFMETProducer
         + process.hltPFMETOpenFilter
         + process.HLTEndSequence
       )
    
       ## add path: MC_CaloMET_v1
       process.hltPreMCCaloMET = process.hltPreMCPFMET.clone()
    
       process.hltCaloMETOpenFilter = cms.EDFilter('HLT1CaloMET',
         MaxEta = cms.double(-1.0),
         MaxMass = cms.double(-1.0),
         MinE = cms.double(-1.0),
         MinEta = cms.double(-1.0),
         MinMass = cms.double(-1.0),
         MinN = cms.int32(1),
         MinPt = cms.double(0.0),
         inputTag = cms.InputTag('hltMet'),
         saveTags = cms.bool(True),
         triggerType = cms.int32(87)
       )
    
       process.MC_CaloMET_v1 = cms.Path(
           process.HLTBeginSequence
         + process.hltPreMCCaloMET
         + process.HLTRecoMETSequence
         + process.hltCaloMETOpenFilter
         + process.HLTEndSequence
       )
    
    else:
       raise RuntimeError('invalid argument for option "keyword": "'+keyword+'"')

    ## add path: MC_AK4PFClusterJets_v1
    process.hltPreMCAK4PFClusterJets = process.hltPreMCAK4PFJets.clone()

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
      src = cms.VInputTag('hltParticleFlowClusterRefsECALUnseeded', 'hltParticleFlowClusterRefsHCAL', 'hltParticleFlowClusterRefsHF')
    )
    
    from RecoJets.JetProducers.ak4PFClusterJets_cfi import ak4PFClusterJets
    process.hltAK4PFClusterJets = ak4PFClusterJets.clone(
      src = 'hltParticleFlowClusterRefs',
      doPVCorrection = False,
    )
    
    process.HLTPFClusterRefsSequence = cms.Sequence(
        process.HLTParticleFlowSequence
      + process.hltParticleFlowClusterRefsECALUnseeded
      + process.hltParticleFlowClusterRefsHCAL
      + process.hltParticleFlowClusterRefsHF
      + process.hltParticleFlowClusterRefs
    )
    
    process.HLTAK4PFClusterJetsSequence = cms.Sequence(
        process.HLTPFClusterRefsSequence
      + process.hltAK4PFClusterJets
    )
    
    process.MC_AK4PFClusterJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PFClusterJets
      + process.HLTAK4PFClusterJetsSequence
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK8PFClusterJets_v1
    process.hltPreMCAK8PFClusterJets = process.hltPreMCAK4PFJets.clone()
    
    process.hltAK8PFClusterJets = process.hltAK4PFClusterJets.clone(rParam = 0.8)
    
    process.HLTAK8PFClusterJetsSequence = cms.Sequence(
        process.HLTPFClusterRefsSequence
      + process.hltAK8PFClusterJets
    )
    
    process.MC_AK8PFClusterJets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PFClusterJets
      + process.HLTAK8PFClusterJetsSequence
      + process.HLTEndSequence
    )
    
    ## add path: MC_PFClusterMET_v1
    process.hltPreMCPFClusterMET = process.hltPreMCPFMET.clone()
    
    process.hltPFClusterMET = cms.EDProducer('PFClusterMETProducer',
      src = cms.InputTag('hltParticleFlowClusterRefs'),
      globalThreshold = cms.double(0.0),
      alias = cms.string('')
    )
    
    process.MC_PFClusterMET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPFClusterMET
      + process.HLTPFClusterRefsSequence
      + process.hltPFClusterMET
      + process.HLTEndSequence
    )
    
    ## add path: MC_PFMETNoMu_v1
    process.hltPreMCPFMETNoMu = process.hltPreMCPFMET.clone()
    
    process.hltPFMETNoMuOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPFMETNoMuProducer'
    )
    
    process.HLTParticleFlowJMESequence = cms.Sequence(
        process.HLTPreAK4PFJetsRecoSequence
      + process.HLTL2muonrecoSequence
      + process.HLTL3muonrecoSequence
      + process.HLTTrackReconstructionForPF
      + process.HLTParticleFlowSequence
    )
    
    process.MC_PFMETNoMu_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPFMETNoMu
      + process.HLTParticleFlowJMESequence
      + process.hltParticleFlowNoMu
      + process.hltPFMETNoMuProducer
      + process.hltPFMETNoMuOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK4PFCHSv1Jets_v1
    if not hasattr(process, 'hltVerticesPF'):
       process.hltVerticesPF = cms.EDProducer('PrimaryVertexProducer',
         TkClusParameters = cms.PSet(
            TkDAClusParameters = cms.PSet(
                Tmin = cms.double(2.4),
                Tpurge = cms.double(2.0),
                Tstop = cms.double(0.5),
                coolingFactor = cms.double(0.6),
                d0CutOff = cms.double(999.0),
                dzCutOff = cms.double(4.0),
                uniquetrkweight = cms.double(0.9),
                use_vdt = cms.untracked.bool(True),
                vertexSize = cms.double(0.15),
                zmerge = cms.double(0.01)
            ),
            algorithm = cms.string('DA_vect')
         ),
         TkFilterParameters = cms.PSet(
            algorithm = cms.string('filter'),
            maxD0Significance = cms.double(999.0),
            maxEta = cms.double(100.0),
            maxNormalizedChi2 = cms.double(20.0),
            minPixelLayersWithHits = cms.int32(2),
            minPt = cms.double(0.0),
            minSiliconLayersWithHits = cms.int32(5),
            trackQuality = cms.string('any')
         ),
         TrackLabel = cms.InputTag('hltPFMuonMerging'),
         beamSpotLabel = cms.InputTag('hltOnlineBeamSpot'),
         verbose = cms.untracked.bool(False),
         vertexCollections = cms.VPSet(
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(3.0),
                label = cms.string(''),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(0.0),
                useBeamConstraint = cms.bool(False)
            ),
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(3.0),
                label = cms.string('WithBS'),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(0.0),
                useBeamConstraint = cms.bool(True)
            )
         )
       )
    
    #if not hasattr(process, 'hltVerticesPFSelector'):
    #   process.hltVerticesPFSelector = cms.EDFilter('PrimaryVertexObjectFilter',
    #     filterParams = cms.PSet(
    #       maxRho = cms.double(2.0),
    #       maxZ = cms.double(24.0),
    #       minNdof = cms.double(4.0),
    #       pvSrc = cms.InputTag('hltVerticesPF')
    #     ),
    #     src = cms.InputTag('hltVerticesPF')
    #   )
    #
    #if not hasattr(process, 'hltVerticesPFFilter'):
    #   process.hltVerticesPFFilter = cms.EDFilter('VertexSelector',
    #     cut = cms.string('!isFake'),
    #     filter = cms.bool(True),
    #     src = cms.InputTag('hltVerticesPFSelector')
    #   )
    
    process.hltPreMCAK4PFCHSv1Jets = process.hltPreMCAK4PFJets.clone()
    
    process.hltParticleFlowPtrs = cms.EDProducer('PFCandidateFwdPtrProducer',
      src = cms.InputTag('hltParticleFlow')
    )
    process.hltParticleFlowCHSv1PileUp = cms.EDProducer('PFPileUp',
      Enable = cms.bool(True),
      PFCandidates = cms.InputTag('hltParticleFlowPtrs'),
      Vertices = cms.InputTag('hltVerticesPF'),
      checkClosestZVertex = cms.bool(False),
      verbose = cms.untracked.bool(False)
    )
    process.hltParticleFlowCHSv1NoPileUp = cms.EDProducer('TPPFCandidatesOnPFCandidates',
      enable = cms.bool(True),
      bottomCollection = cms.InputTag('hltParticleFlowPtrs'),
      name = cms.untracked.string('pileUpOnPFCandidates'),
      topCollection = cms.InputTag('hltParticleFlowCHSv1PileUp'),
#     verbose = cms.untracked.bool(False)
    )
    
    process.HLTParticleFlowCHSv1PtrsSequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltVerticesPF
    #  + process.hltVerticesPFSelector
    #  + process.hltVerticesPFFilter
      + process.hltParticleFlowPtrs
      + process.hltParticleFlowCHSv1PileUp
      + process.hltParticleFlowCHSv1NoPileUp
    )
    
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsCHS
    process.hltAK4PFCHSv1Jets = ak4PFJetsCHS.clone(
      src = 'hltParticleFlowCHSv1NoPileUp',
    )
    
    process.hltAK4PFCHSv1L1Corrector = cms.EDProducer('L1FastjetCorrectorProducer', algorithm = cms.string('AK4PFHLT'), level = cms.string('L1FastJet'), srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'))
    process.hltAK4PFCHSv1L2Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK4PFHLT'), level = cms.string('L2Relative'))
    process.hltAK4PFCHSv1L3Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK4PFHLT'), level = cms.string('L3Absolute'))
    process.hltAK4PFCHSv1Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK4PFCHSv1L1Corrector','hltAK4PFCHSv1L2Corrector','hltAK4PFCHSv1L3Corrector'))
    process.hltAK4PFCHSv1JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK4PFCHSv1Jets'), correctors = cms.VInputTag('hltAK4PFCHSv1Corrector'))
    
    process.HLTAK4PFCHSv1JetsSequence = cms.Sequence(
        process.HLTParticleFlowCHSv1PtrsSequence
      + process.hltAK4PFCHSv1Jets
      + process.hltFixedGridRhoFastjetAll
      + process.hltAK4PFCHSv1L1Corrector
      + process.hltAK4PFCHSv1L2Corrector
      + process.hltAK4PFCHSv1L3Corrector
      + process.hltAK4PFCHSv1Corrector
      + process.hltAK4PFCHSv1JetsCorrected
    )
    
    process.hltAK4PFCHSv1JetsCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK4PFCHSv1JetsCorrected'
    )
    
    process.MC_AK4PFCHSv1Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PFCHSv1Jets
      + process.HLTAK4PFCHSv1JetsSequence
      + process.hltAK4PFCHSv1JetsCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK8PFCHSv1Jets_v1
    process.hltPreMCAK8PFCHSv1Jets = process.hltPreMCAK4PFJets.clone()
    
    from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsCHS
    process.hltAK8PFCHSv1Jets = ak8PFJetsCHS.clone(
      src = 'hltParticleFlowCHSv1NoPileUp',
    )
    
    process.hltAK8PFCHSv1L1Corrector = cms.EDProducer('L1FastjetCorrectorProducer', algorithm = cms.string('AK8PFHLT'), level = cms.string('L1FastJet'), srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'))
    process.hltAK8PFCHSv1L2Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK8PFHLT'), level = cms.string('L2Relative'))
    process.hltAK8PFCHSv1L3Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK8PFHLT'), level = cms.string('L3Absolute'))
    process.hltAK8PFCHSv1Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK8PFCHSv1L1Corrector','hltAK8PFCHSv1L2Corrector','hltAK8PFCHSv1L3Corrector'))
    process.hltAK8PFCHSv1JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK8PFCHSv1Jets'), correctors = cms.VInputTag('hltAK8PFCHSv1Corrector'))
    
    process.HLTAK8PFCHSv1JetsSequence = cms.Sequence(
        process.HLTParticleFlowCHSv1PtrsSequence
      + process.hltAK8PFCHSv1Jets
      + process.hltFixedGridRhoFastjetAll
      + process.hltAK8PFCHSv1L1Corrector
      + process.hltAK8PFCHSv1L2Corrector
      + process.hltAK8PFCHSv1L3Corrector
      + process.hltAK8PFCHSv1Corrector
      + process.hltAK8PFCHSv1JetsCorrected
    )
    
    process.hltAK8PFCHSv1JetsCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK8PFCHSv1JetsCorrected'
    )
    
    process.MC_AK8PFCHSv1Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PFCHSv1Jets
      + process.HLTAK8PFCHSv1JetsSequence
      + process.hltAK8PFCHSv1JetsCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PFCHSv1MET_v1
    process.hltPreMCPFCHSv1MET = process.hltPreMCPFMET.clone()
    
    process.hltParticleFlowCHSv1 = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
      src = process.hltAK4PFCHSv1Jets.src,
    )
    
    process.hltPFCHSv1MET = process.hltPFMETProducer.clone(
      src = 'hltParticleFlowCHSv1',
      alias = ''
    )
    
    process.HLTPFCHSv1METSequence = cms.Sequence(
        process.HLTParticleFlowCHSv1PtrsSequence
      + process.hltParticleFlowCHSv1
      + process.hltPFCHSv1MET
    )
    
    process.hltPFCHSv1METOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPFCHSv1MET'
    )
    
    process.MC_PFCHSv1MET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPFCHSv1MET
      + process.HLTPFCHSv1METSequence
      + process.hltPFCHSv1METOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK4PFCHSv2Jets_v1
    process.hltPreMCAK4PFCHSv2Jets = process.hltPreMCAK4PFJets.clone()
    
    process.hltParticleFlowCHSv2PileUp = cms.EDProducer('PFPileUp',
      Enable = cms.bool(True),
      PFCandidates = cms.InputTag('hltParticleFlowPtrs'),
      Vertices = cms.InputTag('hltPixelVertices'),
      checkClosestZVertex = cms.bool(True),
      verbose = cms.untracked.bool(False)
    )
    process.hltParticleFlowCHSv2NoPileUp = cms.EDProducer('TPPFCandidatesOnPFCandidates',
      enable = cms.bool(True),
      bottomCollection = cms.InputTag('hltParticleFlowPtrs'),
      name = cms.untracked.string('pileUpOnPFCandidates'),
      topCollection = cms.InputTag('hltParticleFlowCHSv2PileUp'),
#     verbose = cms.untracked.bool(False)
    )
    
    process.HLTParticleFlowCHSv2PtrsSequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltParticleFlowPtrs
      + process.hltParticleFlowCHSv2PileUp
      + process.hltParticleFlowCHSv2NoPileUp
    )
    
    process.hltAK4PFCHSv2Jets = ak4PFJetsCHS.clone(
      src = 'hltParticleFlowCHSv2NoPileUp',
    )
    
    process.hltAK4PFCHSv2L1Corrector = cms.EDProducer('L1FastjetCorrectorProducer', algorithm = cms.string('AK4PFHLT'), level = cms.string('L1FastJet'), srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'))
    process.hltAK4PFCHSv2L2Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK4PFHLT'), level = cms.string('L2Relative'))
    process.hltAK4PFCHSv2L3Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK4PFHLT'), level = cms.string('L3Absolute'))
    process.hltAK4PFCHSv2Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK4PFCHSv2L1Corrector','hltAK4PFCHSv2L2Corrector','hltAK4PFCHSv2L3Corrector'))
    process.hltAK4PFCHSv2JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK4PFCHSv2Jets'), correctors = cms.VInputTag('hltAK4PFCHSv2Corrector'))
    
    process.HLTAK4PFCHSv2JetsSequence = cms.Sequence(
        process.HLTParticleFlowCHSv2PtrsSequence
      + process.hltAK4PFCHSv2Jets
      + process.hltFixedGridRhoFastjetAll
      + process.hltAK4PFCHSv2L1Corrector
      + process.hltAK4PFCHSv2L2Corrector
      + process.hltAK4PFCHSv2L3Corrector
      + process.hltAK4PFCHSv2Corrector
      + process.hltAK4PFCHSv2JetsCorrected
    )
    
    process.hltAK4PFCHSv2JetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK4PFCHSv2JetsCorrected'
    )
    
    process.MC_AK4PFCHSv2Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PFCHSv2Jets
      + process.HLTAK4PFCHSv2JetsSequence
      + process.hltAK4PFCHSv2JetCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK8PFCHSv2Jets_v1
    process.hltPreMCAK8PFCHSv2Jets = process.hltPreMCAK4PFJets.clone()
    
    process.hltAK8PFCHSv2Jets = ak8PFJetsCHS.clone(
      src = 'hltParticleFlowCHSv2NoPileUp',
    )
    
    process.hltAK8PFCHSv2L1Corrector = cms.EDProducer('L1FastjetCorrectorProducer', algorithm = cms.string('AK8PFchs'), level = cms.string('L1FastJet'), srcRho = cms.InputTag('hltFixedGridRhoFastjetAll'))
    process.hltAK8PFCHSv2L2Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK8PFchs'), level = cms.string('L2Relative'))
    process.hltAK8PFCHSv2L3Corrector = cms.EDProducer('LXXXCorrectorProducer'     , algorithm = cms.string('AK8PFchs'), level = cms.string('L3Absolute'))
    process.hltAK8PFCHSv2Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK8PFCHSv2L1Corrector','hltAK8PFCHSv2L2Corrector','hltAK8PFCHSv2L3Corrector'))
    process.hltAK8PFCHSv2JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK8PFCHSv2Jets'), correctors = cms.VInputTag('hltAK8PFCHSv2Corrector'))
    
    process.HLTAK8PFCHSv2JetsSequence = cms.Sequence(
        process.HLTParticleFlowCHSv2PtrsSequence
      + process.hltAK8PFCHSv2Jets
      + process.hltFixedGridRhoFastjetAll
      + process.hltAK8PFCHSv2L1Corrector
      + process.hltAK8PFCHSv2L2Corrector
      + process.hltAK8PFCHSv2L3Corrector
      + process.hltAK8PFCHSv2Corrector
      + process.hltAK8PFCHSv2JetsCorrected
    )
    
    process.hltAK8PFCHSv2JetsCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK8PFCHSv2JetsCorrected'
    )
    
    process.MC_AK8PFCHSv2Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PFCHSv2Jets
      + process.HLTAK8PFCHSv2JetsSequence
      + process.hltAK8PFCHSv2JetsCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PFCHSv2MET_v1
    process.hltPreMCPFCHSv2MET = process.hltPreMCPFMET.clone()
    
    process.hltParticleFlowCHSv2 = cms.EDProducer('FwdPtrRecoPFCandidateConverter',
      src = process.hltAK4PFCHSv2Jets.src,
    )
    
    process.hltPFCHSv2MET = process.hltPFMETProducer.clone(
      src = 'hltParticleFlowCHSv2',
      alias = ''
    )
    
    process.HLTPFCHSv2METSequence = cms.Sequence(
        process.HLTParticleFlowCHSv2PtrsSequence
      + process.hltParticleFlowCHSv2
      + process.hltPFCHSv2MET
    )
    
    process.hltPFCHSv2METOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPFCHSv2MET'
    )
    
    process.MC_PFCHSv2MET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPFCHSv2MET
      + process.HLTPFCHSv2METSequence
      + process.hltPFCHSv2METOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK4PuppiV1Jets_v1
    process.hltPreMCAK4PuppiV1Jets = process.hltPreMCAK4PFJets.clone()
    
    from CommonTools.PileupAlgos.Puppi_cff import puppi
    process.hltPuppiV1 = puppi.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltVerticesPF',
    #  puppiDiagnostics = True,
    )
    
    process.HLTPuppiV1Sequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltVerticesPF
    # + process.hltVerticesPFSelector
    # + process.hltVerticesPFFilter
      + process.hltPuppiV1
    )
    
    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJetsPuppi
    process.hltAK4PuppiV1Jets = ak4PFJetsPuppi.clone(
      src = 'hltPuppiV1',
      applyWeight = False,
    )
    
    process.hltAK4PuppiV1L2Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK4PFHLT'), level = cms.string('L2Relative'))
    process.hltAK4PuppiV1L3Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK4PFHLT'), level = cms.string('L3Absolute'))
    process.hltAK4PuppiV1Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK4PuppiV1L2Corrector','hltAK4PuppiV1L3Corrector'))
    process.hltAK4PuppiV1JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK4PuppiV1Jets'), correctors = cms.VInputTag('hltAK4PuppiV1Corrector'))
    
    process.HLTAK4PuppiV1JetsSequence = cms.Sequence(
        process.HLTPuppiV1Sequence
      + process.hltAK4PuppiV1Jets
      + process.hltAK4PuppiV1L2Corrector
      + process.hltAK4PuppiV1L3Corrector
      + process.hltAK4PuppiV1Corrector
      + process.hltAK4PuppiV1JetsCorrected
    )
    
    process.hltAK4PuppiV1JetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK4PuppiV1JetsCorrected'
    )
    
    process.MC_AK4PuppiV1Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PuppiV1Jets
      + process.HLTAK4PuppiV1JetsSequence
      + process.hltAK4PuppiV1JetCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK8PuppiV1Jets_v1
    process.hltPreMCAK8PuppiV1Jets = process.hltPreMCAK4PFJets.clone()
    
    from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsPuppi
    process.hltAK8PuppiV1Jets = ak8PFJetsPuppi.clone(
      src = 'hltPuppiV1',
      applyWeight = False,
    )
    
    process.hltAK8PuppiV1L2Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK8PFPuppi'), level = cms.string('L2Relative'))
    process.hltAK8PuppiV1L3Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK8PFPuppi'), level = cms.string('L3Absolute'))
    process.hltAK8PuppiV1Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK8PuppiV1L2Corrector','hltAK8PuppiV1L3Corrector'))
    process.hltAK8PuppiV1JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK8PuppiV1Jets'), correctors = cms.VInputTag('hltAK8PuppiV1Corrector'))
    
    process.HLTAK8PuppiV1JetsSequence = cms.Sequence(
        process.HLTPuppiV1Sequence
      + process.hltAK8PuppiV1Jets
      + process.hltAK8PuppiV1L2Corrector
      + process.hltAK8PuppiV1L3Corrector
      + process.hltAK8PuppiV1Corrector
      + process.hltAK8PuppiV1JetsCorrected
    )
    
    process.hltAK8PuppiV1JetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK8PuppiV1JetsCorrected'
    )
    
    process.MC_AK8PuppiV1Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PuppiV1Jets
      + process.HLTAK8PuppiV1JetsSequence
      + process.hltAK8PuppiV1JetCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV1MET_v1
    process.hltPreMCPuppiV1MET = process.hltPreMCPFMET.clone()
    
    process.hltPuppiV1MET = process.hltPFMETProducer.clone(
      src = 'hltPuppiV1',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV1METSequence = cms.Sequence(
        process.HLTPuppiV1Sequence
      + process.hltPuppiV1MET
    )
    
    process.hltPuppiV1METOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV1MET'
    )
    
    process.MC_PuppiV1MET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV1MET
      + process.HLTPuppiV1METSequence
      + process.hltPuppiV1METOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV1METNoMu_v1
    process.hltPreMCPuppiV1METNoMu = process.hltPreMCPFMET.clone()
    
    process.hltPuppiV1NoMu = process.hltParticleFlowNoMu.clone(src = 'hltPuppiV1')
    
    process.hltPuppiV1METNoMu = process.hltPFMETProducer.clone(
      src = 'hltPuppiV1NoMu',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV1METNoMuSequence = cms.Sequence(
        process.HLTPuppiV1Sequence
      + process.hltPuppiV1NoMu
      + process.hltPuppiV1METNoMu
    )
    
    process.hltPuppiV1METNoMuOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV1METNoMu'
    )
    
    process.MC_PuppiV1METNoMu_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV1METNoMu
      + process.HLTPuppiV1METNoMuSequence
      + process.hltPuppiV1METNoMuOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV2MET_v1
    process.hltPreMCPuppiV2MET = process.hltPreMCPFMET.clone()
    
    # Puppi candidates for MET
    process.hltParticleFlowNoLeptons = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag( 'hltParticleFlow' ),
      pdgId = cms.vint32( 1, 2, 22, 111, 130, 310, 2112, 211, -211, 321, -321, 999211, 2212, -2212 )
    )
    process.hltParticleFlowLeptons = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag( 'hltParticleFlow' ),
      pdgId = cms.vint32( -11, 11, -13, 13 ),
    )
    process.hltPuppiV2NoLeptons = puppi.clone(
      candName = 'hltParticleFlowNoLeptons',
      vertexName = 'hltVerticesPF',
      PtMaxPhotons = 20.,
    )
    process.hltPuppiV2 = cms.EDProducer('CandViewMerger',
      src = cms.VInputTag( 'hltPuppiV2NoLeptons', 'hltParticleFlowLeptons' ),
    )
    process.hltPuppiV2MET = process.hltPFMETProducer.clone(
      src = 'hltPuppiV2',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV2METSequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltVerticesPF
    #  + process.hltVerticesPFSelector
    #  + process.hltVerticesPFFilter
      + process.hltParticleFlowNoLeptons
      + process.hltParticleFlowLeptons
      + process.hltPuppiV2NoLeptons
      + process.hltPuppiV2
      + process.hltPuppiV2MET
    )
    
    process.hltPuppiV2METOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV2MET'
    )
    
    process.MC_PuppiV2MET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV2MET
      + process.HLTPuppiV2METSequence
      + process.hltPuppiV2METOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV2METNoMu_v1
    process.hltPreMCPuppiV2METNoMu = process.hltPreMCPFMET.clone()
    
    process.hltParticleFlowElectrons = cms.EDFilter('PdgIdCandViewSelector',
      src = cms.InputTag( 'hltParticleFlow' ),
      pdgId = cms.vint32( -11, 11 ),
    )
    process.hltPuppiV2NoMu = process.hltPuppiV2.clone(
      src = ['hltPuppiV2NoLeptons', 'hltParticleFlowElectrons'],
    )
    process.hltPuppiV2METNoMu = process.hltPFMETProducer.clone(
      src = 'hltPuppiV2NoMu',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV2METNoMuSequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltVerticesPF
    #  + process.hltVerticesPFSelector
    #  + process.hltVerticesPFFilter
      + process.hltParticleFlowNoLeptons
      + process.hltParticleFlowElectrons
      + process.hltPuppiV2NoLeptons
      + process.hltPuppiV2NoMu
      + process.hltPuppiV2METNoMu
    )
    
    process.hltPuppiV2METNoMuOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV2METNoMu'
    )
    
    process.MC_PuppiV2METNoMu_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV2METNoMu
      + process.HLTPuppiV2METNoMuSequence
      + process.hltPuppiV2METNoMuOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK4PuppiV3Jets_v1
    process.hltPreMCAK4PuppiV3Jets = process.hltPreMCAK4PFJets.clone()
    
    process.hltPuppiV3 = puppi.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltPixelVertices',
      UseFromPVLooseTight = True,
      vtxNdofCut = 0,
    #  puppiDiagnostics = True,
    )
    
    process.HLTPuppiV3Sequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltPuppiV3
    )
    
    process.hltAK4PuppiV3Jets = ak4PFJetsPuppi.clone(
      src = 'hltPuppiV3',
      applyWeight = False,
    )
    
    process.hltAK4PuppiV3L2Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK4PFHLT'), level = cms.string('L2Relative'))
    process.hltAK4PuppiV3L3Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK4PFHLT'), level = cms.string('L3Absolute'))
    process.hltAK4PuppiV3Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK4PuppiV3L2Corrector','hltAK4PuppiV3L3Corrector'))
    process.hltAK4PuppiV3JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK4PuppiV3Jets'), correctors = cms.VInputTag('hltAK4PuppiV3Corrector'))
    
    process.HLTAK4PuppiV3JetsSequence = cms.Sequence(
        process.HLTPuppiV3Sequence
      + process.hltAK4PuppiV3Jets
      + process.hltAK4PuppiV3L2Corrector
      + process.hltAK4PuppiV3L3Corrector
      + process.hltAK4PuppiV3Corrector
      + process.hltAK4PuppiV3JetsCorrected
    )
    
    process.hltAK4PuppiV3JetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK4PuppiV3JetsCorrected'
    )
    
    process.MC_AK4PuppiV3Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK4PuppiV3Jets
      + process.HLTAK4PuppiV3JetsSequence
      + process.hltAK4PuppiV3JetCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_AK8PuppiV3Jets_v1
    process.hltPreMCAK8PuppiV3Jets = process.hltPreMCAK4PFJets.clone()
    
    process.hltAK8PuppiV3Jets = ak8PFJetsPuppi.clone(
      src = 'hltPuppiV3',
      applyWeight = False,
    )
    
    process.hltAK8PuppiV3L2Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK8PFPuppi'), level = cms.string('L2Relative'))
    process.hltAK8PuppiV3L3Corrector = cms.EDProducer('LXXXCorrectorProducer', algorithm = cms.string('AK8PFPuppi'), level = cms.string('L3Absolute'))
    process.hltAK8PuppiV3Corrector = cms.EDProducer('ChainedJetCorrectorProducer', correctors = cms.VInputTag('hltAK8PuppiV3L2Corrector','hltAK8PuppiV3L3Corrector'))
    process.hltAK8PuppiV3JetsCorrected = cms.EDProducer('CorrectedPFJetProducer', src = cms.InputTag('hltAK8PuppiV3Jets'), correctors = cms.VInputTag('hltAK8PuppiV3Corrector'))
    
    process.HLTAK8PuppiV3JetsSequence = cms.Sequence(
        process.HLTPuppiV3Sequence
      + process.hltAK8PuppiV3Jets
      + process.hltAK8PuppiV3L2Corrector
      + process.hltAK8PuppiV3L3Corrector
      + process.hltAK8PuppiV3Corrector
      + process.hltAK8PuppiV3JetsCorrected
    )
    
    process.hltAK8PuppiV3JetCollection20Filter = process.hltAK4PFJetCollection20Filter.clone(
      inputTag = 'hltAK8PuppiV3JetsCorrected'
    )
    
    process.MC_AK8PuppiV3Jets_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCAK8PuppiV3Jets
      + process.HLTAK8PuppiV3JetsSequence
      + process.hltAK8PuppiV3JetCollection20Filter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV3MET_v1
    process.hltPreMCPuppiV3MET = process.hltPreMCPFMET.clone()
    
    process.hltPuppiV3MET = process.hltPFMETProducer.clone(
      src = 'hltPuppiV3',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV3METSequence = cms.Sequence(
        process.HLTPuppiV3Sequence
      + process.hltPuppiV3MET
    )
    
    process.hltPuppiV3METOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV3MET'
    )
    
    process.MC_PuppiV3MET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV3MET
      + process.HLTPuppiV3METSequence
      + process.hltPuppiV3METOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV3METNoMu_v1
    process.hltPreMCPuppiV3METNoMu = process.hltPreMCPFMET.clone()
    
    process.hltPuppiV3NoMu = process.hltParticleFlowNoMu.clone(src = 'hltPuppiV3')
    
    process.hltPuppiV3METNoMu = process.hltPFMETProducer.clone(
      src = 'hltPuppiV3NoMu',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV3METNoMuSequence = cms.Sequence(
        process.HLTPuppiV3Sequence
      + process.hltPuppiV3NoMu
      + process.hltPuppiV3METNoMu
    )
    
    process.hltPuppiV3METNoMuOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV3METNoMu'
    )
    
    process.MC_PuppiV3METNoMu_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV3METNoMu
      + process.HLTPuppiV3METNoMuSequence
      + process.hltPuppiV3METNoMuOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV4MET_v1
    process.hltPreMCPuppiV4MET = process.hltPreMCPFMET.clone()
    
    # Puppi candidates for MET
    process.hltPuppiV4NoLeptons = puppi.clone(
      candName = 'hltParticleFlowNoLeptons',
      vertexName = 'hltPixelVertices',
      UseFromPVLooseTight = True,
      vtxNdofCut = 0,
      PtMaxPhotons = 20.,
    )

    process.hltPuppiV4 = cms.EDProducer('CandViewMerger',
      src = cms.VInputTag( 'hltPuppiV4NoLeptons', 'hltParticleFlowLeptons' ),
    )

    process.hltPuppiV4MET = process.hltPFMETProducer.clone(
      src = 'hltPuppiV4',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV4METSequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltParticleFlowNoLeptons
      + process.hltParticleFlowLeptons
      + process.hltPuppiV4NoLeptons
      + process.hltPuppiV4
      + process.hltPuppiV4MET
    )
    
    process.hltPuppiV4METOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV4MET'
    )
    
    process.MC_PuppiV4MET_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV4MET
      + process.HLTPuppiV4METSequence
      + process.hltPuppiV4METOpenFilter
      + process.HLTEndSequence
    )
    
    ## add path: MC_PuppiV4METNoMu_v1
    process.hltPreMCPuppiV4METNoMu = process.hltPreMCPFMET.clone()
    
    process.hltPuppiV4NoMu = process.hltPuppiV4.clone(
      src = ['hltPuppiV4NoLeptons', 'hltParticleFlowElectrons'],
    )
    process.hltPuppiV4METNoMu = process.hltPFMETProducer.clone(
      src = 'hltPuppiV4NoMu',
      applyWeight = False,
      alias = ''
    )
    
    process.HLTPuppiV4METNoMuSequence = cms.Sequence(
        process.HLTParticleFlowJMESequence
      + process.hltParticleFlowNoLeptons
      + process.hltParticleFlowElectrons
      + process.hltPuppiV4NoLeptons
      + process.hltPuppiV4NoMu
      + process.hltPuppiV4METNoMu
    )
    
    process.hltPuppiV4METNoMuOpenFilter = process.hltPFMETOpenFilter.clone(
      inputTag = 'hltPuppiV4METNoMu'
    )
    
    process.MC_PuppiV4METNoMu_v1 = cms.Path(
        process.HLTBeginSequence
      + process.hltPreMCPuppiV4METNoMu
      + process.HLTPuppiV4METNoMuSequence
      + process.hltPuppiV4METNoMuOpenFilter
      + process.HLTEndSequence
    )

    return cms, process
