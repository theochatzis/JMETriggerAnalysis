###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('lumis', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to .json with list of luminosity sections')

opts.register('logs', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'create log files configured via MessageLogger')

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_TRKv06_TICL',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

opts.register('onlyTriggerResultsInNTuple', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'store only the trigger-results booleans in the output NTuple')

opts.register('trkdqm', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'added monitoring histograms for selected Tracks and Vertices')

opts.register('pfdqm', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'added monitoring histograms for selected PF-Candidates')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.parseArguments()

###
### base configuration file
###

# flag: skim original collection of generalTracks (only tracks associated to first N pixel vertices)
opt_skimTracks = False

opt_reco = opts.reco
if opt_reco.endswith('_skimmedTracks'):
   opt_reco = opt_reco[:-len('_skimmedTracks')]
   opt_skimTracks = True

if   opt_reco == 'HLT_TRKv00':      from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_cfg      import cms, process
elif opt_reco == 'HLT_TRKv00_TICL': from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv00_TICL_cfg import cms, process
elif opt_reco == 'HLT_TRKv02':      from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_cfg      import cms, process
elif opt_reco == 'HLT_TRKv02_TICL': from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv02_TICL_cfg import cms, process
elif opt_reco == 'HLT_TRKv06':      from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_cfg      import cms, process
elif opt_reco == 'HLT_TRKv06_TICL': from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06_TICL_cfg import cms, process
else:
   raise RuntimeError('invalid argument for option "reco": "'+opt_reco+'"')

## JMETrigger NTuple
process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',

  TTreeName = cms.string('Events'),

  TriggerResults = cms.InputTag('TriggerResults'),

  TriggerResultsFilterOR = cms.vstring(),

  TriggerResultsFilterAND = cms.vstring(),

  TriggerResultsCollections = cms.vstring(
    'MC_JME',
    'L1T_AK4PFPuppiJet130',
    'HLT_AK4PFJet550',
    'HLT_AK4PFCHSJet550',
    'HLT_AK4PFPuppiJet550',
    'L1T_PFPuppiHT440',
    'HLT_PFPuppiHT1050',
    'L1T_PFPuppiMET100',
    'HLT_PFMET250',
    'HLT_PFCHSMET250',
    'HLT_PFPuppiMET250',
    'HLT_PFPuppiMET120',
    'HLT_PFPuppiMET120_PFPuppiMHT120',
    'HLT_PFPuppiMET120_PFPuppiMHT120_PFPuppiHT60',
  ),

  fillCollectionConditions = cms.PSet(),

  doubles = cms.PSet(
    fixedGridRhoFastjetAllTmp = cms.InputTag('fixedGridRhoFastjetAllTmp'),
  ),

  recoVertexCollections = cms.PSet(

    hltPixelVertices = cms.InputTag('pixelVertices'),
    hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
    offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  l1tPFCandidateCollections = cms.PSet(

#   l1tPFPuppi = cms.InputTag('l1pfCandidates', 'Puppi'),
  ),

  recoPFCandidateCollections = cms.PSet(

#   hltParticleFlow = cms.InputTag('particleFlowTmp'),
#   hltPFPuppi = cms.InputTag('hltPFPuppi'),
#   hltPFPuppiNoLep = cms.InputTag('hltPFPuppiNoLep'),
  ),

  patPackedCandidateCollections = cms.PSet(

#   offlinePFCandidates = cms.InputTag('packedPFCandidates'),
  ),

  recoGenJetCollections = cms.PSet(

    ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  l1tPFJetCollections = cms.PSet(

    l1tAK4CaloJetsCorrected = cms.InputTag('ak4PFL1CaloCorrected'),
    l1tAK4PFJetsCorrected = cms.InputTag('ak4PFL1PFCorrected'),
    l1tAK4PFPuppiJetsCorrected = cms.InputTag('ak4PFL1PuppiCorrected'),
  ),

  recoCaloJetCollections = cms.PSet(

    hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
#   hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
  ),

  recoPFClusterJetCollections = cms.PSet(

#   hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
#   hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
  ),

  recoPFJetCollections = cms.PSet(

    hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
    hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),
    hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),
    hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),
    hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),
    hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),

