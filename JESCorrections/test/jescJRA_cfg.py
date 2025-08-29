import fnmatch

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

#opts.register('globalTag', None,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.string,
#              'argument of process.GlobalTag.globaltag')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('bpixMode', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'if stated as noBPix removes -1.2<phi<-0.8 , else if BPix keeps only this phi region, or BPixPlus/BPixMinus which is the BPix +/- half jet radius')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('reco', 'default',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.parseArguments()

supported_bpix_options = ['noBPix', 'BPix', 'FPix', 'BPixPlus', 'BPixMinus']

if opts.bpixMode is not None and opts.bpixMode not in supported_bpix_options:
    raise ValueError("Error: The bpixMode value provided is not one of the supported options.")

###
### HLT configuration
###

print(f'Using {opts.reco}')


if opts.reco == 'default':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_15_0_0_GRun_configDump import *
  
elif opts.reco == 'mixedPFPuppi':
  from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_15_0_0_GRun_configDump import *
  # adding mixed tracking in PF
  print("adding mixed tracking in PF")
  from HLTrigger.Configuration.customizeHLTforMixedTrkPUPPI import *
  process = customizeHLTForMixedPF(process)
   # adding CHS/PUPPI
  print("adding CHS/PUPPI")
  process = addPaths_MC_JMEPFCHS(process)
  process = addPaths_MC_JMEPFPuppi(process)[0]

else:
   raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')


# New PFHC
#process.GlobalTag.toGet += [
#  cms.PSet(
#      record = cms.string('PFCalibrationRcd'),
#      tag = cms.string('PFCalibration_Run3Winter25_MC_hlt_v1'),
#      label = cms.untracked.string('HLT'),
#  )
#]

# Use always the Ecal PF RecHit Thresholds in Calo Towers:
from HLTrigger.Configuration.common import producers_by_type
for producer in producers_by_type(process, "CaloTowersCreator"):
  producer.EcalRecHitThresh = cms.bool(True)


# Remove HLT_PFJet40_GPUvsCPU_v7
process.schedule.remove(process.HLT_PFJet40_GPUvsCPU_v7)


# remove cms.OutputModule objects from HLT config-dump
for _modname in process.outputModules_():
  _mod = getattr(process, _modname)
  if type(_mod) == cms.OutputModule:
    process.__delattr__(_modname)
    if opts.verbosity > 0:
      print('> removed cms.OutputModule:', _modname)

# remove cms.EndPath objects from HLT config-dump
for _modname in process.endpaths_():
  _mod = getattr(process, _modname)
  if type(_mod) == cms.EndPath:
    process.__delattr__(_modname)
    if opts.verbosity > 0:
      print('> removed cms.EndPath:', _modname)

# remove selected cms.Path objects from HLT config-dump
print('-'*108)
print('{:<99} | {:<4} |'.format('cms.Path', 'keep'))
print('-'*108)

# list of patterns to determine which paths to keep
keepPaths = [
  'MC_*Jets*',
  'MC_*AK8Calo*',
]

for _modname in sorted(process.paths_()):
  _keepPath = False
  for _tmpPatt in keepPaths:
    _keepPath = fnmatch.fnmatch(_modname, _tmpPatt)
    if _keepPath: break
  if _keepPath:
    print('{:<99} | {:<4} |'.format(_modname, '+'))
    continue
  _mod = getattr(process, _modname)
  if type(_mod) == cms.Path:
    process.__delattr__(_modname)
    print('{:<99} | {:<4} |'.format(_modname, ''))
print('-'*108)

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

# remove MessageLogger
#if hasattr(process, 'MessageLogger'):
#  del process.MessageLogger

#from FWCore.MessageService.MessageLogger_cfi import *
#MessageLogger = cms.Service("MessageLogger")


###
### customisations
###

## customised JME collections
#from JMETriggerAnalysis.Common.customise_hlt import *
#process = addPaths_MC_JMEPFCluster(process)
#process = addPaths_MC_JMEPFCHS(process)
#process = addPaths_MC_JMEPFPuppi(process)

## ES modules for PF-Hadron Calibrations with db file

import os

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB
## ES modules for PF-Hadron Calibrations
process.pfhcESSource = cms.ESSource('PoolDBESSource',
  _CondDB.clone(connect = 'sqlite_file:PFCalibration.db'),
  toGet = cms.VPSet(
    cms.PSet(
      record = cms.string('PFCalibrationRcd'),
      tag = cms.string('PFCalibration_142X_mcRun3_2025_v7_forHLT'),
      label = cms.untracked.string('HLT'),
    ),
  ),
)
process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')

