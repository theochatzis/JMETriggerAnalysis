"""
cmsRun jescDBToTxtConverter_cfg.py gt=GlobalTag [onlyHLT=0|1] [tag=OutputPrefix]
"""
import FWCore.ParameterSet.Config as cms

process = cms.Process('JESCTXT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

import FWCore.ParameterSet.VarParsing as vpo
opts = vpo.VarParsing('analysis')

opts.register('gt', None,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.string,
              'argument of process.GlobalTag.globaltag')

opts.register('onlyHLT', False,
              vpo.VarParsing.multiplicity.singleton,
              vpo.VarParsing.varType.bool,
              'include only HLT-JECs')

opts.parseArguments()

if opts.gt is None:
   raise RuntimeError('name of GlobalTag not specified [use command-line argument "gt=X"]')

process.GlobalTag.globaltag = opts.gt

if not opts.tag:
   opts.tag = opts.gt

import os
opts_tag_dirname = os.path.dirname(opts.tag)
if opts_tag_dirname:
   os.makedirs(opts_tag_dirname)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.source = cms.Source('EmptySource')

process.readAK4CaloHLT = cms.EDAnalyzer('JetCorrectorDBReader',
  # label of DB record
  payloadName = cms.untracked.string('AK4CaloHLT'),

  # print to stdout
  printScreen = cms.untracked.bool(False),

  # create output .txt file(s)
  createTextFile = cms.untracked.bool(True),

  # prefix of name of output .txt file(s)
  globalTag = cms.untracked.string(opts.tag),
)

process.readAK8CaloHLT = process.readAK4CaloHLT.clone(payloadName = 'AK8CaloHLT')
process.readAK4PFHLT   = process.readAK4CaloHLT.clone(payloadName = 'AK4PFHLT')
process.readAK8PFHLT   = process.readAK4CaloHLT.clone(payloadName = 'AK8PFHLT')

process.p = cms.Path(
    process.readAK4CaloHLT
  + process.readAK8CaloHLT
  + process.readAK4PFHLT
  + process.readAK8PFHLT
)

if not opts.onlyHLT:
   process.readAK4PF      = process.readAK4CaloHLT.clone(payloadName = 'AK4PF')
   process.readAK4PFchs   = process.readAK4CaloHLT.clone(payloadName = 'AK4PFchs')
   process.readAK4PFPuppi = process.readAK4CaloHLT.clone(payloadName = 'AK4PFPuppi')
   process.readAK8PF      = process.readAK4CaloHLT.clone(payloadName = 'AK8PF')
   process.readAK8PFchs   = process.readAK4CaloHLT.clone(payloadName = 'AK8PFchs')
   process.readAK8PFPuppi = process.readAK4CaloHLT.clone(payloadName = 'AK8PFPuppi')

   process.p += process.readAK4PF
   process.p += process.readAK4PFchs
   process.p += process.readAK4PFPuppi
   process.p += process.readAK8PF
   process.p += process.readAK8PFchs
   process.p += process.readAK8PFPuppi
