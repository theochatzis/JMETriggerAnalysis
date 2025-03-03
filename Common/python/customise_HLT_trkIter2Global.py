import FWCore.ParameterSet.Config as cms

def customise_HLT_trkIter2Global(process, ptMin=0.9):

    process.hltIter2PFlowPixelTrackingRegions = cms.EDProducer( 'GlobalTrackingRegionWithVerticesEDProducer',
      RegionPSet = cms.PSet( 
        useFixedError = cms.bool( True ),
        nSigmaZ = cms.double( 4.0 ),
        VertexCollection = cms.InputTag( 'hltTrimmedPixelVertices' ),
        beamSpot = cms.InputTag( 'hltOnlineBeamSpot' ),
        useFoundVertices = cms.bool( True ),
        fixedError = cms.double( 0.2 ),
        sigmaZVertex = cms.double( 3.0 ),
        useFakeVertices = cms.bool( False ),
        ptMin = cms.double( ptMin ),
        originRadius = cms.double( 0.05 ),
        precise = cms.bool( True ),
        useMultipleScattering = cms.bool( False )
      )
    )

    return process
