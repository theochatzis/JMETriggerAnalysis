import FWCore.ParameterSet.Config as cms

# taken from https://fwyzard.web.cern.ch/fwyzard/customizeHLTforOption0.py
# (credits: A. Bocci, M. Masciovecchio)

def customise_hltTRK_singleIteration(process):
  # select the pixel tracks around the trimmed pixel vertices
  from CommonTools.RecoAlgos.TrackWithVertexSelector_cfi import trackWithVertexSelector as _trackWithVertexSelector 
  process.hltPixelTracksClean = _trackWithVertexSelector.clone(
    src = "hltPixelTracks",                 # track collection
    ptMin = 0.0,                            # kinematic cuts  (pT in GeV)
    ptMax = 999999.0,
    ptErrorCut = 999999.0,                  # relative pT error
    quality = "any",                        # quality cut as defined in reco::TrackBase
    vertexTag = "hltTrimmedPixelVertices",  # compatibility with a vertex collection
    nVertices = 100,
    rhoVtx = 0.1,
    zetaVtx = 0.3,
    copyExtras = True,                      # copy also extras and rechits
    copyTrajectories = False                # do not copy the trajectories
  )

  from HLTrigger.Configuration.common import insert_modules_before
  insert_modules_before(process, process.hltIter0PFLowPixelSeedsFromPixelTracks, process.hltPixelTracksClean)

  # update parameters of the Iter0 seed generator
  process.hltIter0PFLowPixelSeedsFromPixelTracks.InputCollection = "hltPixelTracksClean"
  process.hltIter0PFLowPixelSeedsFromPixelTracks.includeFourthHit = True

  # update the parameters of the Iter0 trajectory builder
  process.HLTIter0PSetTrajectoryFilterIT.minHitsMinPt = 3
  process.HLTIter0PSetTrajectoryFilterIT.minimumNumberOfHits = 3

  # update the parameters of the "high purity" selection
  process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_par1 = (3.40282346639e+38, 0.4, 0.4)
  process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_par2 = (3.40282346639e+38, 0.3, 0.3)
  process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_par1 = (3.40282346639e+38, 0.4, 0.4)
  process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_par2 = (3.40282346639e+38, 0.35, 0.35)
  process.hltIter0PFlowTrackCutClassifier.mva.min3DLayers = (0, 0, 0)
  process.hltIter0PFlowTrackCutClassifier.mva.minLayers = (3, 3, 3)
  process.hltIter0PFlowTrackCutClassifier.mva.minPixelHits = (0, 0, 0)
 
  # replace "hltIter2Merged" and "hltMergedTracks" with "hltIter0PFlowTrackSelectionHighPurity"
  from FWCore.ParameterSet.MassReplace import massReplaceInputTag
  massReplaceInputTag(process, "hltIter2Merged", "hltIter0PFlowTrackSelectionHighPurity")
  del process.hltIter2Merged
  massReplaceInputTag(process, "hltMergedTracks", "hltIter0PFlowTrackSelectionHighPurity")
  del process.hltMergedTracks

  # replace Iter02 with just Iter0
  process.HLTIterativeTrackingIter02 = cms.Sequence(process.HLTIterativeTrackingIteration0)
  del process.HLTIterativeTrackingDoubletRecovery
  del process.HLTIterativeTrackingIteration2
  del process.HLTIter1TrackAndTauJets4Iter2Sequence

  # done
  return process
