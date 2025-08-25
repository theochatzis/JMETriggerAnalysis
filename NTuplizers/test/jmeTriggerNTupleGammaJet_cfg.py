import os
import fnmatch
import csv 

from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB

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
opts.register('reco', 'default',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'keyword to define HLT reconstruction')

opts.register('sampletype', 'data',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
                'keyword either "mc" or "data" to define whether working on data or MC. Default is "data".')

opts.register('output', 'out.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('keepPFPuppi', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'keep full collection of PFlow and PFPuppi candidates')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('jecDBfile', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to db file used for HLT jecs - in case it is used the jecs will be automatically updated.'
)

opts.register('pfhcDBfile', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to db file used for HLT pfhcs - in case it is used the pfhcs will be automatically updated.'
)



#opts.register('printSummaries', False,
#              vpo.VarParsing.multiplicity.singleton,
#              vpo.VarParsing.varType.bool,
#              'show summaries from HLT services')

opts.parseArguments()

###
### HLT configuration
###
##from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_15_0_0_GRun_configDump_data import cms, process

if opts.sampletype == 'data':
    from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_15_0_0_GRun_configDump_data import cms, process
elif opts.sampletype == 'mc':
    from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_15_0_0_GRun_configDump_mc import cms, process
else:
    raise RuntimeError('keyword "sampletype = '+opts.sampletype'" not recognised or not given.')


if opts.reco == 'default':
    if opts.sampletype =='data':
        process.GlobalTag.globaltag = cms.string('150X_dataRun3_HLT_v1') # DATA (DEFAULT) GLOBAL TAG used for HCAL resp. corr. investigations (August '25)
    elif opts.sampletype =='mc':
        process.GlobalTag.globaltag = cms.string('142X_mcRun3_2025_realistic_v7') # MONTE CARLO GLOBAL TAG
elif opts.reco == 'hcal_hbhe':
  process.GlobalTag.globaltag = cms.string('150X_dataRun3_HLT_HCAL_HBHE_Target_w30_v1')
elif opts.reco == 'hcal_alcaraw':
  process.GlobalTag.globaltag = cms.string('150X_dataRun3_HLT_HCAL_AlCaRAW_Target_w30_v1')
elif opts.reco == 'hcal_depth1':
  process.GlobalTag.globaltag = cms.string('150X_dataRun3_HLT_HCAL_Depth1_Target_w30_v1')
elif opts.reco == 'hcal_depth12':
  process.GlobalTag.globaltag = cms.string('150X_dataRun3_HLT_HCAL_Depth12_Target_w30_v1')

else:
  raise RuntimeError('keyword "reco = '+opts.reco+'" not recognised')

# Set the latest Global Tag
#process.GlobalTag.globaltag = cms.string('140X_dataRun3_HLT_v3')
if opts.globalTag != None:
  process.GlobalTag.globaltag = cms.string(opts.globalTag)

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

# list of patterns to determine paths to keep
keepPaths = [
  'MC_*Jets*',
  'MC_*MET*',
  'MC_*AK8Calo*',
  'MC_*HT*',
  'HLT_*Photon*TightID_TightIso*',
  # 'HLT_PFJet*_v*',
  # 'HLT_AK4PFJet*_v*',
  # 'HLT_AK8PFJet*_v*',
  # 'AlCa_*Jet*',
  # 'HLT_PFHT*_v*',
  # 'HLT_PFMET*_PFMHT*_v*',
  # 'HLT_IsoMu27_v*',
]

vetoPaths = [
  'HLT_*ForPPRef_v*',
]

# list of paths that are kept
listOfPaths = []

for _modname in sorted(process.paths_()):
    _keepPath = False
    for _tmpPatt in keepPaths:
      _keepPath = fnmatch.fnmatch(_modname, _tmpPatt)
      if _keepPath: break

    if _keepPath:
      for _tmpPatt in vetoPaths:
        if fnmatch.fnmatch(_modname, _tmpPatt):
          _keepPath = False
          break

    if _keepPath:
      print('{:<99} | {:<4} |'.format(_modname, '+'))
      listOfPaths.append(_modname)
      continue
    _mod = getattr(process, _modname)
    if type(_mod) == cms.Path:
      process.__delattr__(_modname)
      print('{:<99} | {:<4} |'.format(_modname, ''))
