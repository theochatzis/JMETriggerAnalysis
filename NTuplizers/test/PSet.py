#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#       lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = []
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('events.root')
)
process.out = cms.EndPath(process.output)
