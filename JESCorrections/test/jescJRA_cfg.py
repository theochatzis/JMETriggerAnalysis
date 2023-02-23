import fnmatch

###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

# options to control puppi tuning at different regions
opts.register('puppiParamsHB',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HB region given as [parameter_name]:[parameter_scale] ')

opts.register('puppiParamsHE1',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HE1 region given as [parameter_name]:[parameter_scale] ')

opts.register('puppiParamsHE2',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HE2 region given as [parameter_name]:[parameter_scale] ')

opts.register('puppiParamsHF',[],
             vpo.VarParsing.multiplicity.list,
             vpo.VarParsing.varType.string,
             'puppi parameters factors for HF region given as [parameter_name]:[parameter_scale] ')
             
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
opts.register('useMixedTrk',False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'use  full + pixel tracks in PF')
              
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

#from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_3_0_GRun_configDump import cms, process
from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_12_4_0_GRun_configDump import cms, process

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

###
### customisations
###

## customised JME collections
from JMETriggerAnalysis.Common.customise_hlt import addPaths_MC_JMEPFCluster, addPaths_MC_JMEPFCHS, addPaths_MC_JMEPFPuppi
process = addPaths_MC_JMEPFCluster(process)
process = addPaths_MC_JMEPFCHS(process)

puppi_modifications_list = []
for param_change in opts.puppiParamsHB:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HB',parameter_name, parameter_scale])

for param_change in opts.puppiParamsHE1:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HE1',parameter_name, parameter_scale]) 

for param_change in opts.puppiParamsHE2:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HE2',parameter_name, parameter_scale])

for param_change in opts.puppiParamsHF:
     parameter_name, parameter_scale = param_change.split(':')
     puppi_modifications_list.append(['HF',parameter_name, parameter_scale])

process = addPaths_MC_JMEPFPuppi(process, puppi_modifications_list) # added empty PUPPI modifications list

###
### updating Phase 0 HCAL thresholds
###

#process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].name = "PFRecHitQTestHCALThresholdVsDepth"
#del process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].threshold

## ECAL UL calibrations
process.GlobalTag.toGet = cms.VPSet(
 cms.PSet(record = cms.string("EcalLaserAlphasRcd"),
 tag = cms.string("EcalLaserAlphas_UL_Run1_Run2_2018_lastIOV_movedTo1"),
 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
 ),
 cms.PSet(record = cms.string("EcalIntercalibConstantsRcd"),
 tag = cms.string("EcalIntercalibConstants_UL_Run1_Run2_2018_lastIOV_movedTo1"),
 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
 ),)

## ES modules for PF-Hadron Calibrations
import os

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB
process.pfhcESSource = cms.ESSource('PoolDBESSource',
  #_CondDB.clone(connect = 'sqlite_file:PFCalibration.db'),
  _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/PFHC_Run3Summer21_MC.db'),
  toGet = cms.VPSet(
    cms.PSet(
      record = cms.string('PFCalibrationRcd'),
      tag = cms.string('PFCalibration_CMSSW_12_4_0_pre3_HLT_112X_mcRun3_2022'),
      label = cms.untracked.string('HLT'),
    ),
  ),
)
process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
#process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

if opts.useMixedTrk:
  from HLTrigger.Configuration.customizeHLTforMixedPF import customizeHLTForMixedPF
  process = customizeHLTForMixedPF(process)

###
### Jet Response Analyzer (JRA) NTuple
###
from jescJRA_utils import addJRAPath

#addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4caloHLT'     , recoJets = 'hltAK4CaloJets'     , rho = 'hltFixedGridRhoFastjetAllCalo')
addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfHLT'       , recoJets = 'hltAK4PFJets'       , rho = 'hltFixedGridRhoFastjetAll')
#addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfclusterHLT', recoJets = 'hltAK4PFClusterJets', rho = 'hltFixedGridRhoFastjetAllPFCluster')
#addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfchsHLT'    , recoJets = 'hltAK4PFCHSJets'    , rho = 'hltFixedGridRhoFastjetAll')
addJRAPath(process, genJets = 'ak4GenJetsNoNu', maxDeltaR = 0.2, moduleNamePrefix = 'ak4pfpuppiHLT'  , recoJets = 'hltAK4PFPuppiJets'  , rho = 'hltFixedGridRhoFastjetAll')

#addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8caloHLT'     , recoJets = 'hltAK8CaloJets'     , rho = 'hltFixedGridRhoFastjetAllCalo')
#addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8pfHLT'       , recoJets = 'hltAK8PFJets'       , rho = 'hltFixedGridRhoFastjetAll')
#addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8pfclusterHLT', recoJets = 'hltAK8PFClusterJets', rho = 'hltFixedGridRhoFastjetAllPFCluster')
#addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8pfchsHLT'    , recoJets = 'hltAK8PFCHSJets'    , rho = 'hltFixedGridRhoFastjetAll')
#addJRAPath(process, genJets = 'ak8GenJetsNoNu', maxDeltaR = 0.4, moduleNamePrefix = 'ak8pfpuppiHLT'  , recoJets = 'hltAK8PFPuppiJets'  , rho = 'hltFixedGridRhoFastjetAll')

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
     #'',
     '/store/mc/Run3Summer21DR/QCD_Pt15to7000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU0to80FEVT_castor_120X_mcRun3_2021_realistic_v6-v1/30000/0d8a6361-5115-49d3-86a4-4dbeca2e2fd6.root'
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
