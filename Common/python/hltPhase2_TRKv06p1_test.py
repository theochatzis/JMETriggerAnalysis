import FWCore.ParameterSet.Config as cms

from L1Trigger.TrackFindingTracklet.Tracklet_cfi import *
from Configuration.StandardSequences.Reconstruction_cff import *
from RecoTracker.GeometryESProducer.TrackerRecoGeometryESProducer_cfi import *
from RecoTracker.MeasurementDet.MeasurementTrackerESProducer_cfi import *

def customise_hltPhase2_TRKv06p1(process):

    ###
    ### Modules (taken from configuration developed by TRK POG)
    ###
    ## ---- NEW MODULES ------------

    process.TrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer",
        trackerGeometryLabel = cms.untracked.string('')
    )
    """
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
        appendToDataLabel = cms.string(''),
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
    """

    """
    process.MeasurementTrackerEvent = cms.EDProducer("MeasurementTrackerEventProducer",
        Phase2TrackerCluster1DProducer = cms.string('siPhase2Clusters'),
        badPixelFEDChannelCollectionLabels = cms.VInputTag("siPixelDigis"),
        inactivePixelDetectorLabels = cms.VInputTag(),
        inactiveStripDetectorLabels = cms.VInputTag("siStripDigis"),
        measurementTracker = cms.string(''),
        mightGet = cms.optional.untracked.vstring,
        pixelCablingMapLabel = cms.string(''),
        pixelClusterProducer = cms.string('siPixelClusters'),
        skipClusters = cms.InputTag(""),
        stripClusterProducer = cms.string(''),
        switchOffPixelsIfEmpty = cms.bool(True)
    )
    """
    

    process.hltPhase2PixelTrackFilterByKinematics = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
        nSigmaTipMaxTolerance = cms.double( 0.0 ),
        chi2 = cms.double( 1000.0 ),
        nSigmaInvPtTolerance = cms.double( 0.0 ),
        ptMin = cms.double( 0.9 ), #previous 0.1
        tipMax = cms.double( 1.0 )
    )
    
    process.hltPhase2PixelFitterByHelixProjections = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
        scaleErrorsForBPix1 = cms.bool( False ),
        scaleFactor = cms.double( 0.65 )
    )

    process.hltPhase2PixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            nSigmaZ = cms.double( 4.0 ),
            beamSpot = cms.InputTag( "offlineBeamSpot" ),
            ptMin = cms.double( 0.9 ), # previous 0.8
            originRadius = cms.double( 0.02 ),
            precise = cms.bool( True )
        )
    )

    process.hltPhase2PixelTracksSeedLayers = cms.EDProducer( "SeedingLayersEDProducer",
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
        ),
        MTOB = cms.PSet(  ),
        TEC = cms.PSet(  ),
        MTID = cms.PSet(  ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'), #PreSplitting'),
            TTRHBuilder = cms.string('WithTrackAngle')
    #      hitErrorRPhi = cms.double( 0.0051 ),
    #      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    #      useErrorsFromParam = cms.bool( True ),
    #      hitErrorRZ = cms.double( 0.0036 ),
    #      HitProducer = cms.string( "hltSiPixelRecHits" )
        ),
        MTEC = cms.PSet(  ),
        MTIB = cms.PSet(  ),
        TID = cms.PSet(  ),
        TOB = cms.PSet(  ),
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'), #PreSplitting'),
            TTRHBuilder = cms.string('WithTrackAngle')
    #      hitErrorRPhi = cms.double( 0.0027 ),
    #      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
    #      useErrorsFromParam = cms.bool( True ),
    #      hitErrorRZ = cms.double( 0.006 ),
    #      HitProducer = cms.string( "hltSiPixelRecHits" )
        ),
        TIB = cms.PSet(  ),
        mightGet = cms.optional.untracked.vstring
    )

    process.hltPhase2PixelTracksHitDoublets = cms.EDProducer( "HitPairEDProducer",
        trackingRegions = cms.InputTag( "hltPhase2PixelTracksTrackingRegions" ),
        layerPairs = cms.vuint32( 0, 1, 2 ),
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        produceSeedingHitSets = cms.bool( False ),
        produceIntermediateHitDoublets = cms.bool( True ),
        trackingRegionsSeedingLayers = cms.InputTag( "" ),
        maxElementTotal = cms.uint32( 50000000 ),
        maxElement = cms.uint32(50000000), # 0 ),
        seedingLayers = cms.InputTag( "hltPhase2PixelTracksSeedLayers" )
    )

    process.hltPhase2PixelTracksHitSeeds = cms.EDProducer( "CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double( 0.5 ), #hevjin 0.0
        SeedComparitorPSet = cms.PSet(
        clusterShapeHitFilter = cms.string( "ClusterShapeHitFilter" ),
        ComponentName = cms.string( "LowPtClusterShapeSeedComparitor" ),
        clusterShapeCacheSrc = cms.InputTag( "siPixelClusterShapeCache") # pixelVertices
        ),
        extraHitRPhitolerance = cms.double( 0.032 ),
        doublets = cms.InputTag( "hltPhase2PixelTracksHitDoublets" ),
        fitFastCircle = cms.bool( True ),
        CAThetaCut = cms.double( 0.0012 ), # 0.002 ),
        maxChi2 = cms.PSet(
        value2 = cms.double( 50.0 ),
        value1 = cms.double( 200.0 ),
        pt1 = cms.double( 0.7 ),
        enabled = cms.bool( True ),
        pt2 = cms.double( 2.0 )
        ),
        CAPhiCut = cms.double( 0.2 ),
        useBendingCorrection = cms.bool( True ),
        fitFastCircleChi2Cut = cms.bool( True )#,
    )


    #process.vertexFromL1 = cms.EDProducer("L1ToVertex")
    
    #process.pixelVertexCoordinates = cms.EDProducer("PixelVertexCoordinates",
    #    mightGet = cms.optional.untracked.vstring,
    #    src = cms.InputTag("vertexFromL1")
    #)
    """
    process.hltPhase2PixelTrackSoA = cms.EDProducer("CAHitNtupletCUDA",
        CAThetaCutBarrel = cms.double(0.00200000009499),
        CAThetaCutForward = cms.double(0.00300000002608),
        dcaCutInnerTriplet = cms.double(0.15000000596),
        dcaCutOuterTriplet = cms.double(0.25),
        doClusterCut = cms.bool(False),
        doPtCut = cms.bool(True),
        doRegion = cms.bool(False),
        doZ0Cut = cms.bool(True),
        earlyFishbone = cms.bool(True),
        fillStatistics = cms.bool(False),
        fit5as4 = cms.bool(True),
        hardCurvCut = cms.double(0.0328407224959),
        idealConditions = cms.bool(True),
        includeJumpingForwardDoublets = cms.bool(False),
        isUpgrade = cms.bool(True),
        lateFishbone = cms.bool(False),
        maxNumberOfDoublets = cms.uint32(8388608),
        mightGet = cms.optional.untracked.vstring,
        minHitsPerNtuplet = cms.uint32(3),
        onGPU = cms.bool(False),
        pixelRecHitSrc = cms.InputTag("siPixelRecHits"),
        ptmin = cms.double(0.899999976158),
        trackQualityCuts = cms.PSet(
            chi2Coeff = cms.vdouble(0.68177776, 0.74609577, -0.08035491, 0.00315399),
            chi2MaxPt = cms.double(3.5),
            chi2Scale = cms.double(30),
            quadrupletMaxTip = cms.double(0.25),
            quadrupletMaxZip = cms.double(12),
            quadrupletMinPt = cms.double(0.8),
            tripletChi2MaxPt = cms.double(2.5),
            tripletMaxTip = cms.double(0.22),
            tripletMaxZip = cms.double(11.5),
            tripletMinPt = cms.double(0.8),
            upgrade = cms.bool(True)
        ),
        useRiemannFit = cms.bool(False),
        vertexRegion = cms.InputTag("pixelVertexCoordinates")
    )
    """
    process.hltPhase2PixelTracks = cms.EDProducer("PixelTrackProducer",
        Cleaner = cms.string('hltPhase2PixelTrackCleanerBySharedHits'),
        passLabel = cms.string('hltPhase2PixelTracks'),
        Filter = cms.InputTag("hltPhase2PixelTrackFilterByKinematics"),
        Fitter = cms.InputTag("hltPhase2PixelFitterByHelixProjections"),
        SeedingHitSets = cms.InputTag("hltPhase2PixelTracksHitSeeds"),
        mightGet = cms.untracked.vstring("")#'RegionsSeedingHitSets_pixelTracksHitQuadruplets__RECO')
    )

    """
    process.hltPhase2PixelTracks = cms.EDProducer("PixelTrackProducerFromSoA",
        beamSpot = cms.InputTag("offlineBeamSpot"),
        keepBad = cms.int32(2),
        keepDup = cms.int32(2),
        mightGet = cms.optional.untracked.vstring,
        minNumberOfHits = cms.int32(0),
        pixelRecHitLegacySrc = cms.InputTag("siPixelRecHits"),
        tpMap = cms.InputTag("tpClusterProducerPreSplitting"),
        trackSrc = cms.InputTag("hltPhase2PixelTrackSoA")
    )
    """
    process.hltPhase2PSetPvClusterComparerForIT = cms.PSet(
        track_chi2_max = cms.double(20.0),
        track_prob_min = cms.double(-1.0),
        track_pt_max = cms.double(100.0),
        track_pt_min = cms.double(1.0)
    )

    process.hltPhase2PixelTracksClean = cms.EDProducer("RecoTrackViewRefSelector",
        algorithm = cms.vstring(),
        algorithmMaskContains = cms.vstring(),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        invertRapidityCut = cms.bool(False), # cmssw_11_1
        lip = cms.double(300.0),
        maxChi2 = cms.double(100.0),
        maxPhi = cms.double(3.2),
        maxRapidity = cms.double(4.5),
        min3DLayer = cms.int32(0),
        minHit = cms.int32(0),
        minLayer = cms.int32(2),
        minPhi = cms.double(-3.2),
        minPixelHit = cms.int32(0), maxPixelHit = cms.int32(99),
        minRapidity = cms.double(-4.5),
        minPixelLayer = cms.int32(0),
        originalAlgorithm = cms.vstring(),
        ptMin = cms.double(1.2), # previous 0.1
        quality = cms.vstring('any'),
        src = cms.InputTag("hltPhase2PixelTracks"),
        tip = cms.double(120),
        usePV = cms.bool(False),
        vertexTag = cms.InputTag("")#hltPhase2PixelVertices") #("hltPhase2OfflinePrimaryVertices")
    )

    process.hltPhase2PixelVertices = cms.EDProducer( "PixelVertexProducer",
        WtAverage = cms.bool( True ),
        Method2 = cms.bool( True ),
        beamSpot = cms.InputTag( "offlineBeamSpot" ),
        PVcomparer = cms.PSet(  refToPSet_ = cms.string( "hltPhase2PSetPvClusterComparerForIT" ) ),
        Verbosity = cms.int32( 0 ),
        UseError = cms.bool( True ),
        TrackCollection = cms.InputTag( "hltPhase2PixelTracksClean" ),
        PtMin = cms.double( 2.0 ),
        NTrkMin = cms.int32( 2 ),
        ZOffset = cms.double( 5.0 ),
        Finder = cms.string( "DivisiveVertexFinder" ),
        ZSeparation = cms.double( 0.025 )
    )

    """
    process.hltPhase2TrimmedPixelVertices = cms.EDProducer("MeasurementTrackerEventProducer",
        Phase2TrackerCluster1DProducer = cms.string('siPhase2Clusters'),
        badPixelFEDChannelCollectionLabels = cms.VInputTag("siPixelDigis"),
        inactivePixelDetectorLabels = cms.VInputTag(),
        inactiveStripDetectorLabels = cms.VInputTag("siStripDigis"),
        measurementTracker = cms.string(''),
        mightGet = cms.optional.untracked.vstring,
        pixelCablingMapLabel = cms.string(''),
        pixelClusterProducer = cms.string('siPixelClusters'),
        skipClusters = cms.InputTag(""),
        stripClusterProducer = cms.string(''),
        switchOffPixelsIfEmpty = cms.bool(True)
    )
    """
    
    process.hltPhase2PixelTracksCleaner = cms.EDProducer("TrackWithVertexSelector",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        d0Max = cms.double(999.0),
        dzMax = cms.double(999.0),
        etaMax = cms.double(5.0),
        etaMin = cms.double(0.0),
        nSigmaDtVertex = cms.double(0),
        nVertices = cms.uint32(20),
        normalizedChi2 = cms.double(999999.0),
        numberOfLostHits = cms.uint32(999),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(4),
        maxOfValidPixelHits = cms.uint32(99),
        ptErrorCut = cms.double(9999999.0),
        ptMax = cms.double(100000.0),
        ptMin = cms.double(0.0),
        quality = cms.string('any'),
        rhoVtx = cms.double(0.1),
        src = cms.InputTag("hltPhase2PixelTracks"),
        timeResosTag = cms.InputTag(""),
        timesTag = cms.InputTag(""),
        useVtx = cms.bool(True),
        vertexTag = cms.InputTag("hltPhase2PixelVertices"),
        vtxFallback = cms.bool(True),
        zetaVtx = cms.double(0.3)
    )

    process.hltPhase2PixelTripletsCleaner = cms.EDProducer("TrackWithVertexSelector",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        d0Max = cms.double(999.0),
        dzMax = cms.double(999.0),
        etaMax = cms.double(5.0),
        etaMin = cms.double(0.0),
        nSigmaDtVertex = cms.double(0),
        nVertices = cms.uint32(20),
        normalizedChi2 = cms.double(999999.0),
        numberOfLostHits = cms.uint32(999),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(3),
        maxOfValidPixelHits = cms.uint32(3),
        ptErrorCut = cms.double(9999999.0),
        ptMax = cms.double(100000.0),
        ptMin = cms.double(0.0),
        quality = cms.string('any'),
        rhoVtx = cms.double(0.06),
        src = cms.InputTag("hltPhase2PixelTracks"),
        timeResosTag = cms.InputTag(""),
        timesTag = cms.InputTag(""),
        useVtx = cms.bool(True),
        vertexTag = cms.InputTag("hltPhase2PixelVertices"),
        vtxFallback = cms.bool(True),
        zetaVtx = cms.double(0.18)
    )
    
    process.hltPhase2PixelTripletsSelector= cms.EDProducer("RecoTrackViewRefSelector",
        algorithm = cms.vstring(),
        algorithmMaskContains = cms.vstring(),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        invertRapidityCut = cms.bool(False), # cmssw_11_1
        lip = cms.double(300.0),
        maxChi2 = cms.double(10000000.0),
        maxPhi = cms.double(3.2),
        maxRapidity = cms.double(4.5),
        min3DLayer = cms.int32(0),
        minHit = cms.int32(0),
        minLayer = cms.int32(0),
        minPhi = cms.double(-3.2),
        minPixelHit = cms.int32(2), maxPixelHit = cms.int32(3),
        minRapidity = cms.double(-4.5),
        originalAlgorithm = cms.vstring(),
        ptMin = cms.double(0.9), # previous 0.1
        quality = cms.vstring(''),
        src = cms.InputTag("hltPhase2PixelTracks"),
        tip = cms.double(120),
        minPixelLayer = cms.int32(2),
        usePV = cms.bool(False),
        vertexTag = cms.InputTag("")
    )

    process.hltPhase2PixelQuadrupletsSelector= cms.EDProducer("RecoTrackViewRefSelector",
        algorithm = cms.vstring(),
        algorithmMaskContains = cms.vstring(),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        invertRapidityCut = cms.bool(False), # cmssw_11_1
        lip = cms.double(300.0),
        maxChi2 = cms.double(10000.0),
        maxPhi = cms.double(3.2),
        maxRapidity = cms.double(4.5),
        min3DLayer = cms.int32(0),
        minHit = cms.int32(0),
        minLayer = cms.int32(2),
        minPhi = cms.double(-3.2),
        minPixelHit = cms.int32(4), maxPixelHit = cms.int32(99),
        minRapidity = cms.double(-4.5),
        minPixelLayer = cms.int32(3),
        originalAlgorithm = cms.vstring(),
        ptMin = cms.double(0.9), # previous 0.1
        quality = cms.vstring('any'),
        src = cms.InputTag("hltPhase2PixelTracks"),
        tip = cms.double(120),
        usePV = cms.bool(False),
        vertexTag = cms.InputTag("")#hltPhase2PixelVertices") #("hltPhase2OfflinePrimaryVertices")
    )
    

    

    process.hltPhase2PixelTracksMerger = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(5.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.9), # ptcut previous 0.05
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag( 
        cms.InputTag("hltPhase2PixelTracksCleaner"),
    cms.InputTag("hltPhase2PixelTripletsCleaner")

        ),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False), # trackcutclassifier before True
        hasSelector = cms.vint32(
            0, 0#, 1#, 1, 1,  ### v2 # trackcutclassifier 
        ),
        indivShareFrac = cms.vdouble( 
            1.0, 1.0 # trackcutclassifier
        ),
        makeReKeyedSeeds = cms.untracked.bool(False),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag(
        cms.InputTag("hltPhase2PixelTracksCleaner"),
    cms.InputTag("hltPhase2PixelTripletsCleaner") 
        ),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(True),
            tLists = cms.vint32(
                0, 1#, 2#, 3, 4, ### v2
                #5
            )
        )),
        trackAlgoPriorityOrder = cms.string('hltPhase2TrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    
    
    process.hltPhase2SeedFromProtoTracks = cms.PSet(
        TTRHBuilder = cms.string( "WithTrackAngle"), #hltESPTTRHBuilderPixelOnly" ),
        SeedMomentumForBOFF = cms.double( 5.0 ),
        propagator = cms.string( "PropagatorWithMaterial"),# previous PropagatorWithMaterialParabolicMf" ), # used also elsewhere though
        forceKinematicWithRegionDirection = cms.bool( False ),
        magneticField = cms.string( ""), # previous ParabolicMf" ),
        OriginTransverseErrorMultiplier = cms.double( 1.0 ),
        ComponentName = cms.string( "SeedFromConsecutiveHitsCreator" ),
        MinOneOverPtError = cms.double( 1.0 ) 
    )


    process.hltPhase2InitialStepSeeds = cms.EDProducer( "SeedGeneratorFromProtoTracksEDProducer",
        useEventsWithNoVertex = cms.bool( True ),
        originHalfLength = cms.double(0.3), #10 1  previous 0.3 ),
        useProtoTrackKinematics = cms.bool( False ),
        usePV = cms.bool( False ),
        includeFourthHit = cms.bool(True),
        SeedCreatorPSet = cms.PSet(  refToPSet_ = cms.string( "hltPhase2SeedFromProtoTracks" ) ),
        InputVertexCollection = cms.InputTag(""),
        TTRHBuilder = cms.string( "WithTrackAngle"), #hltESPTTRHBuilderPixelOnly" ),
        InputCollection = cms.InputTag( "hltPhase2PixelTracks" ),
        originRadius = cms.double( 0.1 ) # 5 #0.5  previous 0.1
    )
    
    process.hltPhase2InitialStepTrajectoryFilter = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0), # previous 2
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(0), # previous 9999
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(1), # previous 999
        maxLostHitsFraction = cms.double(999), # previous 0.1
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(4), # previous 3
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9), # previous 0.2 # ptcut previous 0.3
        minimumNumberOfHits = cms.int32(4), # previous 3
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.hltPhase2InitialStepTrajectoryBuilder = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),# previous GroupedCkfTrajectoryBuilder --> CkfTrajectoryBuilder
        #MeasurementTrackerName = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(False), # previous True
        bestHitOnly = cms.bool(True),
        estimator = cms.string('hltPhase2InitialStepChi2Est'),
        foundHitBonus = cms.double(10.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('hltPhase2InitialStepTrajectoryFilter') # previous CkfBaseTrajectoryFilter_block
        ),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(True),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(1), # previous 3
        maxDPhiForLooperReconstruction = cms.double(2.0),
        maxPtForLooperReconstruction = cms.double(0.7),
        minNrOfHitsForRebuild = cms.int32(1),
        propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'), # previous PropagatorWithMaterial
        propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'), # previous PropagatorWithMaterialOpposite
        requireSeedHitsInRebuild = cms.bool(True),
        seedAs5DHit = cms.bool(False), #cmssw_11_0
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('hltPhase2InitialStepTrajectoryFilter')
        ),
        #seedPairPenalty = cms.int32(0),
        #minPt = cms.double(0.9),
        #maxLostHitsFraction = cms.double(999.0), # previous 0.1
        #maxNumberOfHits = cms.int32(100),
        updator = cms.string('KFUpdator'),
        useSameTrajFilter = cms.bool(True)
    )

    process.hltPhase2InitialStepTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        ### if we use 'CachingSeedCleanerBySharedInput' as the redundantseedcleaner
        ### then numHitsForSeedCleaner = cms.int32(4) and onlyPixelHitsForSeedCleaner = cms.bool(False) by default
        ### unless they are changed explicitly
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        #SimpleMagneticField = cms.string('ParabolicMf'), # previous ''
        #TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'), # previous GroupedCkfTrajectoryBuilder --> ''
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('hltPhase2InitialStepTrajectoryBuilder')
        ),
        TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(16),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'), # previous PropagatorWithMaterial
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite') # previous PropagatorWithMaterialOpposite
        ),
        cleanTrajectoryAfterInOut = cms.bool(True), # previous True --> False
        doSeedingRegionRebuilding = cms.bool(True),# previous True --> False
        maxNSeeds = cms.uint32(100000), # previous 500000
        maxSeedsBeforeCleaning = cms.uint32(1000), # previous 5000
        numHitsForSeedCleaner = cms.int32(50), ##########
        onlyPixelHitsForSeedCleaner = cms.bool(True), ##########
        reverseTrajectories = cms.bool(False), # previous False, try both F/T for timing/performance
        src = cms.InputTag("hltPhase2InitialStepSeeds"),
        useHitsSplitting = cms.bool(False) # previous True
    )

    process.hltPhase2InitialStepTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('initialStep'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(False),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        Propagator = cms.string('RungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'), # cmssw_11_1 --> WithTrackAngleTemplate but not corrected yet
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("offlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltPhase2InitialStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.hltPhase2InitialStepTrackCutClassifier = cms.EDProducer( "TrackCutClassifier",
        src = cms.InputTag( "hltPhase2InitialStepTracks" ),
        beamspot = cms.InputTag( "offlineBeamSpot" ),
        vertices = cms.InputTag( "hltPhase2PixelVertices" ), # pixelVertices previous hltPhase2FirstStepPrimaryVertices" ),
        qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
        mva = cms.PSet(
        minPixelHits = cms.vint32(0,0,3), ######
        maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
        dr_par = cms.PSet(
        d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
        dr_par1 = cms.vdouble( 0.8, 0.7, 0.6 ),
        dr_par2 = cms.vdouble( 0.6, 0.5, 0.45 ),
        dr_exp = cms.vint32( 4, 4, 4 ),
        d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
        ),
        maxLostLayers = cms.vint32( 3, 2, 2 ),
        min3DLayers = cms.vint32( 3, 3, 3),
        dz_par = cms.PSet(
        dz_par1 = cms.vdouble( 0.9, 0.8, 0.7 ),
        dz_par2 = cms.vdouble( 0.8, 0.7, 0.55 ),
        dz_exp = cms.vint32( 4, 4, 4 )
        ),
        minNVtxTrk = cms.int32( 3 ), # offline 2, online 3 switching to 3
        maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639E38 ), ##
        minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ), ##
        maxChi2 = cms.vdouble( 9999.0, 25.0, 16.0 ),
        maxChi2n = cms.vdouble( 2.0, 1.4, 1.2),
        maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ), ##
        minLayers = cms.vint32( 3, 3, 3 ) ##
        ),
        ignoreVertices = cms.bool( False )
    )
    
    process.hltPhase2InitialStepTracksSelectionHighPurity = cms.EDProducer( "TrackCollectionFilterCloner",
        minQuality = cms.string( "highPurity" ),
        copyExtras = cms.untracked.bool( True ),
        copyTrajectories = cms.untracked.bool( False ),
        originalSource = cms.InputTag( "hltPhase2InitialStepTracks" ),
        originalQualVals = cms.InputTag('hltPhase2InitialStepTrackCutClassifier','QualityMasks' ),
        originalMVAVals = cms.InputTag('hltPhase2InitialStepTrackCutClassifier','MVAValues' )
    )
    

    process.hltPhase2GeneralTracks = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(5.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.9), # ptcut previous 0.05
        ShareFrac = cms.double(0.2),
        TrackProducers = cms.VInputTag(
            #"hltPhase2InitialStepTracks", "hltPhase2HighPtTripletStepTracks" ### v2
        "hltPhase2InitialStepTracksSelectionHighPurity", "hltPhase2HighPtTripletStepTracksSelectionHighPurity" ### v2 # trackcutclassifier
        ),
        allowFirstHitShare = cms.bool(False),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False), # trackcutclassifier before True
        hasSelector = cms.vint32(
            0, 0#, 1#, 1, 1,  ### v2 # trackcutclassifier
            #1
        ),
        indivShareFrac = cms.vdouble(
            #1.0, 0.16#, 0.095, 0.09, 0.09, ### v2
            ##0.09
        1.0, 1.0 # trackcutclassifier
        ),
        makeReKeyedSeeds = cms.untracked.bool(False),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag(
            #cms.InputTag("initialStepSelector","initialStep"), cms.InputTag("highPtTripletStepSelector","highPtTripletStep")### v2
        cms.InputTag("hltPhase2InitialStepTracksSelectionHighPurity"), cms.InputTag("hltPhase2HighPtTripletStepTracksSelectionHighPurity") # trackcutclassifier

        ),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(True),
            tLists = cms.vint32(
                0, 1#, 2#, 3, 4, ### v2
                #5
            )
        )),
        trackAlgoPriorityOrder = cms.string('hltPhase2TrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    process.hltPhase2HighPtTripletStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        mightGet = cms.optional.untracked.vstring, # cmssw_11_1
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag(""),
        #overrideTrkQuals = cms.InputTag("initialStepSelector","initialStep"),
        overrideTrkQuals = cms.InputTag(""), # trackcutclassifier
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("hltPhase2InitialStepTracksSelectionHighPurity")
    )

    
    process.hltPhase2HighPtTripletStepSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("hltPhase2HighPtTripletStepClusters")
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('siPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("hltPhase2HighPtTripletStepClusters")
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
        ),
        mightGet = cms.optional.untracked.vstring
    )


    process.hltPhase2HighPtTripletStepSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
        MinOneOverPtError = cms.double(1),
        OriginTransverseErrorMultiplier = cms.double(1),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_hltPhase2HighPtTripletStepHitTriplets__RECO'),
        propagator = cms.string('PropagatorWithMaterial'),
        seedingHitSets = cms.InputTag("hltPhase2HighPtTripletStepHitTriplets")
    )
    
    process.hltPhase2HighPtTripletStepTrajectoryFilter = cms.PSet(
        ComponentType = cms.string('CompositeTrajectoryFilter'),
        filters = cms.VPSet(
            cms.PSet(
                refToPSet_ = cms.string('hltPhase2HighPtTripletStepTrajectoryFilterBase')
            ),
            cms.PSet(
                refToPSet_ = cms.string('ClusterShapeTrajectoryFilter')
            )
        )
    )

    process.hltPhase2HighPtTripletStepTrajectoryFilterBase = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0), # previous 2.0
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(0), # previous 9999
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(1), # previous 999
        maxLostHitsFraction = cms.double(999.0), # previous 0.1
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9), # ptcut previous 0.2
        minimumNumberOfHits = cms.int32(3),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(1), # previous 0
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.hltPhase2HighPtTripletStepTrajectoryFilterInOut = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(2.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(999),
        maxLostHitsFraction = cms.double(0.1),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9), # ptcut previous 0.4
        minimumNumberOfHits = cms.int32(4),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(1),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    
    process.hltPhase2HighPtTripletStepChi2Est = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
        ComponentName = cms.string('hltPhase2HighPtTripletStepChi2Est'),
        MaxChi2 = cms.double(16.0), # previous 20.0
        MaxDisplacement = cms.double(0.5),
        MaxSagitta = cms.double(2),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000.0), # previous 1000000000000
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutLoose') # previous SiStripClusterChargeCutNone
        ),
        nSigma = cms.double(3),
        pTChargeCutThreshold = cms.double(-1) # previous 15.0
    )


    process.hltPhase2HighPtTripletStepTrajectoryBuilder = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'), #needs to stay like this for now
        #MeasurementTrackerName = cms.string(''), #??
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(False), # previous True
        bestHitOnly = cms.bool(True),
        estimator = cms.string('hltPhase2HighPtTripletStepChi2Est'),
        foundHitBonus = cms.double(10.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('hltPhase2HighPtTripletStepTrajectoryFilterInOut') #??
        ),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(False),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(1), # previous 3
        maxDPhiForLooperReconstruction = cms.double(2.0),
        maxPtForLooperReconstruction = cms.double(0.7),
        minNrOfHitsForRebuild = cms.int32(5),
        propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'), # previous PropagatorWithMaterial
        propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'), # previous PropagatorWithMaterialOpposite
        requireSeedHitsInRebuild = cms.bool(True),
        seedAs5DHit = cms.bool(False), #cmssw_11_0
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('hltPhase2HighPtTripletStepTrajectoryFilter')
        ),
        #seedPairPenalty = cms.int32(0),
        #minPt = cms.double(0.9),
        #maxLostHitsFraction = cms.double(999.0), # previous 0.1
        #maxNumberOfHits = cms.int32(100),
        updator = cms.string('KFUpdator'),
        useSameTrajFilter = cms.bool(False)
    )

    process.hltPhase2HighPtTripletStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
        ComponentName = cms.string('hltPhase2HighPtTripletStepTrajectoryCleanerBySharedHits'),
        ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
        MissingHitPenalty = cms.double(20.0),
        ValidHitBonus = cms.double(5.0),
        allowSharedFirstHit = cms.bool(True),
        fractionShared = cms.double(0.16)
    )

    process.hltPhase2HighPtTripletStepTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        ### if we use 'CachingSeedCleanerBySharedInput' as the redundantseedcleaner
        ### then numHitsForSeedCleaner = cms.int32(4) and onlyPixelHitsForSeedCleaner = cms.bool(False) by default
        ### unless they are changed explicitly
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        #SimpleMagneticField = cms.string('ParabolicMf'), # previous ''
        #sTrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'), #needs to stay this way
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('hltPhase2HighPtTripletStepTrajectoryBuilder')
        ),
        TrajectoryCleaner = cms.string('hltPhase2HighPtTripletStepTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'), # previous PropagatorWithMaterial
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite') # previous PropagatorWithMaterialOpposite
        ),
        cleanTrajectoryAfterInOut = cms.bool(True), #needs to stay True
        doSeedingRegionRebuilding = cms.bool(True), #needs to stay True
        maxNSeeds = cms.uint32(100000), # previous 500000
        maxSeedsBeforeCleaning = cms.uint32(1000), # previous 5000
        numHitsForSeedCleaner = cms.int32(50), #############
        onlyPixelHitsForSeedCleaner = cms.bool(True),  # previous ################
        phase2clustersToSkip = cms.InputTag("hltPhase2HighPtTripletStepClusters"),
        reverseTrajectories = cms.bool(False),
        src = cms.InputTag("hltPhase2HighPtTripletStepSeeds"),
        useHitsSplitting = cms.bool(False) # previous True
    )


    


    process.hltPhase2HighPtTripletStepTrackCutClassifier = cms.EDProducer( "TrackCutClassifier",
        src = cms.InputTag( "hltPhase2HighPtTripletStepTracks" ),
        beamspot = cms.InputTag( "offlineBeamSpot" ),
        vertices = cms.InputTag( "hltPhase2PixelVertices" ), # pixelVertices previous hltPhase2FirstStepPrimaryVertices" ),
        qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
        mva = cms.PSet(
        minPixelHits = cms.vint32( 0, 0, 3 ), ##
        maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
        dr_par = cms.PSet(
            d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
            dr_par2 = cms.vdouble( 0.6, 0.5, 0.45 ), ##
            dr_par1 = cms.vdouble( 0.7, 0.6, 0.6 ),
            dr_exp = cms.vint32( 4, 4, 4 ),
            d0err_par = cms.vdouble( 0.002, 0.002, 0.001 )
        ),
        maxLostLayers = cms.vint32( 3, 3, 2 ),
        min3DLayers = cms.vint32( 3, 3, 4 ),
        dz_par = cms.PSet(
            dz_par1 = cms.vdouble( 0.8, 0.7, 0.7 ),
            dz_par2 = cms.vdouble( 0.6, 0.6, 0.55 ),
            dz_exp = cms.vint32( 4, 4, 4 )
        ),
        minNVtxTrk = cms.int32( 3 ), ## offline 2, online 3 switching to 3
        maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639E38 ), ##
        minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ), ##
        maxChi2 = cms.vdouble( 9999.0, 9999.0, 9999.0 ),
        maxChi2n = cms.vdouble( 2.0, 1.0, 0.8 ),
        maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ), ##
        minLayers = cms.vint32( 3, 3, 4 )
        ),
        ignoreVertices = cms.bool( False )
    )


    process.hltPhase2HighPtTripletStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.02),
            precise = cms.bool(True),
            ptMin = cms.double(0.9), # ptcut previous 0.7
            useMultipleScattering = cms.bool(False)
        ),
        mightGet = cms.optional.untracked.vstring  # cmssw_11_1
    )

    process.hltPhase2HighPtTripletStepHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("trackerClusterCheck"),
        layerPairs = cms.vuint32(0, 1),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        mightGet = cms.optional.untracked.vstring, # cmssw_11_1
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("hltPhase2HighPtTripletStepSeedLayers"),
        trackingRegions = cms.InputTag("hltPhase2HighPtTripletStepTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.hltPhase2HighPtTripletStepHitTriplets = cms.EDProducer("CAHitTripletEDProducer",
        CAHardPtCut = cms.double(0.5),
        CAPhiCut = cms.double(0.06),
        CAThetaCut = cms.double(0.003),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("hltPhase2HighPtTripletStepHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(8),
            value1 = cms.double(100),
            value2 = cms.double(6)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_highPtTripletStepHitDoublets__RECO'),
        useBendingCorrection = cms.bool(True)
    )


    process.hltPhase2HighPtTripletStepTracks = cms.EDProducer("TrackProducer",
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
        src = cms.InputTag("hltPhase2HighPtTripletStepTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )


    process.hltPhase2HighPtTripletStepTracksSelectionHighPurity = cms.EDProducer( "TrackCollectionFilterCloner",
        minQuality = cms.string( "highPurity" ),
        copyExtras = cms.untracked.bool( True ),
        copyTrajectories = cms.untracked.bool( False ),
        originalSource = cms.InputTag( "hltPhase2HighPtTripletStepTracks" ),
        originalQualVals = cms.InputTag( 'hltPhase2HighPtTripletStepTrackCutClassifier','QualityMasks' ),
        originalMVAVals = cms.InputTag( 'hltPhase2HighPtTripletStepTrackCutClassifier','MVAValues' )
    )
    
    process.hltPhase2UnsortedOfflinePrimaryVertices = cms.EDProducer("PrimaryVertexProducer",
        TkClusParameters = cms.PSet(
            TkDAClusParameters = cms.PSet(
                Tmin = cms.double(2.0),
                Tpurge = cms.double(2.0),
                Tstop = cms.double(0.5),
                coolingFactor = cms.double(0.6),
                d0CutOff = cms.double(3.0),
                dzCutOff = cms.double(3.0),
                uniquetrkweight = cms.double(0.8),
                vertexSize = cms.double(0.006),
                zmerge = cms.double(0.01)
            ),
            algorithm = cms.string('DA_vect')
        ),
        TkFilterParameters = cms.PSet(
            algorithm = cms.string('filter'),
            maxD0Significance = cms.double(4.0),
            maxEta = cms.double(4.0),
            maxNormalizedChi2 = cms.double(10.0),
            minPixelLayersWithHits = cms.int32(2),
            minPt = cms.double(0.9), # ptcut previous 0.0
            minSiliconLayersWithHits = cms.int32(5),
            trackQuality = cms.string('any')
        ),
        TrackLabel = cms.InputTag("hltPhase2GeneralTracks"), ## hltPhase2
        beamSpotLabel = cms.InputTag("offlineBeamSpot"),
        verbose = cms.untracked.bool(False),
        vertexCollections = cms.VPSet(
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string(''),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(0.0),
                useBeamConstraint = cms.bool(False)
            ),
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string('WithBS'),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(2.0),
                useBeamConstraint = cms.bool(True)
            )
        )
    )

    process.hltPhase2TrackWithVertexRefSelectorBeforeSorting = cms.EDProducer("TrackWithVertexRefSelector",
        copyExtras = cms.untracked.bool(False),
        copyTrajectories = cms.untracked.bool(False),
        d0Max = cms.double(999.0),
        dzMax = cms.double(999.0),
        etaMax = cms.double(5.0),
        etaMin = cms.double(0.0),
        nSigmaDtVertex = cms.double(0),
        nVertices = cms.uint32(0),
        normalizedChi2 = cms.double(999999.0),
        numberOfLostHits = cms.uint32(999),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(0),
        maxOfValidPixelHits = cms.uint32(999),

        ptErrorCut = cms.double(9e+99),
        ptMax = cms.double(9e+99),
        ptMin = cms.double(0.9), # ptcut previous 0.3
        quality = cms.string('highPurity'),
        rhoVtx = cms.double(0.2),
        src = cms.InputTag("hltPhase2GeneralTracks"), ## hltPhase2
        timeResosTag = cms.InputTag(""),
        timesTag = cms.InputTag(""),
        useVtx = cms.bool(True),
        vertexTag = cms.InputTag("hltPhase2UnsortedOfflinePrimaryVertices"),
        vtxFallback = cms.bool(True),
        zetaVtx = cms.double(1.0)
    )

    process.hltPhase2TrackRefsForJetsBeforeSorting = cms.EDProducer("ChargedRefCandidateProducer",
        particleType = cms.string('pi+'),
        src = cms.InputTag("hltPhase2TrackWithVertexRefSelectorBeforeSorting")
    )

    process.hltPhase2Ak4CaloJetsForTrk = cms.EDProducer("FastjetJetProducer",
        Active_Area_Repeats = cms.int32(1),
        GhostArea = cms.double(0.01),
        Ghost_EtaMax = cms.double(5.0),
        Rho_EtaMax = cms.double(4.4),
        doAreaDiskApprox = cms.bool(False),
        doAreaFastjet = cms.bool(False),
        doPUOffsetCorr = cms.bool(False),
        doPVCorrection = cms.bool(True),
        doRhoFastjet = cms.bool(False),
        inputEMin = cms.double(0.0),
        inputEtMin = cms.double(0.3),
        jetAlgorithm = cms.string('AntiKt'),
        jetPtMin = cms.double(10.0),
        jetType = cms.string('CaloJet'),
        maxBadEcalCells = cms.uint32(9999999),
        maxBadHcalCells = cms.uint32(9999999),
        maxProblematicEcalCells = cms.uint32(9999999),
        maxProblematicHcalCells = cms.uint32(9999999),
        maxRecoveredEcalCells = cms.uint32(9999999),
        maxRecoveredHcalCells = cms.uint32(9999999),
        minSeed = cms.uint32(14327),
        nSigmaPU = cms.double(1.0),
        puPtMin = cms.double(10),
        rParam = cms.double(0.4),
        radiusPU = cms.double(0.5),
        src = cms.InputTag("caloTowerForTrk"),
        srcPVs = cms.InputTag("hltPhase2UnsortedOfflinePrimaryVertices"),
        useDeterministicSeed = cms.bool(True),
        voronoiRfact = cms.double(-0.9)
    )

    process.hltPhase2OfflinePrimaryVertices = cms.EDProducer("RecoChargedRefCandidatePrimaryVertexSorter",
        assignment = cms.PSet(
            DzCutForChargedFromPUVtxs = cms.double(0.2),
            EtaMinUseDz = cms.double(-1),
            NumOfPUVtxsForCharged = cms.uint32(0),
            OnlyUseFirstDz = cms.bool(False),
            PtMaxCharged = cms.double(-1),
            maxDistanceToJetAxis = cms.double(0.07),
            maxDtSigForPrimaryAssignment = cms.double(4.0),
            maxDxyForJetAxisAssigment = cms.double(0.1),
            maxDxyForNotReconstructedPrimary = cms.double(0.01),
            maxDxySigForNotReconstructedPrimary = cms.double(2),
            maxDzErrorForPrimaryAssignment = cms.double(0.05),
            maxDzForJetAxisAssigment = cms.double(0.1),
            maxDzForPrimaryAssignment = cms.double(0.1),
            maxDzSigForPrimaryAssignment = cms.double(5.0),
            maxJetDeltaR = cms.double(0.5),
            minJetPt = cms.double(25),
            preferHighRanked = cms.bool(False),
            useTiming = cms.bool(False),
            useVertexFit = cms.bool(True)
        ),
        jets = cms.InputTag("hltPhase2Ak4CaloJetsForTrk"),
        particles = cms.InputTag("hltPhase2TrackRefsForJetsBeforeSorting"),
        produceAssociationToOriginalVertices = cms.bool(False),
        produceNoPileUpCollection = cms.bool(False),
        producePileUpCollection = cms.bool(False),
        produceSortedVertices = cms.bool(True),
        qualityForPrimary = cms.int32(3),
        sorting = cms.PSet(

        ),
        trackTimeResoTag = cms.InputTag(""),
        trackTimeTag = cms.InputTag(""),
        usePVMET = cms.bool(True),
        vertices = cms.InputTag("hltPhase2UnsortedOfflinePrimaryVertices")
    )

    process.hltPhase2OfflinePrimaryVerticesWithBS = cms.EDProducer("RecoChargedRefCandidatePrimaryVertexSorter",
        assignment = cms.PSet(
            DzCutForChargedFromPUVtxs = cms.double(0.2),
            EtaMinUseDz = cms.double(-1),
            NumOfPUVtxsForCharged = cms.uint32(0),
            OnlyUseFirstDz = cms.bool(False),
            PtMaxCharged = cms.double(-1),
            maxDistanceToJetAxis = cms.double(0.07),
            maxDtSigForPrimaryAssignment = cms.double(4.0),
            maxDxyForJetAxisAssigment = cms.double(0.1),
            maxDxyForNotReconstructedPrimary = cms.double(0.01),
            maxDxySigForNotReconstructedPrimary = cms.double(2),
            maxDzErrorForPrimaryAssignment = cms.double(0.05),
            maxDzForJetAxisAssigment = cms.double(0.1),
            maxDzForPrimaryAssignment = cms.double(0.1),
            maxDzSigForPrimaryAssignment = cms.double(5.0),
            maxJetDeltaR = cms.double(0.5),
            minJetPt = cms.double(25),
            preferHighRanked = cms.bool(False),
            useTiming = cms.bool(False),
            useVertexFit = cms.bool(True)
        ),
        jets = cms.InputTag("hltPhase2Ak4CaloJetsForTrk"),
        particles = cms.InputTag("hltPhase2TrackRefsForJetsBeforeSorting"),
        produceAssociationToOriginalVertices = cms.bool(False),
        produceNoPileUpCollection = cms.bool(False),
        producePileUpCollection = cms.bool(False),
        produceSortedVertices = cms.bool(True),
        qualityForPrimary = cms.int32(3),
        sorting = cms.PSet(

        ),
        trackTimeResoTag = cms.InputTag(""),
        trackTimeTag = cms.InputTag(""),
        usePVMET = cms.bool(True),
        vertices = cms.InputTag("hltPhase2UnsortedOfflinePrimaryVertices","WithBS")
    )
    
    process.hltPhase2InclusiveVertexFinder = cms.EDProducer("InclusiveVertexFinder",
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
        minPt = cms.double(0.9), # ptcut previous 0.8
        primaryVertices = cms.InputTag("hltPhase2OfflinePrimaryVertices"),
        tracks = cms.InputTag("hltPhase2GeneralTracks"), ## hltPhase2
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

    process.hltPhase2VertexMerger = cms.EDProducer("VertexMerger",
        maxFraction = cms.double(0.7),
        minSignificance = cms.double(2),
        secondaryVertices = cms.InputTag("hltPhase2InclusiveVertexFinder")
    )

    process.hltPhase2TrackVertexArbitrator = cms.EDProducer("TrackVertexArbitrator",
        beamSpot = cms.InputTag("offlineBeamSpot"),
        dLenFraction = cms.double(0.333),
        dRCut = cms.double(0.4),
        distCut = cms.double(0.04),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3),
        fitterTini = cms.double(256),
        maxTimeSignificance = cms.double(3.5),
        primaryVertices = cms.InputTag("hltPhase2OfflinePrimaryVertices"),
        secondaryVertices = cms.InputTag("hltPhase2VertexMerger"),
        sigCut = cms.double(5),
        trackMinLayers = cms.int32(4),
        trackMinPixels = cms.int32(1),
        trackMinPt = cms.double(0.9), # ptcut previous 0.4
        tracks = cms.InputTag("hltPhase2GeneralTracks") ## hltPhase2
    )
    
    process.hltPhase2InclusiveSecondaryVertices = cms.EDProducer("VertexMerger",
        maxFraction = cms.double(0.2),
        minSignificance = cms.double(10.0),
        secondaryVertices = cms.InputTag("hltPhase2TrackVertexArbitrator")
    )

    ## ----------------------------
    """
    ### OLD MODULES

    process.seedFromProtoTracks = cms.PSet(
        ComponentName = cms.string('SeedFromConsecutiveHitsCreator'),
        MinOneOverPtError = cms.double(1.0),
        OriginTransverseErrorMultiplier = cms.double(1.0),
        SeedMomentumForBOFF = cms.double(5.0),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string(''),
        propagator = cms.string('PropagatorWithMaterial')
    )

    process.pixelTracksSeedLayers = cms.EDProducer("SeedingLayersEDProducer",
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

    process.pixelTrackFilterByKinematics = cms.EDProducer("PixelTrackFilterByKinematicsProducer",
        chi2 = cms.double(1000.0),
        nSigmaInvPtTolerance = cms.double(0.0),
        nSigmaTipMaxTolerance = cms.double(0.0),
        ptMin = cms.double(0.9),
        tipMax = cms.double(1.0)
    )

    process.pixelFitterByHelixProjections = cms.EDProducer("PixelFitterByHelixProjectionsProducer",
        scaleErrorsForBPix1 = cms.bool(False),
        scaleFactor = cms.double(0.65)
    )

    process.pSetPvClusterComparerForIT = cms.PSet(
        track_chi2_max = cms.double(20.0),
        track_prob_min = cms.double(-1.0),
        track_pt_max = cms.double(30.0),
        track_pt_min = cms.double(1.0)
    )

    process.pixelTracksTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4.0),
            originRadius = cms.double(0.02),
            precise = cms.bool(True),
            ptMin = cms.double(0.9)
        )
    )

    process.pixelTracksHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag(""),
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(50000000),
        maxElementTotal = cms.uint32(50000000),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("pixelTracksSeedLayers"),
        trackingRegions = cms.InputTag("pixelTracksTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.pixelTracksHitSeeds = cms.EDProducer("CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double(0.0),
        CAPhiCut = cms.double(0.2),
        CAThetaCut = cms.double(0.0012),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("siPixelClusterShapeCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("pixelTracksHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        fitFastCircle = cms.bool(True),
        fitFastCircleChi2Cut = cms.bool(True),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.7),
            pt2 = cms.double(2.0),
            value1 = cms.double(200.0),
            value2 = cms.double(50.0)
        ),
        mightGet = cms.untracked.vstring('IntermediateHitDoublets_pixelTracksHitDoublets__HLTX'),
        useBendingCorrection = cms.bool(True)
    )

    process.pixelTracks = cms.EDProducer("PixelTrackProducer",
        Cleaner = cms.string('pixelTrackCleanerBySharedHits'),
        Filter = cms.InputTag("pixelTrackFilterByKinematics"),
        Fitter = cms.InputTag("pixelFitterByHelixProjections"),
        SeedingHitSets = cms.InputTag("pixelTracksHitSeeds"),
        mightGet = cms.untracked.vstring('RegionsSeedingHitSets_pixelTracksHitSeeds__HLTX'),
        passLabel = cms.string('pixelTracks')
    )

    process.pixelVertices = cms.EDProducer("PixelVertexProducer",
        Finder = cms.string('DivisiveVertexFinder'),
        Method2 = cms.bool(True),
        NTrkMin = cms.int32(2),
        PVcomparer = cms.PSet(
            refToPSet_ = cms.string('pSetPvClusterComparerForIT')
        ),
        PtMin = cms.double(1.0),
        TrackCollection = cms.InputTag("pixelTracks"),
        UseError = cms.bool(True),
        Verbosity = cms.int32(0),
        WtAverage = cms.bool(True),
        ZOffset = cms.double(5.0),
        ZSeparation = cms.double(0.005),
        beamSpot = cms.InputTag("offlineBeamSpot")
    )

    process.initialStepTrajectoryBuilder = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(False),
        bestHitOnly = cms.bool(True),
        estimator = cms.string('initialStepChi2Est'),
        foundHitBonus = cms.double(10.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('initialStepTrajectoryFilter')
        ),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(True),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(2),
        maxDPhiForLooperReconstruction = cms.double(2.0),
        maxPtForLooperReconstruction = cms.double(0.7),
        minNrOfHitsForRebuild = cms.int32(1),
        propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
        requireSeedHitsInRebuild = cms.bool(True),
        seedAs5DHit = cms.bool(False),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('initialStepTrajectoryFilter')
        ),
        updator = cms.string('KFUpdator'),
        useSameTrajFilter = cms.bool(True)
    )



    process.initialStepChi2Est = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
        ComponentName = cms.string('initialStepChi2Est'),
        MaxChi2 = cms.double(9.0),
        MaxDisplacement = cms.double(0.5),
        MaxSagitta = cms.double(2),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutLoose')
        ),
        nSigma = cms.double(3.0),
        pTChargeCutThreshold = cms.double(15.0)
    )


    process.initialStepTrajectoryFilter = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(0),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(1),
        maxLostHitsFraction = cms.double(999),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(4),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9),
        minimumNumberOfHits = cms.int32(4),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.initialStepSeeds = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
        InputCollection = cms.InputTag("pixelTracks"),
        InputVertexCollection = cms.InputTag(""),
        SeedCreatorPSet = cms.PSet(
            refToPSet_ = cms.string('seedFromProtoTracks')
        ),
        TTRHBuilder = cms.string('WithTrackAngle'),
        originHalfLength = cms.double(0.3),
        originRadius = cms.double(0.1),
        useEventsWithNoVertex = cms.bool(True),
        usePV = cms.bool(False),
        useProtoTrackKinematics = cms.bool(False)
    )

    process.highPtTripletStepTrackingRegions = cms.EDProducer("GlobalTrackingRegionFromBeamSpotEDProducer",
        RegionPSet = cms.PSet(
            beamSpot = cms.InputTag("offlineBeamSpot"),
            nSigmaZ = cms.double(4),
            originHalfLength = cms.double(0),
            originRadius = cms.double(0.02),
            precise = cms.bool(True),
            ptMin = cms.double(0.9),
            useMultipleScattering = cms.bool(False)
        ),
        mightGet = cms.optional.untracked.vstring
    )

    process.highPtTripletStepTrajectoryFilterInOut = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(2.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(999),
        maxLostHitsFraction = cms.double(0.1),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9),
        minimumNumberOfHits = cms.int32(4),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(1),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.highPtTripletStepTrajectoryFilterBase = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(0),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(1),
        maxLostHitsFraction = cms.double(999.0),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9),
        minimumNumberOfHits = cms.int32(3),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(1),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.highPtTripletStepChi2Est = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
        ComponentName = cms.string('highPtTripletStepChi2Est'),
        MaxChi2 = cms.double(16.0),
        MaxDisplacement = cms.double(0.5),
        MaxSagitta = cms.double(2),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('SiStripClusterChargeCutLoose')
        ),
        nSigma = cms.double(3),
        pTChargeCutThreshold = cms.double(-1)
    )

    process.initialStepTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('initialStepTrajectoryBuilder')
        ),
        TrajectoryCleaner = cms.string('TrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(True),
        doSeedingRegionRebuilding = cms.bool(True),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        numHitsForSeedCleaner = cms.int32(50),
        onlyPixelHitsForSeedCleaner = cms.bool(True),
        reverseTrajectories = cms.bool(False),
        src = cms.InputTag("initialStepSeeds"),
        useHitsSplitting = cms.bool(False)
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

    process.initialStepTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("offlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 0.003),
                d0err_par = cms.vdouble(0.001, 0.001, 0.001),
                dr_exp = cms.vint32(4, 4, 4),
                dr_par1 = cms.vdouble(0.8, 0.7, 0.6),
                dr_par2 = cms.vdouble(0.6, 0.5, 0.45)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 4),
                dz_par1 = cms.vdouble(0.9, 0.8, 0.7),
                dz_par2 = cms.vdouble(0.8, 0.7, 0.55)
            ),
            maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
            maxChi2n = cms.vdouble(2.0, 1.4, 1.2),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
            maxLostLayers = cms.vint32(3, 2, 2),
            min3DLayers = cms.vint32(3, 3, 3),
            minLayers = cms.vint32(3, 3, 3),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 3)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("initialStepTracks"),
        vertices = cms.InputTag("pixelVertices")
    )

    process.initialStepTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("initialStepTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("initialStepTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("initialStepTracks")
    )

    process.highPtTripletStepClusters = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(9.0),
        mightGet = cms.optional.untracked.vstring,
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag(""),
        overrideTrkQuals = cms.InputTag(""),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        phase2pixelClusters = cms.InputTag("siPixelClusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("initialStepTrackSelectionHighPurity")
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

    process.firstStepPrimaryVerticesUnsorted = cms.EDProducer("PrimaryVertexProducer",
        TkClusParameters = cms.PSet(
            TkDAClusParameters = cms.PSet(
                Tmin = cms.double(2.0),
                Tpurge = cms.double(2.0),
                Tstop = cms.double(0.5),
                coolingFactor = cms.double(0.6),
                d0CutOff = cms.double(3.0),
                dzCutOff = cms.double(3.0),
                uniquetrkweight = cms.double(0.8),
                vertexSize = cms.double(0.006),
                zmerge = cms.double(0.01)
            ),
            algorithm = cms.string('DA_vect')
        ),
        TkFilterParameters = cms.PSet(
            algorithm = cms.string('filter'),
            maxD0Significance = cms.double(4.0),
            maxEta = cms.double(4.0),
            maxNormalizedChi2 = cms.double(10.0),
            minPixelLayersWithHits = cms.int32(2),
            minPt = cms.double(0.9),
            minSiliconLayersWithHits = cms.int32(5),
            trackQuality = cms.string('any')
        ),
        TrackLabel = cms.InputTag("initialStepTracks"),
        beamSpotLabel = cms.InputTag("offlineBeamSpot"),
        verbose = cms.untracked.bool(False),
        vertexCollections = cms.VPSet(cms.PSet(
            algorithm = cms.string('AdaptiveVertexFitter'),
            chi2cutoff = cms.double(2.5),
            label = cms.string(''),
            maxDistanceToBeam = cms.double(1.0),
            minNdof = cms.double(0.0),
            useBeamConstraint = cms.bool(False)
        ))
    )

    process.ak4CaloJetsForTrk = cms.EDProducer("FastjetJetProducer",
        Active_Area_Repeats = cms.int32(1),
        GhostArea = cms.double(0.01),
        Ghost_EtaMax = cms.double(5.0),
        Rho_EtaMax = cms.double(4.4),
        doAreaDiskApprox = cms.bool(False),
        doAreaFastjet = cms.bool(False),
        doPUOffsetCorr = cms.bool(False),
        doPVCorrection = cms.bool(True),
        doRhoFastjet = cms.bool(False),
        inputEMin = cms.double(0.0),
        inputEtMin = cms.double(0.3),
        jetAlgorithm = cms.string('AntiKt'),
        jetPtMin = cms.double(10.0),
        jetType = cms.string('CaloJet'),
        maxBadEcalCells = cms.uint32(9999999),
        maxBadHcalCells = cms.uint32(9999999),
        maxProblematicEcalCells = cms.uint32(9999999),
        maxProblematicHcalCells = cms.uint32(9999999),
        maxRecoveredEcalCells = cms.uint32(9999999),
        maxRecoveredHcalCells = cms.uint32(9999999),
        minSeed = cms.uint32(14327),
        nSigmaPU = cms.double(1.0),
        puPtMin = cms.double(10),
        rParam = cms.double(0.4),
        radiusPU = cms.double(0.5),
        src = cms.InputTag("caloTowerForTrk"),
        srcPVs = cms.InputTag("firstStepPrimaryVerticesUnsorted"),
        useDeterministicSeed = cms.bool(True),
        voronoiRfact = cms.double(-0.9)
    )

    process.highPtTripletStepTrajectoryBuilder = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(False),
        bestHitOnly = cms.bool(True),
        estimator = cms.string('highPtTripletStepChi2Est'),
        foundHitBonus = cms.double(10.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('highPtTripletStepTrajectoryFilterInOut')
        ),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(False),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(2),
        maxDPhiForLooperReconstruction = cms.double(2.0),
        maxPtForLooperReconstruction = cms.double(0.7),
        minNrOfHitsForRebuild = cms.int32(5),
        propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
        requireSeedHitsInRebuild = cms.bool(True),
        seedAs5DHit = cms.bool(False),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('highPtTripletStepTrajectoryFilter')
        ),
        updator = cms.string('KFUpdator'),
        useSameTrajFilter = cms.bool(False)
    )

    process.highPtTripletStepTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('highPtTripletStepTrajectoryBuilder')
        ),
        TrajectoryCleaner = cms.string('highPtTripletStepTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(True),
        doSeedingRegionRebuilding = cms.bool(True),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        numHitsForSeedCleaner = cms.int32(50),
        onlyPixelHitsForSeedCleaner = cms.bool(True),
        phase2clustersToSkip = cms.InputTag("highPtTripletStepClusters"),
        reverseTrajectories = cms.bool(False),
        src = cms.InputTag("highPtTripletStepSeeds"),
        useHitsSplitting = cms.bool(False)
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

    process.highPtTripletStepTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("offlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 0.003),
                d0err_par = cms.vdouble(0.002, 0.002, 0.001),
                dr_exp = cms.vint32(4, 4, 4),
                dr_par1 = cms.vdouble(0.7, 0.6, 0.6),
                dr_par2 = cms.vdouble(0.6, 0.5, 0.45)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 4),
                dz_par1 = cms.vdouble(0.8, 0.7, 0.7),
                dz_par2 = cms.vdouble(0.6, 0.6, 0.55)
            ),
            maxChi2 = cms.vdouble(9999.0, 9999.0, 9999.0),
            maxChi2n = cms.vdouble(2.0, 1.0, 0.8),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
            maxLostLayers = cms.vint32(3, 3, 2),
            min3DLayers = cms.vint32(3, 3, 4),
            minLayers = cms.vint32(3, 3, 4),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 3)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("highPtTripletStepTracks"),
        vertices = cms.InputTag("pixelVertices")
    )

    process.highPtTripletStepTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("highPtTripletStepTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("highPtTripletStepTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("highPtTripletStepTracks")
    )

    process.generalTracks = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(5.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.9),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag("initialStepTrackSelectionHighPurity", "highPtTripletStepTrackSelectionHighPurity"),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        makeReKeyedSeeds = cms.untracked.bool(False),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag(cms.InputTag("initialStepTrackSelectionHighPurity"), cms.InputTag("highPtTripletStepTrackSelectionHighPurity")),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(True),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('trackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    process.unsortedOfflinePrimaryVertices = cms.EDProducer("PrimaryVertexProducer",
        TkClusParameters = cms.PSet(
            TkDAClusParameters = cms.PSet(
                Tmin = cms.double(2.0),
                Tpurge = cms.double(2.0),
                Tstop = cms.double(0.5),
                coolingFactor = cms.double(0.6),
                d0CutOff = cms.double(3.0),
                dzCutOff = cms.double(3.0),
                uniquetrkweight = cms.double(0.8),
                vertexSize = cms.double(0.006),
                zmerge = cms.double(0.01)
            ),
            algorithm = cms.string('DA_vect')
        ),
        TkFilterParameters = cms.PSet(
            algorithm = cms.string('filter'),
            maxD0Significance = cms.double(4.0),
            maxEta = cms.double(4.0),
            maxNormalizedChi2 = cms.double(10.0),
            minPixelLayersWithHits = cms.int32(2),
            minPt = cms.double(0.9),
            minSiliconLayersWithHits = cms.int32(5),
            trackQuality = cms.string('any')
        ),
        TrackLabel = cms.InputTag("generalTracks"),
        beamSpotLabel = cms.InputTag("offlineBeamSpot"),
        verbose = cms.untracked.bool(False),
        vertexCollections = cms.VPSet(
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string(''),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(0.0),
                useBeamConstraint = cms.bool(False)
            ),
            cms.PSet(
                algorithm = cms.string('AdaptiveVertexFitter'),
                chi2cutoff = cms.double(2.5),
                label = cms.string('WithBS'),
                maxDistanceToBeam = cms.double(1.0),
                minNdof = cms.double(2.0),
                useBeamConstraint = cms.bool(True)
            )
        )
    )

    process.trackWithVertexRefSelectorBeforeSorting = cms.EDProducer("TrackWithVertexRefSelector",
        copyExtras = cms.untracked.bool(False),
        copyTrajectories = cms.untracked.bool(False),
        d0Max = cms.double(999.0),
        dzMax = cms.double(999.0),
        etaMax = cms.double(5.0),
        etaMin = cms.double(0.0),
        nSigmaDtVertex = cms.double(0),
        nVertices = cms.uint32(0),
        normalizedChi2 = cms.double(999999.0),
        numberOfLostHits = cms.uint32(999),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(0),
        ptErrorCut = cms.double(9e+99),
        ptMax = cms.double(9e+99),
        ptMin = cms.double(0.9),
        quality = cms.string('highPurity'),
        rhoVtx = cms.double(0.2),
        src = cms.InputTag("generalTracks"),
        timeResosTag = cms.InputTag(""),
        timesTag = cms.InputTag(""),
        useVtx = cms.bool(True),
        vertexTag = cms.InputTag("unsortedOfflinePrimaryVertices"),
        vtxFallback = cms.bool(True),
        zetaVtx = cms.double(1.0)
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
        minPt = cms.double(0.9),
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
        trackMinPt = cms.double(0.9),
        tracks = cms.InputTag("generalTracks")
    )
    """

    ###
    ### Sequences
    ###

    """ old sequences
    process.itLocalReco = cms.Sequence(
        process.siPhase2Clusters
      + process.siPixelClusters
      + process.siPixelClusterShapeCache
      + process.siPixelRecHits
    )

    process.otLocalReco = cms.Sequence(
        process.MeasurementTrackerEvent
    )

    process.pixelTracksSequence = cms.Sequence(
        process.pixelTrackFilterByKinematics
      + process.pixelFitterByHelixProjections
      + process.pixelTracksTrackingRegions
      + process.pixelTracksSeedLayers
      + process.pixelTracksHitDoublets
      + process.pixelTracksHitSeeds
      + process.pixelTracks
    )

    process.pixelVerticesSequence = cms.Sequence(
        process.pixelVertices
    )

    process.initialStepSequence = cms.Sequence(process.initialStepSeeds
      + process.initialStepTrackCandidates
      + process.initialStepTracks
      + process.initialStepTrackCutClassifier
      + process.initialStepTrackSelectionHighPurity
    )

    process.highPtTripletStepSeeding = cms.Sequence(
        process.highPtTripletStepClusters
      + process.highPtTripletStepSeedLayers
      + process.highPtTripletStepTrackingRegions
      + process.highPtTripletStepHitDoublets
      + process.highPtTripletStepHitTriplets
      + process.highPtTripletStepSeeds
    )

    process.highPtTripletStepSequence = cms.Sequence(
        process.highPtTripletStepSeeding
      + process.highPtTripletStepTrackCandidates
      + process.highPtTripletStepTracks
      + process.highPtTripletStepTrackCutClassifier
      + process.highPtTripletStepTrackSelectionHighPurity
    )

    process.initialStepPVSequence = cms.Sequence(
        process.firstStepPrimaryVerticesUnsorted
      + process.initialStepTrackRefsForJets
      + process.caloTowerForTrk
      + process.ak4CaloJetsForTrk
      + process.firstStepPrimaryVertices
    )

    process.vertexReco = cms.Sequence(
        process.initialStepPVSequence
      + process.ak4CaloJetsForTrk
      + process.unsortedOfflinePrimaryVertices
      + process.trackWithVertexRefSelectorBeforeSorting
      + process.trackRefsForJetsBeforeSorting
      + process.offlinePrimaryVertices
      + process.offlinePrimaryVerticesWithBS
      + process.inclusiveVertexFinder
      + process.vertexMerger
      + process.trackVertexArbitrator
      + process.inclusiveSecondaryVertices
    )
    
    process.globalreco_tracking = cms.Sequence(
        process.offlineBeamSpot
      + process.itLocalReco
      + process.otLocalReco
      + process.trackerClusterCheck
      + process.pixelTracksSequence
      + process.pixelVerticesSequence
      + process.initialStepSequence
      + process.highPtTripletStepSequence
      + process.generalTracks
      + process.vertexReco
    )
    """
    #process.offlineBeamSpot = cms.EDProducer("BeamSpotProducer")
    
    ### new sequences

    process.itLocalReco = cms.Sequence( #
        process.siPhase2Clusters 
      + process.siPixelClusters
      + process.siPixelClusterShapeCache
      + process.siPixelRecHits
    )

    process.trackerGeoTask = cms.Task(process.TrackerRecoGeometryESProducer)
    process.trackerGeo = cms.Sequence(process.trackerGeoTask)

    process.trackerMeaTask = cms.Task(process.MeasurementTracker)
    process.trackerMea = cms.Sequence(process.trackerMeaTask)

    

    process.otLocalReco = cms.Sequence( #
        process.trackerGeo
      + process.trackerMea
      + process.MeasurementTrackerEvent
    )

    process.hltPhase2StartUp = cms.Sequence( #
        process.offlineBeamSpot 
      + process.itLocalReco
      + process.otLocalReco
      + process.trackerClusterCheck 
      + process.caloTowerForTrk 
    )

    #process.hltPhase2PixelTracksSequence = cms.Sequence( #
    #    process.vertexFromL1
    #  + process.pixelVertexCoordinates
    #  + process.hltPhase2PixelTrackSoA
    #  + process.hltPhase2PixelTracks
    #)
    process.hltPhase2PixelTracksSequence = cms.Sequence(
         process.hltPhase2PixelTrackFilterByKinematics
       + process.hltPhase2PixelFitterByHelixProjections 
       + process.hltPhase2PixelTracksTrackingRegions
       + process.hltPhase2PixelTracksSeedLayers
       + process.hltPhase2PixelTracksHitDoublets
       + process.hltPhase2PixelTracksHitSeeds
       + process.hltPhase2PixelTracks
       + process.hltPhase2PixelTripletsSelector
       + process.hltPhase2PixelQuadrupletsSelector 
       + process.hltPhase2PixelTracksClean 
    )
    
    process.hltPhase2PixelVerticesSequence = cms.Sequence( 
        process.hltPhase2PixelVertices
      #+ process.hltPhase2TrimmedPixelVertices
      + process.hltPhase2PixelTracksCleaner
      + process.hltPhase2PixelTripletsCleaner
      + process.hltPhase2PixelTripletsSelector
      + process.hltPhase2PixelQuadrupletsSelector
      + process.hltPhase2PixelTracksMerger
    )
    
    process.hltPhase2InitialStepSequence = cms.Sequence( 
        process.hltPhase2InitialStepSeeds
      + process.hltPhase2InitialStepTrackCandidates
      + process.hltPhase2InitialStepTracks
      + process.hltPhase2InitialStepTrackCutClassifier
      + process.hltPhase2InitialStepTracksSelectionHighPurity
    )

    process.hltPhase2HighPtTripletStepSequence = cms.Sequence(
        process.hltPhase2HighPtTripletStepClusters
      + process.hltPhase2HighPtTripletStepSeedLayers
      + process.hltPhase2HighPtTripletStepTrackingRegions
      + process.hltPhase2HighPtTripletStepHitDoublets
      + process.hltPhase2HighPtTripletStepHitTriplets
      + process.hltPhase2HighPtTripletStepSeeds
      + process.hltPhase2HighPtTripletStepTrackCandidates
      + process.hltPhase2HighPtTripletStepTracks
      + process.hltPhase2HighPtTripletStepTrackCutClassifier
      + process.hltPhase2HighPtTripletStepTracksSelectionHighPurity
    )
    
    process.vertexReco = cms.Sequence(
        process.hltPhase2UnsortedOfflinePrimaryVertices
      + process.hltPhase2TrackWithVertexRefSelectorBeforeSorting
      + process.hltPhase2TrackRefsForJetsBeforeSorting
      + process.hltPhase2Ak4CaloJetsForTrk
      + process.hltPhase2OfflinePrimaryVertices
      + process.hltPhase2OfflinePrimaryVerticesWithBS
      + process.hltPhase2InclusiveVertexFinder
      + process.hltPhase2VertexMerger
      + process.hltPhase2TrackVertexArbitrator
      + process.hltPhase2InclusiveSecondaryVertices
    )
    
    ### combined tracking and vertexing
    process.globalreco_tracking = cms.Sequence(
        #### tracking
        process.hltPhase2StartUp
      + process.hltPhase2PixelTracksSequence
      + process.hltPhase2PixelVerticesSequence
      + process.hltPhase2InitialStepSequence
      + process.hltPhase2HighPtTripletStepSequence
      + process.hltPhase2GeneralTracks
      ### vertexing
      + process.vertexReco
    )
    
    """
    ### definitions from configDump for vertexReco -> vertexing and original_v6 -> tracking
    process.vertexReco = cms.Sequence(
        process.hltPhase2UnsortedOfflinePrimaryVertices
      + process.hltPhase2TrackWithVertexRefSelectorBeforeSorting
      + process.hltPhase2TrackRefsForJetsBeforeSorting
      + process.hltPhase2Ak4CaloJetsForTrk
      + process.hltPhase2OfflinePrimaryVertices
      + process.hltPhase2OfflinePrimaryVerticesWithBS
      + process.hltPhase2InclusiveVertexFinder
      + process.hltPhase2VertexMerger
      + process.hltPhase2TrackVertexArbitrator
      + process.hltPhase2InclusiveSecondaryVertices
    )

    process.original_v6 = cms.Path(
        process.hltPhase2StartUp
      + process.hltPhase2PixelTracksSequence
      + process.hltPhase2PixelVerticesSequence
      + process.hltPhase2InitialStepSequence
      + process.hltPhase2HighPtTripletStepSequence
      + process.hltPhase2GeneralTracks
    )
    """
    
    ### changed this bit
    # remove globalreco_trackingTask to avoid any ambiguities
    # with the updated sequence process.globalreco_tracking
    #if hasattr(process, 'globalreco_trackingTask'):
    #   del process.globalreco_trackingTask

    return process
