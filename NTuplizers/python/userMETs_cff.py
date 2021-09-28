import FWCore.ParameterSet.Config as cms

def userMETs(process, isData, era):

    ### MET recalculation
    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD

    # https://twiki.cern.ch/twiki/bin/view/CMS/MissingETUncertaintyPrescription#Puppi_MET
    
    process.noMuCands = cms.EDFilter("CandPtrSelector",
                                 src=cms.InputTag("packedPFCandidates"),
                                 cut=cms.string("abs(pdgId)!=13")
                                 )

    makePuppiesFromMiniAOD(process, True)
    if era == '2016':
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,
       )
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,pfCandColl=cms.InputTag("noMuCands"),postfix="noMu",
       )

       process.puppiNoLep.useExistingWeights = True
       process.puppi.useExistingWeights = True
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,postfix="puppi",metType = 'Puppi',jetFlavor = 'AK4PFPuppi',
       )

       process.puppinoMu = process.puppi.clone(
        candName = cms.InputTag('noMuCands')
       )
       process.puppinoMu.useExistingWeights = True
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,pfCandColl=cms.InputTag("puppinoMu"),postfix="puppinoMu",metType = 'Puppi',jetFlavor = 'AK4PFPuppi',
       )
      
    elif era == '2017':

       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = True,
         fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
       )
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = True,pfCandColl=cms.InputTag("noMuCands"),postfix="noMu",
         fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
       )

       process.puppiNoLep.useExistingWeights = False
       process.puppi.useExistingWeights = False
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = True,postfix="puppi",metType = 'Puppi',jetFlavor = 'AK4PFPuppi',
         fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
       )

       process.puppinoMu = process.puppi.clone(
        candName = cms.InputTag('noMuCands')
       )
       process.puppinoMu.useExistingWeights = False
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = True,pfCandColl=cms.InputTag("puppinoMu"),postfix="puppinoMu",metType = 'Puppi',jetFlavor = 'AK4PFPuppi',
         fixEE2017Params = {'userawPt': True, 'ptThreshold': 50.0, 'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
       )
    elif era == '2018':
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,
       )
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,pfCandColl=cms.InputTag("noMuCands"),postfix="noMu",
       )

       process.puppiNoLep.useExistingWeights = False
       process.puppi.useExistingWeights = False
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,postfix="puppi",metType = 'Puppi',jetFlavor = 'AK4PFPuppi',
       )

       process.puppinoMu = process.puppi.clone(
        candName = cms.InputTag('noMuCands')
       )
       process.puppinoMu.useExistingWeights = False
       runMetCorAndUncFromMiniAOD(process, isData = isData,recoMetFromPFCs=True,
         fixEE2017 = False,pfCandColl=cms.InputTag("puppinoMu"),postfix="puppinoMu",metType = 'Puppi',jetFlavor = 'AK4PFPuppi',
       )
    else:
       raise RuntimeError('userMETs_cff.py -- invalid value for "era"OA: '+str(era))

    process.METSeq = cms.Sequence(
      process.noMuCands
      *process.puppiMETSequence
      *process.puppinoMu
      *getattr(process, 'fullPatMetSequence')#process.fullPatMetSequencePuppinoMu,
      *getattr(process, 'fullPatMetSequencenoMu')#process.fullPatMetSequencePuppinoMu,
      *getattr(process, 'fullPatMetSequencepuppi')#process.fullPatMetSequencePuppinoMu,
      *getattr(process, 'fullPatMetSequencepuppinoMu')#process.fullPatMetSequencePuppinoMu,
    )
    return process
