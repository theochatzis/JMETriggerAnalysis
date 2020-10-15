import FWCore.ParameterSet.Config as cms

from JMETriggerAnalysis.Common.hltPhase2_L1T import customise_hltPhase2_L1T
from JMETriggerAnalysis.Common.hltPhase2_TRKv00 import customise_hltPhase2_TRKv00
from JMETriggerAnalysis.Common.hltPhase2_TRKv02 import customise_hltPhase2_TRKv02
from JMETriggerAnalysis.Common.hltPhase2_TRKv06 import customise_hltPhase2_TRKv06
from JMETriggerAnalysis.Common.hltPhase2_PF import customise_hltPhase2_PF
from JMETriggerAnalysis.Common.hltPhase2_JME import customise_hltPhase2_JME

from HLTrigger.Configuration.common import producers_by_type

from RecoHGCal.TICL.iterativeTICL_cff import injectTICLintoPF

def customise_hltPhase2_enableTICLInHGCalReconstruction(process):
    if not hasattr(process, 'iterTICLTask'):
       raise RuntimeError('process.iterTICLTask not found')

    # remove modules specific to SIM-assisted reconstruction
    del process.tpClusterProducer
    del process.quickTrackAssociatorByHits
    del process.simPFProducer

    process.iterTICLSequence = cms.Sequence(process.iterTICLTask)
    process.globalreco += process.iterTICLSequence
    process = injectTICLintoPF(process)

    return process

def customise_hltPhase2_disableMTDReconstruction(process):
    for _tmp1 in [
      'fastTimingLocalReco',
      'fastTimingLocalRecoTask',
      'fastTimingGlobalReco',
      'fastTimingGlobalRecoTask',
      'tofPIDSequence',
    ]:
      if hasattr(process, _tmp1):
        for _tmp2 in getattr(process, _tmp1).moduleNames():
          if hasattr(process, _tmp2):
            process.__delattr__(_tmp2)
        process.__delattr__(_tmp1)

    # disable use of timing information in simPFProducer
    if hasattr(process, 'simPFProducer') and hasattr(process.simPFProducer, 'trackTimeValueMap'):
       del process.simPFProducer.trackTimeValueMap

    # remove MTD element from PFBlock inputs
    process.particleFlowBlock.elementImporters = [
      _tmp for _tmp in process.particleFlowBlock.elementImporters if _tmp.importerName != 'TrackTimingImporter'
    ]

    return process