## Used to test applying the offline PFHC from GT: 
#process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

# Test option to skip forward PFHC application (after eta = 2.5)
#process.hltParticleFlow.skipForwardCalibrations = cms.bool(True)


## Modification to select jets 4
# [-1.20 , -0.80]
process.hltAK4PFJetsBPix = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK4PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi<-0.80 && phi>-1.20")
)

process.hltAK4PFJetsFPix = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK4PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi>2.30 && phi<3.15")
)

# [-0.80 , -0.60]
process.hltAK4PFJetsBPixPlus = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK4PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi<-0.60 && phi>-0.80")
)

# [-1.40 , -1.20]
process.hltAK4PFJetsBPixMinus = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK4PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi<-1.20 && phi>-1.40")
)

# Not in [-1.40 , -0.60]
process.hltAK4PFJetsnoBPix = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK4PFJets"),
    filter = cms.bool(False),
    cut = cms.string("!(phi<-0.60 && phi>-1.40) && !(phi>2.30 && phi<3.15)")
)


process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsBPix
process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsFPix
process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsBPixPlus
process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsBPixMinus
process.HLTAK4PFJetsReconstructionSequence += process.hltAK4PFJetsnoBPix

# [-1.20 , -0.80]
process.hltAK8PFJetsBPix = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK8PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi<-0.80 && phi>-1.20")
)

process.hltAK8PFJetsFPix = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK8PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi>2.30 && phi<3.15")
)

# [-0.80 , -0.40]
process.hltAK8PFJetsBPixPlus = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK8PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi<-0.40 && phi>-0.80")
)

# [-1.60 , -1.20]
process.hltAK8PFJetsBPixMinus = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK8PFJets"),
    filter = cms.bool(False),
    cut = cms.string("phi<-1.20 && phi>-1.60")
)

# Not in [-1.60 , -0.40]
process.hltAK8PFJetsnoBPix = cms.EDFilter( "PFJetSelector",
    src = cms.InputTag("hltAK8PFJets"),
    filter = cms.bool(False),
    cut = cms.string("!(phi<-0.40 && phi>-1.60) && !(phi>2.30 && phi<3.15)")
)


process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsBPix
process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsFPix
process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsBPixPlus
process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsBPixMinus
process.HLTAK8PFJetsReconstructionSequence += process.hltAK8PFJetsnoBPix

###
### Jet Response Analyzer (JRA) NTuple
###
from JMETriggerAnalysis.JESCorrections.jescJRA_utils import addJRAPath


addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfHLT'       , recoJets = 'hltAK4PFJets'+(str(opts.bpixMode) if opts.bpixMode else '')      , rho = 'hltFixedGridRhoFastjetAll')
addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8pfHLT'       , recoJets = 'hltAK8PFJets'+(str(opts.bpixMode) if opts.bpixMode else '')         , rho = 'hltFixedGridRhoFastjetAll')

if (opts.bpixMode is None) or (opts.bpixMode == 'noBPix'):  
  addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4caloHLT'     , recoJets = 'hltAK4CaloJets'      , rho = 'hltFixedGridRhoFastjetAllCalo')
  addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8caloHLT'     , recoJets = 'hltAK8CaloJets'      , rho = 'hltFixedGridRhoFastjetAllCalo')