print('-'*108)

# remove FastTimerService
if hasattr(process, 'FastTimerService'):
  del process.FastTimerService

###
### customisations
###

## customised JME collections
from JMETriggerAnalysis.Common.customise_hlt import *
#process = addPaths_MC_JMECalo(process)
#process = addPaths_MC_JMEPFCluster(process)
#process = addPaths_MC_JMEPF(process)
#process = addPaths_MC_JMEPFCHS(process)
#process = addPaths_MC_JMEPFPuppi(process)

#process.MC_PFMET_v20 = cms.Path(
#    process.SimL1Emulator
#  +process.HLTBeginSequence
#  +process.hltPreMCPFMET
#  +process.HLTAK4PFJetsSequence
#  +process.hltPFMETProducer
#  +process.hltcorrPFMETTypeOne
#  +process.hltPFMETTypeOne
#  +process.hltPFMETOpenFilter
#  +process.HLTEndSequence
#)

#process.MC_CaloHT_v11 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltPreMCCaloHT+process.HLTAK4CaloJetsSequence+process.hltHtMhtForMC+process.hltHtMhtJet30+process.hltCaloHTOpenFilter+process.HLTEndSequence)
#process.MC_PFHT_v19 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltPreMCPFHT+process.HLTAK4PFJetsSequence+process.hltPFHTForMC+process.hltPFHTJet30+process.hltPFHTOpenFilter+process.HLTEndSequence)

# check using only L1T for one path:
# process.HLT_PFJet140_v22 = cms.Path(
#   process.SimL1Emulator
# + process.HLTBeginSequence
# + process.hltL1sSingleJet90
# + process.HLTEndSequence
# )


if opts.pfhcDBfile is not None:
  ## ES modules for PF-Hadron Calibrations
  
  process.pfhcESSource = cms.ESSource('PoolDBESSource',
    # In case you want to run with condor need to specify it with the CMSSW_BASE as follows:
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/PFCalibration.db'),
    _CondDB.clone(connect = f'sqlite_file:{opts.pfhcDBfile}'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('PFCalibrationRcd'),
        tag = cms.string('PFCalibration_HLT_133X_mcRun3_2024_realistic_v9'),
        label = cms.untracked.string('HLT'),
      ),
    ),
  )
  process.pfhcESPrefer = cms.ESPrefer('PoolDBESSource', 'pfhcESSource')
  #process.hltParticleFlow.calibrationsLabel = '' # standard label for Offline-PFHC in GT

if opts.jecDBfile is not None:
  ##ES modules for HLT JECs
  process.jescESSource = cms.ESSource('PoolDBESSource',
    # In case you want to run with condor need to specify it with the CMSSW_BASE as follows:
    #_CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Run3Winter23Digi.db'),
    _CondDB.clone(connect = f'sqlite_file:{opts.jecDBfile}'),
    toGet = cms.VPSet(
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK4CaloHLT'),
        label = cms.untracked.string('AK4CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK4PFHLT'),
        label = cms.untracked.string('AK4PFHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK8CaloHLT'),
        label = cms.untracked.string('AK8CaloHLT'),
      ),
      cms.PSet(
        record = cms.string('JetCorrectionsRecord'),
        tag = cms.string('JetCorrectorParametersCollection_Run3Winter24Digi_AK8PFHLT'),
        label = cms.untracked.string('AK8PFHLT'),
      ),
    ),
  )
  process.jescESPrefer = cms.ESPrefer('PoolDBESSource', 'jescESSource')