def customise_hltPhase2_redefineReconstructionSequencesCommon(process):
    if not hasattr(process, 'reconstruction'):
       raise RuntimeError('reconstruction sequence process.reconstruction not found')

    # redefine input to fixedGridRhoFastjetAll
    # (in principle, this is not needed, since JESC modules are configured with 'fixedGridRhoFastjetAllTmp';
    #  nevertheless, this modification is applied, in order to make sure _particleFlowCands is consistently used)
    process.fixedGridRhoFastjetAll.pfCandidatesTag = 'particleFlowTmp'

    # redefine process.hgcalLocalReco sequence
    # to disable unnecessary producers in HGCal local reconstruction
    process.hgcalLocalRecoSequence = cms.Sequence(
        process.HGCalUncalibRecHit
      + process.HGCalRecHit
      + process.hgcalLayerClusters
      + process.hgcalMultiClusters
      + process.particleFlowRecHitHGC
      + process.particleFlowClusterHGCal
      + process.particleFlowClusterHGCalFromMultiCl
    )

    process.calolocalreco = cms.Sequence(
        process.ecalLocalRecoSequence
      + process.hcalLocalRecoSequence
      + process.hgcalLocalRecoSequence
    )

    process.localreco = cms.Sequence(
        process.bunchSpacingProducer
      + process.calolocalreco
      + process.muonlocalreco
      + process.trackerlocalreco
      + process.fastTimingLocalReco
    )

    # process.globalreco: reconstruction up to PFClusters
    if (not hasattr(process, 'globalreco_tracking')) and hasattr(process, 'globalreco_trackingTask'):
       process.globalreco_tracking = cms.Sequence(process.globalreco_trackingTask)

    process.tofPIDSequence = cms.Sequence(
        process.unsortedOfflinePrimaryVertices4DnoPID
      + process.tofPID4DnoPID
      + process.unsortedOfflinePrimaryVertices4D
      + process.tofPID
    )

    # remove unnecessary modules related
    # to muon reconstruction
    for _tmp1 in [
      'muIsolationTask',
      'muonSelectionTypeTask',
    ]:
      if hasattr(process, _tmp1):
        for _tmp2 in getattr(process, _tmp1).moduleNames():
          if hasattr(process, _tmp2):
            process.__delattr__(_tmp2)
        process.__delattr__(_tmp1)

    process.globalreco = cms.Sequence(
        process.caloTowersRec
      + process.ecalClusters
#     + process.egammaGlobalReco

        # tracking
      + process.globalreco_tracking
      + process.standalonemuontracking # needs to be included for early muons of PF

        # timing
      + process.fastTimingGlobalReco # necessary for MTD inputs to PF
      + process.tofPIDSequence # contains tofPID maps

        # insert CaloJets sequence in process.globalreco
        # (module muons1stStep from muonGlobalReco requires AK4CaloJets [1])
      + process.hltAK4CaloJets # was: process.jetGlobalReco

      + process.muonGlobalReco
#     + process.muoncosmicreco
      + process.particleFlowCluster
#     + process.pfTrackingGlobalReco
    )

    if hasattr(process, 'hltAK4CaloJets'):
       process.globalreco += process.hltAK4CaloJets
       # modify CaloJets input to muons1stStep
       process.muons1stStep.JetExtractorPSet.JetCollectionLabel = 'hltAK4CaloJets'
    else:
       process.globalreco += process.jetGlobalReco

    process.highlevelreco = cms.Sequence(
        process.particleFlowReco
    )

    process.reconstruction = cms.Sequence(
        process.localreco
      + process.globalreco
      + process.highlevelreco
    )

    return process

def customise_hltPhase2_redefineReconstructionSequences(process, useL1T=False, TRK='v06', useTICL=True, useMTD=False):
    # reset schedule
    process.setSchedule_(cms.Schedule())

    if useL1T:
       process = customise_hltPhase2_L1T(process)

    _trkCustomFuncDict = {
      'v00': customise_hltPhase2_TRKv00,
      'v02': customise_hltPhase2_TRKv02,
      'v06': customise_hltPhase2_TRKv06,
    }
    process = _trkCustomFuncDict[TRK](process)

    process = customise_hltPhase2_PF(process)
    process = customise_hltPhase2_JME(process)
    process = customise_hltPhase2_redefineReconstructionSequencesCommon(process)

    if not useMTD:
       process = customise_hltPhase2_disableMTDReconstruction(process)

    if useTICL:
       process = customise_hltPhase2_enableTICLInHGCalReconstruction(process)

    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process):
    process.HLTJMESequence = cms.Sequence(
        process.HLTCaloMETReconstruction
#     + process.HLTCaloJetsReconstruction
      + process.HLTPFClusterJMEReconstruction
      + process.HLTAK4PFJetsReconstruction
      + process.HLTAK8PFJetsReconstruction
      + process.HLTPFJetsCHSReconstruction
      + process.HLTPFMETsReconstruction
      + process.HLTPFCHSMETReconstruction
      + process.HLTPFSoftKillerMETReconstruction
      + process.HLTPFPuppiJMEReconstruction
    )

    process.reconstruction += process.HLTJMESequence

    process.p = cms.Path(process.RawToDigi + process.reconstruction)

    # schedule
    process.schedule_().append(process.p)

    return process

