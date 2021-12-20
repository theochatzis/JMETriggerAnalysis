###
### config to create a .db file with payload for PF-Hadron Calibrations
###

# command-line arguments
import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('dumpPython', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to python file with content of cms.Process')

opts.register('verbosity', 0,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.int,
              'level of output verbosity')

opts.register('inputJson', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to input .json file with PF-Hadron calibration functions')

opts.register('tag', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'name of the tag in the output .db file')

opts.register('output', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'path to output .db file')

opts.parseArguments()

if opts.inputJson is None:
  raise RuntimeError('command-line argument "inputJson" not specified')
else:
  if not os.path.isfile(opts.inputJson):
    raise RuntimeError('invalid path for command-line argument "inputJson": '+opts.inputJson)

if opts.tag is None:
  raise RuntimeError('command-line argument "tag" not specified')
else:
  if ' ' in opts.tag:
    raise RuntimeError('invalid format for command-line argument "tag": '+opts.tag)

if opts.output is None:
  raise RuntimeError('command-line argument "output" not specified')
else:
  if os.path.exists(opts.output):
    raise RuntimeError('target path to output .db file already exists: '+opts.output)

if opts.verbosity >= 0:
  print '-'*100
  print 'input .json file:', opts.inputJson
  print 'name of the record\'s tag:', opts.tag
  print 'output .db file:', opts.output
  print '-'*100

# process
import FWCore.ParameterSet.Config as cms
process = cms.Process('PFHC')

listFromJson = json.load(open(opts.inputJson, 'r'))
if not isinstance(listFromJson, list):
  raise RuntimeError('file under "inputJson" does not contain a list: '+opts.inputJson)

if opts.verbosity >= 1:
  print listFromJson

vpset_toWrite = cms.VPSet()
for _tmp in listFromJson:
  vpset_toWrite.append(cms.PSet(
    fType = cms.untracked.string(_tmp['fType']),
    formula = cms.untracked.string(_tmp['formula']),
    limits = cms.untracked.vdouble(_tmp['limits']),
    parameters = cms.untracked.vdouble(_tmp['parameters']),
  ))

process.pfCalObj = cms.EDAnalyzer('ProducePFCalibrationObject',
  read = cms.untracked.bool(False),
  write = cms.untracked.bool(True),
  toWrite = vpset_toWrite,
)

from CondCore.DBCommon.CondDBCommon_cfi import CondDBCommon as _CondDBCommon
process.PoolDBOutputService = cms.Service('PoolDBOutputService',
  _CondDBCommon.clone(connect = 'sqlite_file:'+opts.output),
  toPut = cms.VPSet(
    cms.PSet(
      tag = cms.string(opts.tag),
      record = cms.string('PFCalibrationRcd'),
      timetype = cms.untracked.string('runnumber'),
    ),
  ),
  loadBlobStreamer = cms.untracked.bool(False),
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.source = cms.Source('EmptySource')

process.p = cms.Path(process.pfCalObj)

# dump content of cms.Process to python file
if opts.dumpPython is not None:
  open(opts.dumpPython, 'w').write(process.dumpPython())
