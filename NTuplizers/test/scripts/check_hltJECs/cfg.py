from hlt_data import cms, process
#/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/Run2018D/EphemeralHLTPhysics/RAW/Run_323775/0E695C4C-7D5C-C641-AE82-3E5901DF846F.root
process.source.fileNames = ['file:0E695C4C-7D5C-C641-AE82-3E5901DF846F.root']

#from hlt_mc import cms, process
##/store/mc/Run3Winter20DRPremixMiniAOD/GluGluToHHTo4B_node_SM_TuneCP5_14TeV-madgraph-pythia8/GEN-SIM-RAW/110X_mcRun3_2021_realistic_v6-v2/250000/904FDC0F-6179-7E44-9988-C20E997EFFA8.root
#process.source.fileNames = ['file:904FDC0F-6179-7E44-9988-C20E997EFFA8.root']

process.FastTimerService.printRunSummary = False
process.FastTimerService.printJobSummary = False
process.options.wantSummary = False
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.hltAK4PFJetsCorrected.verbose = cms.untracked.bool(True)
process.hltAK4PFJetsCorrected.correctors = [
  'hltAK4PFFastJetCorrector',
#  'hltAK4PFRelativeCorrector',
#  'hltAK4PFAbsoluteCorrector',
#  'hltAK4PFResidualCorrector',
]

#process.hltAK4PFFastJetCorrector .algorithm = 'AK4PF' #HLT'
#process.hltAK4PFRelativeCorrector.algorithm = 'AK4PF' #HLT'
#process.hltAK4PFAbsoluteCorrector.algorithm = 'AK4PF' #HLT'
#process.hltAK4PFResidualCorrector.algorithm = 'AK4PF' #HLT'

process.Debug = cms.Path(
  process.HLTAK4PFJetsSequence
)

process.GlobalTag.toGet += [
  cms.PSet(
    record = cms.string('JetCorrectionsRecord'),
    tag = cms.string('JetCorrectorParametersCollection_HLT_BX25_V12_MC_AK4CaloHLT'),
    label = cms.untracked.string('AK4CaloHLT'),
  ),
  cms.PSet(
    record = cms.string('JetCorrectionsRecord'),
    tag = cms.string('JetCorrectorParametersCollection_HLT_BX25_V12_MC_AK4PFHLT'),
    label = cms.untracked.string('AK4PFHLT'),
  ),
]
