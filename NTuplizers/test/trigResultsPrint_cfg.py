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
### Path
###
import FWCore.ParameterSet.Config as cms
process = cms.Process('TEST')

from JMETriggerAnalysis.NTuplizers.triggerFlagsProducer_cfi import triggerFlagsProducer

process.AAA = triggerFlagsProducer.clone(pathName = 'HLT_IsoMu24', ignorePathVersion = True)

process.trigSeq = cms.Sequence(
  process.AAA
)

process.trigPath = cms.Path(process.trigSeq)

#process.trigEndPath = cms.EndPath(process.trigPathpuppiNTuple)

#process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

if opts.printSummaries:
  from HLTrigger.Timer.FastTimer import customise_timer_service_print
  process = customise_timer_service_print(process)

###
### standard I/O options
###

# update process.GlobalTag.globaltag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if opts.globalTag is not None:
  from Configuration.AlCa.GlobalTag import GlobalTag
  process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

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
  numberOfThreads = cms.untracked.uint32(1),
  printDependencies = cms.untracked.bool(False),
  sizeOfStackForThreadsInKB = cms.untracked.uint32(10240),
  throwIfIllegalParameter = cms.untracked.bool(True),
  wantSummary = cms.untracked.bool(opts.wantSummary)
)

process.options.numberOfThreads = cms.untracked.uint32(opts.numThreads if (opts.numThreads > 1) else 1)
process.options.numberOfStreams = cms.untracked.uint32(opts.numStreams if (opts.numStreams > 0) else 0)

# show cmsRun summary at job completion
process.options.wantSummary = opts.wantSummary

# select luminosity sections from .json file
if opts.lumis is not None:
  import FWCore.PythonUtilities.LumiList as LumiList
  process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    '/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/Run2018D/EphemeralHLTPhysics/RAW/Run_323775/F22781A8-0B0A-F54E-9528-982309BF7C7D.root',
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