# -- adding the offline jecs separately
# process.offlinejescESSource = cms.ESSource('PoolDBESSource',
#   _CondDB.clone(connect = 'sqlite_file:'+os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/Winter23Prompt23_RunA_V1_DATA.db'),
#   #_CondDB.clone(connect = 'sqlite_file:Winter23Prompt23_RunA_V1_DATA.db'),
#   toGet = cms.VPSet(
#     cms.PSet(
#       record = cms.string('JetCorrectionsRecord'),
#       tag = cms.string('JetCorrectorParametersCollection_Winter23Prompt23_RunA_V1_DATA_AK4PFPuppi'),
#       label = cms.untracked.string('AK4PFPuppi'),
#     ),
#     cms.PSet(
#       record = cms.string('JetCorrectionsRecord'),
#       tag = cms.string('JetCorrectorParametersCollection_Winter23Prompt23_RunA_V1_DATA_AK8PFPuppi'),
#       label = cms.untracked.string('AK8PFPuppi'),
#     ),
#   ),
# )
# process.offlinejescESPrefer = cms.ESPrefer('PoolDBESSource', 'offlinejescESSource')

#--- Updating offline JECs 
#from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
# Load JECs
#jecLevels = ['L1FastJet', 'L2Relative', 'L3Absolute','L2L3Residual']
#jecToUse = cms.vstring(jecLevels)
#updateJetCollection(
#    process,
#    jetSource=cms.InputTag("slimmedJetsPuppi"),  # Input PAT jet collection
#    labelName="AK4PFPuppi",  # Label for the updated jet collection - will become patJetCorrFactors[labelName]
#    jetCorrections=("AK4PFPuppi", jecToUse, "None"),  # JECs to be applied
#)

#updateJetCollection(
#    process,
#    jetSource=cms.InputTag("slimmedJetsAK8"),  # Input PAT jet collection
#    labelName="AK8PFPuppi",  # Label for the updated jet collection - will become patJetCorrFactors[labelName]
#    jetCorrections=("AK8PFPuppi", jecToUse, "None"),  # JECs to be applied
#)

#process.jecSequence = cms.Sequence(process.patJetCorrFactorsAK4PFPuppi * process.updatedPatJetsAK4PFPuppi * process.patJetCorrFactorsAK8PFPuppi * process.updatedPatJetsAK8PFPuppi)
#process.offlineJecPath = cms.Path(process.jecSequence)
#process.schedule.append(process.offlineJecPath)




# ### selection of specific events to fill
# # CSV file with columns:
# #Run,Lumi,Event
# specificEventsFile = os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/events_tr_fail_ht1050.csv'

# # Open the CSV file
# with open(specificEventsFile,'r') as file:
#     # Create a CSV reader object
#     reader = csv.reader(file)
    
#     # Read the first row to get the column names
#     headers = next(reader)
    
#     # Create empty lists for each column
#     columns = [[] for _ in headers]
    
#     # Iterate over each row in the CSV file
#     for row in reader:
#         # Iterate over each value in the row and append it to the respective column list
#         for i, value in enumerate(row):
#             columns[i].append(int(value)) # convert string to int and append to each column

## Output NTuple
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