#   l1tAK4CaloJets = cms.InputTag('ak4PFL1Calo'),
#   l1tAK4PFJets = cms.InputTag('ak4PFL1PF'),
#   l1tAK4PFPuppiJets = cms.InputTag('ak4PFL1Puppi'),
  ),

  patJetCollections = cms.PSet(

    offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    offlineAK8PFPuppiJetsCorrected = cms.InputTag('slimmedJetsAK8'),
  ),

  recoGenMETCollections = cms.PSet(

    genMETCalo = cms.InputTag('genMetCalo::HLT'),
    genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),

  recoCaloMETCollections = cms.PSet(

    hltCaloMET = cms.InputTag('hltCaloMET'),
#   hltCaloMETClean = cms.InputTag('hltMetClean'),
  ),

  recoPFClusterMETCollections = cms.PSet(

#   hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
  ),

  recoPFMETCollections = cms.PSet(

    l1tCaloMET = cms.InputTag('l1PFMetCalo'),
    l1tPFMET = cms.InputTag('l1PFMetPF'),
    l1tPFPuppiMET = cms.InputTag('l1PFMetPuppi'),

    hltPFMET = cms.InputTag('hltPFMET'),
#   hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),
    hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    hltPFSoftKillerMET = cms.InputTag('hltPFSoftKillerMET'),
    hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),
#   hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
    hltPFPuppiMETv0 = cms.InputTag('hltPFPuppiMETv0'),
  ),

  patMETCollections = cms.PSet(

    offlinePFMET = cms.InputTag('slimmedMETs'),
    offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  patMuonCollections = cms.PSet(

#   offlineIsolatedMuons = cms.InputTag('userIsolatedMuons'),
  ),

  patElectronCollections = cms.PSet(

#   offlineIsolatedElectrons = cms.InputTag('userIsolatedElectrons'),
  ),

  stringCutObjectSelectors = cms.PSet(
    # GEN
    ak4GenJetsNoNu = cms.string('pt > 15'),
    ak8GenJetsNoNu = cms.string('pt > 50'),

    # L1T AK4
#   l1tAK4CaloJets = cms.string('pt > 20'),
#   l1tAK4PFJets = cms.string('pt > 20'),
#   l1tAK4PFPuppiJets = cms.string('pt > 20'),

    l1tAK4CaloJetsCorrected = cms.string('pt > 20'),
    l1tAK4PFJetsCorrected = cms.string('pt > 20'),
    l1tAK4PFPuppiJetsCorrected = cms.string('pt > 20'),

    # HLT AK4
    hltAK4CaloJets = cms.string('pt > 20'),
#   hltAK4PFClusterJets = cms.string('pt > 20'),
    hltAK4PFJets = cms.string('pt > 20'),
    hltAK4PFJetsCorrected = cms.string('pt > 20'),
    hltAK4PFCHSJetsCorrected = cms.string('pt > 20'),
    hltAK4PFPuppiJetsCorrected = cms.string('pt > 20'),

    # HLT AK8
#   hltAK8CaloJets = cms.string('pt > 80'),
#   hltAK8PFClusterJets = cms.string('pt > 80'),
    hltAK8PFJetsCorrected = cms.string('pt > 80'),
    hltAK8PFCHSJetsCorrected = cms.string('pt > 80'),
    hltAK8PFPuppiJetsCorrected = cms.string('pt > 80'),

    # Offline
    offlineAK4PFCHSJetsCorrected = cms.string('pt > 20'),
    offlineAK4PFPuppiJetsCorrected = cms.string('pt > 20'),
    offlineAK8PFPuppiJetsCorrected = cms.string('pt > 80'),
  ),

  outputBranchesToBeDropped = cms.vstring(

    'offlinePrimaryVertices_tracksSize',

#   'hltPFMET_ChargedEMEtFraction',
#   'hltPFMETTypeOne_ChargedEMEtFraction',

    'genMETCalo_MuonEtFraction',
    'genMETCalo_InvisibleEtFraction',
  ),
)

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.extend([process.analysisNTupleEndPath])

if opts.onlyTriggerResultsInNTuple:
   # reset input collections
   process.JMETriggerNTuple.doubles = cms.PSet()
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet()
   process.JMETriggerNTuple.l1tPFCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.patPackedCandidateCollections = cms.PSet()
   process.JMETriggerNTuple.recoGenJetCollections = cms.PSet()
   process.JMETriggerNTuple.l1tPFJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoCaloJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFClusterJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFJetCollections = cms.PSet()
   process.JMETriggerNTuple.patJetCollections = cms.PSet()
   process.JMETriggerNTuple.recoGenMETCollections = cms.PSet()
   process.JMETriggerNTuple.recoCaloMETCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFClusterMETCollections = cms.PSet()
   process.JMETriggerNTuple.recoPFMETCollections = cms.PSet()
   process.JMETriggerNTuple.patMETCollections = cms.PSet()
   process.JMETriggerNTuple.patMuonCollections = cms.PSet()
   process.JMETriggerNTuple.patElectronCollections = cms.PSet()

# update process.GlobalTag.globaltag
if opts.globalTag is not None:
   process.GlobalTag.globaltag = opts.globalTag

