import FWCore.ParameterSet.Config as cms

def addJRAPath(process, moduleNamePrefix, genJets, recoJets, maxDeltaR, rho):
    ## reference (genjet) kinematic selection
    refPtEta = cms.EDFilter('EtaPtMinCandViewRefSelector',
      src = cms.InputTag(genJets),
      etaMin = cms.double(-5.5),
      etaMax = cms.double(5.5),
      ptMin = cms.double(1.0)
    )
    setattr(process, moduleNamePrefix + 'GenPtEta', refPtEta)

    ## reco jet kinematic selection
    jetPtEta = cms.EDFilter('EtaPtMinCandViewRefSelector',
      src = cms.InputTag(recoJets),
      etaMin = cms.double(-5.5),
      etaMax = cms.double(5.5),
      ptMin = cms.double(1.0)
    )
    setattr(process, moduleNamePrefix + 'PtEta', jetPtEta)

    ## reference to jet matching
    jetToRef = cms.EDProducer('MatchRecToGen',
      srcGen = cms.InputTag(refPtEta.label()),
      srcRec = cms.InputTag(jetPtEta.label())
    )
    setattr(process, moduleNamePrefix + 'JetToRef', jetToRef)

    ## jet response analyzer
    jra = cms.EDAnalyzer('JetResponseAnalyzer',
      doComposition = cms.bool(True),
      doFlavor = cms.bool(False), # record flavor information
      doRefPt = cms.bool(True),
      doJetPt = cms.bool(True),
      saveCandidates = cms.bool(False),
      deltaRMax = cms.double(maxDeltaR), # deltaR(ref,jet)
      deltaRPartonMax = cms.double(maxDeltaR), # deltaR(ref,parton) (if doFlavor=True)
      nRefMax = cms.uint32(0), # consider all matched references
      doHLT = cms.bool(False), # is the sample an HLT sample (IGNORE THIS)

      srcRefToJetMap = cms.InputTag(jetToRef.label(), 'gen2rec'),
      srcRef = cms.InputTag(refPtEta.label()),
      jecLabel = cms.string(''),
      srcRhos = cms.InputTag(''),
      srcRho = cms.InputTag(rho),
      srcRhoHLT = cms.InputTag(''),
      srcVtx = cms.InputTag('hltPixelVertices'),
      applyVtxCuts = cms.bool(False),
      srcJetToUncorJetMap = cms.InputTag(''),
      srcPFCandidates = cms.InputTag(''),
      srcGenParticles = cms.InputTag('genParticles')
    )
    setattr(process, moduleNamePrefix, jra)

    ## sequence, path, schedule
    sequence = cms.Sequence(refPtEta + jetPtEta + jetToRef + jra)
    setattr(process, moduleNamePrefix + 'Sequence', sequence)
    setattr(process, moduleNamePrefix + 'Path', cms.Path(sequence))

    if process.schedule_() is not None:
      process.schedule_().append(getattr(process, moduleNamePrefix + 'Path'))