def customise_hltPhase2_scheduleJMETriggers(process):
    ## sequence: HLT-JME objects (without filters)
    ## (kept for now to study object performance without preselections)
    process.HLTJMESequence = cms.Sequence(
        process.HLTCaloMETReconstruction
#     + process.HLTCaloJetsReconstruction
      + process.HLTPFClusterJMEReconstruction
      + process.HLTAK4PFJetsReconstruction
      + process.HLTAK8PFJetsReconstruction
      + process.HLTPFJetsCHSReconstruction
      + process.HLTPFMETsReconstruction
      + process.HLTPFCHSMETReconstruction
      + process.HLTPFSoftKillerMETReconstruction
      + process.HLTPFPuppiJMEReconstruction
    )

    ## sequence: ParticleFlow
    process.HLTParticleFlowSequence = cms.Sequence(
        process.RawToDigi
      + process.localreco
      + process.globalreco
      + process.highlevelreco
    )

    ## sequence: AK4 Jets, PFCHS
    process.HLTParticleFlowCHSSequence = cms.Sequence(
        process.HLTParticleFlowSequence
      + process.particleFlowPtrs
      + process.goodOfflinePrimaryVertices
      + process.pfPileUpJME
      + process.pfNoPileUpJME
    )

    process.HLTAK4PFCHSJetsReconstruction = cms.Sequence(
        process.hltAK4PFCHSJets
      + process.hltAK4PFCHSJetCorrectorL1
      + process.hltAK4PFCHSJetCorrectorL2
      + process.hltAK4PFCHSJetCorrectorL3
      + process.hltAK4PFCHSJetCorrectorL2L3
      + process.hltAK4PFCHSJetCorrector
      + process.hltAK4PFCHSJetsCorrected
    )

#    ## sequence: AK8 Jets, PFCHS
#    process.HLTAK8PFCHSJetsReconstruction = cms.Sequence(
#        process.hltAK8PFCHSJets
#      + process.hltAK8PFCHSJetCorrectorL1
#      + process.hltAK8PFCHSJetCorrectorL2
#      + process.hltAK8PFCHSJetCorrectorL3
#      + process.hltAK8PFCHSJetCorrectorL2L3
#      + process.hltAK8PFCHSJetCorrector
#      + process.hltAK8PFCHSJetsCorrected
#    )

    ## sequence: AK4 Jets, PFPuppi
    process.HLTAK4PFPuppiJetsReconstruction = cms.Sequence(
        process.goodOfflinePrimaryVertices
      + process.hltPFPuppi
      + process.hltAK4PFPuppiJets
      + process.hltAK4PFPuppiJetCorrectorL1
      + process.hltAK4PFPuppiJetCorrectorL2
      + process.hltAK4PFPuppiJetCorrectorL3
      + process.hltAK4PFPuppiJetCorrectorL2L3
      + process.hltAK4PFPuppiJetCorrector
      + process.hltAK4PFPuppiJetsCorrected
    )

