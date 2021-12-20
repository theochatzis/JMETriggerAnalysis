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

opts.register('globalTag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('reco', 'HLT_GRun',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.parseArguments()

###
### HLT configuration
###
update_jmeCalibs = False

def fixForGRunConfig(process):
  from HLTrigger.Configuration.common import producers_by_type
  for producer in producers_by_type(process, 'TrackWithVertexSelector'):
    if not hasattr(producer, 'numberOfValidHitsForGood'):
      producer.numberOfValidHitsForGood = cms.uint32(999)
    if not hasattr(producer, 'numberOfValidPixelHitsForGood'):
      producer.numberOfValidPixelHitsForGood = cms.uint32(999)
    if not hasattr(producer, 'zetaVtxScale'):
      producer.zetaVtxScale = cms.double(1.0)
    if not hasattr(producer, 'rhoVtxScale'):
      producer.rhoVtxScale = cms.double(1.0)
    if not hasattr(producer, 'zetaVtxSig'):
      producer.zetaVtxSig = cms.double(999.0)
    if not hasattr(producer, 'rhoVtxSig'):
      producer.rhoVtxSig = cms.double(999.0)
  return process

if opts.reco == 'HLT_GRun_oldJECs':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_Data_NoOutput_configDump import cms, process
  process = fixForGRunConfig(process)
  update_jmeCalibs = False

elif opts.reco == 'HLT_GRun':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_Data_NoOutput_configDump import cms, process
  process = fixForGRunConfig(process)
  update_jmeCalibs = True

elif opts.reco == 'HLT_Run3TRK':
  # (a) Run-3 tracking: standard
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_Data_NoOutput_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3Tracking
  process = customizeHLTRun3Tracking(process)
  update_jmeCalibs = True

  if hasattr(process, 'hltEG60R9Id90CaloIdLIsoLDisplacedIdFilter'):
    process.hltEG60R9Id90CaloIdLIsoLDisplacedIdFilter.inputTrack = 'hltMergedTracks'

  if hasattr(process, 'hltIter1ClustersRefRemoval'):
    process.hltIter1ClustersRefRemoval.trajectories = 'hltMergedTracks'

  for _tmpPathName in [
    'AlCa_LumiPixelsCounts_ZeroBias_v1',
    'AlCa_LumiPixelsCounts_Random_v1',
  ]:
    if hasattr(process, _tmpPathName):
      _tmpPath = getattr(process, _tmpPathName)
      _tmpPath.remove(process.hltSiPixelDigis)
      _tmpPath.remove(process.hltSiPixelClusters)
      _tmpPath.associate(process.HLTDoLocalPixelTask)

elif opts.reco == 'HLT_Run3TRKWithPU':
  # (b) Run-3 tracking: all pixel vertices
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_Data_NoOutput_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3TrackingAllPixelVertices
  process = customizeHLTRun3TrackingAllPixelVertices(process)
  update_jmeCalibs = True

  if hasattr(process, 'hltEG60R9Id90CaloIdLIsoLDisplacedIdFilter'):
    process.hltEG60R9Id90CaloIdLIsoLDisplacedIdFilter.inputTrack = 'hltMergedTracks'

  if hasattr(process, 'hltIter1ClustersRefRemoval'):
    process.hltIter1ClustersRefRemoval.trajectories = 'hltMergedTracks'

  for _tmpPathName in [
    'AlCa_LumiPixelsCounts_ZeroBias_v1',
    'AlCa_LumiPixelsCounts_Random_v1',
  ]:
    if hasattr(process, _tmpPathName):
      _tmpPath = getattr(process, _tmpPathName)
      _tmpPath.remove(process.hltSiPixelDigis)
      _tmpPath.remove(process.hltSiPixelClusters)
      _tmpPath.associate(process.HLTDoLocalPixelTask)

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

# remove MessageLogger
if hasattr(process, 'MessageLogger'):
  del process.MessageLogger

if update_jmeCalibs:
  ## ES modules for PF-Hadron Calibrations
  import os
  from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/PFHC_Run3Winter20_HLT_v01.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_HLT_mcRun3_2021'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

  ## ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V2_MC.db'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFClusterHLT'),
        label = cms.untracked.string('AK4PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFHLT'),#!!
        label = cms.untracked.string('AK4PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK4PFPuppiHLT'),
        label = cms.untracked.string('AK4PFPuppiHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFClusterHLT'),
        label = cms.untracked.string('AK8PFClusterHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFHLT'),#!!
        label = cms.untracked.string('AK8PFchsHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V2_MC_AK8PFPuppiHLT'),
        label = cms.untracked.string('AK8PFPuppiHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

###
### output
###
if hasattr(process, 'DQMOutput'):
  process.DQMOutput.remove(process.dqmOutput)

process.hltOutput = cms.OutputModule('PoolOutputModule',
  fileName = cms.untracked.string(opts.output),
  fastCloning = cms.untracked.bool(False),
  dataset = cms.untracked.PSet(
    filterName = cms.untracked.string(''),
    dataTier = cms.untracked.string('RAW')
  ),
  outputCommands = cms.untracked.vstring(
    'drop *',
    'keep edmTriggerResults_*_*_'+process.name_(),
  )
)

process.hltOutputEndPath = cms.EndPath(process.hltOutput)

###
### standard options
###

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = max(opts.numThreads, 1)
process.options.numberOfStreams = max(opts.numStreams, 0)

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# update process.GlobalTag.globaltag
if opts.globalTag is not None:
  from Configuration.AlCa.GlobalTag import GlobalTag
  process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# select luminosity sections from .json file
if opts.lumis is not None:
  import FWCore.PythonUtilities.LumiList as LumiList
  process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    '/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/65EA98C3-88C1-5A43-8152-824F3169174E.root',
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
  ]

# dump content of cms.Process to python file
if opts.dumpPython is not None:
  open(opts.dumpPython, 'w').write(process.dumpPython())

# printouts
if opts.verbosity > 0:
  print '--- hltResults_cfg.py ---------'
  print ''
  print 'option: output =', opts.output
  print 'option: reco =', opts.reco
  print 'option: dumpPython =', opts.dumpPython
  print ''
  print 'process.name_() =', process.name_()
  print 'process.GlobalTag =', process.GlobalTag.dumpPython()
  print 'process.source =', process.source.dumpPython()
  print 'process.maxEvents =', process.maxEvents.dumpPython()
  print 'process.options =', process.options.dumpPython()
  print '-------------------------------'
