#!/usr/bin/env python
import json
from JMETriggerAnalysis.NTuplizers.utils.common import *

dset = '/EphemeralHLTPhysics1/Run2018D-v1/RAW'
run = 323775
lumiBlocks = [ls for ls in range(52,152) if ls not in [71, 72, 78, 82, 83]]

outputFile = 'tmp.json'
verbosity = 1

###

dsetDict = {"DAS": dset, 'files': []}

edmFiles = []
for lumiBlock in lumiBlocks:
  edmFilesTmp = get_output('dasgoclient -query "file run='+str(run)+' dataset='+dset+' lumi='+str(lumiBlock)+'"')
  edmFilesTmp = [edmFile.replace('\n', '') for edmFile in edmFilesTmp]
  edmFilesTmp = [edmFile for edmFile in edmFilesTmp if edmFile]
  edmFiles += edmFilesTmp

  if verbosity > 0:
    print edmFilesTmp

edmFiles = sorted(list(set(edmFiles)))

for edmFile in edmFiles:

  edmFileNEvents = get_output('dasgoclient -query "file='+edmFile+' | grep file.nevents"')
  edmFileNEvents = [nEvt.replace('\n', '') for nEvt in edmFileNEvents]
  edmFileNEvents = [nEvt for nEvt in edmFileNEvents if nEvt]

  if len(edmFileNEvents) != 1:
    raise RuntimeError(edmFileNEvents)

  dsetDict['files'] += [{
    'file': edmFile,
    'nevents': int(edmFileNEvents[0]),
    'parentFiles_1': [],
    'parentFiles_2': [],
  }]

  if verbosity > 0:
    print dsetDict['files'][-1]

json.dump(dsetDict, open(outputFile, 'w'), sort_keys=True, indent=2)