# fix for AK4PF Phase-2 JECs
process.GlobalTag.toGet.append(cms.PSet(
  record = cms.string('JetCorrectionsRecord'),
  tag = cms.string('JetCorrectorParametersCollection_PhaseIIFall17_V5b_MC_AK4PF'),
  label = cms.untracked.string('AK4PF'),
))

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)
#if hasattr(process, 'DQMStore'):
#   process.DQMStore.enableMultiThread = (process.options.numberOfThreads > 1)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JMETriggerNTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# Tracking Monitoring
if opts.trkdqm:

   if opt_reco in ['HLT_TRKv00', 'HLT_TRKv00_TICL', 'HLT_TRKv02', 'HLT_TRKv02_TICL']:
      process.reconstruction_pixelTrackingOnly_step = cms.Path(process.reconstruction_pixelTrackingOnly)
      process.schedule.extend([process.reconstruction_pixelTrackingOnly_step])

   from JMETriggerAnalysis.Common.trackHistogrammer_cfi import trackHistogrammer
   process.TrackHistograms_hltPixelTracks = trackHistogrammer.clone(src = 'pixelTracks')
   process.TrackHistograms_hltGeneralTracks = trackHistogrammer.clone(src = 'generalTracks')

   process.trkMonitoringSeq = cms.Sequence(
       process.TrackHistograms_hltPixelTracks
     + process.TrackHistograms_hltGeneralTracks
   )

   if opt_skimTracks:
      process.TrackHistograms_hltGeneralTracksOriginal = trackHistogrammer.clone(src = 'generalTracksOriginal')
      process.trkMonitoringSeq += process.TrackHistograms_hltGeneralTracksOriginal

   from JMETriggerAnalysis.Common.vertexHistogrammer_cfi import vertexHistogrammer
   process.VertexHistograms_hltPixelVertices = vertexHistogrammer.clone(src = 'pixelVertices')
   process.VertexHistograms_hltPrimaryVertices = vertexHistogrammer.clone(src = 'offlinePrimaryVertices')
   process.VertexHistograms_offlinePrimaryVertices = vertexHistogrammer.clone(src = 'offlineSlimmedPrimaryVertices')

   process.trkMonitoringSeq += cms.Sequence(
       process.VertexHistograms_hltPixelVertices
     + process.VertexHistograms_hltPrimaryVertices
     + process.VertexHistograms_offlinePrimaryVertices
   )

#  from Validation.RecoVertex.PrimaryVertexAnalyzer4PUSlimmed_cfi import vertexAnalysis, pixelVertexAnalysisPixelTrackingOnly
#  process.vertexAnalysis = vertexAnalysis.clone(vertexRecoCollections = ['offlinePrimaryVertices'])
#  process.pixelVertexAnalysis = pixelVertexAnalysisPixelTrackingOnly.clone(vertexRecoCollections = ['pixelVertices'])
#
#  process.trkMonitoringSeq += cms.Sequence(
#      process.vertexAnalysis
#    + process.pixelVertexAnalysis
#  )

   process.trkMonitoringEndPath = cms.EndPath(process.trkMonitoringSeq)
   process.schedule.extend([process.trkMonitoringEndPath])

# ParticleFlow Monitoring
if opts.pfdqm > 0:

   from JMETriggerAnalysis.Common.pfCandidateHistogrammerRecoPFCandidate_cfi import pfCandidateHistogrammerRecoPFCandidate
   from JMETriggerAnalysis.Common.pfCandidateHistogrammerPatPackedCandidate_cfi import pfCandidateHistogrammerPatPackedCandidate

   _candTags = [
     ('_offlineParticleFlow', 'packedPFCandidates', '', pfCandidateHistogrammerPatPackedCandidate),
     ('_particleFlowTmp', 'particleFlowTmp', '', pfCandidateHistogrammerRecoPFCandidate),
     ('_hltPFPuppi', 'hltPFPuppi', '(pt > 0)', pfCandidateHistogrammerRecoPFCandidate),
   ]

   if 'TICL' in opt_reco:
      _candTags += [
        ('_pfTICL', 'pfTICL', '', pfCandidateHistogrammerRecoPFCandidate),
      ]
   else:
      _candTags += [
        ('_simPFProducer', 'simPFProducer', '', pfCandidateHistogrammerRecoPFCandidate),
      ]

   if opts.pfdqm > 2:
      _tmpCandTags = []
      for _tmp in _candTags:
          _tmpCandTags += [(_tmp[0]+'_2GeV', _tmp[1], '(pt > 2.)', _tmp[3])]
      _candTags += _tmpCandTags
      del _tmpCandTags

   _regTags = [
     ['', ''],
     ['_HB'   , '(0.0<=abs(eta) && abs(eta)<1.5)'],
     ['_HGCal', '(1.5<=abs(eta) && abs(eta)<3.0)'],
     ['_HF'   , '(3.0<=abs(eta) && abs(eta)<5.0)'],
   ]

   _pidTags = [['', '']]
   if opts.pfdqm > 1:
      _pidTags += [
        ['_h', '(abs(pdgId) == 211)'],
        ['_e', '(abs(pdgId) == 11)'],
        ['_mu', '(abs(pdgId) == 13)'],
        ['_gamma', '(abs(pdgId) == 22)'],
        ['_h0', '(abs(pdgId) == 130)'],
      ]

   process.pfMonitoringSeq = cms.Sequence()
   for _candTag in _candTags:
     for _regTag in _regTags:
       for _pidTag in _pidTags:
         _modName = 'PFCandidateHistograms'+_candTag[0]+_regTag[0]+_pidTag[0]
         setattr(process, _modName, _candTag[3].clone(
           src = _candTag[1],
           cut = ' && '.join([_tmp for _tmp in [_candTag[2], _regTag[1], _pidTag[1]] if _tmp]),
         ))
         process.pfMonitoringSeq += getattr(process, _modName)

   process.pfMonitoringEndPath = cms.EndPath(process.pfMonitoringSeq)
   process.schedule.extend([process.pfMonitoringEndPath])

