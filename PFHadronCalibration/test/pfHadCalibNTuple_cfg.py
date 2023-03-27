###
### command-line arguments
###
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('skipEvents', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of events to be skipped')

opts.register('numThreads', 1,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of threads')

opts.register('numStreams', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'number of streams')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('output', 'pfHCNTuple.root',
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output ROOT file')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'verbosity level')

opts.parseArguments()

###
### HLT configuration
###

from HLT_dev_CMSSW_13_0_0_GRun_configDump import *
#from HLT_dev_CMSSW_13_0_0_GRun_configDump import cms, process

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
for _modname in sorted(process.paths_()):
  _keepPath = _modname.startswith('MC_') and ('Jets' in _modname or 'MET' in _modname)
  _keepPath |= _modname.startswith('MC_ReducedIterativeTracking')
  if _keepPath:
    print('{:<99} | {:<4} |'.format(_modname, '+'))
    continue
  _mod = getattr(process, _modname)
  if type(_mod) == cms.Path:
    process.__delattr__(_modname)
    print('{:<99} | {:<4} |'.format(_modname, ''))
print('-'*108)

# remove FastTimerService
del process.FastTimerService

###
### PFHC-specific paths
###
process.particleFlowSimParticle = cms.EDProducer('PFSimParticleProducer',
  Fitter = cms.string('KFFittingSmoother'),
  MCTruthMatchingInfo = cms.untracked.bool(False),
  ParticleFilter = cms.PSet(
    EMin = cms.double(0),
    chargedPtMin = cms.double(0),
    etaMax = cms.double(5.3),
    invisibleParticles = cms.vint32(),
    protonEMin = cms.double(5000.0),
    rMax = cms.double(129.0),
    zMax = cms.double(317.0),
  ),
  Propagator = cms.string('PropagatorWithMaterial'),
  RecTracks = cms.InputTag('trackerDrivenElectronSeeds'),
  TTRHBuilder = cms.string('WithTrackAngle'),
  ecalRecHitsEB = cms.InputTag('caloRecHits','EcalRecHitsEB'),
  ecalRecHitsEE = cms.InputTag('caloRecHits','EcalRecHitsEE'),
  fastSimProducer = cms.untracked.InputTag('fastSimProducer','EcalHitsEB'),
  process_Particles = cms.untracked.bool(True),
  process_RecTracks = cms.untracked.bool(False),
  sim = cms.InputTag('g4SimHits'),
  verbose = cms.untracked.bool(False)
)

process.pfHadCalibNTuple = cms.EDAnalyzer('PFHadCalibNTuple',
  TTreeName = cms.string('Candidates'),

  genParticles = cms.InputTag('genParticles'),
  pfSimParticles = cms.InputTag('particleFlowSimParticle'),
  recoPFCandidates = cms.InputTag('hltParticleFlow'),

  genParticleStatus = cms.int32(1), # status code of selected GEN particles
  genParticlePdgId = cms.int32(-211), # pdgID of selected GEN particles
  genParticleIsoMinDeltaR = cms.double(1.0), # min deltaR between "isolated" GEN particles and other GEN particles

  minPt = cms.double(0.01), # min pt
  minTrackP = cms.double(0.01), # min track momentum
  minTrackPt = cms.double(0.01), # min track transverse momentum
  minCaloEnergy = cms.double(0.0), # min ecal+hcal energy
  maxECalEnergy = cms.double(1e12), # max ecal energy

  # min nb of pixel and pixel+strip hits (per track-eta range)
  minPixelHits = cms.vuint32(2, 2, 2, 2, 2),
  minTrackerHits = cms.vuint32(2, 2, 2, 2, 2),
  maxEtaForMinTrkHitsCuts = cms.vdouble(1.4, 1.6, 2.0, 2.5, 999.0),

  usePFBlockElements = cms.bool(True),
)

process.pfSimParticleSeq = cms.Sequence(process.particleFlowSimParticle)
process.pfSimParticlePath = cms.Path(process.pfSimParticleSeq)
process.schedule.append(process.pfSimParticlePath)

process.pfHadCalibNTupleSeq = cms.Sequence(process.pfHadCalibNTuple)
process.pfHadCalibNTupleEndPath = cms.EndPath(process.pfHadCalibNTupleSeq)
process.schedule.append(process.pfHadCalibNTupleEndPath)

###
### updating Phase 0 HCAL thresholds
###

#process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].name = "PFRecHitQTestHCALThresholdVsDepth"
#del process.hltParticleFlowRecHitHBHE.producers[0].qualityTests[0].threshold

###
### ECAL UL calibrations
###

process.GlobalTag.toGet = cms.VPSet(
 cms.PSet(record = cms.string("EcalLaserAlphasRcd"),
 tag = cms.string("EcalLaserAlphas_UL_Run1_Run2_2018_lastIOV_movedTo1"),
 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
 ),
 cms.PSet(record = cms.string("EcalIntercalibConstantsRcd"),
 tag = cms.string("EcalIntercalibConstants_UL_Run1_Run2_2018_lastIOV_movedTo1"),
 connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
 ),)

###
### options
###

# number of events
process.maxEvents.input = opts.maxEvents

# number of events to be skipped
process.source.skipEvents = cms.untracked.uint32(opts.skipEvents)

# number of threads/streams
process.options.numberOfThreads = opts.numThreads
process.options.numberOfStreams = opts.numStreams

process.options.wantSummary = cms.untracked.bool(False)

# input files
if opts.inputFiles:
  process.source.fileNames = opts.inputFiles
else:
  process.source.fileNames = [
    #'/store/mc/Run3Winter21DRMiniAOD/SinglePion_PT0to200/GEN-SIM-DIGI-RAW/NoPUFEVT_112X_mcRun3_2021_realistic_v16-v2/140000/53fc39b0-c12c-419f-ba73-78c4d032ff3e.root',
		#'/store/mc/Run3Summer21DR/Single_Pion_gun_E_2to200_14TeV_pythia8/GEN-SIM-RAW/NoPURAWRECO_120X_mcRun3_2021_realistic_v6-v2/270000/49a1fc5f-af28-4189-9842-399295b12d9e.root',
		#'/store/mc/Run3Winter20DRMiniAOD/SinglePion_PT0to200/GEN-SIM-RAW/NoPU_110X_mcRun3_2021_realistic_v6-v3/10000/037D66E6-1789-3741-9DC4-669B2EDDA263.root',
		'/store/mc/Run3Winter23Digi/SinglePionGun_E0p2to200/GEN-SIM-RAW/NoPU_126X_mcRun3_2023_forPU65_v1-v2/40000/00045a90-b54d-429d-8494-4d6d5148bbb4.root',
  ]

# output file
process.TFileService = cms.Service('TFileService', fileName = cms.string(opts.output))

# dump content of cms.Process to python file
if opts.dumpPython is not None:
  process.prune()
  open(opts.dumpPython, 'w').write(process.dumpPython())
