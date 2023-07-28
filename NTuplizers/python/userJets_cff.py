import FWCore.ParameterSet.Config as cms

def userJets(process):
    # task
    process.userJetsTask = cms.Task()

    # Update the jet collection:
    # This applies JESCs from the given Global-Tag. 
    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

    updateJetCollection(process, postfix = 'AK04PUPPI',
      jetSource = cms.InputTag('slimmedJetsPuppi'),
      pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
      jetCorrections = ('AK4PFPuppi', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'], 'None'),
    )
    process.userJetsTask.add(process.patAlgosToolsTask)
    process.userJetsTask.add(process.selectedUpdatedPatJetsAK04PUPPI)
    _lastJetCollection = 'selectedUpdatedPatJetsAK04PUPPI'

    ### jet selection: make PF-Jet ID maps with the collection we have
    from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector

    process.selectedJetsValueMapPFJetIDTightLepVeto = cms.EDProducer('PatJetIDValueMapProducer',
      src = cms.InputTag(_lastJetCollection),
      filterParams = cms.PSet(
        version = cms.string('RUN3WINTER22PUPPI'), # if you give a wrong option it will show you available options
        quality = cms.string('TIGHTLEPVETO')
      )
    )

    process.selectedJetsValueMapPFJetIDLoose = process.selectedJetsValueMapPFJetIDTightLepVeto.clone()
    process.selectedJetsValueMapPFJetIDLoose.filterParams.quality = 'LOOSE'

    process.selectedJetsValueMapPFJetIDTight = process.selectedJetsValueMapPFJetIDTightLepVeto.clone()
    process.selectedJetsValueMapPFJetIDTight.filterParams.quality = 'TIGHT'

    process.userJetsTask.add(process.selectedJetsValueMapPFJetIDLoose)
    process.userJetsTask.add(process.selectedJetsValueMapPFJetIDTight)
    process.userJetsTask.add(process.selectedJetsValueMapPFJetIDTightLepVeto)
    
    # add label maps data in collection
    process.selectedUpdatedPatJetsAK04PUPPIUserData = cms.EDProducer('PATJetUserDataEmbedder',
      src = cms.InputTag(_lastJetCollection),
      userInts = cms.PSet(
        PFJetIDLoose = cms.InputTag('selectedJetsValueMapPFJetIDLoose'),
        PFJetIDTight = cms.InputTag('selectedJetsValueMapPFJetIDTight'),
        PFJetIDTightLepVeto = cms.InputTag('selectedJetsValueMapPFJetIDTightLepVeto'),
      ),
    )

    process.userJetsTask.add(process.selectedUpdatedPatJetsAK04PUPPIUserData)
    _lastJetCollection = 'selectedUpdatedPatJetsAK04PUPPIUserData'


    ### jet selection: kinematic cuts (pT, eta)
    from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets
    process.selectedJets = selectedPatJets.clone(
      src = _lastJetCollection,
      cut = '(pt > 30.) && (abs(eta) < 5.0)',
    )

    process.userJetsTask.add(process.selectedJets)
    _lastJetCollection = 'selectedJets'

    process.userJetsSeq = cms.Sequence(process.userJetsTask)

    return process, _lastJetCollection