#    ## sequence: AK8 Jets, PFPuppi
#    process.HLTAK8PFPuppiJetsReconstruction = cms.Sequence(
#        process.goodOfflinePrimaryVertices
#      + process.hltPFPuppi
#      + process.hltAK8PFPuppiJets
#      + process.hltAK8PFPuppiJetCorrectorL2
#      + process.hltAK8PFPuppiJetCorrectorL3
#      + process.hltAK8PFPuppiJetCorrectorL2L3
#      + process.hltAK8PFPuppiJetCorrector
#      + process.hltAK8PFPuppiJetsCorrected
#    )

    ## sequence: PFPuppi MET (Raw)
    process.HLTPFPuppiMETReconstruction = cms.Sequence(
        process.goodOfflinePrimaryVertices
      + process.hltPFPuppiNoLep
      + process.hltPFPuppiMET
    )

    ## Single-Jet producers+filters
    _l1tSinglePFJet100 = cms.EDFilter('HLTLevel1PFJet',
      MaxEta = cms.double(5.0),
      MaxMass = cms.double(-1.0),
      MinE = cms.double(-1.0),
      MinEta = cms.double(-1.0),
      MinMass = cms.double(-1.0),
      MinN = cms.int32(1),
      MinPt = cms.double(100.0),
      inputTag = cms.InputTag(''),
      saveTags = cms.bool(True),
      triggerType = cms.int32(-114),
    )

    _hltSinglePFJet100 = cms.EDFilter('HLT1PFJet',
      MaxEta = cms.double(5.0),
      MaxMass = cms.double(-1.0),
      MinE = cms.double(-1.0),
      MinEta = cms.double(-1.0),
      MinMass = cms.double(-1.0),
      MinN = cms.int32(1),
      MinPt = cms.double(100.0),
      inputTag = cms.InputTag(''),
      saveTags = cms.bool(True),
      triggerType = cms.int32(85),
    )

    process.l1tSingleAK4PFPuppiJet130 = _l1tSinglePFJet100.clone(inputTag = 'ak4PFL1PuppiCorrected', MinPt = 130.)

    process.hltSingleAK4PFJet550 = _hltSinglePFJet100.clone(inputTag = 'hltAK4PFJetsCorrected', MinPt = 550.)
    process.hltSingleAK4PFCHSJet550 = _hltSinglePFJet100.clone(inputTag = 'hltAK4PFCHSJetsCorrected', MinPt = 550.)
    process.hltSingleAK4PFPuppiJet550 = _hltSinglePFJet100.clone(inputTag = 'hltAK4PFPuppiJetsCorrected', MinPt = 550.)

    ## HT/MHT producers+filters
    _hltHtMht = cms.EDProducer('HLTHtMhtProducer',
      excludePFMuons = cms.bool(False),
      jetsLabel = cms.InputTag(''),
      maxEtaJetHt = cms.double(2.4),
      maxEtaJetMht = cms.double(999.0),
      minNJetHt = cms.int32(0),
      minNJetMht = cms.int32(0),
      minPtJetHt = cms.double(30.0),
      minPtJetMht = cms.double(0.0),
      pfCandidatesLabel = cms.InputTag(''),
      usePt = cms.bool(True)
    )

    _hltHT100 = cms.EDFilter('HLTHtMhtFilter',
      htLabels = cms.VInputTag(''),
      meffSlope = cms.vdouble(1.0),
      mhtLabels = cms.VInputTag(''),
      minHt = cms.vdouble(100.0),
      minMeff = cms.vdouble(0.0),
      minMht = cms.vdouble(0.0),
      saveTags = cms.bool(True)
    )

    _hltMHT100 = cms.EDFilter('HLTMhtFilter',
      mhtLabels = cms.VInputTag(''),
      minMht = cms.vdouble(100.0),
      saveTags = cms.bool(True)
    )

    # L1T-HT
    process.l1tHtMhtPFPuppiJetPt30Eta2p4 = _hltHtMht.clone(jetsLabel = 'ak4PFL1PuppiCorrected', maxEtaJetHt = 2.4, minPtJetHt = 30., maxEtaJetMht = 2.4, minPtJetMht = 30.)
    process.l1tPFPuppiHT440 = _hltHT100.clone(htLabels = ['l1tHtMhtPFPuppiJetPt30Eta2p4'], mhtLabels = ['l1tHtMhtPFPuppiJetPt30Eta2p4'], minHt = [440.])

    # HLT-HT
    process.hltHtMhtPFPuppiJetPt30Eta4 = _hltHtMht.clone(jetsLabel = 'hltAK4PFPuppiJetsCorrected', maxEtaJetHt = 4.0, minPtJetHt = 30., maxEtaJetMht = 4.0, minPtJetMht = 30.)
    process.hltPFPuppiHT60 = _hltHT100.clone(htLabels = ['hltHtMhtPFPuppiJetPt30Eta4'], mhtLabels = ['hltHtMhtPFPuppiJetPt30Eta4'], minHt = [60.])
    process.hltPFPuppiHT1050 = _hltHT100.clone(htLabels = ['hltHtMhtPFPuppiJetPt30Eta4'], mhtLabels = ['hltHtMhtPFPuppiJetPt30Eta4'], minHt = [1050.])

    # HLT-MHT
    process.hltHtMhtPFPuppiJetPt30Eta5 = _hltHtMht.clone(jetsLabel = 'hltAK4PFPuppiJetsCorrected', maxEtaJetHt = 5.0, minPtJetHt = 30., maxEtaJetMht = 5.0, minPtJetMht = 30., usePt = False)
    process.hltPFPuppiMHT120 = _hltMHT100.clone(mhtLabels = ['hltHtMhtPFPuppiJetPt30Eta5'], minMht = [120.])

    ## MET producers+filters
    _hltPFMET200 = cms.EDFilter('HLT1PFMET',
      MaxEta = cms.double(-1.0),
      MaxMass = cms.double(-1.0),
      MinE = cms.double(-1.0),
      MinEta = cms.double(-1.0),
      MinMass = cms.double(-1.0),
      MinN = cms.int32(1),
      MinPt = cms.double(200.0),
      inputTag = cms.InputTag(''),
      saveTags = cms.bool(True),
      triggerType = cms.int32(87),
    )

    process.l1tPFPuppiMET100 = _hltPFMET200.clone(inputTag = 'l1PFMetPuppi', MinPt = 100.)

    process.hltPFMET250 = _hltPFMET200.clone(inputTag = 'hltPFMET', MinPt = 250.)
    process.hltPFCHSMET250 = _hltPFMET200.clone(inputTag = 'hltPFCHSMET', MinPt = 250.)
    process.hltPFPuppiMET250 = _hltPFMET200.clone(inputTag = 'hltPFPuppiMET', MinPt = 250.)

    process.hltPFPuppiMET120 = _hltPFMET200.clone(inputTag = 'hltPFPuppiMET', MinPt = 120.)

    ## Trigger Paths
    process.MC_JME_v1 = cms.Path(
        process.HLTParticleFlowSequence
      + process.HLTJMESequence
    )

    process.L1T_AK4PFPuppiJet130_v1 = cms.Path(
      process.l1tSingleAK4PFPuppiJet130
    )

    process.HLT_AK4PFJet550_v1 = cms.Path(
        process.l1tSingleAK4PFPuppiJet130
      + process.HLTParticleFlowSequence
      + process.HLTAK4PFJetsReconstruction
      + process.hltSingleAK4PFJet550
    )

    process.HLT_AK4PFCHSJet550_v1 = cms.Path(
        process.l1tSingleAK4PFPuppiJet130
      + process.HLTParticleFlowCHSSequence
      + process.HLTAK4PFCHSJetsReconstruction
      + process.hltSingleAK4PFCHSJet550
    )

    process.HLT_AK4PFPuppiJet550_v1 = cms.Path(
        process.l1tSingleAK4PFPuppiJet130
      + process.HLTParticleFlowSequence
      + process.HLTAK4PFPuppiJetsReconstruction
      + process.hltSingleAK4PFPuppiJet550
    )

    process.L1T_PFPuppiHT440_v1 = cms.Path(
        process.l1tHtMhtPFPuppiJetPt30Eta2p4
      + process.l1tPFPuppiHT440
    )

    process.HLT_PFPuppiHT1050_v1 = cms.Path(
        process.l1tHtMhtPFPuppiJetPt30Eta2p4
      + process.l1tPFPuppiHT440
      + process.HLTParticleFlowSequence
      + process.HLTAK4PFPuppiJetsReconstruction
      + process.hltHtMhtPFPuppiJetPt30Eta4
      + process.hltPFPuppiHT1050
    )

    process.L1T_PFPuppiMET100_v1 = cms.Path(
      process.l1tPFPuppiMET100
    )

    process.HLT_PFMET250_v1 = cms.Path(
        process.l1tPFPuppiMET100
      + process.HLTParticleFlowSequence
      + process.hltPFMET
      + process.hltPFMET250
    )

    process.HLT_PFCHSMET250_v1 = cms.Path(
        process.l1tPFPuppiMET100
      + process.HLTParticleFlowCHSSequence
      + process.HLTPFCHSMETReconstruction
      + process.hltPFCHSMET250
    )

    process.HLT_PFPuppiMET250_v1 = cms.Path(
        process.l1tPFPuppiMET100
      + process.HLTParticleFlowSequence
      + process.HLTPFPuppiMETReconstruction
      + process.hltPFPuppiMET250
    )

    process.HLT_PFPuppiMET120_v1 = cms.Path(
        process.l1tPFPuppiMET100
      + process.HLTParticleFlowSequence
      + process.HLTPFPuppiMETReconstruction
      + process.hltPFPuppiMET120
    )

    process.HLT_PFPuppiMET120_PFPuppiMHT120_v1 = cms.Path(
        process.l1tPFPuppiMET100
      + process.HLTParticleFlowSequence
      + process.HLTPFPuppiMETReconstruction
      + process.hltPFPuppiMET120
      + process.HLTAK4PFPuppiJetsReconstruction
      + process.hltHtMhtPFPuppiJetPt30Eta5
      + process.hltPFPuppiMHT120
    )

    process.HLT_PFPuppiMET120_PFPuppiMHT120_PFPuppiHT60_v1 = cms.Path(
        process.l1tPFPuppiMET100
      + process.HLTParticleFlowSequence
      + process.HLTPFPuppiMETReconstruction
      + process.hltPFPuppiMET120
      + process.HLTAK4PFPuppiJetsReconstruction
      + process.hltHtMhtPFPuppiJetPt30Eta5
      + process.hltPFPuppiMHT120
      + process.hltHtMhtPFPuppiJetPt30Eta4
      + process.hltPFPuppiHT60
    )

    # schedule
    process.schedule_().extend([
      process.MC_JME_v1,

#      process.L1T_AK4PFPuppiJet130_v1,
#      process.HLT_AK4PFJet550_v1,
#      process.HLT_AK4PFCHSJet550_v1,
#      process.HLT_AK4PFPuppiJet550_v1,
#
#      process.L1T_PFPuppiHT440_v1,
#      process.HLT_PFPuppiHT1050_v1,
#
#      process.L1T_PFPuppiMET100_v1,
#      process.HLT_PFMET250_v1,
#      process.HLT_PFCHSMET250_v1,
#      process.HLT_PFPuppiMET250_v1,
#
#      process.HLT_PFPuppiMET120_v1,
#      process.HLT_PFPuppiMET120_PFPuppiMHT120_v1,
#      process.HLT_PFPuppiMET120_PFPuppiMHT120_PFPuppiHT60_v1,
    ])

    return process

