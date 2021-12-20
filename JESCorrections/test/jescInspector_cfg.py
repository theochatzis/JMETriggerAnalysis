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
              'keyword defining reconstruction methods for JME inputs')

opts.register('txtFilesPrefix', '',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'common part of paths to JESC .txt files')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.parseArguments()

###
### GlobalTag
###
# update process.GlobalTag.globaltag
if opts.globalTag is not None:
  from Configuration.AlCa.GlobalTag import GlobalTag
  process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

###
### HLT configuration
###
if opts.reco == 'HLT_GRun':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process

elif opts.reco == 'HLT_Run3TRK':
  # (a) Run-3 tracking: standard
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3Tracking
  process = customizeHLTRun3Tracking(process)

elif opts.reco == 'HLT_Run3TRKWithPU':
  # (b) Run-3 tracking: all pixel vertices
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_configDump import cms, process
  from HLTrigger.Configuration.customizeHLTRun3Tracking import customizeHLTRun3TrackingAllPixelVertices
  process = customizeHLTRun3TrackingAllPixelVertices(process)

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.OutputModule:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print '> removed cms.OutputModule:', _modname

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
    _mod = getattr(process, _modname)
    if type(_mod) == cms.EndPath:
       process.__delattr__(_modname)
       if opts.verbosity > 0:
          print '> removed cms.EndPath:', _modname

# remove selected cms.Path objects from HLT config-dump
print '-'*108
print '{:<99} | {:<4} |'.format('cms.Path', 'keep')
print '-'*108
for _modname in sorted(process.paths_()):
    _keepPath = _modname.startswith('MC_') and ('Jets' in _modname or 'MET' in _modname or 'AK8Calo' in _modname)
    if _keepPath:
      print '{:<99} | {:<4} |'.format(_modname, '+')
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print '{:<99} | {:<4} |'.format(_modname, '')
print '-'*108

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

# remove MessageLogger
if hasattr(process, 'MessageLogger'):
  del process.MessageLogger

###
### customisations
###

## customised JME collections
from JMETriggerAnalysis.Common.customise_hlt import *
process = addPaths_MC_JMEPFCluster(process)
process = addPaths_MC_JMEPFPuppi(process)

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
  _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/data/JESC_Run3Winter20_V1_MC.db'),
  toGet = cms.VPSet(
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4CaloHLT'),
      label = cms.untracked.string('AK4CaloHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFClusterHLT'),
      label = cms.untracked.string('AK4PFClusterHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFHLT'),
      label = cms.untracked.string('AK4PFHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFHLT'),
      label = cms.untracked.string('AK4PFchsHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFPuppiHLT'),
      label = cms.untracked.string('AK4PFPuppiHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4CaloHLT'),#!!
      label = cms.untracked.string('AK8CaloHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFClusterHLT'),#!!
      label = cms.untracked.string('AK8PFClusterHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFHLT'),#!!
      label = cms.untracked.string('AK8PFHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFHLT'),#!!
      label = cms.untracked.string('AK8PFchsHLT'),
    ),
    cms.PSet(
      record = cms.string('JetCorrectionsRecord'),
      tag = cms.string('JetCorrectorParametersCollection_Run3Winter20_V1_MC_AK4PFPuppiHLT'),#!!
      label = cms.untracked.string('AK8PFPuppiHLT'),
    ),
  ),
)
process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

###
### JESC analyzers
###
import os
process.hltJESCAnalysisSeq = cms.Sequence()

for [rawJetsMod, jetCorrMod, jecAlgo] in [
  ['hltAK4PFPuppiJets', 'hltAK4PFPuppiJetCorrector', 'AK4PFPuppiHLT'],
#  ['hltAK8PFPuppiJets', 'hltAK8PFPuppiJetCorrector', 'AK8PFPuppiHLT'],
]:
  if hasattr(process, rawJetsMod+'JESCAnalyzer'):
    raise RuntimeError('module "'+rawJetsMod+'JESCAnalyzer" already exists')

  for _tmp in getattr(process, jetCorrMod).correctors:
    getattr(process, _tmp).algorithm = jecAlgo

  _txtFiles = []
  for _tmp in [
    'L1FastJet',
    'L2Relative',
    'L3Absolute',
  ]:
    _txtFile = opts.txtFilesPrefix+_tmp+'_'+jecAlgo+'.txt'
    if not os.path.isfile(_txtFile):
      raise RuntimeError('target .txt file not found: '+_txtFile)
    _txtFiles.append(os.path.relpath(os.path.abspath(_txtFile), os.environ['CMSSW_BASE']+'/src'))

  setattr(process, rawJetsMod+'JESCAnalyzer', cms.EDAnalyzer('CorrectedPFJetAnalyzer',
    src = cms.InputTag(rawJetsMod),
    correctors = cms.VInputTag(jetCorrMod),
    textFiles = cms.vstring(_txtFiles),
    useRho = cms.bool(True),
    rho = cms.InputTag('hltFixedGridRhoFastjetAll'),
    verbose = cms.bool(True),
  ))

  process.hltJESCAnalysisSeq += getattr(process, rawJetsMod+'JESCAnalyzer')

process.hltJESCAnalysisEndPath = cms.EndPath(process.hltJESCAnalysisSeq)
if process.schedule_() is not None:
  process.schedule_().append(process.hltJESCAnalysisEndPath)
#process.prune()

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

# show cmsRun summary at job completion
process.options.wantSummary = cms.untracked.bool(opts.wantSummary)

# select luminosity sections from .json file
if opts.lumis is not None:
  import FWCore.PythonUtilities.LumiList as LumiList
  process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# EDM Input Files
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.inputFiles and opts.secondaryInputFiles:
  process.source.fileNames = opts.inputFiles
  process.source.secondaryFileNames = opts.secondaryInputFiles
elif opts.inputFiles:
  process.source.fileNames = opts.inputFiles
  process.source.secondaryFileNames = []
else:
  process.source.fileNames = [
    '/store/mc/Run3Winter20DRMiniAOD/QCD_Pt-15to7000_TuneCP5_Flat_14TeV_pythia8/GEN-SIM-RAW/FlatPU0to80_110X_mcRun3_2021_realistic_v6-v1/100000/07634100-A880-4E4D-BAA3-D9C0B5356C2D.root',
  ]
  process.source.secondaryFileNames = []

# dump content of cms.Process to python file
if opts.dumpPython is not None:
  open(opts.dumpPython, 'w').write(process.dumpPython())