process.JMETriggerNTuple = cms.EDAnalyzer('JMETriggerNTuple',
  TTreeName = cms.string('Events'),
  TriggerResults = cms.InputTag('TriggerResults'),
  TriggerResultsFilterOR = cms.vstring(),
  TriggerResultsFilterAND = cms.vstring(),
  TriggerResultsCollections = cms.vstring(
    sorted(list(set([(_tmp[:_tmp.rfind('_v')] if '_v' in _tmp else _tmp) for _tmp in listOfPaths])))
  ),
  # SelectionRun = cms.vuint32(columns[0]),
  # SelectionLumi = cms.vuint32(columns[1]),
  # SelectionEvent = cms.vuint32(columns[2]),
  outputBranchesToBeDropped = cms.vstring(),

  #HepMCProduct = cms.InputTag('generatorSmeared'),
  #GenEventInfoProduct = cms.InputTag('generator'),
  #PileupSummaryInfo = cms.InputTag('addPileupInfo'),

  doubles = cms.PSet(

    #hltFixedGridRhoFastjetAllCalo = cms.InputTag('hltFixedGridRhoFastjetAllCalo'),
    #hltFixedGridRhoFastjetAllPFCluster = cms.InputTag('hltFixedGridRhoFastjetAllPFCluster'),
    hltFixedGridRhoFastjetAll = cms.InputTag('hltFixedGridRhoFastjetAll'),
    
    #offlineFixedGridRhoFastjetAll = cms.InputTag('fixedGridRhoFastjetAll::RECO'),

    #hltPixelClustersMultiplicity = cms.InputTag('hltPixelClustersMultiplicity'),
  ),

  vdoubles = cms.PSet(
  ),

  recoVertexCollections = cms.PSet(

    #hltPixelVertices = cms.InputTag('hltPixelVertices'),
    #hltTrimmedPixelVertices = cms.InputTag('hltTrimmedPixelVertices'),
    #hltVerticesPF = cms.InputTag('hltVerticesPF'),
    #offlinePrimaryVertices = cms.InputTag('offlineSlimmedPrimaryVertices'),
  ),

  recoPFCandidateCollections = cms.PSet(
  ),

  recoGenJetCollections = cms.PSet(

    #ak4GenJetsNoNu = cms.InputTag('ak4GenJetsNoNu::HLT'),
    #ak8GenJetsNoNu = cms.InputTag('ak8GenJetsNoNu::HLT'),
  ),

  recoCaloJetCollections = cms.PSet(

    #hltAK4CaloJets = cms.InputTag('hltAK4CaloJets'),
    #hltAK4CaloJetsCorrected = cms.InputTag('hltAK4CaloJetsCorrected'),

    #hltAK8CaloJets = cms.InputTag('hltAK8CaloJets'),
    #hltAK8CaloJetsCorrected = cms.InputTag('hltAK8CaloJetsCorrected'),
  ),

  recoPFClusterJetCollections = cms.PSet(

    #hltAK4PFClusterJets = cms.InputTag('hltAK4PFClusterJets'),
    #hltAK4PFClusterJetsCorrected = cms.InputTag('hltAK4PFClusterJetsCorrected'),

    #hltAK8PFClusterJets = cms.InputTag('hltAK8PFClusterJets'),
    #hltAK8PFClusterJetsCorrected = cms.InputTag('hltAK8PFClusterJetsCorrected'),
  ),

  recoPFJetCollections = cms.PSet(

    #hltAK4PFJets = cms.InputTag('hltAK4PFJets'),
    hltAK4PFJetsCorrected = cms.InputTag('hltAK4PFJetsCorrected'),
    #hltAK4PFJetsTightIDCorrected = cms.InputTag('hltAK4PFJetsTightIDCorrected'),
    #hltAK4PFCHSJets = cms.InputTag('hltAK4PFCHSJets'),
    #hltAK4PFCHSJetsCorrected = cms.InputTag('hltAK4PFCHSJetsCorrected'),

    #hltAK4PFPuppiJets = cms.InputTag('hltAK4PFPuppiJets'),
    #hltAK4PFPuppiJetsCorrected = cms.InputTag('hltAK4PFPuppiJetsCorrected'),

    #hltAK8PFJets = cms.InputTag('hltAK8PFJets'),
    #hltAK8PFJetsCorrected = cms.InputTag('hltAK8PFJetsCorrected'),

    #hltAK8PFCHSJets = cms.InputTag('hltAK8PFCHSJets'),
    #hltAK8PFCHSJetsCorrected = cms.InputTag('hltAK8PFCHSJetsCorrected'),

    #hltAK8PFPuppiJets = cms.InputTag('hltAK8PFPuppiJets'),
    #hltAK8PFPuppiJetsCorrected = cms.InputTag('hltAK8PFPuppiJetsCorrected'),

  ),

  patJetCollections = cms.PSet(
    # default "Slimmed" collections
    #offlineAK4PFCHSJetsCorrected = cms.InputTag('slimmedJets'),
    #offlineAK4PFPuppiJetsCorrected = cms.InputTag('slimmedJetsPuppi'),
    # in case you want to use the offline with updated JECs
    #offlineAK4PFPuppiJetsCorrected = cms.InputTag('updatedPatJetsAK4PFPuppi'),
    #offlineAK8PFPuppiJetsCorrected = cms.InputTag('updatedPatJetsAK8PFPuppi'),
  ),

  recoGenMETCollections = cms.PSet(

    #genMETCalo = cms.InputTag('genMetCalo::HLT'),
    #genMETTrue = cms.InputTag('genMetTrue::HLT'),
  ),
  # recoMETCollections = cms.PSet (
  #   hltCaloHT = cms.InputTag('hltHtMhtJet30'),
  #   hltPFHT = cms.InputTag('hltPFHTJet30')
  # ),
  recoCaloMETCollections = cms.PSet(

    #hltCaloMET = cms.InputTag('hltMet'),
    #hltCaloMETTypeOne = cms.InputTag('hltCaloMETTypeOne'),
  ),

  recoPFClusterMETCollections = cms.PSet(

    #hltPFClusterMET = cms.InputTag('hltPFClusterMET'),
    #hltPFClusterMETTypeOne = cms.InputTag('hltPFClusterMETTypeOne'),
  ),

  recoPFMETCollections = cms.PSet(

    #hltPFMET = cms.InputTag('hltPFMETProducer'),
    #hltPFMETTypeOne = cms.InputTag('hltPFMETTypeOne'),

    #hltPFCHSMET = cms.InputTag('hltPFCHSMET'),
    #hltPFCHSMETTypeOne = cms.InputTag('hltPFCHSMETTypeOne'),

    #hltPFPuppiMET = cms.InputTag('hltPFPuppiMET'),                 #is this the one we need for MPF: I need RawPuppiMET
    #hltPFPuppiMETTypeOne = cms.InputTag('hltPFPuppiMETTypeOne'),
  ),

  patMETCollections = cms.PSet(

    #offlinePFMET = cms.InputTag('slimmedMETs'),
    #offlinePFPuppiMET = cms.InputTag('slimmedMETsPuppi'),
  ),

  recoPhotonCollections = cms.PSet(
    gedPhotons = cms.InputTag('gedPhotons'),
    photons = cms.InputTag('photons'),
  ),
)

