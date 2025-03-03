import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import puppiNoLep as _puppiNoLep
from FWCore.ParameterSet.MassReplace import massReplaceInputTag
from HLTrigger.Configuration.common import producers_by_type

def customise_replacePFMETWithPuppiMETBasedOnPatatrackPixelVertices(process):
    process.hltPuppiNoLep = _puppiNoLep.clone(
      candName = 'hltParticleFlow',
      vertexName = 'hltPixelVertices',
      UseFromPVLooseTight = True,
      vtxNdofCut = 0,
    )

    process.hltPuppiMET = cms.EDProducer('PFMETProducer',
      alias = cms.string(''),
      applyWeight = cms.bool(True),
      calculateSignificance = cms.bool(False),
      globalThreshold = cms.double(0.0),
      parameters = cms.PSet(),
      src = cms.InputTag('hltParticleFlow'),
      srcWeights = cms.InputTag('hltPuppiNoLep')
    )

    process.hltPuppiMETSequence = cms.Sequence(
        process.hltPuppiNoLep
      + process.hltPuppiMET
    )

    process = massReplaceInputTag(process, 'hltPFMETProducer', 'hltPuppiMET')

    for path_i in process.paths_():
        getattr(process, path_i).replace(process.hltPFMETProducer, process.hltPuppiMETSequence)

    # delete PFMET
    del process.hltPFMETProducer

    # retuning of Puppi parameters for HLT inputs
    # tuned on hltPixelVertices with Patatrack Pixel Quadruplets
    _nPVfit_p0, _nPVfit_p1 = 0.9, 1.415
    for mod_i in producers_by_type(process, 'PuppiProducer'):
       for algo_idx in range(len(mod_i.algos)):
          if len(mod_i.algos[algo_idx].MinNeutralPt) != len(mod_i.algos[algo_idx].MinNeutralPtSlope):
             raise RuntimeError('instance of PuppiProducer is misconfigured:\n\n'+str(mod_i)+' = '+mod_i.dumpPython())
          for algoReg_idx in range(len(mod_i.algos[algo_idx].MinNeutralPt)):
             mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] += _nPVfit_p0 * mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx]
             mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] *= _nPVfit_p1

    return process
