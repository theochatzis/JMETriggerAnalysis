import FWCore.ParameterSet.Config as cms

def customize_hltPhase2_skimmedTracks(process):

    ###
    ### redefine GeneralTracks, selecting a subset of tracks associated to N pixel vertices
    ###  - each track is associated to the pixel vertex which is closest to it in Z
    ###  - the track is retained only if the associated pixel vertex is one of the first N of the vertex collection (ranking is based on sum-pT2)
    ###

    # check if reconstruction sequence exists
    if not hasattr(process, 'reconstruction'):
       raise RuntimeError('reconstruction sequence process.reconstruction not found')

    # check if globalreco_tracking sequence exists
    if not hasattr(process, 'globalreco_tracking'):
       raise RuntimeError('process has no member named "globalreco_tracking"')

    # check if generalTracks module exists
    if not hasattr(process, 'hltPhase2GeneralTracks'):
       raise RuntimeError('process has no member named "generalTracks"')

    # check if pixelVertices module exists
    if not hasattr(process, 'hltPhase2PixelVertices'):
       raise RuntimeError('process has no member named "pixelVertices"')

    # check if generalTracksOriginal module exists
    if hasattr(process, 'generalTracksOriginal'):
       raise RuntimeError('process already has member named "generalTracksOriginal"')

    # check if hltTrimmedPixelVertices module exists
    if hasattr(process, 'hltTrimmedPixelVertices'):
       raise RuntimeError('process already has member named "hltTrimmedPixelVertices"')

    # clone original collection of generalTracks
    process.generalTracksOriginal = process.generalTracks.clone()

    # re-order (see ranker) and restrict the original list of pixel vertices similarly
    # to what was done at HLT in Run-2 (see hltTrimmedPrimaryVertices in 2018 HLT Menu)
    process.hltTrimmedPixelVertices = cms.EDProducer('PixelVerticesSelector',

      src = cms.InputTag('hltPhase2PixelVertices'),

      minSumPt2 = cms.double( 0.0 ),
      minSumPt2FractionWrtMax = cms.double( 0.3 ),

      # criterion to rank pixel vertices
      # (utilizes PVClusterComparer to compute
      # the vertex SumPtSquared f.o.m. using a sub-set of tracks)
      ranker = cms.PSet(
        track_chi2_max = cms.double( 20.0 ),
        track_pt_max = cms.double( 20.0 ),
        track_prob_min = cms.double( -1.0 ),
        track_pt_min = cms.double( 1.0 )
      ),

      # retain only first N vertices
      maxNVertices = cms.int32( -1 ),
    )

    # updated collection of generalTracks
    #  - redefine the module "generalTracks", so that downstream modules
    #    automatically use this updated collection
    #    (instead of the original "generalTracks" collection)
    #  - new set of generalTracks contains only the input tracks
    #    associated to one of the first N pixel vertices
    process.generalTracks = cms.EDProducer('TracksClosestToFirstVerticesSelector',
      tracks = cms.InputTag('generalTracksOriginal'),
      vertices = cms.InputTag('hltTrimmedPixelVertices'),

      # retain only tracks associated to one of the first N vertices
      maxNVertices = cms.int32( 10 ),

      # track-vertex association: max delta-Z between track and z-closest vertex
      maxDeltaZ = cms.double( 0.2 ),
    )

    # check if generalTracksTask task exists
    if hasattr(process, 'globalreco_trackingTask'):
       # [customization without TRK-v02 applied] insert updated generalTracks into tracking task
       process.globalreco_trackingTask.replace(process.generalTracks, cms.Task(
          process.generalTracksOriginal,
          process.reconstruction_pixelTrackingOnlyTask,
          process.hltTrimmedPixelVertices,
          process.generalTracks,
       ))
       if hasattr(process, 'generalTracksTask'):
          process.generalTracksTask.add(process.generalTracksOriginal, process.hltTrimmedPixelVertices)
    else:
       # [customization on top of TRK-v02] insert updated generalTracks into tracking sequence
       process.globalreco_tracking.replace(process.generalTracks, cms.Sequence(
            process.generalTracksOriginal
          + process.reconstruction_pixelTrackingOnly
          + process.hltTrimmedPixelVertices
          + process.generalTracks
       ))

    return process
