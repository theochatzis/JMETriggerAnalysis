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

opts.register('wantSummary', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show cmsRun summary at job completion')

opts.register('printSummaries', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'show summaries from HLT services')

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'verbosity level')

opts.parseArguments()

###
### Puppi Sequence
###
import FWCore.ParameterSet.Config as cms
process = cms.Process('TEST')

from CommonTools.PileupAlgos.Puppi_cff import puppi as _puppi, puppiNoLep as _puppiNoLep
process.pfPuppi = _puppi.clone()
process.pfPuppiNoLep = _puppiNoLep.clone()

#process.pfPuppiPix = _puppi.clone(
#  candName = 'particleFlow',
#  vertexName = 'pixelVertices',
#  UseFromPVLooseTight = True,
#  vtxNdofCut = 0,
#)
#
#process.pfPuppiNoLepPix = _puppiNoLep.clone(
#  candName = 'particleFlow',
#  vertexName = 'pixelVertices',
#  UseFromPVLooseTight = True,
#  vtxNdofCut = 0,
#)

process.puppiSeq = cms.Sequence(
    process.pfPuppi
  + process.pfPuppiNoLep
#  + process.pfPuppiPix
#  + process.pfPuppiNoLepPix
)

process.puppiPath = cms.Path(process.puppiSeq)

process.puppiNTuple = cms.EDAnalyzer('JMETriggerNTuple',
  TTreeName = cms.string('Events'),
  TriggerResults = cms.InputTag('TriggerResults'),
  TriggerResultsFilterOR = cms.vstring(),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(),
  outputBranchesToBeDropped = cms.vstring(),
  recoVertexCollections = cms.PSet(
  ),
  recoPFCandidateCollections = cms.PSet(
#   particleFlow = cms.InputTag('particleFlow'),
    puppi = cms.InputTag('pfPuppi'),
    puppiNoLep = cms.InputTag('pfPuppiNoLep'),
#   puppiPix = cms.InputTag('pfPuppiPix'),
#   puppiNoLepPix = cms.InputTag('pfPuppiNoLepPix'),
  )
)

process.puppiNTupleEndPath = cms.EndPath(process.puppiNTuple)

process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

if opts.printSummaries:
   from HLTrigger.Timer.FastTimer import customise_timer_service_print
   process = customise_timer_service_print(process)

###
### standard I/O options
###

# update process.GlobalTag.globaltag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if opts.globalTag is not None:
   process.GlobalTag.globaltag = opts.globalTag

# max number of events to be processed
process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(opts.maxEvents),
)

# number of events to be skipped
process.source = cms.Source('PoolSource',
  fileNames = cms.untracked.vstring(),
  secondaryFileNames = cms.untracked.vstring(),
  inputCommands = cms.untracked.vstring('keep *'),
  skipEvents = cms.untracked.uint32(opts.skipEvents),
)

# multi-threading settings
process.options = cms.untracked.PSet(
  FailPath = cms.untracked.vstring(),
  IgnoreCompletely = cms.untracked.vstring(),
  Rethrow = cms.untracked.vstring(),
  SkipEvent = cms.untracked.vstring(),
  canDeleteEarly = cms.untracked.vstring(),
  eventSetup = cms.untracked.PSet(
    forceNumberOfConcurrentIOVs = cms.untracked.PSet(
    ),
    numberOfConcurrentIOVs = cms.untracked.uint32(1)
  ),
  fileMode = cms.untracked.string('FULLMERGE'),
  forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
  numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(1),
  numberOfConcurrentRuns = cms.untracked.uint32(1),
  numberOfStreams = cms.untracked.uint32(0),
  numberOfThreads = cms.untracked.uint32(4),
  printDependencies = cms.untracked.bool(False),
  sizeOfStackForThreadsInKB = cms.untracked.uint32(10240),
  throwIfIllegalParameter = cms.untracked.bool(True),
   wantSummary = cms.untracked.bool(opts.wantSummary)
)

process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 1) else 1)
# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/AODSIM/FlatPU0to80_110X_mcRun3_2021_realistic_v6-v1/100000/972E4466-10B8-1345-A0F9-8ECBF8D1D772.root',
   ]

# input EDM files [secondary]
if opts.secondaryInputFiles == ['None']:
   process.source.secondaryFileNames = []
elif opts.secondaryInputFiles != []:
   process.source.secondaryFileNames = opts.secondaryInputFiles
else:
   process.source.secondaryFileNames = []

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())
