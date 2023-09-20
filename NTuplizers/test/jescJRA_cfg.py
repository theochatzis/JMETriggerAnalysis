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

opts.register('numStreams', 0,
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

opts.register('reco', 'HLT_75e33',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword defining reconstruction methods for JME inputs')

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

# customisation to change min-pT threshold of tracks in HLT reco
def customisePhase2TrackingPtThresholds(process, ptMin):
  process.CkfBaseTrajectoryFilter_block.minPt = cms.double(ptMin)
  process.HLTIter0Phase2L3FromL1TkMuonGroupedCkfTrajectoryFilterIT.minPt = cms.double(ptMin)
  process.HLTPSetMuonCkfTrajectoryFilter.minPt = cms.double(ptMin)
  process.TrajectoryFilterForConversions.minPt = cms.double(ptMin)
  process.highPtTripletStepTrajectoryFilterBase.minPt = cms.double(ptMin)
  process.highPtTripletStepTrajectoryFilterInOut.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryBuilder.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterBase.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrajectoryFilterInOut.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonInitialStepTrajectoryBuilder.minPt = cms.double(ptMin)
  process.hltPhase2L3MuonInitialStepTrajectoryFilter.minPt = cms.double(ptMin)
  process.initialStepTrajectoryFilter.minPt = cms.double(ptMin)
  process.muonSeededTrajectoryFilterForInOut.minPt = cms.double(ptMin)
  process.muonSeededTrajectoryFilterForOutIn.minPt = cms.double(ptMin)
  process.muonSeededTrajectoryFilterForOutInDisplaced.minPt = cms.double(ptMin)
  process.firstStepPrimaryVerticesUnsorted.TkFilterParameters.minPt = cms.double(ptMin)
  process.generalTracks.MinPT = cms.double(ptMin)
  process.highPtTripletStepTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonGeneralTracks.MinPT = cms.double(ptMin)
  process.hltPhase2L3MuonHighPtTripletStepTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonPixelTrackFilterByKinematics.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonPixelTracksFilter.ptMin = cms.double(ptMin)
  process.hltPhase2L3MuonPixelTracksTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.pixelTrackFilterByKinematics.ptMin = cms.double(ptMin)
  process.pixelTracksTrackingRegions.RegionPSet.ptMin = cms.double(ptMin)
  process.trackWithVertexRefSelectorBeforeSorting.ptMin = cms.double(ptMin)
  process.unsortedOfflinePrimaryVertices.TkFilterParameters.minPt = cms.double(ptMin)
  return process

if opts.reco == 'HLT_TRKv06p1':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_cfg import cms, process
elif opts.reco == 'HLT_TRKv06p1_TICL':
  from JMETriggerAnalysis.Common.configs.hltPhase2_TRKv06p1_TICL_cfg import cms, process
elif opts.reco == 'HLT_75e33':
  from JMETriggerAnalysis.Common.configs.HLT_75e33_ticlv4_cfg import cms, process
  # optimal tracking thresholds for MET
  #process = customisePhase2TrackingPtThresholds(process,1.8)
  #process.schedule_().append(process.MC_JME)
  # Input source
  process.source.inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_hlt*_*_HLT',
        'drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT'
  )
else:
   raise RuntimeError('invalid argument for option "reco": "'+opts.reco+'"')

# use only the cms.Path with the full HLT reconstruction (no specific trigger paths)
#process.setSchedule_(cms.Schedule(process.MC_JME))

###
### Jet Response Analyzer (JRA) NTuple
###
#import JetMETAnalysis.JetAnalyzers.DefaultsHLT_cff as Defaults
import JetMETAnalysis.JetAnalyzers.Defaults_cff as Defaults
from JetMETAnalysis.JetAnalyzers.addAlgorithmHLT import addAlgorithm

for algorithm in [
  'ak4pfpuppiHLT',
  #'ak8pfpuppiHLT',
]:
  addAlgorithm(process, algorithm, Defaults)
  getattr(process, algorithm).srcRho = 'fixedGridRhoFastjetAllTmp'
  getattr(process, algorithm).srcRhoHLT = ''
  getattr(process, algorithm).srcRhos = ''
  getattr(process, algorithm).deltaRMax = 0.1

## update process.GlobalTag.globaltag
if opts.globalTag is not None:
   from Configuration.AlCa.GlobalTag import GlobalTag
   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')


# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 1)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JRA-NTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

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

# input EDM files
process.source.secondaryFileNames = []
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     #'/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v2/280000/015FB6F1-59B4-304C-B540-2392A983A97D.root',
     '/store/mc/Phase2Spring23DIGIRECOMiniAOD/QCD_Pt-15To3000_TuneCP5_Flat_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_131X_mcRun4_realistic_v5-v2/50000/00158fbd-efe4-4454-9d7c-8a0266757074.root',
   ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# print-outs
if opts.verbosity > 0:
   print('--- hltJRA_mcRun4_cfg.py ---')
   print('')
   print('option: output =', opts.output)
   print('option: reco =', opts.reco)
   print('option: dumpPython =', opts.dumpPython)
   print('')
   print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('-------------------------------')