if opts.reco == 'mixedPFPuppi':
  # [-1.20 , -0.80]
  process.hltAK4PFPuppiJetsBPix = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFPuppiJets"),
      filter = cms.bool(False),
      cut = cms.string("phi<-0.80 && phi>-1.20")
  )

  process.hltAK4PFPuppiJetsFPix = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFPuppiJets"),
      filter = cms.bool(False),
      cut = cms.string("phi>2.30 && phi<3.15")
  )

  # [-0.80 , -0.60]
  process.hltAK4PFPuppiJetsBPixPlus = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFPuppiJets"),
      filter = cms.bool(False),
      cut = cms.string("phi<-0.60 && phi>-0.80")
  )

  # [-1.40 , -1.20]
  process.hltAK4PFPuppiJetsBPixMinus = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFPuppiJets"),
      filter = cms.bool(False),
      cut = cms.string("phi<-1.20 && phi>-1.40")
  )

  # Not in [-1.40 , -0.60]
  process.hltAK4PFPuppiJetsnoBpix = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFPuppiJets"),
      filter = cms.bool(False),
      cut = cms.string("!(phi<-0.60 && phi>-1.40) && !(phi>2.30 && phi<3.15)")
  )


  process.HLTAK4PFPuppiJetsSequence += process.hltAK4PFPuppiJetsBPix
  process.HLTAK4PFPuppiJetsSequence += process.hltAK4PFPuppiJetsFPix
  process.HLTAK4PFPuppiJetsSequence += process.hltAK4PFPuppiJetsBPixPlus
  process.HLTAK4PFPuppiJetsSequence += process.hltAK4PFPuppiJetsBPixMinus
  process.HLTAK4PFPuppiJetsSequence += process.hltAK4PFPuppiJetsnoBpix


  # [-1.20 , -0.80]
  process.hltAK4PFCHSJetsBPix = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFCHSJets"),
      filter = cms.bool(False),
      cut = cms.string("phi<-0.80 && phi>-1.20")
  )

  process.hltAK4PFCHSJetsFPix = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFCHSJets"),
      filter = cms.bool(False),
      cut = cms.string("phi>2.30 && phi<3.15")
  )

  # [-0.80 , -0.60]
  process.hltAK4PFCHSJetsBPixPlus = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFCHSJets"),
      filter = cms.bool(False),
      cut = cms.string("phi<-0.60 && phi>-0.80")
  )

  # [-1.40 , -1.20]
  process.hltAK4PFCHSJetsBPixMinus = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFCHSJets"),
      filter = cms.bool(False),
      cut = cms.string("phi<-1.20 && phi>-1.40")
  )

  # Not in [-1.40 , -0.60]
  process.hltAK4PFCHSJetsnoBpix = cms.EDFilter( "PFJetSelector",
      src = cms.InputTag("hltAK4PFCHSJets"),
      filter = cms.bool(False),
      cut = cms.string("!(phi<-0.60 && phi>-1.40) && !(phi>2.30 && phi<3.15)")
  )


  process.HLTAK4PFCHSJetsSequence += process.hltAK4PFCHSJetsBPix
  process.HLTAK4PFCHSJetsSequence += process.hltAK4PFCHSJetsFPix
  process.HLTAK4PFCHSJetsSequence += process.hltAK4PFCHSJetsBPixPlus
  process.HLTAK4PFCHSJetsSequence += process.hltAK4PFCHSJetsBPixMinus
  process.HLTAK4PFCHSJetsSequence += process.hltAK4PFCHSJetsnoBpix

  addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfchsHLT'    , recoJets = 'hltAK4PFCHSJets'+(str(opts.bpixMode) if opts.bpixMode else '')    , rho = 'hltFixedGridRhoFastjetAll')
  addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfpuppiHLT'  , recoJets = 'hltAK4PFPuppiJets'+(str(opts.bpixMode) if opts.bpixMode else '')  , rho = 'hltFixedGridRhoFastjetAll')


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

## update process.GlobalTag.globaltag
#if opts.globalTag is not None:
#   from Configuration.AlCa.GlobalTag import GlobalTag
#   process.GlobalTag = GlobalTag(process.GlobalTag, opts.globalTag, '')

# select luminosity sections from .json file
if opts.lumis is not None:
   import FWCore.PythonUtilities.LumiList as LumiList
   process.source.lumisToProcess = LumiList.LumiList(filename = opts.lumis).getVLuminosityBlockRange()

# create TFileService to be accessed by JRA-NTuple plugin
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# input EDM files [primary]
if opts.inputFiles:
   process.source.fileNames = opts.inputFiles
else:
   process.source.fileNames = [
     '/store/mc/Run3Winter25Digi/QCD_Bin-Pt-15to7000_TuneCP5_13p6TeV_pythia8/GEN-SIM-RAW/FlatPU0to120_142X_mcRun3_2025_realistic_v7-v3/90000/01264d3b-3e70-4995-aeea-ce434d408b6e.root',
   ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
   process.source.secondaryFileNames = cms.untracked.vstring()
if opts.secondaryInputFiles:
   process.source.secondaryFileNames = opts.secondaryInputFiles

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# printouts
if opts.verbosity > 0:
   print('--- jescJRA_cfg.py ---')
   print('')
   print('option: output =', opts.output)
   print('option: reco =', opts.reco)
   print('option: dumpPython =', opts.dumpPython)
   print('')
   print('process.GlobalTag =', process.GlobalTag.dumpPython())
   print('process.source =', process.source.dumpPython())
   print('process.maxEvents =', process.maxEvents.dumpPython())
   print('process.options =', process.options.dumpPython())
   print('----------------------')
