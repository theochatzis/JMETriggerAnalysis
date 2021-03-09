import FWCore.ParameterSet.Config as cms

def customise_hltPhase2_TRKv00(process):

    process.PixelCPEGenericESProducer = cms.ESProducer("PixelCPEGenericESProducer",
        Alpha2Order = cms.bool(True),
        ClusterProbComputationFlag = cms.int32(0),
        ComponentName = cms.string('PixelCPEGeneric'),
        DoCosmics = cms.bool(False),
        DoLorentz = cms.bool(False),
        EdgeClusterErrorX = cms.double(50.0),
        EdgeClusterErrorY = cms.double(85.0),
        IrradiationBiasCorrection = cms.bool(False),
        LoadTemplatesFromDB = cms.bool(False),
        MagneticFieldRecord = cms.ESInputTag("",""),
        SmallPitch = cms.bool(False),
        TruncatePixelCharge = cms.bool(False),
        Upgrade = cms.bool(True),
        UseErrorsFromTemplates = cms.bool(False),
        appendToDataLabel = cms.string(''),
        eff_charge_cut_highX = cms.double(1.0),
        eff_charge_cut_highY = cms.double(1.0),
        eff_charge_cut_lowX = cms.double(0.0),
        eff_charge_cut_lowY = cms.double(0.0),
        inflate_all_errors_no_trk_angle = cms.bool(False),
        inflate_errors = cms.bool(False),
        lAOffset = cms.double(0),
        lAWidthBPix = cms.double(0),
        lAWidthFPix = cms.double(0),
        size_cutX = cms.double(3.0),
        size_cutY = cms.double(3.0),
        useLAAlignmentOffsets = cms.bool(False),
        useLAWidthFromDB = cms.bool(True)
    )

    process.MeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
        ComponentName = cms.string(''),
        DebugPixelModuleQualityDB = cms.untracked.bool(False),
        DebugPixelROCQualityDB = cms.untracked.bool(False),
        DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
        DebugStripModuleQualityDB = cms.untracked.bool(False),
        DebugStripStripQualityDB = cms.untracked.bool(False),
        HitMatcher = cms.string('StandardMatcher'),
        MaskBadAPVFibers = cms.bool(True),
        Phase2StripCPE = cms.string('Phase2StripCPE'),
        PixelCPE = cms.string('PixelCPEGeneric'),
        SiStripQualityLabel = cms.string(''),
        StripCPE = cms.string('StripCPEfromTrackAngle'),
        UsePixelModuleQualityDB = cms.bool(True),
        UsePixelROCQualityDB = cms.bool(True),
        UseStripAPVFiberQualityDB = cms.bool(True),
        UseStripModuleQualityDB = cms.bool(True),
        UseStripStripQualityDB = cms.bool(True),
        badStripCuts = cms.PSet(
            TEC = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            ),
            TIB = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            ),
            TID = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            ),
            TOB = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            )
        )
    )

    process.siPixelClustersPreSplitting = cms.EDProducer("SiPixelClusterProducer",
        ChannelThreshold = cms.int32(1000),
        ClusterThreshold = cms.int32(4000),
        ClusterThreshold_L1 = cms.int32(4000),
        ElectronPerADCGain = cms.double(600.0),
        MissCalibrate = cms.bool(False),
        Phase2Calibration = cms.bool(True),
        Phase2DigiBaseline = cms.double(1200.0),
        Phase2KinkADC = cms.int32(8),
        Phase2ReadoutMode = cms.int32(-1),
        SeedThreshold = cms.int32(1000),
        SplitClusters = cms.bool(False),
        VCaltoElectronGain = cms.int32(65),
        VCaltoElectronGain_L1 = cms.int32(65),
        VCaltoElectronOffset = cms.int32(-414),
        VCaltoElectronOffset_L1 = cms.int32(-414),
        maxNumberOfClusters = cms.int32(-1),
        payloadType = cms.string('Offline'),
        src = cms.InputTag("simSiPixelDigis","Pixel")
    )

    process.siPixelClusters = cms.EDProducer("SiPixelClusterProducer",
        ChannelThreshold = cms.int32(1000),
        ClusterThreshold = cms.int32(4000),
        ClusterThreshold_L1 = cms.int32(4000),
        ElectronPerADCGain = cms.double(600.0),
        MissCalibrate = cms.bool(False),
        Phase2Calibration = cms.bool(True),
        Phase2DigiBaseline = cms.double(1200.0),
        Phase2KinkADC = cms.int32(8),
        Phase2ReadoutMode = cms.int32(-1),
        SeedThreshold = cms.int32(1000),
        SplitClusters = cms.bool(False),
        VCaltoElectronGain = cms.int32(65),
        VCaltoElectronGain_L1 = cms.int32(65),
        VCaltoElectronOffset = cms.int32(-414),
        VCaltoElectronOffset_L1 = cms.int32(-414),
        maxNumberOfClusters = cms.int32(-1),
        payloadType = cms.string('Offline'),
        src = cms.InputTag("simSiPixelDigis","Pixel")
    )

    process.trackerClusterCheck = cms.EDProducer("ClusterCheckerEDProducer",
        ClusterCollectionLabel = cms.InputTag("siStripClusters"),
        MaxNumberOfCosmicClusters = cms.uint32(400000),
        MaxNumberOfPixelClusters = cms.uint32(40000),
        PixelClusterCollectionLabel = cms.InputTag("siPixelClusters"),
        cut = cms.string('strip < 400000 && pixel < 40000 && (strip < 50000 + 10*pixel) && (pixel < 5000 + 0.1*strip)'),
        doClusterCheck = cms.bool(False),
        silentClusterCheck = cms.untracked.bool(False)
    )

    process.siPixelClusterShapeCache = cms.EDProducer("SiPixelClusterShapeCacheProducer",
        onDemand = cms.bool(False),
        src = cms.InputTag("siPixelClusters")
    )

    process.lowPtTripletStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.02),
            precise = cms.bool(True),
            ptMin = cms.double(0.4),
            useMultipleScattering = cms.bool(False)
        )
    )

    process.lowPtQuadStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.025),
            precise = cms.bool(True),
            ptMin = cms.double(0.35),
            useMultipleScattering = cms.bool(False)
        )
    )

    process.initialStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.03),
            precise = cms.bool(True),
            ptMin = cms.double(0.6),
            useMultipleScattering = cms.bool(False)
        )
    )

    process.initialStepSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3+BPix4',
            'BPix1+BPix2+BPix3+FPix1_pos',
            'BPix1+BPix2+BPix3+FPix1_neg',
            'BPix1+BPix2+FPix1_pos+FPix2_pos',
            'BPix1+BPix2+FPix1_neg+FPix2_neg',
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos',
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg',
            'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg',
            'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos',
            'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg'
        )
    )

    process.initialStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("initialStepSeedLayers"),
        trackingRegions = cms.InputTag("initialStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.initialStepHitQuadruplets = cms.EDProducer("CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double(0),
        CAPhiCut = cms.double(0.175),
        CAThetaCut = cms.double(0.001),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("initialStepHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        fitFastCircle = cms.bool(True),
        fitFastCircleChi2Cut = cms.bool(True),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.7),
            pt2 = cms.double(2),
            value1 = cms.double(200),
            value2 = cms.double(50)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_initialStepHitDoublets__HLTX'),
        useBendingCorrection = cms.bool(True)
    )

    process.initialStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ClusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            ClusterShapeHitFilterName = cms.string('ClusterShapeHitFilter'),
            ComponentName = cms.string('PixelClusterShapeSeedComparitor'),
            FilterAtHelixStage = cms.bool(False),
            FilterPixelHits = cms.bool(True),
            FilterStripHits = cms.bool(False)
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_initialStepHitQuadruplets__HLTX'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("initialStepHitQuadruplets")
    )

    process.highPtTripletStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.02),
            precise = cms.bool(True),
            ptMin = cms.double(0.7),
            useMultipleScattering = cms.bool(False)
        )
    )

    process.detachedQuadStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(5.0),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.9),
            precise = cms.bool(True),
            ptMin = cms.double(0.45),
            useMultipleScattering = cms.bool(False)
        )
    )

    process.MeasurementTrackerEvent = cms.EDProducer("MeasurementTrackerEventProducer",
        Phase2TrackerCluster1DProducer = cms.string('siPhase2Clusters'),
        badPixelFEDChannelCollectionLabels = cms.VInputTag("siPixelDigis"),
        inactivePixelDetectorLabels = cms.VInputTag(),
        inactiveStripDetectorLabels = cms.VInputTag("siStripDigis"),
        measurementTracker = cms.string(''),
        pixelCablingMapLabel = cms.string(''),
        pixelClusterProducer = cms.string('siPixelClusters'),
        skipClusters = cms.InputTag(""),
        stripClusterProducer = cms.string(''),
        switchOffPixelsIfEmpty = cms.bool(True)
    )

    process.initialStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('initialStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("initialStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.pixelPairStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionWithVerticesEDProducer",
        RegionPSet = cms.PSet(
            VertexCollection = cms.InputTag("firstStepPrimaryVertices"),
            beamSpot = cms.InputTag("offlineBeamSpot"),
            fixedError = cms.double(0.03),
            halfLengthScaling4BigEvts = cms.bool(False),
            maxNVertices = cms.int32(5),
            maxPtMin = cms.double(1000),
            minHalfLength = cms.double(0),
            minOriginR = cms.double(0),
            nSigmaZ = cms.double(4),
            originRScaling4BigEvts = cms.bool(False),
            originRadius = cms.double(0.015),
            pixelClustersForScaling = cms.InputTag("siPixelClusters"),
            precise = cms.bool(True),
            ptMin = cms.double(0.6),
            ptMinScaling4BigEvts = cms.bool(False),
            scalingEndNPix = cms.double(1),
            scalingStartNPix = cms.double(0),
            sigmaZVertex = cms.double(3),
            useFakeVertices = cms.bool(False),
            useFixedError = cms.bool(True),
            useFoundVertices = cms.bool(True),
            useMultipleScattering = cms.bool(False)
        )
    )

    process.initialStepSelector = cms.EDProducer("MultiTrackSelector",
        beamspot = cms.InputTag("offlineBeamSpot"),
        src = cms.InputTag("initialStepTracks"),
        trackSelectors = cms.VPSet(
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(2.0),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.8, 4.0),
                d0_par2 = cms.vdouble(0.6, 4.0),
                dz_par1 = cms.vdouble(0.9, 4.0),
                dz_par2 = cms.vdouble(0.8, 4.0),
                keepAllTracks = cms.bool(False),
                maxNumberLostLayers = cms.uint32(3),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('initialStepLoose'),
                preFilterName = cms.string(''),
                qualityBit = cms.string('loose'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.4),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.7, 4.0),
                d0_par2 = cms.vdouble(0.5, 4.0),
                dz_par1 = cms.vdouble(0.8, 4.0),
                dz_par2 = cms.vdouble(0.7, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('initialStepTight'),
                preFilterName = cms.string('initialStepLoose'),
                qualityBit = cms.string('tight'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.2),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.6, 4.0),
                d0_par2 = cms.vdouble(0.45, 4.0),
                dz_par1 = cms.vdouble(0.7, 4.0),
                dz_par2 = cms.vdouble(0.55, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('initialStep'),
                preFilterName = cms.string('initialStepTight'),
                qualityBit = cms.string('highPurity'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            )
        ),
        useVertices = cms.bool(True),
        useVtxError = cms.bool(False),
        vertices = cms.InputTag("firstStepPrimaryVertices")
    )

    process.trackVertexArbitrator = cms.EDProducer("TrackVertexArbitrator",
        beamSpot = cms.InputTag("offlineBeamSpot"),
        dLenFraction = cms.double(0.333),
        dRCut = cms.double(0.4),
        distCut = cms.double(0.04),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3),
        fitterTini = cms.double(256),
        maxTimeSignificance = cms.double(3.5),
        primaryVertices = cms.InputTag("offlinePrimaryVertices"),
        secondaryVertices = cms.InputTag("vertexMerger"),
        sigCut = cms.double(5),
        trackMinLayers = cms.int32(4),
        trackMinPixels = cms.int32(1),
        trackMinPt = cms.double(0.4),
        tracks = cms.InputTag("generalTracks")
    )

    process.inclusiveVertexFinder = cms.EDProducer("InclusiveVertexFinder",
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterizer = cms.PSet(
            clusterMaxDistance = cms.double(0.05),
            clusterMaxSignificance = cms.double(4.5),
            clusterMinAngleCosine = cms.double(0.5),
            distanceRatio = cms.double(20),
            maxTimeSignificance = cms.double(3.5),
            seedMax3DIPSignificance = cms.double(9999),
            seedMax3DIPValue = cms.double(9999),
            seedMin3DIPSignificance = cms.double(1.2),
            seedMin3DIPValue = cms.double(0.005)
        ),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3),
        fitterTini = cms.double(256),
        maxNTracks = cms.uint32(30),
        maximumLongitudinalImpactParameter = cms.double(0.3),
        maximumTimeSignificance = cms.double(3),
        minHits = cms.uint32(8),
        minPt = cms.double(0.8),
        primaryVertices = cms.InputTag("offlinePrimaryVertices"),
        tracks = cms.InputTag("generalTracks"),
        useDirectVertexFitter = cms.bool(True),
        useVertexReco = cms.bool(True),
        vertexMinAngleCosine = cms.double(0.95),
        vertexMinDLen2DSig = cms.double(2.5),
        vertexMinDLenSig = cms.double(0.5),
        vertexReco = cms.PSet(
            finder = cms.string('avr'),
            primcut = cms.double(1),
            seccut = cms.double(3),
            smoothing = cms.bool(True)
        )
    )

    process.muonSeededTracksOutIn = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('muonSeededStepOutIn'),
        Fitter = cms.string('muonSeededFittingSmootherWithOutliersRejectionAndRK'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("muonSeededTrackCandidatesOutIn"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.muonSeededTracksInOut = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('muonSeededStepInOut'),
        Fitter = cms.string('muonSeededFittingSmootherWithOutliersRejectionAndRK'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("muonSeededTrackCandidatesInOut"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.muonSeededSeedsInOut = cms.EDProducer("MuonReSeeder",
        DoPredictionsOnly = cms.bool(False),
        Fitter = cms.string('KFFitterForRefitInsideOut'),
        MTDRecHitBuilder = cms.string('MTDRecHitBuilder'),
        MuonRecHitBuilder = cms.string('MuonRecHitBuilder'),
        Propagator = cms.string('SmartPropagatorAnyRKOpposite'),
        RefitDirection = cms.string('alongMomentum'),
        RefitRPCHits = cms.bool(True),
        Smoother = cms.string('KFSmootherForRefitInsideOut'),
        TrackerRecHitBuilder = cms.string('WithTrackAngle'),
        cut = cms.string('pt > 2'),
        debug = cms.untracked.bool(False),
        insideOut = cms.bool(True),
        layersToKeep = cms.int32(5),
        src = cms.InputTag("earlyMuons")
    )

    process.generalTracks = cms.EDProducer("DuplicateListMerger",
        candidateComponents = cms.InputTag("duplicateTrackCandidates","candidateMap"),
        candidateSource = cms.InputTag("duplicateTrackCandidates","candidates"),
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        diffHitsCut = cms.int32(5),
        mergedMVAVals = cms.InputTag("duplicateTrackClassifier","MVAValues"),
        mergedSource = cms.InputTag("mergedDuplicateTracks"),
        originalMVAVals = cms.InputTag("preDuplicateMergingGeneralTracks","MVAValues"),
        originalSource = cms.InputTag("preDuplicateMergingGeneralTracks"),
        trackAlgoPriorityOrder = cms.string('trackAlgoPriorityOrder')
    )

    process.duplicateTrackClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("offlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 0.003),
                d0err_par = cms.vdouble(0.001, 0.001, 0.001),
                drWPVerr_par = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
                dr_exp = cms.vint32(2147483647, 2147483647, 2147483647),
                dr_par1 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
                dr_par2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38)
            ),
            dz_par = cms.PSet(
                dzWPVerr_par = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
                dz_exp = cms.vint32(2147483647, 2147483647, 2147483647),
                dz_par1 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
                dz_par2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38)
            ),
            isHLT = cms.bool(False),
            maxChi2 = cms.vdouble(9999.0, 9999.0, 9999.0),
            maxChi2n = cms.vdouble(10.0, 1.0, 0.4),
            maxDr = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
            maxDz = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24, 15),
            maxLostLayers = cms.vint32(99, 99, 99),
            maxRelPtErr = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
            min3DLayers = cms.vint32(0, 0, 0),
            minHits = cms.vint32(0, 0, 1),
            minHits4pass = cms.vint32(2147483647, 2147483647, 2147483647),
            minLayers = cms.vint32(0, 0, 0),
            minNVtxTrk = cms.int32(2),
            minNdof = cms.vdouble(-1, -1, -1),
            minPixelHits = cms.vint32(0, 0, 0)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("mergedDuplicateTracks"),
        vertices = cms.InputTag("firstStepPrimaryVertices")
    )

    process.mergedDuplicateTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('undefAlgorithm'),
        Fitter = cms.string('RKFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("duplicateTrackCandidates","candidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.duplicateTrackCandidates = cms.EDProducer("DuplicateTrackMerger",
        GBRForestFileName = cms.string(''),
        chi2EstimatorName = cms.string('duplicateTrackCandidatesChi2Est'),
        forestLabel = cms.string('MVADuplicate'),
        maxDCA = cms.double(30),
        maxDLambda = cms.double(0.3),
        maxDPhi = cms.double(0.3),
        maxDQoP = cms.double(0.25),
        maxDdsz = cms.double(10),
        maxDdxy = cms.double(10),
        minBDTG = cms.double(-0.1),
        minDeltaR3d = cms.double(-4),
        minP = cms.double(0.4),
        minpT = cms.double(0.2),
        overlapCheckMaxHits = cms.uint32(4),
        overlapCheckMaxMissingLayers = cms.uint32(1),
        overlapCheckMinCosT = cms.double(0.99),
        propagatorName = cms.string('PropagatorWithMaterial'),
        source = cms.InputTag("preDuplicateMergingGeneralTracks"),
        ttrhBuilderName = cms.string('WithTrackAngle'),
        useInnermostState = cms.bool(True)
    )

    process.pixelPairStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('pixelPairStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("pixelPairStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.pixelPairStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ClusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            ClusterShapeHitFilterName = cms.string('ClusterShapeHitFilter'),
            ComponentName = cms.string('PixelClusterShapeSeedComparitor'),
            FilterAtHelixStage = cms.bool(True),
            FilterPixelHits = cms.bool(True),
            FilterStripHits = cms.bool(False)
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_pixelPairStepHitDoublets__HLTX'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("pixelPairStepHitDoublets")
    )

    process.pixelPairStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0),
        maxElement = cms.uint32(0),
        maxElementTotal = cms.uint32(12000000),
        produceIntermediateHitDoublets = cms.bool(False),
        produceSeedingHitSets = cms.bool(True),
        seedingLayers = cms.InputTag("pixelPairStepSeedLayers"),
        trackingRegions = cms.InputTag("pixelPairStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.pixelPairStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag("detachedQuadStepClusters"),
        overrideTrkQuals = cms.InputTag("detachedQuadStep"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("detachedQuadStepTracks")
    )

    process.detachedQuadStepSelector = cms.EDProducer("MultiTrackSelector",
        beamspot = cms.InputTag("offlineBeamSpot"),
        src = cms.InputTag("detachedQuadStepTracks"),
        trackSelectors = cms.VPSet(
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.0),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.9, 3.0),
                d0_par2 = cms.vdouble(1.0, 3.0),
                dz_par1 = cms.vdouble(0.9, 3.0),
                dz_par2 = cms.vdouble(1.0, 3.0),
                keepAllTracks = cms.bool(False),
                maxNumberLostLayers = cms.uint32(999),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(0),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('detachedQuadStepVtxLoose'),
                preFilterName = cms.string(''),
                qualityBit = cms.string('loose'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.6),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(1.3, 4.0),
                d0_par2 = cms.vdouble(1.3, 4.0),
                dz_par1 = cms.vdouble(1.3, 4.0),
                dz_par2 = cms.vdouble(1.3, 4.0),
                keepAllTracks = cms.bool(False),
                maxNumberLostLayers = cms.uint32(999),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(0),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('detachedQuadStepTrkLoose'),
                preFilterName = cms.string(''),
                qualityBit = cms.string('loose'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.9),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.9, 3.0),
                d0_par2 = cms.vdouble(0.9, 3.0),
                dz_par1 = cms.vdouble(0.9, 3.0),
                dz_par2 = cms.vdouble(0.9, 3.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(1),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('detachedQuadStepVtxTight'),
                preFilterName = cms.string('detachedQuadStepVtxLoose'),
                qualityBit = cms.string('tight'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.5),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(1.1, 4.0),
                d0_par2 = cms.vdouble(1.1, 4.0),
                dz_par1 = cms.vdouble(1.1, 4.0),
                dz_par2 = cms.vdouble(1.1, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(1),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(4),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('detachedQuadStepTrkTight'),
                preFilterName = cms.string('detachedQuadStepTrkLoose'),
                qualityBit = cms.string('tight'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.9),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.8, 3.0),
                d0_par2 = cms.vdouble(0.8, 3.0),
                dz_par1 = cms.vdouble(0.8, 3.0),
                dz_par2 = cms.vdouble(0.8, 3.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(1),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('detachedQuadStepVtx'),
                preFilterName = cms.string('detachedQuadStepVtxTight'),
                qualityBit = cms.string('highPurity'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.5),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.9, 4.0),
                d0_par2 = cms.vdouble(0.9, 4.0),
                dz_par1 = cms.vdouble(0.9, 4.0),
                dz_par2 = cms.vdouble(0.9, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(1),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(4),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('detachedQuadStepTrk'),
                preFilterName = cms.string('detachedQuadStepTrkTight'),
                qualityBit = cms.string('highPurity'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            )
        ),
        useVertices = cms.bool(True),
        useVtxError = cms.bool(False),
        vertices = cms.InputTag("firstStepPrimaryVertices")
    )

    process.detachedQuadStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('detachedQuadStepXXX'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("detachedQuadStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.detachedQuadStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ClusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            ClusterShapeHitFilterName = cms.string('ClusterShapeHitFilter'),
            ComponentName = cms.string('PixelClusterShapeSeedComparitor'),
            FilterAtHelixStage = cms.bool(False),
            FilterPixelHits = cms.bool(True),
            FilterStripHits = cms.bool(False)
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_detachedQuadStepHitQuadruplets__HLTX'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("detachedQuadStepHitQuadruplets")
    )

    process.detachedQuadStepHitQuadruplets = cms.EDProducer("CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double(0),
        CAPhiCut = cms.double(0),
        CAThetaCut = cms.double(0.0011),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        doublets = cms.InputTag("detachedQuadStepHitDoublets"),
        extraHitRPhitolerance = cms.double(0),
        fitFastCircle = cms.bool(True),
        fitFastCircleChi2Cut = cms.bool(True),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(2),
            value1 = cms.double(500),
            value2 = cms.double(100)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_detachedQuadStepHitDoublets__HLTX'),
        useBendingCorrection = cms.bool(True)
    )

    process.detachedQuadStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("detachedQuadStepSeedLayers"),
        trackingRegions = cms.InputTag("detachedQuadStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.detachedQuadStepSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("detachedQuadStepClusters")
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("detachedQuadStepClusters")
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3+BPix4',
            'BPix1+BPix2+BPix3+FPix1_pos',
            'BPix1+BPix2+BPix3+FPix1_neg',
            'BPix1+BPix2+FPix1_pos+FPix2_pos',
            'BPix1+BPix2+FPix1_neg+FPix2_neg',
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos',
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg',
            'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg',
            'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos',
            'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg'
        )
    )

    process.detachedQuadStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag("lowPtTripletStepClusters"),
        overrideTrkQuals = cms.InputTag("lowPtTripletStepSelector","lowPtTripletStep"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("lowPtTripletStepTracks")
    )

    process.lowPtTripletStepSelector = cms.EDProducer("MultiTrackSelector",
        beamspot = cms.InputTag("offlineBeamSpot"),
        src = cms.InputTag("lowPtTripletStepTracks"),
        trackSelectors = cms.VPSet(
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.2),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.7, 4.0),
                d0_par2 = cms.vdouble(0.6, 4.0),
                dz_par1 = cms.vdouble(0.7, 4.0),
                dz_par2 = cms.vdouble(0.6, 4.0),
                keepAllTracks = cms.bool(False),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('lowPtTripletStepLoose'),
                preFilterName = cms.string(''),
                qualityBit = cms.string('loose'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.7),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.6, 4.0),
                d0_par2 = cms.vdouble(0.5, 4.0),
                dz_par1 = cms.vdouble(0.6, 4.0),
                dz_par2 = cms.vdouble(0.5, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('lowPtTripletStepTight'),
                preFilterName = cms.string('lowPtTripletStepLoose'),
                qualityBit = cms.string('tight'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.4),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.5, 4.0),
                d0_par2 = cms.vdouble(0.45, 4.0),
                dz_par1 = cms.vdouble(0.5, 4.0),
                dz_par2 = cms.vdouble(0.45, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(4),
                minNumberLayers = cms.uint32(4),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(3),
                nSigmaZ = cms.double(4.0),
                name = cms.string('lowPtTripletStep'),
                preFilterName = cms.string('lowPtTripletStepTight'),
                qualityBit = cms.string('highPurity'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            )
        ),
        useVertices = cms.bool(True),
        useVtxError = cms.bool(False),
        vertices = cms.InputTag("firstStepPrimaryVertices")
    )

    process.lowPtTripletStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('lowPtTripletStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("lowPtTripletStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.lowPtTripletStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_lowPtTripletStepHitTriplets__HLTX'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("lowPtTripletStepHitTriplets")
    )

    process.lowPtTripletStepHitTriplets = cms.EDProducer("CAHitTripletEDProducer",
        CAHardPtCut = cms.double(0),
        CAPhiCut = cms.double(0.05),
        CAThetaCut = cms.double(0.002),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("lowPtTripletStepHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(2),
            value1 = cms.double(70),
            value2 = cms.double(8)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_lowPtTripletStepHitDoublets__HLTX'),
        useBendingCorrection = cms.bool(True)
    )

    process.lowPtTripletStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0, 1),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("lowPtTripletStepSeedLayers"),
        trackingRegions = cms.InputTag("lowPtTripletStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.lowPtTripletStepSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("lowPtTripletStepClusters")
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("lowPtTripletStepClusters")
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3',
            'BPix2+BPix3+BPix4',
            'BPix1+BPix2+FPix1_pos',
            'BPix1+BPix2+FPix1_neg',
            'BPix1+FPix1_pos+FPix2_pos',
            'BPix1+FPix1_neg+FPix2_neg',
            'FPix1_pos+FPix2_pos+FPix3_pos',
            'FPix1_neg+FPix2_neg+FPix3_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg'
        )
    )

    process.lowPtTripletStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag("lowPtQuadStepClusters"),
        overrideTrkQuals = cms.InputTag("lowPtQuadStepSelector","lowPtQuadStep"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("lowPtQuadStepTracks")
    )

    process.lowPtQuadStepSelector = cms.EDProducer("MultiTrackSelector",
        beamspot = cms.InputTag("offlineBeamSpot"),
        src = cms.InputTag("lowPtQuadStepTracks"),
        trackSelectors = cms.VPSet(
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(2.0),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.8, 4.0),
                d0_par2 = cms.vdouble(0.6, 4.0),
                dz_par1 = cms.vdouble(0.7, 4.0),
                dz_par2 = cms.vdouble(0.6, 4.0),
                keepAllTracks = cms.bool(False),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('lowPtQuadStepLoose'),
                preFilterName = cms.string(''),
                qualityBit = cms.string('loose'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.4),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.7, 4.0),
                d0_par2 = cms.vdouble(0.5, 4.0),
                dz_par1 = cms.vdouble(0.6, 4.0),
                dz_par2 = cms.vdouble(0.5, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('lowPtQuadStepTight'),
                preFilterName = cms.string('lowPtQuadStepLoose'),
                qualityBit = cms.string('tight'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.2),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.5, 4.0),
                d0_par2 = cms.vdouble(0.45, 4.0),
                dz_par1 = cms.vdouble(0.5, 4.0),
                dz_par2 = cms.vdouble(0.45, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('lowPtQuadStep'),
                preFilterName = cms.string('lowPtQuadStepTight'),
                qualityBit = cms.string('highPurity'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            )
        ),
        useVertices = cms.bool(True),
        useVtxError = cms.bool(False),
        vertices = cms.InputTag("firstStepPrimaryVertices")
    )

    process.lowPtQuadStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('lowPtQuadStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("lowPtQuadStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.lowPtQuadStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_lowPtQuadStepHitQuadruplets__HLTX'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("lowPtQuadStepHitQuadruplets")
    )

    process.lowPtQuadStepHitQuadruplets = cms.EDProducer("CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double(0),
        CAPhiCut = cms.double(0.25),
        CAThetaCut = cms.double(0.0015),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("lowPtQuadStepHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        fitFastCircle = cms.bool(True),
        fitFastCircleChi2Cut = cms.bool(True),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.7),
            pt2 = cms.double(2),
            value1 = cms.double(1000),
            value2 = cms.double(150)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_lowPtQuadStepHitDoublets__HLTX'),
        useBendingCorrection = cms.bool(True)
    )

    process.lowPtQuadStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("lowPtQuadStepSeedLayers"),
        trackingRegions = cms.InputTag("lowPtQuadStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.lowPtQuadStepSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("lowPtQuadStepClusters")
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("lowPtQuadStepClusters")
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3+BPix4',
            'BPix1+BPix2+BPix3+FPix1_pos',
            'BPix1+BPix2+BPix3+FPix1_neg',
            'BPix1+BPix2+FPix1_pos+FPix2_pos',
            'BPix1+BPix2+FPix1_neg+FPix2_neg',
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos',
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg',
            'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg',
            'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos',
            'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg'
        )
    )

    process.lowPtQuadStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag("highPtTripletStepClusters"),
        overrideTrkQuals = cms.InputTag("highPtTripletStepSelector","highPtTripletStep"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("highPtTripletStepTracks")
    )

    process.highPtTripletStepSelector = cms.EDProducer("MultiTrackSelector",
        beamspot = cms.InputTag("offlineBeamSpot"),
        src = cms.InputTag("highPtTripletStepTracks"),
        trackSelectors = cms.VPSet(
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(2.0),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.7, 4.0),
                d0_par2 = cms.vdouble(0.6, 4.0),
                dz_par1 = cms.vdouble(0.8, 4.0),
                dz_par2 = cms.vdouble(0.6, 4.0),
                keepAllTracks = cms.bool(False),
                maxNumberLostLayers = cms.uint32(3),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('highPtTripletStepLoose'),
                preFilterName = cms.string(''),
                qualityBit = cms.string('loose'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(1.0),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.6, 4.0),
                d0_par2 = cms.vdouble(0.5, 4.0),
                dz_par1 = cms.vdouble(0.7, 4.0),
                dz_par2 = cms.vdouble(0.6, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(3),
                minNumberLayers = cms.uint32(3),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(0),
                nSigmaZ = cms.double(4.0),
                name = cms.string('highPtTripletStepTight'),
                preFilterName = cms.string('highPtTripletStepLoose'),
                qualityBit = cms.string('tight'),
                res_par = cms.vdouble(0.003, 0.002),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            ),
            cms.PSet(
                applyAbsCutsIfNoPV = cms.bool(False),
                applyAdaptedPVCuts = cms.bool(True),
                chi2n_no1Dmod_par = cms.double(9999),
                chi2n_par = cms.double(0.8),
                copyExtras = cms.untracked.bool(True),
                copyTrajectories = cms.untracked.bool(False),
                d0_par1 = cms.vdouble(0.6, 4.0),
                d0_par2 = cms.vdouble(0.45, 4.0),
                dz_par1 = cms.vdouble(0.7, 4.0),
                dz_par2 = cms.vdouble(0.55, 4.0),
                keepAllTracks = cms.bool(True),
                maxNumberLostLayers = cms.uint32(2),
                max_d0 = cms.double(100.0),
                max_eta = cms.double(9999.0),
                max_lostHitFraction = cms.double(1.0),
                max_minMissHitOutOrIn = cms.int32(99),
                max_relpterr = cms.double(9999.0),
                max_z0 = cms.double(100.0),
                minHitsToBypassChecks = cms.uint32(20),
                minNumber3DLayers = cms.uint32(4),
                minNumberLayers = cms.uint32(4),
                min_eta = cms.double(-9999.0),
                min_nhits = cms.uint32(4),
                nSigmaZ = cms.double(4.0),
                name = cms.string('highPtTripletStep'),
                preFilterName = cms.string('highPtTripletStepTight'),
                qualityBit = cms.string('highPurity'),
                res_par = cms.vdouble(0.003, 0.001),
                vertexCut = cms.string('ndof>=2&!isFake'),
                vtxNumber = cms.int32(-1)
            )
        ),
        useVertices = cms.bool(True),
        useVtxError = cms.bool(False),
        vertices = cms.InputTag("firstStepPrimaryVertices")
    )

    process.highPtTripletStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('highPtTripletStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("highPtTripletStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.highPtTripletStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_highPtTripletStepHitTriplets__HLTX'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("highPtTripletStepHitTriplets")
    )

    process.highPtTripletStepHitTriplets = cms.EDProducer("CAHitTripletEDProducer",
        CAHardPtCut = cms.double(0.5),
        CAPhiCut = cms.double(0.06),
        CAThetaCut = cms.double(0.003),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("highPtTripletStepHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(8),
            value1 = cms.double(100),
            value2 = cms.double(6)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_highPtTripletStepHitDoublets__HLTX'),
        useBendingCorrection = cms.bool(True)
    )

    process.highPtTripletStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0, 1),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("highPtTripletStepSeedLayers"),
        trackingRegions = cms.InputTag("highPtTripletStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.highPtTripletStepSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("highPtTripletStepClusters")
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("highPtTripletStepClusters")
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3',
            'BPix2+BPix3+BPix4',
            'BPix1+BPix3+BPix4',
            'BPix1+BPix2+BPix4',
            'BPix2+BPix3+FPix1_pos',
            'BPix2+BPix3+FPix1_neg',
            'BPix1+BPix2+FPix1_pos',
            'BPix1+BPix2+FPix1_neg',
            'BPix2+FPix1_pos+FPix2_pos',
            'BPix2+FPix1_neg+FPix2_neg',
            'BPix1+FPix1_pos+FPix2_pos',
            'BPix1+FPix1_neg+FPix2_neg',
            'FPix1_pos+FPix2_pos+FPix3_pos',
            'FPix1_neg+FPix2_neg+FPix3_neg',
            'BPix1+FPix2_pos+FPix3_pos',
            'BPix1+FPix2_neg+FPix3_neg',
            'FPix2_pos+FPix3_pos+FPix4_pos',
            'FPix2_neg+FPix3_neg+FPix4_neg',
            'FPix3_pos+FPix4_pos+FPix5_pos',
            'FPix3_neg+FPix4_neg+FPix5_neg',
            'FPix4_pos+FPix5_pos+FPix6_pos',
            'FPix4_neg+FPix5_neg+FPix6_neg',
            'FPix5_pos+FPix6_pos+FPix7_pos',
            'FPix5_neg+FPix6_neg+FPix7_neg',
            'FPix6_pos+FPix7_pos+FPix8_pos',
            'FPix6_neg+FPix7_neg+FPix8_neg'
        )
    )

    process.highPtTripletStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag(""),
        overrideTrkQuals = cms.InputTag("initialStepSelector","initialStep"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("initialStepTracks")
    )

    process.caloTowerForTrk = cms.EDProducer("CaloTowersCreator",
        AllowMissingInputs = cms.bool(False),
        EBGrid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        EBSumThreshold = cms.double(0.2),
        EBThreshold = cms.double(0.07),
        EBWeight = cms.double(1.0),
        EBWeights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        EEGrid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        EESumThreshold = cms.double(0.45),
        EEThreshold = cms.double(0.3),
        EEWeight = cms.double(1.0),
        EEWeights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        EcalRecHitSeveritiesToBeExcluded = cms.vstring(
            'kTime',
            'kWeird',
            'kBad'
        ),
        EcalSeveritiesToBeUsedInBadTowers = cms.vstring(),
        EcutTower = cms.double(-1000.0),
        HBGrid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        HBThreshold = cms.double(0.3),
        HBThreshold1 = cms.double(0.1),
        HBThreshold2 = cms.double(0.2),
        HBWeight = cms.double(1.0),
        HBWeights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        HEDGrid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        HEDThreshold = cms.double(0.2),
        HEDThreshold1 = cms.double(0.1),
        HEDWeight = cms.double(1.0),
        HEDWeights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        HESGrid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        HESThreshold = cms.double(0.2),
        HESThreshold1 = cms.double(0.1),
        HESWeight = cms.double(1.0),
        HESWeights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        HF1Grid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        HF1Threshold = cms.double(0.5),
        HF1Weight = cms.double(1.0),
        HF1Weights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        HF2Grid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        HF2Threshold = cms.double(0.85),
        HF2Weight = cms.double(1.0),
        HF2Weights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        HOGrid = cms.vdouble(-1.0, 1.0, 10.0, 100.0, 1000.0),
        HOThreshold0 = cms.double(1.1),
        HOThresholdMinus1 = cms.double(3.5),
        HOThresholdMinus2 = cms.double(3.5),
        HOThresholdPlus1 = cms.double(3.5),
        HOThresholdPlus2 = cms.double(3.5),
        HOWeight = cms.double(1.0),
        HOWeights = cms.vdouble(1.0, 1.0, 1.0, 1.0, 1.0),
        HcalAcceptSeverityLevel = cms.uint32(9),
        HcalAcceptSeverityLevelForRejectedHit = cms.uint32(9999),
        HcalPhase = cms.int32(1),
        HcalThreshold = cms.double(-1000.0),
        MomConstrMethod = cms.int32(1),
        MomEBDepth = cms.double(0.3),
        MomEEDepth = cms.double(0.0),
        MomHBDepth = cms.double(0.2),
        MomHEDepth = cms.double(0.4),
        UseEcalRecoveredHits = cms.bool(False),
        UseEtEBTreshold = cms.bool(False),
        UseEtEETreshold = cms.bool(False),
        UseHO = cms.bool(True),
        UseHcalRecoveredHits = cms.bool(True),
        UseRejectedHitsOnly = cms.bool(False),
        UseRejectedRecoveredEcalHits = cms.bool(False),
        UseRejectedRecoveredHcalHits = cms.bool(True),
        UseSymEBTreshold = cms.bool(True),
        UseSymEETreshold = cms.bool(True),
        ecalInputs = cms.VInputTag(cms.InputTag("ecalRecHit","EcalRecHitsEB"), cms.InputTag("ecalRecHit","EcalRecHitsEE")),
        hbheInput = cms.InputTag("hbhereco"),
        hfInput = cms.InputTag("hfreco"),
        hoInput = cms.InputTag("horeco"),
        missingHcalRescaleFactorForEcal = cms.double(0)
    )

    process.offlineBeamSpot = cms.EDProducer("BeamSpotProducer")

    ############# ordered setup

    # process.ecalUncalibRecHitSequence = cms.Sequence(
    #     process.bunchSpacingProducer +
    #     process.ecalMultiFitUncalibRecHit +
    #     process.ecalDetIdToBeRecovered
    # )

    process.caloLocalReco = cms.Sequence(
        process.hbhereco +
        process.hfprereco + #####
        process.hfreco +
        process.horeco +
        process.ecalUncalibRecHitSequence +
        process.ecalRecHit
    )

    process.muonLocalReco = cms.Sequence(
        process.dtlocalreco +  #not in the clean config
        process.csclocalreco + #not in the clean config
        process.rpcRecHits +
        process.gemLocalReco + #not in the clean config
        process.me0LocalReco #+ #not in the clean config
        #rpcNewRecHits  #not in the clean config
    )

    process.standaloneMuonTrackingSequence = cms.Sequence(
        process.muonLocalReco +
        process.ancientMuonSeed +
        process.standAloneMuons +
        process.refittedStandAloneMuons +
        process.displacedMuonSeeds #+
        #displacedStandAloneMuons #not in the clean config
    )

    process.itLocalReco = cms.Sequence(
        process.siPhase2Clusters +
        process.siPixelClusters +
        process.siPixelClusterShapeCache +
        process.siPixelClustersPreSplitting +
        process.siPixelRecHits +
        process.siPixelRecHitsPreSplitting
    )

    process.otLocalReco = cms.Sequence(
        process.MeasurementTrackerEvent #+
        #clusterSummaryProducer     # not sure what it is :(
    )

    process.initialStepPVSequence = cms.Sequence(
        process.firstStepPrimaryVerticesUnsorted +
        process.initialStepTrackRefsForJets +
        process.caloTowerForTrk +
        process.ak4CaloJetsForTrk +
        process.firstStepPrimaryVertices
    )
    process.initialStepSequence = cms.Sequence(
        process.initialStepSeedLayers +
        process.initialStepTrackingRegions +
        process.initialStepHitDoublets +
        process.initialStepHitQuadruplets +
        process.initialStepSeeds +
        process.initialStepTrackCandidates +
        process.initialStepTracks +
        process.initialStepPVSequence +
        process.initialStepSelector
    )

    process.highPtTripletStepSequence = cms.Sequence(
        process.highPtTripletStepClusters +
        process.highPtTripletStepSeedLayers +
        process.highPtTripletStepTrackingRegions +
        process.highPtTripletStepHitDoublets +
        process.highPtTripletStepHitTriplets +
        process.highPtTripletStepSeedLayers +
        process.highPtTripletStepSeeds +
        process.highPtTripletStepTrackCandidates +
        process.highPtTripletStepTracks +
        process.highPtTripletStepSelector +
        process.initialStepSeedClusterMask + # needed by electron, but also by highPtTripletStepSeedClusterMask
        process.highPtTripletStepSeedClusterMask
    )

    process.lowPtQuadStepSequence = cms.Sequence(
        process.lowPtQuadStepClusters +
        process.lowPtQuadStepSeedLayers +
        process.lowPtQuadStepTrackingRegions +
        process.lowPtQuadStepHitDoublets +
        process.lowPtQuadStepHitQuadruplets +
        process.lowPtQuadStepSeeds +
        process.lowPtQuadStepTrackCandidates +
        process.lowPtQuadStepTracks +
        process.lowPtQuadStepSelector
    )

    process.lowPtTripletStepSequence = cms.Sequence(
        process.lowPtTripletStepClusters +
        process.lowPtTripletStepSeedLayers +
        process.lowPtTripletStepTrackingRegions +
        process.lowPtTripletStepHitDoublets +
        process.lowPtTripletStepHitTriplets +
        process.lowPtTripletStepSeeds +
        process.lowPtTripletStepTrackCandidates +
        process.lowPtTripletStepTracks +
        process.lowPtTripletStepSelector
    )
    process.detachedQuadStepSequence = cms.Sequence(
        process.detachedQuadStepClusters +
        process.detachedQuadStepSeedLayers +
        process.detachedQuadStepTrackingRegions +
        process.detachedQuadStepHitDoublets +
        process.detachedQuadStepHitQuadruplets +
        process.detachedQuadStepSeeds +
        process.detachedQuadStepTrackCandidates +
        process.detachedQuadStepTracks +
        process.detachedQuadStepSelector +
        process.detachedQuadStep
    )
    process.pixelPairStepSequence = cms.Sequence(
        process.pixelPairStepClusters +
        process.pixelPairStepSeedLayers +
        process.pixelPairStepTrackingRegions +
        process.pixelPairStepHitDoublets +
        process.pixelPairStepSeeds +
        process.pixelPairStepTrackCandidates +
        process.pixelPairStepTracks +
        process.pixelPairStepSelector
    #    pixelPairStepSeedClusterMask # used only by electron !
    )
    process.muonSeededTracksOutInSequence = cms.Sequence(
        process.muonSeededSeedsOutIn +
        process.muonSeededTrackCandidatesOutIn +
        process.muonSeededTracksOutIn +
        process.muonSeededTracksOutInSelector
    )
    process.muonSeededTracksInOutSequence = cms.Sequence(
        process.muonSeededSeedsInOut +
        process.muonSeededTrackCandidatesInOut +
        process.muonSeededTracksInOut +
        process.muonSeededTracksInOutSelector
    )

    process.muonSeededStepSequence = cms.Sequence(
        #muonLocalReco +#cmssw_10_6
        process.standaloneMuonTrackingSequence + #cmssw_10_6
        process.earlyMuons +
        process.muonSeededTracksOutInSequence +
        process.muonSeededTracksInOutSequence
    )
    # process.vertexReco = cms.Sequence(
    #     process.ak4CaloJetsForTrk +
    #     process.unsortedOfflinePrimaryVertices +
    #     process.trackWithVertexRefSelectorBeforeSorting +
    #     process.trackRefsForJetsBeforeSorting +
    #     process.offlinePrimaryVertices +
    #     process.offlinePrimaryVerticesWithBS +
    #     process.inclusiveVertexFinder +
    #     process.vertexMerger +
    #     process.trackVertexArbitrator +
    #     process.inclusiveSecondaryVertices
    # )

    process.vertexReco = cms.Sequence(
        process.unsortedOfflinePrimaryVertices4DnoPID
      + process.unsortedOfflinePrimaryVertices
      + process.trackWithVertexRefSelectorBeforeSorting4DnoPID
      + process.trackWithVertexRefSelectorBeforeSorting
      + process.trackRefsForJetsBeforeSorting4DnoPID
      + process.trackRefsForJetsBeforeSorting
      + process.tpClusterProducer
      + process.tofPID4DnoPID
      + process.unsortedOfflinePrimaryVertices4D
      + process.trackWithVertexRefSelectorBeforeSorting4D
      + process.trackRefsForJetsBeforeSorting4D
      + process.tofPID
      + process.quickTrackAssociatorByHits
      + process.trackTimeValueMapProducer
      + process.caloTowerForTrk
      + process.ak4CaloJetsForTrk
#      + process.offlinePrimaryVertices4DnoPIDWithBS
#      + process.offlinePrimaryVertices4DWithBS
#      + process.offlinePrimaryVertices4D
      + process.offlinePrimaryVerticesWithBS
      + process.offlinePrimaryVertices
#      + process.generalV0Candidates
      + process.inclusiveVertexFinder
      + process.vertexMerger
      + process.trackVertexArbitrator
      + process.inclusiveSecondaryVertices
#      + process.offlinePrimaryVertices4DnoPID
    )

    process.globalreco_tracking = cms.Sequence(
        process.itLocalReco +
        process.offlineBeamSpot + #cmssw_10_6
        process.otLocalReco +
        process.caloLocalReco +
    ##############################################
        process.trackerClusterCheck +
    ##############################################
        process.initialStepSequence +
        process.highPtTripletStepSequence +
        process.lowPtQuadStepSequence +
        process.lowPtTripletStepSequence +
        process.detachedQuadStepSequence +
        process.pixelPairStepSequence +
    ##############################################
    #    convClusters +
    #    convLayerPairs +
    #    convStepSelector +
    #    convStepTracks +
    #    convTrackCandidates +
    #    conversionStepTracks +
    ##############################################
    #    dedxHarmonic2 +
    #    dedxHitInfo +
    #    dedxPixelAndStripHarmonic2T085 +
    #    dedxPixelHarmonic2 +
    #    dedxTruncated40 +
    ##############################################
        process.earlyGeneralTracks +
        process.muonSeededStepSequence +
        process.preDuplicateMergingGeneralTracks +
        process.duplicateTrackCandidates +
        process.mergedDuplicateTracks +
        process.duplicateTrackClassifier +
    ##############################################
        process.generalTracks +
    #    generalV0Candidates +        # it would be nice to keep !
    ##############################################
    #    inclusiveSecondaryVertices + # it would be nice to keep !
    #    inclusiveVertexFinder +      # it would be nice to keep !
    ##############################################
    #    newCombinedSeeds +           # used by electron
    ##############################################
        process.vertexReco
    ##############################################
    #    photonConvTrajSeedFromSingleLeg +
    ##############################################
    #    tripletElectronHitDoublets +
    #    tripletElectronHitTriplets +
    #    tripletElectronSeedLayers +
    #    tripletElectronSeeds +
    #    tripletElectronTrackingRegions +
    )

    # remove globalreco_trackingTask to avoid any ambiguities
    # with the updated sequence process.globalreco_tracking
    if hasattr(process, 'globalreco_trackingTask'):
       del process.globalreco_trackingTask

    return process