if opts.keepPFPuppi:
  process.hltPFPuppi.puppiDiagnostics = True
  process.JMETriggerNTuple.vdoubles = cms.PSet(
    hltPFPuppi_PuppiRawAlphas = cms.InputTag('hltPFPuppi:PuppiRawAlphas'),
    hltPFPuppi_PuppiAlphas = cms.InputTag('hltPFPuppi:PuppiAlphas'),
    hltPFPuppi_PuppiAlphasMed = cms.InputTag('hltPFPuppi:PuppiAlphasMed'),
    hltPFPuppi_PuppiAlphasRms = cms.InputTag('hltPFPuppi:PuppiAlphasRms'),
  )
  process.JMETriggerNTuple.recoPFCandidateCollections = cms.PSet(
    hltParticleFlow = cms.InputTag('hltParticleFlow'),
    hltPFPuppi = cms.InputTag('hltPFPuppi'),
  )

process.analysisNTupleEndPath = cms.EndPath(process.JMETriggerNTuple)
process.schedule.append(process.analysisNTupleEndPath)

###
### standard options
###

# max number of events to be processed
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# multi-threading settings
process.options.numberOfThreads = opts.numThreads
process.options.numberOfStreams = opts.numStreams

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

# input EDM files [primary]
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    #'root://cms-xrd-global.cern.ch//store/data/Run2025C/EGamma0/RAW-RECO/IsoPhotonEB-PromptReco-v1/000/392/175/00000/404a96ad-5571-40d3-a9e0-118a23dc75d0.root'
    '/store/data/Run2025C/EGamma0/RAW-RECO/IsoPhotonEB-PromptReco-v1/000/392/175/00000/0a6dde4c-e1da-429d-9793-c6bb6e9a7f5a.root'
  ]

# input EDM files [secondary]
if not hasattr(process.source, 'secondaryFileNames'):
  process.source.secondaryFileNames = cms.untracked.vstring()

if opts.secondaryInputFiles:
  process.source.secondaryFileNames = opts.secondaryInputFiles
else:
  process.source.secondaryFileNames = [
  ]

#process.source.eventsToProcess = cms.untracked.VEventRange("325057:61751881")

# dump content of cms.Process to python file
if opts.dumpPython is not None:
   open(opts.dumpPython, 'w').write(process.dumpPython())

# printouts
if opts.verbosity > 0:
   print('--- jmeTriggerNTuple_cfg.py ---')
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
