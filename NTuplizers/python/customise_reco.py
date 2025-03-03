import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep

def customise_addPuppiNTupleToRECO(process):
    process.pfPuppi = _puppi.clone()
    process.pfPuppiNoLep = _puppiNoLep.clone()

    process.pfPuppiWithPixVtx = _puppi.clone(
      candName = 'particleFlow',
      vertexName = 'pixelVertices',
      UseFromPVLooseTight = True,
      vtxNdofCut = 0,
    )

    process.pfPuppiNoLepWithPixVtx = _puppiNoLep.clone(
      candName = 'particleFlow',
      vertexName = 'pixelVertices',
      UseFromPVLooseTight = True,
      vtxNdofCut = 0,
    )

    process.puppiSeq = cms.Sequence(
        process.pfPuppi
      + process.pfPuppiNoLep
      + process.pfPuppiWithPixVtx
      + process.pfPuppiNoLepWithPixVtx
    )

    process.puppiPath = cms.Path(
        process.reconstruction_pixelTrackingOnly
      + process.puppiSeq
    )

    process.puppiNTuple = cms.EDAnalyzer('JMETriggerNTuple',
      TTreeName = cms.string('Events'),
      TriggerResults = cms.InputTag('TriggerResults'),
      TriggerResultsFilterOR = cms.vstring(),
      TriggerResultsFilterAND = cms.vstring(),
      TriggerResultsCollections = cms.vstring(),
      outputBranchesToBeDropped = cms.vstring(),
      recoVertexCollections = cms.PSet(
        pixelVertices = cms.InputTag('pixelVertices'),
        offlinePrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
      ),
      recoPFCandidateCollections = cms.PSet(
#       particleFlow = cms.InputTag('particleFlow'),
        puppi = cms.InputTag('pfPuppi'),
        puppiNoLep = cms.InputTag('pfPuppiNoLep'),
        puppiWithPixVtx = cms.InputTag('pfPuppiWithPixVtx'),
        puppiNoLepWithPixVtx = cms.InputTag('pfPuppiNoLepWithPixVtx'),
      )
    )

    process.puppiNTupleEndPath = cms.EndPath(process.puppiNTuple)

    if process.schedule_() is not None:
       process.schedule_().append(process.puppiPath)
       process.schedule_().append(process.puppiNTupleEndPath)

    return process
