# adapted from https://github.com/cms-jet/DBUploadTools/blob/23871ac77e6a09db595dce08144013c9d955db26/JEC/createDBFromTxtFiles.py
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as vpo
from CondCore.CondDB.CondDB_cfi import CondDB as _CondDB
import os
import glob

argDoc_input = 'prefix of paths to JESC .txt files (to be glob-ed with *.txt)'

opts = vpo.VarParsing()

opts.register('input', None,
  vpo.VarParsing.multiplicity.singleton,
  vpo.VarParsing.varType.string,
  argDoc_input,
)

opts.register('output', '.',
  vpo.VarParsing.multiplicity.singleton,
  vpo.VarParsing.varType.string,
  'path to output directory',
)

opts.register('dumpPython', None,
  vpo.VarParsing.multiplicity.singleton,
  vpo.VarParsing.varType.string,
  'path to python file with content of cms.Process',
)

opts.parseArguments()

if opts.input is None:
  raise RuntimeError('failed to specify command-line argument "input" ('+argDoc_input+')')

glob_pattern = os.path.abspath(opts.input)
if os.path.isdir(glob_pattern):
  glob_pattern += '/'
glob_pattern += '*.txt'
textFiles = glob.glob(glob_pattern)

algosPerEraDict = {}
for _txtFile in sorted(textFiles):
  _basename_woext = os.path.basename(_txtFile)[:-4]
  _basename_woext_split = _basename_woext.split('_')
  if len(_basename_woext_split) < 3:
    print ('invalid input file (unsupported name format): '+_txtFile)
    continue
  _algo = _basename_woext_split[-1]
  _level = _basename_woext_split[-2]
  _era = '_'.join(_basename_woext_split[:-2])
  if _era not in algosPerEraDict: algosPerEraDict[_era] = {}
  relDirPath = os.path.relpath(os.path.dirname(_txtFile), os.environ['CMSSW_BASE']+'/src')+'/'
  if _algo in algosPerEraDict[_era] and algosPerEraDict[_era][_algo] != relDirPath:
    raise RuntimeError('logic error: attempt to overwrite directory for (era = "'+_era+'", algo = "'+_algo+'"): '+relDirPath)
  algosPerEraDict[_era][_algo] = relDirPath

if len(algosPerEraDict.keys()) == 0:
  raise RuntimeError('no valid input files found')
elif len(algosPerEraDict.keys()) != 1:
  raise RuntimeError('handling of multiple eras is not currently supported: eras='+str(algosPerEraDict.keys()))

process = cms.Process('jecdb')
process.source = cms.Source('EmptySource')
process.maxEvents.input = cms.untracked.int32(0)
process.seq = cms.Sequence()
process.p = cms.Path(process.seq)

if not os.path.isdir(opts.output):
  os.makedirs(opts.output)

for _era in sorted(algosPerEraDict.keys()):
  _dbFilePath = opts.output+'/'+_era+'.db'
  if os.path.exists(_dbFilePath):
    raise RuntimeError("target output .db file already exists (delete or rename it, and try again): "+_dbFilePath)

  _modTag = '' #''.join(_tmp for _tmp in _era if _tmp.isalnum())

  setattr(process, 'CondDB'+_modTag,
    _CondDB.clone(connect = 'sqlite_file:'+_dbFilePath))

  setattr(process, 'PoolDBOutputService'+_modTag,
    cms.Service('PoolDBOutputService', getattr(process, 'CondDB'+_modTag), toPut = cms.VPSet()))

  for _algo in sorted(algosPerEraDict[_era].keys()):
    _relDirPath = algosPerEraDict[_era][_algo]

    getattr(process, 'PoolDBOutputService'+_modTag).toPut += [cms.PSet(
      record = cms.string(_algo),
      tag = cms.string('JetCorrectorParametersCollection_{:}_{:}'.format(_era, _algo)),
      label = cms.string(_algo),
    )]

    setattr(process, 'jecDBWriter'+_algo, cms.EDAnalyzer('JetCorrectorDBWriter',
      era = cms.untracked.string(_era),
      algo = cms.untracked.string(_algo),
      path = cms.untracked.string(_relDirPath),
    ))

    process.seq += getattr(process, 'jecDBWriter'+_algo)

# dump content of cms.Process to python file
if opts.dumpPython is not None:
  open(opts.dumpPython, 'w').write(process.dumpPython())
