import FWCore.ParameterSet.Config as cms

def METFilters(process, isData):
    process.METFiltersTask = cms.Task()

    ### Ref: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2
    METFilterNames = [
      'Flag_goodVertices',
      'Flag_globalSuperTightHalo2016Filter',
      'Flag_EcalDeadCellTriggerPrimitiveFilter',
      'Flag_BadPFMuonFilter',
      'Flag_BadPFMuonDzFilter'
      'Flag_hfNoisyHitsFilter',
      'Flag_eeBadScFilter',
      'Flag_ecalBadCalibFilter'
    ]

    baddetEcallist = cms.vuint32(
    [872439604,872422825,872420274,872423218,872423215,872416066,872435036,872439336,
    872420273,872436907,872420147,872439731,872436657,872420397,872439732,872439339,
    872439603,872422436,872439861,872437051,872437052,872420649,872421950,872437185,
    872422564,872421566,872421695,872421955,872421567,872437184,872421951,872421694,
    872437056,872437057,872437313,872438182,872438951,872439990,872439864,872439609,
    872437181,872437182,872437053,872436794,872436667,872436536,872421541,872421413,
    872421414,872421031,872423083,872421439])


    process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter(
      "EcalBadCalibFilter",
      EcalRecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
      ecalMinEt = cms.double(50.),
      baddetEcal = baddetEcallist, 
      taggingMode = cms.bool(True),
      debug = cms.bool(False)
    )

    process.METFiltersTask.add(process.ecalBadCalibReducedMINIAODFilter)

    from JMETriggerAnalysis.NTuplizers.triggerResultsFilter_cfi import triggerResultsFilter
    process.metFilterFlagsFilter = triggerResultsFilter.clone(
      triggerResults = 'TriggerResults::'+('RECO' if isData else 'PAT'),
      pathNames = METFilterNames,
      ignoreIfMissing = False,
      useLogicalAND = True,
    )

    process.METFiltersTask.add(process.metFilterFlagsFilter)

    process.METFiltersSeq = cms.Sequence(process.METFiltersTask)

    return process