# retuning of Puppi parameters for TRK-v06
def customise_hltPhase2_retunePuppiForTRKv06(process):
    for mod_i in producers_by_type(process, 'PuppiProducer'):
       for algo_idx in range(len(mod_i.algos)):
         if len(mod_i.algos[algo_idx].MinNeutralPt) != len(mod_i.algos[algo_idx].MinNeutralPtSlope):
            raise RuntimeError('instance of PuppiProducer is misconfigured:\n\n'+str(mod_i)+' = '+mod_i.dumpPython())
         for algoReg_idx in range(len(mod_i.algos[algo_idx].MinNeutralPt)):
            mod_i.algos[algo_idx].MinNeutralPt[algoReg_idx] += 18.5 * mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx]
            mod_i.algos[algo_idx].MinNeutralPtSlope[algoReg_idx] *= 1.45

    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv00(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=False)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv00_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=True)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv02(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=False)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv02_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=True)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv06(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=False)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process

def customise_hltPhase2_scheduleHLTJMERecoWithoutFilters_TRKv06_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=True)
    process = customise_hltPhase2_scheduleHLTJMERecoWithoutFilters(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv00(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=False)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv00_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v00', useTICL=True)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv02(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=False)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv02_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v02', useTICL=True)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv06(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=False)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process

def customise_hltPhase2_scheduleJMETriggers_TRKv06_TICL(process):
    process = customise_hltPhase2_redefineReconstructionSequences(process, TRK='v06', useTICL=True)
    process = customise_hltPhase2_scheduleJMETriggers(process)
    process = customise_hltPhase2_retunePuppiForTRKv06(process)
    return process
