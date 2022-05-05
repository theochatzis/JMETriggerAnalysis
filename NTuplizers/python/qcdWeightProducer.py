import FWCore.ParameterSet.Config as cms

from HLTrigger.mcStitching.stitchingWeight_cfi import stitchingWeight as _qcdWgtProducer

def qcdWeightProducer(BXFrequency, PU):

  retMod = _qcdWgtProducer.clone(
    bxFrequency = BXFrequency,
    pT_hat_bins = [
      0., 20., 30., 50., 80., 120., 170., 300., 470., 600., 1e16,
    ]
  )

  retMod.samples = cms.PSet(
    minbias = cms.PSet(
      crossSection = cms.double(80. * 1e9),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(-1)
    ),
    qcd_pt20to30 = cms.PSet(
      crossSection = cms.double(436000000.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(1),
    ),
    qcd_pt30to50 = cms.PSet(
      crossSection = cms.double(118400000.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(2),
    ),
    qcd_pt50to80 = cms.PSet(
      crossSection = cms.double(17650000.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(3),
    ),
    qcd_pt80to120 = cms.PSet(
      crossSection = cms.double(2671000.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(4),
    ),
    qcd_pt120to170 = cms.PSet(
      crossSection = cms.double(469700.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(5),
    ),
    qcd_pt170to300 = cms.PSet(
      crossSection = cms.double(121700.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(6),
    ),
    qcd_pt300to470 = cms.PSet(
      crossSection = cms.double(8251.0),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(7),
    ),
    qcd_pt470to600 = cms.PSet(
      crossSection = cms.double(686.4),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(8),
    ),
    qcd_pt600toInf = cms.PSet(
      crossSection = cms.double(244.8),
      numEvents = cms.uint32(0),
      pT_hat_bin = cms.int32(9),
    ),
  )

  # number of events to be processed for MinBias and QCD-Pt MC samples
  if PU == 140.:
    retMod.samples.minbias.numEvents = int(2 * 1e6) # MinBias: only run on 2M events
    retMod.samples.qcd_pt20to30.numEvents = 999301
    retMod.samples.qcd_pt30to50.numEvents = 499369 + 500000
    retMod.samples.qcd_pt50to80.numEvents = 300000 + 295107
    retMod.samples.qcd_pt80to120.numEvents = 98866
    retMod.samples.qcd_pt120to170.numEvents = 50000
    retMod.samples.qcd_pt170to300.numEvents = 50000
    retMod.samples.qcd_pt300to470.numEvents = 49008
    retMod.samples.qcd_pt470to600.numEvents = 50000
    retMod.samples.qcd_pt600toInf.numEvents = 48976

  elif PU == 200.:
    retMod.samples.minbias.numEvents = int(2 * 1e6) # MinBias: only run on 2M events
    retMod.samples.qcd_pt20to30.numEvents = 996386
    retMod.samples.qcd_pt30to50.numEvents = 483498 + 499401
    retMod.samples.qcd_pt50to80.numEvents = 300000 + 299401
    retMod.samples.qcd_pt80to120.numEvents = 100000
    retMod.samples.qcd_pt120to170.numEvents = 49601
    retMod.samples.qcd_pt170to300.numEvents = 50000
    retMod.samples.qcd_pt300to470.numEvents = 50000
    retMod.samples.qcd_pt470to600.numEvents = 50000
    retMod.samples.qcd_pt600toInf.numEvents = 50000

  else:
    raise RuntimeError('getQCDWeightProducer -- invalid PU value: '+str(PU))

  print('>> WARNING -- getQCDWeightProducer(PU='+str(PU)+'):')
  print('weight depends on hard-coded values of cross sections and #events of various MC samples')
  print('(it will not be valid otherwise)')

  return retMod