# MessageLogger
if opts.logs:
   process.MessageLogger = cms.Service('MessageLogger',
     destinations = cms.untracked.vstring(
       'cerr',
       'logError',
       'logInfo',
       'logDebug',
     ),
     # scram b USER_CXXFLAGS="-DEDM_ML_DEBUG"
     debugModules = cms.untracked.vstring(
       'JMETriggerNTuple',
     ),
     categories = cms.untracked.vstring(
       'FwkReport',
     ),
     cerr = cms.untracked.PSet(
       threshold = cms.untracked.string('WARNING'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logError = cms.untracked.PSet(
       threshold = cms.untracked.string('ERROR'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logInfo = cms.untracked.PSet(
       threshold = cms.untracked.string('INFO'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
     logDebug = cms.untracked.PSet(
       threshold = cms.untracked.string('DEBUG'),
       extension = cms.untracked.string('.txt'),
       FwkReport = cms.untracked.PSet(
         reportEvery = cms.untracked.int32(1),
       ),
     ),
   )

   if opt_skimTracks:
      process.MessageLogger.debugModules += [
        'hltTrimmedPixelVertices',
        'generalTracks',
      ]

# EDM Input Files
if opts.inputFiles and opts.secondaryInputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = opts.secondaryInputFiles
elif opts.inputFiles:
   process.source.fileNames = opts.inputFiles
   process.source.secondaryFileNames = []
else:
   process.source.fileNames = [
     '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8/FEVT/PU200_castor_111X_mcRun4_realistic_T15_v1-v1/100000/DA18C0FC-1189-D64B-B3B6-44F3F96F1840.root',
   ]
   process.source.secondaryFileNames = []

# skimming of tracks
if opt_skimTracks:

   from JMETriggerAnalysis.Common.hltPhase2_skimmedTracks import customize_hltPhase2_skimmedTracks
   process = customize_hltPhase2_skimmedTracks(process)

#   # modify PV inputs of PFPuppi collections
#   process.puppiNoLep.vertexName = process.generalTracks.vertices
#   process.hltPFPuppi.vertexName = process.generalTracks.vertices

   # add PV collections to JMETriggerNTuple
   process.JMETriggerNTuple.recoVertexCollections = cms.PSet(
     hltPixelVertices = cms.InputTag('pixelVertices'),
     hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
     hltPrimaryVertices = cms.InputTag('offlinePrimaryVertices'),
     offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
   )

   process.JMETriggerNTuple.outputBranchesToBeDropped += [
     'hltPixelVertices_isFake',
     'hltPixelVertices_chi2',
     'hltPixelVertices_ndof',

     'hltTrimmedPixelVertices_isFake',
     'hltTrimmedPixelVertices_chi2',
     'hltTrimmedPixelVertices_ndof',
   ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
if opts.verbosity > 0:
   print '--- jmeTriggerNTuple_cfg.py ---'
   print ''
   print 'option: output =', opts.output
   print 'option: reco =', opts.reco, '(skimTracks = '+str(opt_skimTracks)+')'
   print 'option: trkdqm =', opts.trkdqm
   print 'option: pfdqm =', opts.pfdqm
   print 'option: dumpPython =', opts.dumpPython
   print ''
   print 'process.GlobalTag =', process.GlobalTag.dumpPython()
   print 'process.source =', process.source.dumpPython()
   print 'process.maxEvents =', process.maxEvents.dumpPython()
   print 'process.options =', process.options.dumpPython()
   print '-------------------------------'


for _mod in process.MC_JME_v1.moduleNames():
    print _mod

remove all other modules
