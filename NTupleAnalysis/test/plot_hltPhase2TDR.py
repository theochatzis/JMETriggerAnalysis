#!/usr/bin/env python
import os
import sys
import argparse
import ROOT
import math

from common.utils import *
from common.th1 import *
from common.efficiency import *
from common.plot import *
from common.plot_style import *

COUNTER = 0
def tmpName(increment=True):
  global COUNTER
  COUNTER += 1
  return 'tmp'+str(COUNTER)

def getXSec(processName):
  if   processName == 'QCD_Pt020to030_14TeV'      : return 436000000.0
  elif processName == 'QCD_Pt030to050_14TeV'      : return 118400000.0
  elif processName == 'QCD_Pt050to080_14TeV'      : return  17650000.0
  elif processName == 'QCD_Pt080to120_14TeV'      : return   2671000.0
  elif processName == 'QCD_Pt120to170_14TeV'      : return    469700.0
  elif processName == 'QCD_Pt170to300_14TeV'      : return    121700.0
  elif processName == 'QCD_Pt300to470_14TeV'      : return      8251.0
  elif processName == 'QCD_Pt470to600_14TeV'      : return       686.4
  elif processName == 'QCD_Pt600toInf_14TeV'      : return       244.8
  elif processName == 'WJetsToLNu_14TeV'          : return     56990.0
  elif processName == 'DYJetsToLL_M010to050_14TeV': return     16880.0
  elif processName == 'DYJetsToLL_M050toInf_14TeV': return      5795.0
  else:
    raise RuntimeError('getXSec -- '+processName)

def getRateFactor(processName, instLumiHzPerPb):
  if processName == 'MinBias_14TeV': return 1e6 * 30. # 30.903 (L1T TDR)
  else:
    return instLumiHzPerPb * getXSec(processName)

def getHistogram(tfile, key):
  h0 = tfile.Get(key)
  if not h0:
    return None

  hret = h0.Clone()
  hret.SetDirectory(0)
  hret.UseCurrentStyle()

  return hret

def getRateHistogram(h1, rateFac):
  theRateHisto = h1.Clone()

  theRateHisto_name = h1.GetName()+'_rate'
  theRateHisto.SetTitle(theRateHisto_name)
  theRateHisto.SetName(theRateHisto_name)
  theRateHisto.SetDirectory(0)
  theRateHisto.UseCurrentStyle()

  for _tmp_bin_i in range(1, 1+h1.GetNbinsX()):
    _err = ctypes.c_double(0.)
    theRateHisto.SetBinContent(_tmp_bin_i, h1.IntegralAndError(_tmp_bin_i, -1, _err))
    theRateHisto.SetBinError(_tmp_bin_i, _err.value)

  theRateHisto.Scale(rateFac)

  return theRateHisto

def getRates(**kwargs):
  ret = {
    'v_eventsProcessed': 0.,
    't_rates': {},
    'v_rates': {},
    'v_counts': {},
  }

  for fpath in kwargs['fpaths']:
    _tfile = ROOT.TFile.Open(fpath)
    if not _tfile:
      WARNING('failed to open target TFile: '+fpath)
      continue
    _eventsProcessed = _tfile.Get('eventsProcessed')
    ret['v_eventsProcessed'] += _eventsProcessed.GetEntries()
    _tfile.Close()

  if ret['v_eventsProcessed'] == 0:
    return ret

  rateFactor = 1.
  if not (kwargs['qcd_weighted'] and (kwargs['processName'].startswith('MinBias') or kwargs['processName'].startswith('QCD'))):
    rateFactor = getRateFactor(kwargs['processName'], kwargs['instLumiHzPerPb']) / ret['v_eventsProcessed']

  def _addTH1(theDict, theKey, theTH1):
    if theKey not in theDict:
      theDict[theKey] = theTH1
    else:
      theDict[theKey].Add(theTH1)

  def _addRate(theDict, theKey, theRatePair):
    if theKey not in theDict:
      theDict[theKey] = theRatePair[:]
    else:
      theDict[theKey][0] += theRatePair[0]
      oldRateErr2 = math.pow(theDict[theKey][1], 2)
      theDict[theKey][1] = math.sqrt(oldRateErr2 + math.pow(theRatePair[1], 2))

  def _approxCount_valNerr(val, err):
    if err == 0.:
      return [0., 0.]
    else:
      return [val*val/(err*err), val/err]

  for fpath in kwargs['fpaths']:
    _tfile = ROOT.TFile.Open(fpath)
    if not _tfile:
      WARNING('failed to open target TFile: '+fpath)
      continue
    # SingleJet
    _addTH1(ret['t_rates'], 'l1tSlwPFPuppiJet', getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor))
    _addTH1(ret['t_rates'], 'hltAK4PFPuppiJet_woL1T', getRateHistogram(_tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor))
    _addTH1(ret['t_rates'], 'hltAK4PFPuppiJet', getRateHistogram(_tfile.Get('L1T_SinglePFPuppiJet230off2/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor))

    _tmp = _tfile.Get('L1T_SinglePFPuppiJet230off2/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'L1T_SinglePFPuppiJet230off2', [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'L1T_SinglePFPuppiJet230off2', [_tmp.GetEntries(), math.sqrt(_tmp.GetEntries())])

    _tmp = _tfile.Get('L1T_SinglePFPuppiJet230off2/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(kwargs['hltThreshold_SingleJet'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_AK4PFPuppiJet'+str(kwargs['hltThreshold_SingleJet']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_AK4PFPuppiJet'+str(kwargs['hltThreshold_SingleJet']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    # HT
    _addTH1(ret['t_rates'], 'l1tPFPuppiHT', getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_Eta2p4_HT'), rateFactor))
    _addTH1(ret['t_rates'], 'hltPFPuppiHT_woL1T', getRateHistogram(_tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT'), rateFactor))
    _addTH1(ret['t_rates'], 'hltPFPuppiHT', getRateHistogram(_tfile.Get('L1T_PFPuppiHT450off/hltAK4PFPuppiJetsCorrected_Eta2p4_HT'), rateFactor))

    _tmp = _tfile.Get('L1T_PFPuppiHT450off/l1tPFPuppiHT_sumEt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'L1T_PFPuppiHT450off', [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'L1T_PFPuppiHT450off', [_tmp.GetEntries(), math.sqrt(_tmp.GetEntries())])

    _tmp = _tfile.Get('L1T_PFPuppiHT450off/hltAK4PFPuppiJetsCorrected_Eta2p4_HT')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(kwargs['hltThreshold_HT'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiHT'+str(kwargs['hltThreshold_HT']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiHT'+str(kwargs['hltThreshold_HT']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    # MET
    _addTH1(ret['t_rates'], 'l1tPFPuppiMET', getRateHistogram(_tfile.Get('NoSelection/l1tPFPuppiMET_pt'), rateFactor))
    _addTH1(ret['t_rates'], 'hltPFPuppiMET_woL1T', getRateHistogram(_tfile.Get('NoSelection/hltPFPuppiMET_pt'), rateFactor))
    _addTH1(ret['t_rates'], 'hltPFPuppiMET', getRateHistogram(_tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMET_pt'), rateFactor))
    _addTH1(ret['t_rates'], 'hltPFPuppiMETTypeOne', getRateHistogram(_tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMETTypeOne_pt'), rateFactor))

    for _tmpMHT in [
      'MHT20',
      'MHT30',
      'MHT40',
      'MHT50',
    ]:
      _htmp0 = _tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMETTypeOne_pt__vs__hltPFPuppi'+_tmpMHT+'_pt')
      _htmp = _htmp0.ProjectionX('hltPFPuppiMETTypeOne'+_tmpMHT, 0, -1)
      _htmp.SetTitle(_htmp.GetName())
      _htmp.UseCurrentStyle()
      _htmp.SetDirectory(0)
      _htmp.Reset()
      for _htmpbin_i in range(1, 1+_htmp.GetNbinsX()):
        _hbinerr = ctypes.c_double(0.)
        _hbinval = _htmp0.IntegralAndError(_htmpbin_i, -1, _htmpbin_i, -1, _hbinerr)
        _htmp.SetBinContent(_htmpbin_i, _hbinval)
        _htmp.SetBinError(_htmpbin_i, _hbinerr.value)
      _htmp.Scale(rateFactor)
      _addTH1(ret['t_rates'], 'hltPFPuppiMETTypeOne'+_tmpMHT, _htmp)

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/l1tPFPuppiMET_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'L1T_PFPuppiMET220off2', [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'L1T_PFPuppiMET220off2', [_tmp.GetEntries(), math.sqrt(_tmp.GetEntries())])

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMET_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(kwargs['hltThreshold_MET'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiMET'+str(kwargs['hltThreshold_MET']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiMET'+str(kwargs['hltThreshold_MET']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMETTypeOne_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(kwargs['hltThreshold_METTypeOne'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiMETTypeOne'+str(kwargs['hltThreshold_METTypeOne']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiMETTypeOne'+str(kwargs['hltThreshold_METTypeOne']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT20_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp.GetYaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT20'])), -1, _tmp.GetZaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT20'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiMETTypeOneMHT20_'+str(kwargs['hltThreshold_METTypeOneMHT20']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiMETTypeOneMHT20_'+str(kwargs['hltThreshold_METTypeOneMHT20']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT30_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp.GetYaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT30'])), -1, _tmp.GetZaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT30'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiMETTypeOneMHT30_'+str(kwargs['hltThreshold_METTypeOneMHT30']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiMETTypeOneMHT30_'+str(kwargs['hltThreshold_METTypeOneMHT30']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT40_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp.GetYaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT40'])), -1, _tmp.GetZaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT40'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiMETTypeOneMHT40_'+str(kwargs['hltThreshold_METTypeOneMHT40']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiMETTypeOneMHT40_'+str(kwargs['hltThreshold_METTypeOneMHT40']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    _tmp = _tfile.Get('L1T_PFPuppiMET220off2/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT50_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp.GetYaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT50'])), -1, _tmp.GetZaxis().FindBin(float(kwargs['hltThreshold_METTypeOneMHT50'])), -1, _tmp_integErr)
    _addRate(ret['v_rates'] , 'HLT_PFPuppiMETTypeOneMHT50_'+str(kwargs['hltThreshold_METTypeOneMHT50']), [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value])
    _addRate(ret['v_counts'], 'HLT_PFPuppiMETTypeOneMHT50_'+str(kwargs['hltThreshold_METTypeOneMHT50']), _approxCount_valNerr(_tmp_integ, _tmp_integErr.value))

    _tfile.Close()

  ## common
  for _tmp1 in ret:
    if not _tmp1.startswith('t_'):
      continue
    for _tmp2 in ret[_tmp1]:
      if ret[_tmp1][_tmp2].InheritsFrom('TH1'):
        ret[_tmp1][_tmp2].SetDirectory(0)
        ret[_tmp1][_tmp2].UseCurrentStyle()

  return ret

def getJetEfficiencies(fpath, hltThreshold_SingleJet):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'GEN',
#    'Offline',
  ]

  # SingleJet
  binEdges_pT = array.array('d', [_tmp*20 for _tmp in range(35)] + [700+_tmp*50 for _tmp in range(6+1)])

  for _tmpRef in _tmpRefs:
    if _tmpRef != 'GEN': continue

    _tmp_num = _tfile.Get('L1T_SinglePFPuppiJet230off2/ak4GenJetsNoNu_EtaIncl_MatchedTohltPFPuppiCorr_pt__vs__hltPFPuppiCorr_pt')
    _tmp_num = _tmp_num.ProjectionX(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/ak4GenJetsNoNu_EtaIncl_MatchedTohltPFPuppiCorr_pt__vs__hltPFPuppiCorr_pt')
    _tmp_den = _tmp_den.ProjectionX(tmpName(), 0, -1)

    ret['SingleJet_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1T_wrt_'+_tmpRef].SetName('SingleJet_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/ak4GenJetsNoNu_EtaIncl_MatchedTohltPFPuppiCorr_pt__vs__hltPFPuppiCorr_pt')
    _tmp_num = _tmp_num.ProjectionX(tmpName(), _tmp_num.GetYaxis().FindBin(hltThreshold_SingleJet), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    _tmp_den = _tfile.Get('NoSelection/ak4GenJetsNoNu_EtaIncl_MatchedTohltPFPuppiCorr_pt__vs__hltPFPuppiCorr_pt')
    _tmp_den = _tmp_den.ProjectionX(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    ret['SingleJet_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_HLT_wrt_'+_tmpRef].SetName('SingleJet_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_SinglePFPuppiJet230off2/ak4GenJetsNoNu_EtaIncl_MatchedTohltPFPuppiCorr_pt__vs__hltPFPuppiCorr_pt')
    _tmp_num = _tmp_num.ProjectionX(tmpName(), _tmp_num.GetYaxis().FindBin(hltThreshold_SingleJet), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    _tmp_den = _tfile.Get('NoSelection/ak4GenJetsNoNu_EtaIncl_MatchedTohltPFPuppiCorr_pt__vs__hltPFPuppiCorr_pt')
    _tmp_den = _tmp_den.ProjectionX(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_pT)-1, tmpName(), binEdges_pT)

    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetName('SingleJet_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getHTEfficiencies(fpath, hltThreshold_HT):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'GEN',
#    'Offline',
  ]

  # HT
  binEdges_HT = array.array('d', [50.*_tmpIdx for _tmpIdx in range(44+1)])

  for _tmpRef in _tmpRefs:

    _tmp_num = _tfile.Get('L1T_PFPuppiHT450off/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1T_wrt_'+_tmpRef].SetName('HT_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    ret['HT_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_HLT_wrt_'+_tmpRef].SetName('HT_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiHT450off/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_Eta2p4_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_HT)-1, tmpName(), binEdges_HT)

    ret['HT_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1TpHLT_wrt_'+_tmpRef].SetName('HT_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getMETEfficiencies(**kwargs):
  ret = {}

  _tfile = ROOT.TFile.Open(kwargs['fpath'])
  if not _tfile:
    WARNING('failed to open target TFile: '+kwargs['fpath'])
    return ret

  _tmpRefs = [
    'GEN',
#    'Offline',
  ]

  binEdges_MET = array.array('d', [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 140, 160, 180, 200, 220, 240, 280, 320, 360, 430, 500, 600, 700, 800])

  for _tmpRef in _tmpRefs:
    # MET
    _tmp_num = _tfile.Get('L1T_PFPuppiMET220off2/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    ret['MET_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_L1T_wrt_'+_tmpRef].SetName('MET_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(kwargs['hltThreshold_MET']), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    ret['MET_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_HLT_wrt_'+_tmpRef].SetName('MET_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(kwargs['hltThreshold_MET']), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    ret['MET_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_L1TpHLT_wrt_'+_tmpRef].SetName('MET_L1TpHLT_wrt_'+_tmpRef)

    # METTypeOne
    _tmp_num = _tfile.Get('L1T_PFPuppiMET220off2/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    ret['METTypeOne_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['METTypeOne_L1T_wrt_'+_tmpRef].SetName('METTypeOne_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(kwargs['hltThreshold_METTypeOne']), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    ret['METTypeOne_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['METTypeOne_HLT_wrt_'+_tmpRef].SetName('METTypeOne_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiMET220off2/hltPFPuppiMETTypeOne_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(kwargs['hltThreshold_METTypeOne']), -1)
    _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
    _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

    ret['METTypeOne_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['METTypeOne_L1TpHLT_wrt_'+_tmpRef].SetName('METTypeOne_L1TpHLT_wrt_'+_tmpRef)

    # METTypeOne+MHT
    for _tmpMHT in [
      'MHT20',
      'MHT30',
      'MHT40',
      'MHT50',
    ]:
      _tmp_num = _tfile.Get('L1T_PFPuppiMET220off2/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
      _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)
      _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

      _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
      _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
      _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

      ret['METTypeOne'+_tmpMHT+'_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
      ret['METTypeOne'+_tmpMHT+'_L1T_wrt_'+_tmpRef].SetName('METTypeOne'+_tmpMHT+'_L1T_wrt_'+_tmpRef)

      _tmp_num = _tfile.Get('NoSelection/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppi'+_tmpMHT+'_pt')
      _tmp_num = _tmp_num.ProjectionX(tmpName(), _tmp_num.GetYaxis().FindBin(kwargs['hltThreshold_METTypeOne'+_tmpMHT]), _tmp_num.GetNbinsY()+1, _tmp_num.GetZaxis().FindBin(kwargs['hltThreshold_METTypeOne'+_tmpMHT]), _tmp_num.GetNbinsZ()+1)
      _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

      _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__'+_tmpRef+'_pt')
      _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
      _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

      ret['METTypeOne'+_tmpMHT+'_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
      ret['METTypeOne'+_tmpMHT+'_HLT_wrt_'+_tmpRef].SetName('METTypeOne'+_tmpMHT+'_HLT_wrt_'+_tmpRef)

      _tmp_num = _tfile.Get('L1T_PFPuppiMET220off2/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppi'+_tmpMHT+'_pt')
      _tmp_num = _tmp_num.ProjectionX(tmpName(), _tmp_num.GetYaxis().FindBin(kwargs['hltThreshold_METTypeOne'+_tmpMHT]), _tmp_num.GetNbinsY()+1, _tmp_num.GetZaxis().FindBin(kwargs['hltThreshold_METTypeOne'+_tmpMHT]), _tmp_num.GetNbinsZ()+1)
      _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

      _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__'+_tmpRef+'_pt')
      _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
      _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)

      ret['METTypeOne'+_tmpMHT+'_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
      ret['METTypeOne'+_tmpMHT+'_L1TpHLT_wrt_'+_tmpRef].SetName('METTypeOne'+_tmpMHT+'_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def plotJetResponse(fpath_PU140, fpath_PU200, outputName, exts):
  for (_etaTag, _etaLabel) in {
    'EtaIncl': '|#eta|<5.0',
    'HB': '|#eta|<1.5',
    'HGCal': '1.5<|#eta|<3.0',
    'HF': '3.0<|#eta|<5.0',
  }.items():
   histos = {
     'PU140': {'pt030to100': None, 'pt100to300': None, 'pt300to600': None},
     'PU200': {'pt030to100': None, 'pt100to300': None, 'pt300to600': None},
   }
   for [_tmp, _tmpFilePath] in [
     ['PU140', fpath_PU140],
     ['PU200', fpath_PU200],
   ]:
     _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
     if not _tmpTFile:
       WARNING('failed to open target TFile: '+_tmpFilePath)
       continue

     _h2tmp = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_MatchedToGEN_pt_overGEN__vs__GEN_pt')
     histos[_tmp]['pt030to100'] = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin( 30.001), _h2tmp.GetYaxis().FindBin( 99.999))
     histos[_tmp]['pt100to300'] = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(100.001), _h2tmp.GetYaxis().FindBin(299.999))
     histos[_tmp]['pt300to600'] = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(300.001), _h2tmp.GetYaxis().FindBin(599.999))

     for _tmp2 in histos[_tmp]:
       histos[_tmp][_tmp2].SetDirectory(0)
       histos[_tmp][_tmp2].UseCurrentStyle()
       histos[_tmp][_tmp2].Scale(1./histos[_tmp][_tmp2].Integral())

   canvas = ROOT.TCanvas(tmpName(), tmpName(False))
   canvas.cd()

   h0 = canvas.DrawFrame(0.001, 0.0001, 2.39, 0.27 if _etaTag in ['EtaIncl', 'HB'] else 0.17)

   try:
     histos['PU140']['pt030to100'].SetMarkerStyle(20)
     histos['PU140']['pt030to100'].SetMarkerSize(.0)
     histos['PU140']['pt030to100'].SetLineWidth(2)
     histos['PU140']['pt030to100'].SetLineStyle(2)
     histos['PU140']['pt030to100'].SetLineColor(1)
     histos['PU140']['pt030to100'].SetMarkerColor(1)
     histos['PU140']['pt030to100'].Draw('hist,e0,same')
  
     histos['PU140']['pt100to300'].SetMarkerStyle(20)
     histos['PU140']['pt100to300'].SetMarkerSize(.0)
     histos['PU140']['pt100to300'].SetLineWidth(2)
     histos['PU140']['pt100to300'].SetLineStyle(2)
     histos['PU140']['pt100to300'].SetLineColor(2)
     histos['PU140']['pt100to300'].SetMarkerColor(2)
     histos['PU140']['pt100to300'].Draw('hist,e0,same')
   
     histos['PU140']['pt300to600'].SetMarkerStyle(20)
     histos['PU140']['pt300to600'].SetMarkerSize(.0)
     histos['PU140']['pt300to600'].SetLineWidth(2)
     histos['PU140']['pt300to600'].SetLineStyle(2)
     histos['PU140']['pt300to600'].SetLineColor(4)
     histos['PU140']['pt300to600'].SetMarkerColor(4)
     histos['PU140']['pt300to600'].Draw('hist,e0,same')
   except: pass

   try:
     histos['PU200']['pt030to100'].SetMarkerStyle(20)
     histos['PU200']['pt030to100'].SetMarkerSize(.0)
     histos['PU200']['pt030to100'].SetLineWidth(2)
     histos['PU200']['pt030to100'].SetLineColor(1)
     histos['PU200']['pt030to100'].SetMarkerColor(1)
     histos['PU200']['pt030to100'].Draw('hist,e0,same')
  
     histos['PU200']['pt100to300'].SetMarkerStyle(20)
     histos['PU200']['pt100to300'].SetMarkerSize(.0)
     histos['PU200']['pt100to300'].SetLineWidth(2)
     histos['PU200']['pt100to300'].SetLineColor(2)
     histos['PU200']['pt100to300'].SetMarkerColor(2)
     histos['PU200']['pt100to300'].Draw('hist,e0,same')
  
     histos['PU200']['pt300to600'].SetMarkerStyle(20)
     histos['PU200']['pt300to600'].SetMarkerSize(.0)
     histos['PU200']['pt300to600'].SetLineWidth(2)
     histos['PU200']['pt300to600'].SetLineColor(4)
     histos['PU200']['pt300to600'].SetMarkerColor(4)
     histos['PU200']['pt300to600'].Draw('hist,e0,same')
   except: pass

   topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
   topLabel.SetFillColor(0)
   topLabel.SetFillStyle(1001)
   topLabel.SetTextColor(ROOT.kBlack)
   topLabel.SetTextAlign(12)
   topLabel.SetTextFont(42)
   topLabel.SetTextSize(0.035)
   topLabel.SetBorderSize(0)
   topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
   topLabel.Draw('same')

   objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
   objLabel.SetFillColor(0)
   objLabel.SetFillStyle(1001)
   objLabel.SetTextColor(ROOT.kBlack)
   objLabel.SetTextAlign(32)
   objLabel.SetTextFont(42)
   objLabel.SetTextSize(0.035)
   objLabel.SetBorderSize(0)
   objLabel.AddText('14 TeV')
   objLabel.Draw('same')

   l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.50, 0.90, 'NDC')
   l1tRateLabel.SetFillColor(0)
   l1tRateLabel.SetFillStyle(1001)
   l1tRateLabel.SetTextColor(ROOT.kBlack)
   l1tRateLabel.SetTextAlign(12)
   l1tRateLabel.SetTextFont(42)
   l1tRateLabel.SetTextSize(0.035)
   l1tRateLabel.SetBorderSize(0)
   l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
   l1tRateLabel.Draw('same')

   hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.35, 0.85, 'NDC')
   hltRateLabel.SetFillColor(0)
   hltRateLabel.SetFillStyle(1001)
   hltRateLabel.SetTextColor(ROOT.kBlack)
   hltRateLabel.SetTextAlign(12)
   hltRateLabel.SetTextFont(42)
   hltRateLabel.SetTextSize(0.035)
   hltRateLabel.SetBorderSize(0)
   hltRateLabel.AddText(_etaLabel)
   hltRateLabel.Draw('same')

   genJetPtLabel = ROOT.TPaveText(0.65, 0.80, 0.94, 0.90, 'NDC')
   genJetPtLabel.SetFillColor(0)
   genJetPtLabel.SetFillStyle(1001)
   genJetPtLabel.SetTextColor(ROOT.kBlack)
   genJetPtLabel.SetTextAlign(22)
   genJetPtLabel.SetTextFont(42)
   genJetPtLabel.SetTextSize(0.035)
   genJetPtLabel.SetBorderSize(0)
   genJetPtLabel.AddText('GEN Jet p_{T} range')
   genJetPtLabel.Draw('same')

   leg1 = ROOT.TLegend(0.65, 0.60, 0.94, 0.81)
   leg1.SetNColumns(1)
   leg1.SetTextFont(42)
   leg1.AddEntry(histos['PU200']['pt030to100'],  '30-100 GeV', 'lex')
   leg1.AddEntry(histos['PU200']['pt100to300'], '100-300 GeV', 'lex')
   leg1.AddEntry(histos['PU200']['pt300to600'], '300-600 GeV', 'lex')
   leg1.Draw('same')

   try:
    _htmpPU140 = histos['PU140']['pt030to100'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
   except: pass

   try:
    _htmpPU200 = histos['PU200']['pt030to100'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
   except: pass

   leg2 = ROOT.TLegend(0.75, 0.45, 0.94, 0.60)
   leg2.SetNColumns(1)
   leg2.SetTextFont(42)
   try:
     leg2.AddEntry(_htmpPU140, '140 PU', 'l')
   except: pass
   try:
     leg2.AddEntry(_htmpPU200, '200 PU', 'l')
   except: pass
   leg2.Draw('same')

   h0.SetTitle(';HLT Jet p_{T} response;a.u.')
   h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

   canvas.SetLogy(0)
   canvas.SetGrid(1, 1)

   for _tmpExt in exts:
     canvas.SaveAs(outputName+'_'+_etaTag+'.'+_tmpExt)

   canvas.Close()

   print '\033[1m'+outputName+'_'+_etaTag+'\033[0m'

def plotJetResolution(fpath_PU140, fpath_PU200, outputName, exts):
  histos = {
    'PU140': {
      'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HF': [30, 40, 50, 60, 80, 120, 240, 600],
    },
    'PU200': {
      'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HF': [30, 40, 50, 60, 80, 120, 240, 600],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _etaTag in histos[_puTag]:
      h1vals = []
      _h2tmp = getHistogram(_tmpTFile, 'NoSelection/hltAK4PFPuppiJetsCorrected_'+_etaTag+'_MatchedToGEN_pt_overGEN__vs__GEN_pt')
      binEdges = array.array('d', histos[_puTag][_etaTag])
      for pTbinEdge_idx in range(len(binEdges)-1):
        _h1tmp = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(1.0001*binEdges[pTbinEdge_idx]), _h2tmp.GetYaxis().FindBin(0.9999*binEdges[pTbinEdge_idx+1]))
        _h1tmp_val = _h1tmp.GetRMS() / _h1tmp.GetMean() if _h1tmp.GetMean() != 0. else None
        _h1tmp_err = _h1tmp.GetRMSError() / _h1tmp.GetMean() if _h1tmp.GetMean() != 0. else None
        h1vals.append([_h1tmp_val, _h1tmp_err])

      histos[_puTag][_etaTag] = ROOT.TH1D(tmpName(), tmpName(False), len(binEdges)-1, binEdges)
      histos[_puTag][_etaTag].SetDirectory(0)
      histos[_puTag][_etaTag].UseCurrentStyle()
      for _binIdx in range(histos[_puTag][_etaTag].GetNbinsX()):
        if h1vals[_binIdx] != [None, None]:
          histos[_puTag][_etaTag].SetBinContent(_binIdx+1, h1vals[_binIdx][0])
          histos[_puTag][_etaTag].SetBinError(_binIdx+1, h1vals[_binIdx][1])

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(30., 0.0001, 600., 0.57)

  try:
    histos['PU140']['HB'].SetMarkerStyle(24)
    histos['PU140']['HB'].SetMarkerSize(1)
    histos['PU140']['HB'].SetLineWidth(2)
    histos['PU140']['HB'].SetLineStyle(2)
    histos['PU140']['HB'].SetLineColor(1)
    histos['PU140']['HB'].SetMarkerColor(1)
  except: pass

  try:
    histos['PU140']['HGCal'].SetMarkerStyle(25)
    histos['PU140']['HGCal'].SetMarkerSize(1)
    histos['PU140']['HGCal'].SetLineWidth(2)
    histos['PU140']['HGCal'].SetLineStyle(2)
    histos['PU140']['HGCal'].SetLineColor(2)
    histos['PU140']['HGCal'].SetMarkerColor(2)
  except: pass

  try:
    histos['PU140']['HF'].SetMarkerStyle(27)
    histos['PU140']['HF'].SetMarkerSize(1.5)
    histos['PU140']['HF'].SetLineWidth(2)
    histos['PU140']['HF'].SetLineStyle(2)
    histos['PU140']['HF'].SetLineColor(4)
    histos['PU140']['HF'].SetMarkerColor(4)
  except: pass

  try:
    histos['PU200']['HB'].SetMarkerStyle(20)
    histos['PU200']['HB'].SetMarkerSize(1)
    histos['PU200']['HB'].SetLineWidth(2)
    histos['PU200']['HB'].SetLineStyle(1)
    histos['PU200']['HB'].SetLineColor(1)
    histos['PU200']['HB'].SetMarkerColor(1)
  except: pass

  try:
    histos['PU200']['HGCal'].SetMarkerStyle(21)
    histos['PU200']['HGCal'].SetMarkerSize(1)
    histos['PU200']['HGCal'].SetLineWidth(2)
    histos['PU200']['HGCal'].SetLineStyle(1)
    histos['PU200']['HGCal'].SetLineColor(2)
    histos['PU200']['HGCal'].SetMarkerColor(2)
  except: pass

  try:
    histos['PU200']['HF'].SetMarkerStyle(33)
    histos['PU200']['HF'].SetMarkerSize(1.5)
    histos['PU200']['HF'].SetLineWidth(2)
    histos['PU200']['HF'].SetLineStyle(1)
    histos['PU200']['HF'].SetLineColor(4)
    histos['PU200']['HF'].SetMarkerColor(4)
  except: pass

  try:
    histos['PU140']['HF'].Draw('hist,e0,same')
    histos['PU140']['HGCal'].Draw('hist,e0,same')
    histos['PU140']['HB'].Draw('hist,e0,same')
    histos['PU200']['HF'].Draw('hist,e0,same')
    histos['PU200']['HGCal'].Draw('hist,e0,same')
    histos['PU200']['HB'].Draw('hist,e0,same')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.50, 0.90, 'NDC')
  l1tRateLabel.SetFillColor(0)
  l1tRateLabel.SetFillStyle(1001)
  l1tRateLabel.SetTextColor(ROOT.kBlack)
  l1tRateLabel.SetTextAlign(12)
  l1tRateLabel.SetTextFont(42)
  l1tRateLabel.SetTextSize(0.035)
  l1tRateLabel.SetBorderSize(0)
  l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
  l1tRateLabel.Draw('same')

  hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.37, 0.85, 'NDC')
  hltRateLabel.SetFillColor(0)
  hltRateLabel.SetFillStyle(1001)
  hltRateLabel.SetTextColor(ROOT.kBlack)
  hltRateLabel.SetTextAlign(12)
  hltRateLabel.SetTextFont(42)
  hltRateLabel.SetTextSize(0.035)
  hltRateLabel.SetBorderSize(0)
  hltRateLabel.AddText('p_{T}^{HLT} > 30 GeV')
  hltRateLabel.Draw('same')

  leg1 = ROOT.TLegend(0.65, 0.70, 0.94, 0.90)
  leg1.SetNColumns(1)
  leg1.SetTextFont(42)
  try:
    leg1.AddEntry(histos['PU200']['HB']   ,     '|#eta|<1.5', 'lepx')
    leg1.AddEntry(histos['PU200']['HGCal'], '1.5<|#eta|<3.0', 'lepx')
    leg1.AddEntry(histos['PU200']['HF']   , '3.0<|#eta|<5.0', 'lepx')
  except: pass
  leg1.Draw('same')

  try:
    _htmpPU140 = histos['PU140']['HB'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
  except: pass

  try:
    _htmpPU200 = histos['PU200']['HB'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
  except: pass

  leg2 = ROOT.TLegend(0.40, 0.70, 0.65, 0.82)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass
  try:
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  h0.SetTitle(';GEN Jet p_{T} [GeV];#sigma(p^{HLT}_{T} / p^{GEN}_{T}) / #LTp^{HLT}_{T} / p^{GEN}_{T}#GT')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogy(0)
  canvas.SetGrid(1, 1)

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'\033[0m'

def plotJetMatchingEff(fpath_PU140, fpath_PU200, keyword, outputName, exts):
  if keyword == 'HLT':
    jetTag1 = 'hltAK4PFPuppiJetsCorrected'
    jetTag2 = 'hltPFPuppiCorr'
    jetTag3 = 'HLT'
  elif keyword == 'L1T':
    jetTag1 = 'l1tSlwPFPuppiJetsCorrected'
    jetTag2 = 'l1tPFPuppiCorr'
    jetTag3 = 'L1T'
  else:
    return

  # HLT - MatchedToGEN
  graphs = {
    'PU140': {
      'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HF': [30, 40, 50, 60, 80, 120, 240, 600],
    },
    'PU200': {
      'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HF': [30, 40, 50, 60, 80, 120, 240, 600],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _etaTag in graphs[_puTag]:
      _binEdges = array.array('d', graphs[_puTag][_etaTag])

      _htmpNum = getHistogram(_tmpTFile, 'NoSelection/'+jetTag1+'_'+_etaTag+'_MatchedToGEN_pt')
      _htmpDen = getHistogram(_tmpTFile, 'NoSelection/'+jetTag1+'_'+_etaTag+'_pt')
      _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
      _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

      graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)
      graphs[_puTag][_etaTag].UseCurrentStyle()
      for _tmpn in range(graphs[_puTag][_etaTag].GetN()):
        graphs[_puTag][_etaTag].SetPointEXhigh(_tmpn, 0.)
        graphs[_puTag][_etaTag].SetPointEXlow(_tmpn, 0.)

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(30., 0.0001, 600., 1.2)

  try:
    graphs['PU140']['HB'].SetMarkerStyle(24)
    graphs['PU140']['HB'].SetMarkerSize(1)
    graphs['PU140']['HB'].SetLineWidth(2)
    graphs['PU140']['HB'].SetLineStyle(2)
    graphs['PU140']['HB'].SetLineColor(1)
    graphs['PU140']['HB'].SetMarkerColor(1)
    graphs['PU140']['HB'].Draw('lepz')
  
    graphs['PU140']['HGCal'].SetMarkerStyle(25)
    graphs['PU140']['HGCal'].SetMarkerSize(1)
    graphs['PU140']['HGCal'].SetLineWidth(2)
    graphs['PU140']['HGCal'].SetLineStyle(2)
    graphs['PU140']['HGCal'].SetLineColor(2)
    graphs['PU140']['HGCal'].SetMarkerColor(2)
    graphs['PU140']['HGCal'].Draw('lepz')
  
    graphs['PU140']['HF'].SetMarkerStyle(27)
    graphs['PU140']['HF'].SetMarkerSize(1.5)
    graphs['PU140']['HF'].SetLineWidth(2)
    graphs['PU140']['HF'].SetLineStyle(2)
    graphs['PU140']['HF'].SetLineColor(4)
    graphs['PU140']['HF'].SetMarkerColor(4)
    graphs['PU140']['HF'].Draw('lepz')
  except: pass

  try:
    graphs['PU200']['HB'].SetMarkerStyle(20)
    graphs['PU200']['HB'].SetMarkerSize(1)
    graphs['PU200']['HB'].SetLineWidth(2)
    graphs['PU200']['HB'].SetLineStyle(1)
    graphs['PU200']['HB'].SetLineColor(1)
    graphs['PU200']['HB'].SetMarkerColor(1)
    graphs['PU200']['HB'].Draw('lepz')
  
    graphs['PU200']['HGCal'].SetMarkerStyle(21)
    graphs['PU200']['HGCal'].SetMarkerSize(1)
    graphs['PU200']['HGCal'].SetLineWidth(2)
    graphs['PU200']['HGCal'].SetLineStyle(1)
    graphs['PU200']['HGCal'].SetLineColor(2)
    graphs['PU200']['HGCal'].SetMarkerColor(2)
    graphs['PU200']['HGCal'].Draw('lepz')
  
    graphs['PU200']['HF'].SetMarkerStyle(33)
    graphs['PU200']['HF'].SetMarkerSize(1.5)
    graphs['PU200']['HF'].SetLineWidth(2)
    graphs['PU200']['HF'].SetLineStyle(1)
    graphs['PU200']['HF'].SetLineColor(4)
    graphs['PU200']['HF'].SetMarkerColor(4)
    graphs['PU200']['HF'].Draw('lepz')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.45, 0.90, 'NDC')
  l1tRateLabel.SetFillColor(0)
  l1tRateLabel.SetFillStyle(1001)
  l1tRateLabel.SetTextColor(ROOT.kBlack)
  l1tRateLabel.SetTextAlign(12)
  l1tRateLabel.SetTextFont(42)
  l1tRateLabel.SetTextSize(0.035)
  l1tRateLabel.SetBorderSize(0)
  l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
  l1tRateLabel.Draw('same')

  hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.45, 0.85, 'NDC')
  hltRateLabel.SetFillColor(0)
  hltRateLabel.SetFillStyle(1001)
  hltRateLabel.SetTextColor(ROOT.kBlack)
  hltRateLabel.SetTextAlign(12)
  hltRateLabel.SetTextFont(42)
  hltRateLabel.SetTextSize(0.035)
  hltRateLabel.SetBorderSize(0)
  hltRateLabel.AddText('p_{T}^{GEN} > 20 GeV')
  hltRateLabel.Draw('same')

  hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
  hltTargetRateLine.SetLineWidth(2)
  hltTargetRateLine.SetLineStyle(2)
  hltTargetRateLine.SetLineColor(ROOT.kGray)
  hltTargetRateLine.Draw('same')

  try:
    _htmpHB = ROOT.TH1D()
    _htmpHB.SetLineStyle(graphs['PU200']['HB'].GetLineStyle())
    _htmpHB.SetLineWidth(graphs['PU200']['HB'].GetLineWidth())
    _htmpHB.SetLineColor(graphs['PU200']['HB'].GetLineColor())
    _htmpHB.SetMarkerColor(graphs['PU200']['HB'].GetMarkerColor())
    _htmpHB.SetMarkerSize(graphs['PU200']['HB'].GetMarkerSize())
    _htmpHB.SetMarkerStyle(graphs['PU200']['HB'].GetMarkerStyle())

    _htmpHGCal = ROOT.TH1D()
    _htmpHGCal.SetLineStyle(graphs['PU200']['HGCal'].GetLineStyle())
    _htmpHGCal.SetLineWidth(graphs['PU200']['HGCal'].GetLineWidth())
    _htmpHGCal.SetLineColor(graphs['PU200']['HGCal'].GetLineColor())
    _htmpHGCal.SetMarkerColor(graphs['PU200']['HGCal'].GetMarkerColor())
    _htmpHGCal.SetMarkerSize(graphs['PU200']['HGCal'].GetMarkerSize())
    _htmpHGCal.SetMarkerStyle(graphs['PU200']['HGCal'].GetMarkerStyle())

    _htmpHF = ROOT.TH1D()
    _htmpHF.SetLineStyle(graphs['PU200']['HF'].GetLineStyle())
    _htmpHF.SetLineWidth(graphs['PU200']['HF'].GetLineWidth())
    _htmpHF.SetLineColor(graphs['PU200']['HF'].GetLineColor())
    _htmpHF.SetMarkerColor(graphs['PU200']['HF'].GetMarkerColor())
    _htmpHF.SetMarkerSize(graphs['PU200']['HF'].GetMarkerSize())
    _htmpHF.SetMarkerStyle(graphs['PU200']['HF'].GetMarkerStyle())

    leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.45)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.SetEntrySeparation(0.4)
    leg1.AddEntry(_htmpHB, '|#eta|<1.5', 'ep')
    leg1.AddEntry(_htmpHGCal, '1.5<|#eta|<3.0', 'ep')
    leg1.AddEntry(_htmpHF, '3.0<|#eta|<5.0', 'ep')
    leg1.Draw('same')
  except: pass

  leg2 = ROOT.TLegend(0.70, 0.47, 0.94, 0.62)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    _htmpPU140 = graphs['PU140']['HB'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass

  try:
    _htmpPU200 = graphs['PU200']['HB'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass

  leg2.Draw('same')

  h0.SetTitle(';'+jetTag3+' Jet p_{T} [GeV];GEN-Matching Efficiency')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogx(1)
  canvas.SetLogy(0)
  canvas.SetGrid(1, 1)

  h0.GetXaxis().SetNoExponent()
  h0.GetXaxis().SetMoreLogLabels()

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'_recoMatchEff.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'_recoMatchEff'+'\033[0m'

  # HLT - NotMatchedToGEN
  graphs = {
    'PU140': {
      'HB': [30, 40, 50, 60, 100, 140, 200, 600],
      'HGCal': [30, 40, 50, 60, 100, 140, 200, 600],
      'HF': [30, 40, 50, 60, 100, 190, 610],
    },
    'PU200': {
      'HB': [30, 40, 50, 60, 100, 140, 200, 600],
      'HGCal': [30, 40, 50, 60, 100, 140, 200, 600],
      'HF': [30, 40, 50, 60, 100, 190, 610],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _etaTag in graphs[_puTag]:
      _binEdges = array.array('d', graphs[_puTag][_etaTag])

      _htmpNum = getHistogram(_tmpTFile, 'NoSelection/'+jetTag1+'_'+_etaTag+'_NotMatchedToGEN_pt')
      _htmpDen = getHistogram(_tmpTFile, 'NoSelection/'+jetTag1+'_'+_etaTag+'_pt')
      _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
      _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

      graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)
      graphs[_puTag][_etaTag].UseCurrentStyle()
      for _tmpn in range(graphs[_puTag][_etaTag].GetN()):
        graphs[_puTag][_etaTag].SetPointEXhigh(_tmpn, 0.)
        graphs[_puTag][_etaTag].SetPointEXlow(_tmpn, 0.)

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(30., 3e-4, 500., 4.9)

  try:
    graphs['PU140']['HB'].SetMarkerStyle(20)
    graphs['PU140']['HB'].SetMarkerSize(1)
    graphs['PU140']['HB'].SetLineWidth(2)
    graphs['PU140']['HB'].SetLineStyle(2)
    graphs['PU140']['HB'].SetLineColor(1)
    graphs['PU140']['HB'].SetMarkerColor(1)
    graphs['PU140']['HB'].Draw('lepz')

    graphs['PU140']['HGCal'].SetMarkerStyle(21)
    graphs['PU140']['HGCal'].SetMarkerSize(1)
    graphs['PU140']['HGCal'].SetLineWidth(2)
    graphs['PU140']['HGCal'].SetLineStyle(2)
    graphs['PU140']['HGCal'].SetLineColor(2)
    graphs['PU140']['HGCal'].SetMarkerColor(2)
    graphs['PU140']['HGCal'].Draw('lepz')

    graphs['PU140']['HF'].SetMarkerStyle(33)
    graphs['PU140']['HF'].SetMarkerSize(1.5)
    graphs['PU140']['HF'].SetLineWidth(2)
    graphs['PU140']['HF'].SetLineStyle(2)
    graphs['PU140']['HF'].SetLineColor(4)
    graphs['PU140']['HF'].SetMarkerColor(4)
    graphs['PU140']['HF'].Draw('lepz')
  except: pass

  try:  
    graphs['PU200']['HB'].SetMarkerStyle(20)
    graphs['PU200']['HB'].SetMarkerSize(1)
    graphs['PU200']['HB'].SetLineWidth(2)
    graphs['PU200']['HB'].SetLineStyle(1)
    graphs['PU200']['HB'].SetLineColor(1)
    graphs['PU200']['HB'].SetMarkerColor(1)
    graphs['PU200']['HB'].Draw('lepz')

    graphs['PU200']['HGCal'].SetMarkerStyle(21)
    graphs['PU200']['HGCal'].SetMarkerSize(1)
    graphs['PU200']['HGCal'].SetLineWidth(2)
    graphs['PU200']['HGCal'].SetLineStyle(1)
    graphs['PU200']['HGCal'].SetLineColor(2)
    graphs['PU200']['HGCal'].SetMarkerColor(2)
    graphs['PU200']['HGCal'].Draw('lepz')

    graphs['PU200']['HF'].SetMarkerStyle(33)
    graphs['PU200']['HF'].SetMarkerSize(1.5)
    graphs['PU200']['HF'].SetLineWidth(2)
    graphs['PU200']['HF'].SetLineStyle(1)
    graphs['PU200']['HF'].SetLineColor(4)
    graphs['PU200']['HF'].SetMarkerColor(4)
    graphs['PU200']['HF'].Draw('lepz')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.45, 0.90, 'NDC')
  l1tRateLabel.SetFillColor(0)
  l1tRateLabel.SetFillStyle(1001)
  l1tRateLabel.SetTextColor(ROOT.kBlack)
  l1tRateLabel.SetTextAlign(12)
  l1tRateLabel.SetTextFont(42)
  l1tRateLabel.SetTextSize(0.035)
  l1tRateLabel.SetBorderSize(0)
  l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
  l1tRateLabel.Draw('same')

  hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.45, 0.85, 'NDC')
  hltRateLabel.SetFillColor(0)
  hltRateLabel.SetFillStyle(1001)
  hltRateLabel.SetTextColor(ROOT.kBlack)
  hltRateLabel.SetTextAlign(12)
  hltRateLabel.SetTextFont(42)
  hltRateLabel.SetTextSize(0.035)
  hltRateLabel.SetBorderSize(0)
  hltRateLabel.AddText('p_{T}^{GEN} > 20 GeV')
  hltRateLabel.Draw('same')

  hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
  hltTargetRateLine.SetLineWidth(2)
  hltTargetRateLine.SetLineStyle(2)
  hltTargetRateLine.SetLineColor(ROOT.kGray)
  hltTargetRateLine.Draw('same')

  try:
    _htmpHB = ROOT.TH1D()
    _htmpHB.SetLineStyle(graphs['PU200']['HB'].GetLineStyle())
    _htmpHB.SetLineWidth(graphs['PU200']['HB'].GetLineWidth())
    _htmpHB.SetLineColor(graphs['PU200']['HB'].GetLineColor())
    _htmpHB.SetMarkerColor(graphs['PU200']['HB'].GetMarkerColor())
    _htmpHB.SetMarkerSize(graphs['PU200']['HB'].GetMarkerSize())
    _htmpHB.SetMarkerStyle(graphs['PU200']['HB'].GetMarkerStyle())
  
    _htmpHGCal = ROOT.TH1D()
    _htmpHGCal.SetLineStyle(graphs['PU200']['HGCal'].GetLineStyle())
    _htmpHGCal.SetLineWidth(graphs['PU200']['HGCal'].GetLineWidth())
    _htmpHGCal.SetLineColor(graphs['PU200']['HGCal'].GetLineColor())
    _htmpHGCal.SetMarkerColor(graphs['PU200']['HGCal'].GetMarkerColor())
    _htmpHGCal.SetMarkerSize(graphs['PU200']['HGCal'].GetMarkerSize())
    _htmpHGCal.SetMarkerStyle(graphs['PU200']['HGCal'].GetMarkerStyle())
  
    _htmpHF = ROOT.TH1D()
    _htmpHF.SetLineStyle(graphs['PU200']['HF'].GetLineStyle())
    _htmpHF.SetLineWidth(graphs['PU200']['HF'].GetLineWidth())
    _htmpHF.SetLineColor(graphs['PU200']['HF'].GetLineColor())
    _htmpHF.SetMarkerColor(graphs['PU200']['HF'].GetMarkerColor())
    _htmpHF.SetMarkerSize(graphs['PU200']['HF'].GetMarkerSize())
    _htmpHF.SetMarkerStyle(graphs['PU200']['HF'].GetMarkerStyle())
  
    leg1 = ROOT.TLegend(0.60, 0.65, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.SetEntrySeparation(0.4)
    leg1.AddEntry(_htmpHB   ,     '|#eta|<1.5', 'ep')
    leg1.AddEntry(_htmpHGCal, '1.5<|#eta|<3.0', 'ep')
    leg1.AddEntry(_htmpHF   , '3.0<|#eta|<5.0', 'ep')
    leg1.Draw('same')
  except: pass

  leg2 = ROOT.TLegend(0.70, 0.48, 0.94, 0.63)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    _htmpPU140 = graphs['PU140']['HB'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass
  try:
    _htmpPU200 = graphs['PU200']['HB'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  h0.SetTitle(';'+jetTag3+' Jet p_{T} [GeV];Jet Mistag Rate')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogx(1)
  canvas.SetLogy(1)
  canvas.SetGrid(1, 1)

  h0.GetXaxis().SetNoExponent()
  h0.GetXaxis().SetMoreLogLabels()

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'_recoMistagRate.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'_recoMistagRate'+'\033[0m'

  # GEN - MatchedToReco
  graphs = {
    'PU140': {
      'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HF': [30, 40, 50, 60, 80, 120, 240, 600],
    },
    'PU200': {
      'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'HF': [30, 40, 50, 60, 80, 120, 240, 600],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _etaTag in graphs[_puTag]:
      _binEdges = array.array('d', graphs[_puTag][_etaTag])

      _htmpNum = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_MatchedTo'+jetTag2+'_pt')
      _htmpDen = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_pt')
      _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
      _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

      graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)
      graphs[_puTag][_etaTag].UseCurrentStyle()
      for _tmpn in range(graphs[_puTag][_etaTag].GetN()):
        graphs[_puTag][_etaTag].SetPointEXhigh(_tmpn, 0.)
        graphs[_puTag][_etaTag].SetPointEXlow(_tmpn, 0.)

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(30., 0.0001, 600., 1.2)

  try:
    graphs['PU140']['HB'].SetMarkerStyle(20)
    graphs['PU140']['HB'].SetMarkerSize(1)
    graphs['PU140']['HB'].SetLineWidth(2)
    graphs['PU140']['HB'].SetLineStyle(2)
    graphs['PU140']['HB'].SetLineColor(1)
    graphs['PU140']['HB'].SetMarkerColor(1)
    graphs['PU140']['HB'].Draw('lepz')
  
    graphs['PU140']['HGCal'].SetMarkerStyle(21)
    graphs['PU140']['HGCal'].SetMarkerSize(1)
    graphs['PU140']['HGCal'].SetLineWidth(2)
    graphs['PU140']['HGCal'].SetLineStyle(2)
    graphs['PU140']['HGCal'].SetLineColor(2)
    graphs['PU140']['HGCal'].SetMarkerColor(2)
    graphs['PU140']['HGCal'].Draw('lepz')
  
    graphs['PU140']['HF'].SetMarkerStyle(33)
    graphs['PU140']['HF'].SetMarkerSize(1.5)
    graphs['PU140']['HF'].SetLineWidth(2)
    graphs['PU140']['HF'].SetLineStyle(2)
    graphs['PU140']['HF'].SetLineColor(4)
    graphs['PU140']['HF'].SetMarkerColor(4)
    graphs['PU140']['HF'].Draw('lepz')
  except: pass

  try:
    graphs['PU200']['HB'].SetMarkerStyle(20)
    graphs['PU200']['HB'].SetMarkerSize(1)
    graphs['PU200']['HB'].SetLineWidth(2)
    graphs['PU200']['HB'].SetLineStyle(1)
    graphs['PU200']['HB'].SetLineColor(1)
    graphs['PU200']['HB'].SetMarkerColor(1)
    graphs['PU200']['HB'].Draw('lepz')
  
    graphs['PU200']['HGCal'].SetMarkerStyle(21)
    graphs['PU200']['HGCal'].SetMarkerSize(1)
    graphs['PU200']['HGCal'].SetLineWidth(2)
    graphs['PU200']['HGCal'].SetLineStyle(1)
    graphs['PU200']['HGCal'].SetLineColor(2)
    graphs['PU200']['HGCal'].SetMarkerColor(2)
    graphs['PU200']['HGCal'].Draw('lepz')
  
    graphs['PU200']['HF'].SetMarkerStyle(33)
    graphs['PU200']['HF'].SetMarkerSize(1.5)
    graphs['PU200']['HF'].SetLineWidth(2)
    graphs['PU200']['HF'].SetLineStyle(1)
    graphs['PU200']['HF'].SetLineColor(4)
    graphs['PU200']['HF'].SetMarkerColor(4)
    graphs['PU200']['HF'].Draw('lepz')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.45, 0.90, 'NDC')
  l1tRateLabel.SetFillColor(0)
  l1tRateLabel.SetFillStyle(1001)
  l1tRateLabel.SetTextColor(ROOT.kBlack)
  l1tRateLabel.SetTextAlign(12)
  l1tRateLabel.SetTextFont(42)
  l1tRateLabel.SetTextSize(0.035)
  l1tRateLabel.SetBorderSize(0)
  l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
  l1tRateLabel.Draw('same')

  hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.45, 0.85, 'NDC')
  hltRateLabel.SetFillColor(0)
  hltRateLabel.SetFillStyle(1001)
  hltRateLabel.SetTextColor(ROOT.kBlack)
  hltRateLabel.SetTextAlign(12)
  hltRateLabel.SetTextFont(42)
  hltRateLabel.SetTextSize(0.035)
  hltRateLabel.SetBorderSize(0)
  hltRateLabel.AddText('p_{T}^{'+jetTag3+'} > 20 GeV')
  hltRateLabel.Draw('same')

  hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
  hltTargetRateLine.SetLineWidth(2)
  hltTargetRateLine.SetLineStyle(2)
  hltTargetRateLine.SetLineColor(ROOT.kGray)
  hltTargetRateLine.Draw('same')

  try:
    _htmpHB = ROOT.TH1D()
    _htmpHB.SetLineStyle(graphs['PU200']['HB'].GetLineStyle())
    _htmpHB.SetLineWidth(graphs['PU200']['HB'].GetLineWidth())
    _htmpHB.SetLineColor(graphs['PU200']['HB'].GetLineColor())
    _htmpHB.SetMarkerColor(graphs['PU200']['HB'].GetMarkerColor())
    _htmpHB.SetMarkerSize(graphs['PU200']['HB'].GetMarkerSize())
    _htmpHB.SetMarkerStyle(graphs['PU200']['HB'].GetMarkerStyle())
  
    _htmpHGCal = ROOT.TH1D()
    _htmpHGCal.SetLineStyle(graphs['PU200']['HGCal'].GetLineStyle())
    _htmpHGCal.SetLineWidth(graphs['PU200']['HGCal'].GetLineWidth())
    _htmpHGCal.SetLineColor(graphs['PU200']['HGCal'].GetLineColor())
    _htmpHGCal.SetMarkerColor(graphs['PU200']['HGCal'].GetMarkerColor())
    _htmpHGCal.SetMarkerSize(graphs['PU200']['HGCal'].GetMarkerSize())
    _htmpHGCal.SetMarkerStyle(graphs['PU200']['HGCal'].GetMarkerStyle())
  
    _htmpHF = ROOT.TH1D()
    _htmpHF.SetLineStyle(graphs['PU200']['HF'].GetLineStyle())
    _htmpHF.SetLineWidth(graphs['PU200']['HF'].GetLineWidth())
    _htmpHF.SetLineColor(graphs['PU200']['HF'].GetLineColor())
    _htmpHF.SetMarkerColor(graphs['PU200']['HF'].GetMarkerColor())
    _htmpHF.SetMarkerSize(graphs['PU200']['HF'].GetMarkerSize())
    _htmpHF.SetMarkerStyle(graphs['PU200']['HF'].GetMarkerStyle())
  
    leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.45)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.SetEntrySeparation(0.4)
    leg1.AddEntry(_htmpHB   ,     '|#eta|<1.5', 'ep')
    leg1.AddEntry(_htmpHGCal, '1.5<|#eta|<3.0', 'ep')
    leg1.AddEntry(_htmpHF   , '3.0<|#eta|<5.0', 'ep')
    leg1.Draw('same')
  except: pass

  leg2 = ROOT.TLegend(0.70, 0.47, 0.94, 0.62)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    _htmpPU140 = graphs['PU140']['HB'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass
  try:
    _htmpPU200 = graphs['PU200']['HB'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  h0.SetTitle(';GEN Jet p_{T} [GeV];Jet-Finding Efficiency')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogx(1)
  canvas.SetLogy(0)
  canvas.SetGrid(1, 1)

  h0.GetXaxis().SetNoExponent()
  h0.GetXaxis().SetMoreLogLabels()

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'_genMatchEff.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'_genMatchEff'+'\033[0m'

  # GEN - NotMatchedToReco
  graphs = {
    'PU140': {
      'HB': [30, 40, 50, 60, 100, 140, 200, 300, 600],
      'HGCal': [30, 40, 50, 60, 100, 140, 200, 300, 600],
      'HF': [30, 40, 50, 60, 80, 180, 600],
    },
    'PU200': {
      'HB': [30, 40, 50, 60, 100, 140, 200, 300, 600],
      'HGCal': [30, 40, 50, 60, 100, 140, 200, 300, 600],
      'HF': [30, 40, 50, 60, 80, 180, 600],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _etaTag in graphs[_puTag]:
      _binEdges = array.array('d', graphs[_puTag][_etaTag])

      _htmpNum = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_NotMatchedTo'+jetTag2+'_pt')
      _htmpDen = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_pt')
      _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
      _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

      graphs[_puTag][_etaTag] = get_efficiency_graph(_htmpNum, _htmpDen)
      graphs[_puTag][_etaTag].UseCurrentStyle()
      for _tmpn in range(graphs[_puTag][_etaTag].GetN()):
        graphs[_puTag][_etaTag].SetPointEXhigh(_tmpn, 0.)
        graphs[_puTag][_etaTag].SetPointEXlow(_tmpn, 0.)

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(30., 1e-4, 500., 4.9)

  try:
    graphs['PU140']['HB'].SetMarkerStyle(20)
    graphs['PU140']['HB'].SetMarkerSize(1)
    graphs['PU140']['HB'].SetLineWidth(2)
    graphs['PU140']['HB'].SetLineStyle(2)
    graphs['PU140']['HB'].SetLineColor(1)
    graphs['PU140']['HB'].SetMarkerColor(1)
    graphs['PU140']['HB'].Draw('lepz')
  
    graphs['PU140']['HGCal'].SetMarkerStyle(21)
    graphs['PU140']['HGCal'].SetMarkerSize(1)
    graphs['PU140']['HGCal'].SetLineWidth(2)
    graphs['PU140']['HGCal'].SetLineStyle(2)
    graphs['PU140']['HGCal'].SetLineColor(2)
    graphs['PU140']['HGCal'].SetMarkerColor(2)
    graphs['PU140']['HGCal'].Draw('lepz')
  
    graphs['PU140']['HF'].SetMarkerStyle(33)
    graphs['PU140']['HF'].SetMarkerSize(1.5)
    graphs['PU140']['HF'].SetLineWidth(2)
    graphs['PU140']['HF'].SetLineStyle(2)
    graphs['PU140']['HF'].SetLineColor(4)
    graphs['PU140']['HF'].SetMarkerColor(4)
    graphs['PU140']['HF'].Draw('lepz')
  except: pass

  try:  
    graphs['PU200']['HB'].SetMarkerStyle(20)
    graphs['PU200']['HB'].SetMarkerSize(1)
    graphs['PU200']['HB'].SetLineWidth(2)
    graphs['PU200']['HB'].SetLineStyle(1)
    graphs['PU200']['HB'].SetLineColor(1)
    graphs['PU200']['HB'].SetMarkerColor(1)
    graphs['PU200']['HB'].Draw('lepz')

    graphs['PU200']['HGCal'].SetMarkerStyle(21)
    graphs['PU200']['HGCal'].SetMarkerSize(1)
    graphs['PU200']['HGCal'].SetLineWidth(2)
    graphs['PU200']['HGCal'].SetLineStyle(1)
    graphs['PU200']['HGCal'].SetLineColor(2)
    graphs['PU200']['HGCal'].SetMarkerColor(2)
    graphs['PU200']['HGCal'].Draw('lepz')

    graphs['PU200']['HF'].SetMarkerStyle(33)
    graphs['PU200']['HF'].SetMarkerSize(1.5)
    graphs['PU200']['HF'].SetLineWidth(2)
    graphs['PU200']['HF'].SetLineStyle(1)
    graphs['PU200']['HF'].SetLineColor(4)
    graphs['PU200']['HF'].SetMarkerColor(4)
    graphs['PU200']['HF'].Draw('lepz')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.45, 0.90, 'NDC')
  l1tRateLabel.SetFillColor(0)
  l1tRateLabel.SetFillStyle(1001)
  l1tRateLabel.SetTextColor(ROOT.kBlack)
  l1tRateLabel.SetTextAlign(12)
  l1tRateLabel.SetTextFont(42)
  l1tRateLabel.SetTextSize(0.035)
  l1tRateLabel.SetBorderSize(0)
  l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
  l1tRateLabel.Draw('same')

  hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.45, 0.85, 'NDC')
  hltRateLabel.SetFillColor(0)
  hltRateLabel.SetFillStyle(1001)
  hltRateLabel.SetTextColor(ROOT.kBlack)
  hltRateLabel.SetTextAlign(12)
  hltRateLabel.SetTextFont(42)
  hltRateLabel.SetTextSize(0.035)
  hltRateLabel.SetBorderSize(0)
  hltRateLabel.AddText('p_{T}^{'+jetTag3+'} > 20 GeV')
  hltRateLabel.Draw('same')

  hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
  hltTargetRateLine.SetLineWidth(2)
  hltTargetRateLine.SetLineStyle(2)
  hltTargetRateLine.SetLineColor(ROOT.kGray)
  hltTargetRateLine.Draw('same')

  try:
    _htmpHB = ROOT.TH1D()
    _htmpHB.SetLineStyle(graphs['PU200']['HB'].GetLineStyle())
    _htmpHB.SetLineWidth(graphs['PU200']['HB'].GetLineWidth())
    _htmpHB.SetLineColor(graphs['PU200']['HB'].GetLineColor())
    _htmpHB.SetMarkerColor(graphs['PU200']['HB'].GetMarkerColor())
    _htmpHB.SetMarkerSize(graphs['PU200']['HB'].GetMarkerSize())
    _htmpHB.SetMarkerStyle(graphs['PU200']['HB'].GetMarkerStyle())

    _htmpHGCal = ROOT.TH1D()
    _htmpHGCal.SetLineStyle(graphs['PU200']['HGCal'].GetLineStyle())
    _htmpHGCal.SetLineWidth(graphs['PU200']['HGCal'].GetLineWidth())
    _htmpHGCal.SetLineColor(graphs['PU200']['HGCal'].GetLineColor())
    _htmpHGCal.SetMarkerColor(graphs['PU200']['HGCal'].GetMarkerColor())
    _htmpHGCal.SetMarkerSize(graphs['PU200']['HGCal'].GetMarkerSize())
    _htmpHGCal.SetMarkerStyle(graphs['PU200']['HGCal'].GetMarkerStyle())

    _htmpHF = ROOT.TH1D()
    _htmpHF.SetLineStyle(graphs['PU200']['HF'].GetLineStyle())
    _htmpHF.SetLineWidth(graphs['PU200']['HF'].GetLineWidth())
    _htmpHF.SetLineColor(graphs['PU200']['HF'].GetLineColor())
    _htmpHF.SetMarkerColor(graphs['PU200']['HF'].GetMarkerColor())
    _htmpHF.SetMarkerSize(graphs['PU200']['HF'].GetMarkerSize())
    _htmpHF.SetMarkerStyle(graphs['PU200']['HF'].GetMarkerStyle())

    leg1 = ROOT.TLegend(0.60, 0.65, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.SetEntrySeparation(0.4)
    leg1.AddEntry(_htmpHB   ,     '|#eta|<1.5', 'ep')
    leg1.AddEntry(_htmpHGCal, '1.5<|#eta|<3.0', 'ep')
    leg1.AddEntry(_htmpHF   , '3.0<|#eta|<5.0', 'ep')
    leg1.Draw('same')
  except: pass

  leg2 = ROOT.TLegend(0.70, 0.48, 0.94, 0.63)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    _htmpPU140 = graphs['PU140']['HB'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass
  try:
    _htmpPU200 = graphs['PU200']['HB'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  h0.SetTitle(';GEN Jet p_{T} [GeV];% of Unreconstructed GEN Jets')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogx(1)
  canvas.SetLogy(1)
  canvas.SetGrid(1, 1)

  h0.GetXaxis().SetNoExponent()
  h0.GetXaxis().SetMoreLogLabels()

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'_genMistagRate.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'_genMistagRate'+'\033[0m'

  # GEN - MatchedToReco wrt eta
  graphs = {
    'PU140': {
      'Pt050': [-5.+_tmp*0.1 for _tmp in range(101)],
      'Pt100': [-5.+_tmp*0.1 for _tmp in range(101)],
      'Pt200': [-5.+_tmp*0.1 for _tmp in range(101)],
    },
    'PU200': {
      'Pt050': [-5.+_tmp*0.1 for _tmp in range(101)],
      'Pt100': [-5.+_tmp*0.1 for _tmp in range(101)],
      'Pt200': [-5.+_tmp*0.1 for _tmp in range(101)],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _ptTag in graphs[_puTag]:
      _binEdges = array.array('d', graphs[_puTag][_ptTag])

      _htmpNum = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_EtaIncl_MatchedTo'+jetTag2+'_eta__vs__pt')
      _htmpDen = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_EtaIncl_eta__vs__pt')

      _htmpNum = _htmpNum.ProjectionX(tmpName(), _htmpNum.GetYaxis().FindBin(float(_ptTag[2:])*1.00001), -1)
      _htmpDen = _htmpDen.ProjectionX(tmpName(), _htmpDen.GetYaxis().FindBin(float(_ptTag[2:])*1.00001), -1)

      _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
      _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)

      graphs[_puTag][_ptTag] = get_efficiency_graph(_htmpNum, _htmpDen)
      graphs[_puTag][_ptTag].UseCurrentStyle()
      for _tmpn in range(graphs[_puTag][_ptTag].GetN()):
        graphs[_puTag][_ptTag].SetPointEXhigh(_tmpn, 0.)
        graphs[_puTag][_ptTag].SetPointEXlow(_tmpn, 0.)

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(-5., 0.51, 5., 1.14)

  try:
    graphs['PU140']['Pt050'].SetMarkerStyle(20)
    graphs['PU140']['Pt050'].SetMarkerSize(1)
    graphs['PU140']['Pt050'].SetLineWidth(2)
    graphs['PU140']['Pt050'].SetLineStyle(2)
    graphs['PU140']['Pt050'].SetLineColor(1)
    graphs['PU140']['Pt050'].SetMarkerColor(1)
    graphs['PU140']['Pt050'].Draw('lepz')

    graphs['PU140']['Pt100'].SetMarkerStyle(21)
    graphs['PU140']['Pt100'].SetMarkerSize(1)
    graphs['PU140']['Pt100'].SetLineWidth(2)
    graphs['PU140']['Pt100'].SetLineStyle(2)
    graphs['PU140']['Pt100'].SetLineColor(2)
    graphs['PU140']['Pt100'].SetMarkerColor(2)
    graphs['PU140']['Pt100'].Draw('lepz')
  
    graphs['PU140']['Pt200'].SetMarkerStyle(33)
    graphs['PU140']['Pt200'].SetMarkerSize(1.5)
    graphs['PU140']['Pt200'].SetLineWidth(2)
    graphs['PU140']['Pt200'].SetLineStyle(2)
    graphs['PU140']['Pt200'].SetLineColor(4)
    graphs['PU140']['Pt200'].SetMarkerColor(4)
    graphs['PU140']['Pt200'].Draw('lepz')
  except: pass

  try:
    graphs['PU200']['Pt050'].SetMarkerStyle(20)
    graphs['PU200']['Pt050'].SetMarkerSize(1)
    graphs['PU200']['Pt050'].SetLineWidth(2)
    graphs['PU200']['Pt050'].SetLineStyle(1)
    graphs['PU200']['Pt050'].SetLineColor(1)
    graphs['PU200']['Pt050'].SetMarkerColor(1)
    graphs['PU200']['Pt050'].Draw('lepz')
  
    graphs['PU200']['Pt100'].SetMarkerStyle(21)
    graphs['PU200']['Pt100'].SetMarkerSize(1)
    graphs['PU200']['Pt100'].SetLineWidth(2)
    graphs['PU200']['Pt100'].SetLineStyle(1)
    graphs['PU200']['Pt100'].SetLineColor(2)
    graphs['PU200']['Pt100'].SetMarkerColor(2)
    graphs['PU200']['Pt100'].Draw('lepz')
  
    graphs['PU200']['Pt200'].SetMarkerStyle(33)
    graphs['PU200']['Pt200'].SetMarkerSize(1.5)
    graphs['PU200']['Pt200'].SetLineWidth(2)
    graphs['PU200']['Pt200'].SetLineStyle(1)
    graphs['PU200']['Pt200'].SetLineColor(4)
    graphs['PU200']['Pt200'].SetMarkerColor(4)
    graphs['PU200']['Pt200'].Draw('lepz')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.50, 0.90, 'NDC')
  l1tRateLabel.SetFillColor(0)
  l1tRateLabel.SetFillStyle(1001)
  l1tRateLabel.SetTextColor(ROOT.kBlack)
  l1tRateLabel.SetTextAlign(12)
  l1tRateLabel.SetTextFont(42)
  l1tRateLabel.SetTextSize(0.035)
  l1tRateLabel.SetBorderSize(0)
  l1tRateLabel.AddText('AK4 PF+PUPPI Jets')
  l1tRateLabel.Draw('same')

  hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.35, 0.85, 'NDC')
  hltRateLabel.SetFillColor(0)
  hltRateLabel.SetFillStyle(1001)
  hltRateLabel.SetTextColor(ROOT.kBlack)
  hltRateLabel.SetTextAlign(12)
  hltRateLabel.SetTextFont(42)
  hltRateLabel.SetTextSize(0.035)
  hltRateLabel.SetBorderSize(0)
  hltRateLabel.AddText('p_{T}^{'+jetTag3+'} > 20 GeV')
  hltRateLabel.Draw('same')

  hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
  hltTargetRateLine.SetLineWidth(2)
  hltTargetRateLine.SetLineStyle(2)
  hltTargetRateLine.SetLineColor(ROOT.kGray)
  hltTargetRateLine.Draw('same')

  try:
    _htmpPt050 = ROOT.TH1D()
    _htmpPt050.SetLineStyle(graphs['PU200']['Pt050'].GetLineStyle())
    _htmpPt050.SetLineWidth(graphs['PU200']['Pt050'].GetLineWidth())
    _htmpPt050.SetLineColor(graphs['PU200']['Pt050'].GetLineColor())
    _htmpPt050.SetMarkerColor(graphs['PU200']['Pt050'].GetMarkerColor())
    _htmpPt050.SetMarkerSize(graphs['PU200']['Pt050'].GetMarkerSize())
    _htmpPt050.SetMarkerStyle(graphs['PU200']['Pt050'].GetMarkerStyle())
  
    _htmpPt100 = ROOT.TH1D()
    _htmpPt100.SetLineStyle(graphs['PU200']['Pt100'].GetLineStyle())
    _htmpPt100.SetLineWidth(graphs['PU200']['Pt100'].GetLineWidth())
    _htmpPt100.SetLineColor(graphs['PU200']['Pt100'].GetLineColor())
    _htmpPt100.SetMarkerColor(graphs['PU200']['Pt100'].GetMarkerColor())
    _htmpPt100.SetMarkerSize(graphs['PU200']['Pt100'].GetMarkerSize())
    _htmpPt100.SetMarkerStyle(graphs['PU200']['Pt100'].GetMarkerStyle())

    _htmpPt200 = ROOT.TH1D()
    _htmpPt200.SetLineStyle(graphs['PU200']['Pt200'].GetLineStyle())
    _htmpPt200.SetLineWidth(graphs['PU200']['Pt200'].GetLineWidth())
    _htmpPt200.SetLineColor(graphs['PU200']['Pt200'].GetLineColor())
    _htmpPt200.SetMarkerColor(graphs['PU200']['Pt200'].GetMarkerColor())
    _htmpPt200.SetMarkerSize(graphs['PU200']['Pt200'].GetMarkerSize())
    _htmpPt200.SetMarkerStyle(graphs['PU200']['Pt200'].GetMarkerStyle())

    leg1 = ROOT.TLegend(0.38, 0.20, 0.72, 0.45)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.SetEntrySeparation(0.4)
    leg1.AddEntry(_htmpPt050, 'p_{T}^{GEN} > 50 GeV', 'ep')
    leg1.AddEntry(_htmpPt100, 'p_{T}^{GEN} > 100 GeV', 'ep')
    leg1.AddEntry(_htmpPt200, 'p_{T}^{GEN} > 200 GeV', 'ep')
    leg1.Draw('same')
  except: pass

  leg2 = ROOT.TLegend(0.42, 0.47, 0.67, 0.62)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    _htmpPU140 = graphs['PU140']['Pt050'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass
  try:
    _htmpPU200 = graphs['PU200']['Pt050'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  h0.SetTitle(';GEN Jet #eta;Jet-Finding Efficiency')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogx(0)
  canvas.SetLogy(0)
  canvas.SetGrid(1, 1)

  h0.GetXaxis().SetNoExponent()
  h0.GetXaxis().SetMoreLogLabels()

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'_genMatchEff_wrtEta.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'_genMatchEff_wrtEta'+'\033[0m'

def plotMETResponse(fpath_PU140, fpath_PU200, outputName, exts):
  histos = {
    'PU140': {
      'PFRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFCHSRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiTypeOne': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
    },
    'PU200': {
      'PFRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFCHSRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiTypeOne': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _metTag, _metHist in {
      'PFRaw': 'NoSelection/hltPFMET_pt_overGEN__vs__GEN_pt',
      'PFCHSRaw': 'NoSelection/hltPFCHSMET_pt_overGEN__vs__GEN_pt',
      'PFPuppiRaw': 'NoSelection/hltPFPuppiMET_pt_overGEN__vs__GEN_pt',
      'PFPuppiTypeOne': 'NoSelection/hltPFPuppiMETTypeOne_pt_overGEN__vs__GEN_pt',
    }.items():
      h1vals = []
      _h2tmp = getHistogram(_tmpTFile, _metHist)
      binEdges = array.array('d', histos[_puTag][_metTag])
      for pTbinEdge_idx in range(len(binEdges)-1):
        _h1tmp = _h2tmp.ProjectionX(tmpName(), _h2tmp.GetYaxis().FindBin(1.0001*binEdges[pTbinEdge_idx]), _h2tmp.GetYaxis().FindBin(0.9999*binEdges[pTbinEdge_idx+1]))
        _h1tmp_val = _h1tmp.GetMean()
        _h1tmp_err = _h1tmp.GetMeanError()
        h1vals.append([_h1tmp_val, _h1tmp_err])

      histos[_puTag][_metTag] = ROOT.TH1D(tmpName(), tmpName(False), len(binEdges)-1, binEdges)
      histos[_puTag][_metTag].SetDirectory(0)
      histos[_puTag][_metTag].UseCurrentStyle()
      for _binIdx in range(histos[_puTag][_metTag].GetNbinsX()):
        if h1vals[_binIdx] != [None, None]:
          histos[_puTag][_metTag].SetBinContent(_binIdx+1, h1vals[_binIdx][0])
          histos[_puTag][_metTag].SetBinError(_binIdx+1, h1vals[_binIdx][1])

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(40, 0.3, 600, 2.19)

  try:
    histos['PU140']['PFRaw'].SetMarkerStyle(24)
    histos['PU140']['PFRaw'].SetMarkerSize(1)
    histos['PU140']['PFRaw'].SetMarkerColor(1)
    histos['PU140']['PFRaw'].SetLineColor(1)
    histos['PU140']['PFRaw'].SetLineWidth(2)
    histos['PU140']['PFRaw'].SetLineStyle(2)
    histos['PU140']['PFRaw'].Draw('ep,same')
  
    histos['PU140']['PFCHSRaw'].SetMarkerStyle(25)
    histos['PU140']['PFCHSRaw'].SetMarkerSize(1)
    histos['PU140']['PFCHSRaw'].SetMarkerColor(ROOT.kViolet)
    histos['PU140']['PFCHSRaw'].SetLineColor(ROOT.kViolet)
    histos['PU140']['PFCHSRaw'].SetLineWidth(2)
    histos['PU140']['PFCHSRaw'].SetLineStyle(2)
    histos['PU140']['PFCHSRaw'].Draw('ep,same')
  
    histos['PU140']['PFPuppiRaw'].SetMarkerStyle(26)
    histos['PU140']['PFPuppiRaw'].SetMarkerSize(1)
    histos['PU140']['PFPuppiRaw'].SetMarkerColor(2)
    histos['PU140']['PFPuppiRaw'].SetLineColor(2)
    histos['PU140']['PFPuppiRaw'].SetLineWidth(2)
    histos['PU140']['PFPuppiRaw'].SetLineStyle(2)
    histos['PU140']['PFPuppiRaw'].Draw('ep,same')
  
    histos['PU140']['PFPuppiTypeOne'].SetMarkerStyle(32)
    histos['PU140']['PFPuppiTypeOne'].SetMarkerSize(1)
    histos['PU140']['PFPuppiTypeOne'].SetMarkerColor(4)
    histos['PU140']['PFPuppiTypeOne'].SetLineColor(4)
    histos['PU140']['PFPuppiTypeOne'].SetLineWidth(2)
    histos['PU140']['PFPuppiTypeOne'].SetLineStyle(2)
    histos['PU140']['PFPuppiTypeOne'].Draw('ep,same')
  except: pass

  try:
    histos['PU200']['PFRaw'].SetMarkerStyle(20)
    histos['PU200']['PFRaw'].SetMarkerSize(1)
    histos['PU200']['PFRaw'].SetMarkerColor(1)
    histos['PU200']['PFRaw'].SetLineColor(1)
    histos['PU200']['PFRaw'].SetLineWidth(2)
    histos['PU200']['PFRaw'].Draw('ep,same')

    histos['PU200']['PFCHSRaw'].SetMarkerStyle(21)
    histos['PU200']['PFCHSRaw'].SetMarkerSize(1)
    histos['PU200']['PFCHSRaw'].SetMarkerColor(ROOT.kViolet)
    histos['PU200']['PFCHSRaw'].SetLineColor(ROOT.kViolet)
    histos['PU200']['PFCHSRaw'].SetLineWidth(2)
    histos['PU200']['PFCHSRaw'].Draw('ep,same')
  
    histos['PU200']['PFPuppiRaw'].SetMarkerStyle(22)
    histos['PU200']['PFPuppiRaw'].SetMarkerSize(1)
    histos['PU200']['PFPuppiRaw'].SetMarkerColor(2)
    histos['PU200']['PFPuppiRaw'].SetLineColor(2)
    histos['PU200']['PFPuppiRaw'].SetLineWidth(2)
    histos['PU200']['PFPuppiRaw'].Draw('ep,same')

    histos['PU200']['PFPuppiTypeOne'].SetMarkerStyle(23)
    histos['PU200']['PFPuppiTypeOne'].SetMarkerSize(1)
    histos['PU200']['PFPuppiTypeOne'].SetMarkerColor(4)
    histos['PU200']['PFPuppiTypeOne'].SetLineColor(4)
    histos['PU200']['PFPuppiTypeOne'].SetLineWidth(2)
    histos['PU200']['PFPuppiTypeOne'].Draw('ep,same')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  leg1 = ROOT.TLegend(0.25, 0.70, 0.94, 0.90)
  leg1.SetNColumns(2)
  leg1.SetTextFont(42)
  try:
    leg1.AddEntry(histos['PU200']['PFRaw'], 'PF (Raw)', 'lepx')
    leg1.AddEntry(histos['PU200']['PFCHSRaw'], 'PF+CHS (Raw)', 'lepx')
    leg1.AddEntry(histos['PU200']['PFPuppiRaw'], 'PF+PUPPI (Raw)', 'lepx')
    leg1.AddEntry(histos['PU200']['PFPuppiTypeOne'], 'PF+PUPPI (Type-1)', 'lepx')
  except: pass
  leg1.Draw('same')

  try:
    _htmpPU140 = histos['PU140']['PFRaw'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
  except: pass

  try:
    _htmpPU200 = histos['PU200']['PFRaw'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
  except: pass

  leg2 = ROOT.TLegend(0.70, 0.53, 0.94, 0.68)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
  except: pass
  try:
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  h0.SetTitle(';GEN p_{T}^{miss} [GeV];#LTp^{HLT}_{T,miss} / p^{GEN}_{T,miss}#GT')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogy(0)
  canvas.SetGrid(1, 1)

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'\033[0m'

def plotMETResolution(resType, fpath_PU140, fpath_PU200, outputName, exts):
  histos = {
    'PU140': {
      'PFRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFCHSRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiTypeOne': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
    },
    'PU200': {
      'PFRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFCHSRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiRaw': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
      'PFPuppiTypeOne': [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300, 350, 400, 500, 600],
    },
  }

  for [_puTag, _tmpFilePath] in [
    ['PU140', fpath_PU140],
    ['PU200', fpath_PU200],
  ]:
    _tmpTFile = ROOT.TFile.Open(_tmpFilePath)
    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue

    for _metTag, _metHistPrefix in {
      'PFRaw': 'NoSelection/hltPFMET_pt_',
      'PFCHSRaw': 'NoSelection/hltPFCHSMET_pt_',
      'PFPuppiRaw': 'NoSelection/hltPFPuppiMET_pt_',
      'PFPuppiTypeOne': 'NoSelection/hltPFPuppiMETTypeOne_pt_',
    }.items():
      h1vals = []
      binEdges = array.array('d', histos[_puTag][_metTag])
      # mean
      _h2tmp_mean = getHistogram(_tmpTFile, _metHistPrefix+'overGEN__vs__GEN_pt')
      _h2tmp_reso = getHistogram(_tmpTFile, _metHistPrefix+resType+'__vs__GEN_pt')
      for pTbinEdge_idx in range(len(binEdges)-1):
        _h1tmp_mean = _h2tmp_mean.ProjectionX(tmpName(), _h2tmp_mean.GetYaxis().FindBin(1.0001*binEdges[pTbinEdge_idx]), _h2tmp_mean.GetYaxis().FindBin(0.9999*binEdges[pTbinEdge_idx+1]))
        _h1tmp_reso = _h2tmp_reso.ProjectionX(tmpName(), _h2tmp_reso.GetYaxis().FindBin(1.0001*binEdges[pTbinEdge_idx]), _h2tmp_reso.GetYaxis().FindBin(0.9999*binEdges[pTbinEdge_idx+1]))

        _h1tmp_val = _h1tmp_reso.GetRMS() / _h1tmp_mean.GetMean() if _h1tmp_mean.GetMean() != 0. else None
        _h1tmp_err = _h1tmp_reso.GetRMSError() / _h1tmp_mean.GetMean() if _h1tmp_mean.GetMean() != 0. else None
        h1vals.append([_h1tmp_val, _h1tmp_err])

      histos[_puTag][_metTag] = ROOT.TH1D(tmpName(), tmpName(False), len(binEdges)-1, binEdges)
      histos[_puTag][_metTag].SetDirectory(0)
      histos[_puTag][_metTag].UseCurrentStyle()
      for _binIdx in range(histos[_puTag][_metTag].GetNbinsX()):
        if h1vals[_binIdx] != [None, None]:
          histos[_puTag][_metTag].SetBinContent(_binIdx+1, h1vals[_binIdx][0])
          histos[_puTag][_metTag].SetBinError(_binIdx+1, h1vals[_binIdx][1])

  canvas = ROOT.TCanvas(tmpName(), tmpName(False))
  canvas.cd()

  h0 = canvas.DrawFrame(40, 20.001, 600, 149.)

  try:
    histos['PU140']['PFRaw'].SetMarkerStyle(24)
    histos['PU140']['PFRaw'].SetMarkerSize(1)
    histos['PU140']['PFRaw'].SetMarkerColor(1)
    histos['PU140']['PFRaw'].SetLineColor(1)
    histos['PU140']['PFRaw'].SetLineWidth(2)
    histos['PU140']['PFRaw'].SetLineStyle(2)
    histos['PU140']['PFRaw'].Draw('ep,same')

    histos['PU140']['PFCHSRaw'].SetMarkerStyle(25)
    histos['PU140']['PFCHSRaw'].SetMarkerSize(1)
    histos['PU140']['PFCHSRaw'].SetMarkerColor(ROOT.kViolet-3)
    histos['PU140']['PFCHSRaw'].SetLineColor(ROOT.kViolet-3)
    histos['PU140']['PFCHSRaw'].SetLineWidth(2)
    histos['PU140']['PFCHSRaw'].SetLineStyle(2)
    histos['PU140']['PFCHSRaw'].Draw('ep,same')
  
    histos['PU140']['PFPuppiRaw'].SetMarkerStyle(26)
    histos['PU140']['PFPuppiRaw'].SetMarkerSize(1)
    histos['PU140']['PFPuppiRaw'].SetMarkerColor(2)
    histos['PU140']['PFPuppiRaw'].SetLineColor(2)
    histos['PU140']['PFPuppiRaw'].SetLineWidth(2)
    histos['PU140']['PFPuppiRaw'].SetLineStyle(2)
    histos['PU140']['PFPuppiRaw'].Draw('ep,same')
  
    histos['PU140']['PFPuppiTypeOne'].SetMarkerStyle(32)
    histos['PU140']['PFPuppiTypeOne'].SetMarkerSize(1)
    histos['PU140']['PFPuppiTypeOne'].SetMarkerColor(4)
    histos['PU140']['PFPuppiTypeOne'].SetLineColor(4)
    histos['PU140']['PFPuppiTypeOne'].SetLineWidth(2)
    histos['PU140']['PFPuppiTypeOne'].SetLineStyle(2)
    histos['PU140']['PFPuppiTypeOne'].Draw('ep,same')
  except: pass

  try:
    histos['PU200']['PFRaw'].SetMarkerStyle(20)
    histos['PU200']['PFRaw'].SetMarkerSize(1)
    histos['PU200']['PFRaw'].SetMarkerColor(1)
    histos['PU200']['PFRaw'].SetLineColor(1)
    histos['PU200']['PFRaw'].SetLineWidth(2)
    histos['PU200']['PFRaw'].Draw('ep,same')
  
    histos['PU200']['PFCHSRaw'].SetMarkerStyle(21)
    histos['PU200']['PFCHSRaw'].SetMarkerSize(1)
    histos['PU200']['PFCHSRaw'].SetMarkerColor(ROOT.kViolet+2)
    histos['PU200']['PFCHSRaw'].SetLineColor(ROOT.kViolet+2)
    histos['PU200']['PFCHSRaw'].SetLineWidth(2)
    histos['PU200']['PFCHSRaw'].Draw('ep,same')
  
    histos['PU200']['PFPuppiRaw'].SetMarkerStyle(22)
    histos['PU200']['PFPuppiRaw'].SetMarkerSize(1)
    histos['PU200']['PFPuppiRaw'].SetMarkerColor(2)
    histos['PU200']['PFPuppiRaw'].SetLineColor(2)
    histos['PU200']['PFPuppiRaw'].SetLineWidth(2)
    histos['PU200']['PFPuppiRaw'].Draw('ep,same')
  
    histos['PU200']['PFPuppiTypeOne'].SetMarkerStyle(23)
    histos['PU200']['PFPuppiTypeOne'].SetMarkerSize(1)
    histos['PU200']['PFPuppiTypeOne'].SetMarkerColor(4)
    histos['PU200']['PFPuppiTypeOne'].SetLineColor(4)
    histos['PU200']['PFPuppiTypeOne'].SetLineWidth(2)
    histos['PU200']['PFPuppiTypeOne'].Draw('ep,same')
  except: pass

  topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
  topLabel.SetFillColor(0)
  topLabel.SetFillStyle(1001)
  topLabel.SetTextColor(ROOT.kBlack)
  topLabel.SetTextAlign(12)
  topLabel.SetTextFont(42)
  topLabel.SetTextSize(0.035)
  topLabel.SetBorderSize(0)
  topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
  topLabel.Draw('same')

  objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
  objLabel.SetFillColor(0)
  objLabel.SetFillStyle(1001)
  objLabel.SetTextColor(ROOT.kBlack)
  objLabel.SetTextAlign(32)
  objLabel.SetTextFont(42)
  objLabel.SetTextSize(0.035)
  objLabel.SetBorderSize(0)
  objLabel.AddText('14 TeV')
  objLabel.Draw('same')

  leg1 = ROOT.TLegend(0.165, 0.72, 0.94, 0.90)
  leg1.SetNColumns(2)
  leg1.SetTextFont(42)
  try:
    leg1.AddEntry(histos['PU200']['PFRaw'], 'PF (Raw)', 'lepx')
    leg1.AddEntry(histos['PU200']['PFCHSRaw'], 'PF+CHS (Raw)', 'lepx')
    leg1.AddEntry(histos['PU200']['PFPuppiRaw'], 'PF+PUPPI (Raw)', 'lepx')
    leg1.AddEntry(histos['PU200']['PFPuppiTypeOne'], 'PF+PUPPI (Type-1)', 'lepx')
  except: pass
  leg1.Draw('same')

  try:
    _htmpPU140 = histos['PU140']['PFRaw'].Clone()
    _htmpPU140.SetLineColor(1)
    _htmpPU140.SetLineStyle(2)
  except: pass

  try:
    _htmpPU200 = histos['PU200']['PFRaw'].Clone()
    _htmpPU200.SetLineColor(1)
    _htmpPU200.SetLineStyle(1)
  except: pass

  leg2 = ROOT.TLegend(0.165, 0.56, 0.38, 0.72)
  leg2.SetNColumns(1)
  leg2.SetTextFont(42)
  try:
    leg2.AddEntry(_htmpPU140, '140 PU', 'l')
    leg2.AddEntry(_htmpPU200, '200 PU', 'l')
  except: pass
  leg2.Draw('same')

  if resType == 'perpToGEN':
    h0.SetTitle(';GEN p_{T}^{miss} [GeV];#sigma_{#perp}  (p^{HLT}_{T,miss}) / #LTp^{HLT}_{T,miss} / p^{GEN}_{T,miss}#GT [GeV]')
  elif resType == 'paraToGENMinusGEN':
    h0.SetTitle(';GEN p_{T}^{miss} [GeV];#sigma_{#parallel}(p^{HLT}_{T,miss}) / #LTp^{HLT}_{T,miss} / p^{GEN}_{T,miss}#GT [GeV]')
  h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

  canvas.SetLogy(0)
  canvas.SetGrid(1, 1)

  for _tmpExt in exts:
    canvas.SaveAs(outputName+'.'+_tmpExt)

  canvas.Close()

  print '\033[1m'+outputName+'\033[0m'

#### main
if __name__ == '__main__':
  ### args ---------------
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument('-i', '--input', dest='inputDir', required=True, action='store', default=None,
                      help='path to input harvesting/ directory')

  parser.add_argument('-o', '--output', dest='output', action='store', default='.',
                      help='path to output directory')

  parser.add_argument('--no-plots', dest='no_plots', action='store_true',
                      help='do not create output plots')

  parser.add_argument('--no-qcd-weighted', dest='no_qcd_weighted', action='store_true',
                      help='input histograms do not include weights for MB+QCD merging')

  parser.add_argument('--minCountsForValidRate', dest='minCountsForValidRate', action='store', type=float, default=-1.0,
                      help='minimum number of counts to consider a sample valid for trigger rate estimates')

  parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png'],
                      help='list of extension(s) for output file(s)')

  parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', const=1, type=int, default=0,
                      help='verbosity level')

  parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                      help='enable dry-run mode')

  opts, opts_unknown = parser.parse_known_args()
  ### --------------------

  log_prx = os.path.basename(__file__)+' -- '

  ROOT.gROOT.SetBatch() # disable interactive graphics
  ROOT.gErrorIgnoreLevel = ROOT.kError # do not display ROOT warnings

#  ROOT.TH1.AddDirectory(False)

  theStyle = get_style(0)
  theStyle.cd()

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir

  recoKeys = [
#    'HLT_TRKv06p1',
    'HLT_TRKv06p1_TICL',
  ]

#      print '-'*110
#      print '\033[1m{:10}\033[0m | \033[1m{:47}\033[0m | \033[1m{:47}\033[0m'.format('Rate [Hz]', '[L1T] '+_tmpL1T, '[L1T+HLT] '+_tmpHLT)
#      print '-'*110

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  for _tmpReco in recoKeys:
    print '='*110
    print '='*110
    print '\033[1m'+_tmpReco+'\033[0m'
    print '='*110
    print '='*110

    plotJetResponse(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140.root',
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetResponse',
      exts = EXTS,
    )

    plotJetResolution(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140.root',
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetResolution',
      exts = EXTS,
    )

    plotJetMatchingEff(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140.root',
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetMatchingEff_L1T',
      keyword = 'L1T',
      exts = EXTS,
    )

    plotJetMatchingEff(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140.root',
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      outputName = outputDir+'/jetMatchingEff_HLT',
      keyword = 'HLT',
      exts = EXTS,
    )

    plotMETResponse(
      fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU140.root',
      fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root',
      outputName = outputDir+'/metResponse',
      exts = EXTS,
    )

    for _tmp in ['perpToGEN', 'paraToGENMinusGEN']:
      plotMETResolution(
        resType = _tmp,
        fpath_PU140 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU140.root',
        fpath_PU200 = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root',
        outputName = outputDir+'/metResolution_'+_tmp,
        exts = EXTS,
      )

    print '='*50
    print '='*50
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*50
    print '='*50

    ## SingleJet
    effysJet = {}
    for _tmpPU in [
      'PU140',
      'PU200',
    ]:
      effysJet[_tmpPU] = {}
      for _tmpJetThresh in ['200', '350', '500']:
        effysJet[_tmpPU][_tmpJetThresh] = getJetEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_'+_tmpPU+'.root',
          hltThreshold_SingleJet = float(_tmpJetThresh),
        )

    for _tmpRef in [
      'GEN',
#      'Offline',
    ]:
      canvas = ROOT.TCanvas(tmpName(), tmpName(False))
      canvas.cd()

      h0 = canvas.DrawFrame(100, 0.0001, 1000, 1.19)

      try:
        effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
        effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
        effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
        effysJet['PU140']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

        effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
        effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
        effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
        effysJet['PU140']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

        effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
        effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
        effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
        effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
      except: pass

      try:
        effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
        effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
        effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
        effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

        effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
        effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
        effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
        effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')

        effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
        effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
        effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
        effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
      except: pass

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText('14 TeV')
      objLabel.Draw('same')

      l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.80, 0.88, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(12)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.035)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('HLT : AK4 PF+PUPPI Jets (|#eta|<5.0)')
      l1tRateLabel.Draw('same')

      leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.44)
      leg1.SetNColumns(1)
      leg1.SetTextFont(42)
      leg1.SetEntrySeparation(0.4) 
      try:
        leg1.AddEntry(effysJet['PU200']['200']['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'p_{T}^{HLT}>200 GeV ', 'lepx')
        leg1.AddEntry(effysJet['PU200']['350']['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'p_{T}^{HLT}>350 GeV ', 'lepx')
        leg1.AddEntry(effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'p_{T}^{HLT}>500 GeV ', 'lepx')
      except: pass
      leg1.Draw('same')

      try:
        _htmpPU140 = effysJet['PU140']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Clone()
        _htmpPU140.SetLineColor(1)
        _htmpPU140.SetLineStyle(2)
      except: pass

      try:
        _htmpPU200 = effysJet['PU200']['500']['SingleJet_L1TpHLT_wrt_'+_tmpRef].Clone()
        _htmpPU200.SetLineColor(1)
        _htmpPU200.SetLineStyle(1)
      except: pass

      leg2 = ROOT.TLegend(0.70, 0.46, 0.94, 0.61)
      leg2.SetNColumns(1)
      leg2.SetTextFont(42)
      try:
        leg2.AddEntry(_htmpPU140, '140 PU', 'l')
      except: pass
      try:
        leg2.AddEntry(_htmpPU200, '200 PU', 'l')
      except: pass
      leg2.Draw('same')

      h0.SetTitle(';'+_tmpRef+' Jet p_{T} [GeV];L1T+HLT Efficiency')
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

      canvas.SetLogy(0)
      canvas.SetGrid(1, 1)

      for _tmpExt in EXTS:
        canvas.SaveAs(outputDir+'/triggerEff_SingleJet_wrt'+_tmpRef+'.'+_tmpExt)

      canvas.Close()

      print '\033[1m'+outputDir+'/triggerEff_SingleJet_wrt'+_tmpRef+'\033[0m'

    ## HT
    effysHT = {}
    for _tmpPU in ['PU140', 'PU200']:
      effysHT[_tmpPU] = {}
      for _tmpHTThresh in ['900', '1100', '1300']:
        effysHT[_tmpPU][_tmpHTThresh] = getHTEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_'+_tmpPU+'.root',
          hltThreshold_HT = float(_tmpHTThresh),
        )

    for _tmpRef in [
      'GEN',
#      'Offline',
    ]:
      canvas = ROOT.TCanvas(tmpName(), tmpName(False))
      canvas.cd()

      h0 = canvas.DrawFrame(600, 0.0001, 2000, 1.19)

      try:
        effysHT['PU140']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysHT['PU140']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysHT['PU140']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
        effysHT['PU140']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
        effysHT['PU140']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
        effysHT['PU140']['900']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
  
        effysHT['PU140']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysHT['PU140']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysHT['PU140']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
        effysHT['PU140']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
        effysHT['PU140']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
        effysHT['PU140']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
  
        effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
        effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
        effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(2)
        effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
      except: pass

      try:  
        effysHT['PU200']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysHT['PU200']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysHT['PU200']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(1)
        effysHT['PU200']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(1)
        effysHT['PU200']['900']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
        effysHT['PU200']['900']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
  
        effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(2)
        effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(2)
        effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
        effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
  
        effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
        effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
        effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
        effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
        effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
        effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
      except: pass

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText('14 TeV')
      objLabel.Draw('same')

      l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.84, 0.88, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(12)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.035)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('HLT : AK4 PF+PUPPI Jets (p_{T} > 30 GeV, |#eta| < 2.4)')
      l1tRateLabel.Draw('same')

      leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.44)
      leg1.SetNColumns(1)
      leg1.SetTextFont(42)
      leg1.SetEntrySeparation(0.4)
      try:
        leg1.AddEntry(effysHT['PU200'][ '900']['HT_L1TpHLT_wrt_'+_tmpRef], 'H_{T}^{HLT}>0.9 TeV', 'lepx')
        leg1.AddEntry(effysHT['PU200']['1100']['HT_L1TpHLT_wrt_'+_tmpRef], 'H_{T}^{HLT}>1.1 TeV', 'lepx')
        leg1.AddEntry(effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef], 'H_{T}^{HLT}>1.3 TeV', 'lepx')
      except: pass
      leg1.Draw('same')

      leg2 = ROOT.TLegend(0.70, 0.46, 0.94, 0.61)
      leg2.SetNColumns(1)
      leg2.SetTextFont(42)
      try:
        _htmpPU140 = effysHT['PU140']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].Clone()
        _htmpPU140.SetLineColor(1)
        _htmpPU140.SetLineStyle(2)
        leg2.AddEntry(_htmpPU140, '140 PU', 'l')
      except: pass
      try:
        _htmpPU200 = effysHT['PU200']['1300']['HT_L1TpHLT_wrt_'+_tmpRef].Clone()
        _htmpPU200.SetLineColor(1)
        _htmpPU200.SetLineStyle(1)
        leg2.AddEntry(_htmpPU200, '200 PU', 'l')
      except: pass
      leg2.Draw('same')

      h0.SetTitle(';'+_tmpRef+' H_{T} [GeV];L1T+HLT Efficiency')
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

      canvas.SetLogy(0)
      canvas.SetGrid(1, 1)

      for _tmpExt in EXTS:
        canvas.SaveAs(outputDir+'/triggerEff_HT_wrt'+_tmpRef+'.'+_tmpExt)

      canvas.Close()

      print '\033[1m'+outputDir+'/triggerEff_HT_wrt'+_tmpRef+'\033[0m'

    ## MET
    effysMET_vbfh = {}
    for _tmpPU in [
      'PU140',
      'PU200',
    ]:
      effysMET_vbfh[_tmpPU] = {}
      for _tmpMETThresh in [
        '120',
        '130',
        '140',
        '150',
        '160',
      ]:
        effysMET_vbfh[_tmpPU][_tmpMETThresh] = getMETEfficiencies(**{
          'fpath': inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_'+_tmpPU+'.root',
          'hltThreshold_MET': float(_tmpMETThresh),
          'hltThreshold_METTypeOne': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT20': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT30': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT40': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT50': float(_tmpMETThresh),
        })
    # 2018
    _fpath_MET2018 = '/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/Upgrade/JetMET_PhaseII/JMETriggerAnalysis_phase2/ntuples/output_mc2018_forHLTTDR/RunIIAutumn18MiniAOD_VBF_HToInvisible_13TeV.root'
    _tfile_MET2018 = ROOT.TFile.Open(_fpath_MET2018)
    if not _tfile_MET2018:
      WARNING('failed to open target TFile: '+_fpath_MET2018)
    else:
      binEdges_MET = array.array('d', [_tmp*10 for _tmp in range(13)] + [140, 160, 180, 200, 220, 240, 280, 320, 360, 430, 500, 600, 700, 800])
      _ttree_MET2018 = _tfile_MET2018.Get('JMETriggerNTuple/Events')

      _tmp_denname = tmpName()
      _tmp_den = ROOT.TH1D(_tmp_denname, _tmp_denname, len(binEdges_MET)-1, binEdges_MET)
      _tmp_den.Sumw2()
      _ttree_MET2018.Draw('genMETTrue_pt>>'+_tmp_denname, '', 'goff')

      _tmp_num1name = tmpName()
      _tmp_num1 = ROOT.TH1D(_tmp_num1name, _tmp_num1name, len(binEdges_MET)-1, binEdges_MET)
      _tmp_num1.Sumw2()
      _ttree_MET2018.Draw('genMETTrue_pt>>'+_tmp_num1name, 'Flag_HLT_PFMET120_PFMHT120_IDTight_L1TSeedAccept == 1', 'goff')

      _tmp_num2name = tmpName()
      _tmp_num2 = ROOT.TH1D(_tmp_num2name, _tmp_num2name, len(binEdges_MET)-1, binEdges_MET)
      _tmp_num2.Sumw2()
      _ttree_MET2018.Draw('genMETTrue_pt>>'+_tmp_num2name, 'HLT_PFMET120_PFMHT120_IDTight == 1', 'goff')

      effysMET_2018 = {'120': {}}
      effysMET_2018['120']['METMHT_L1T_wrt_GEN'] = get_efficiency_graph(_tmp_num1, _tmp_den)
      effysMET_2018['120']['METMHT_L1T_wrt_GEN'].SetName('METMHT_L1T_wrt_GEN')
      effysMET_2018['120']['METMHT_L1TpHLT_wrt_GEN'] = get_efficiency_graph(_tmp_num2, _tmp_den)
      effysMET_2018['120']['METMHT_L1TpHLT_wrt_GEN'].SetName('METMHT_L1TpHLT_wrt_GEN')

    _tfile_MET2018.Close()

    effysMET_ttbar = {}
    for _tmpPU in [
      'NoPU',
      'PU140',
      'PU200',
    ]:
      effysMET_ttbar[_tmpPU] = {}
      for _tmpMETThresh in [
        '120',
        '130',
        '140',
        '150',
        '160',
      ]:
        effysMET_ttbar[_tmpPU][_tmpMETThresh] = getMETEfficiencies(**{
          'fpath': inputDir+'/'+_tmpReco+'/Phase2HLTTDR_TTTo2L2Nu_14TeV_'+_tmpPU+'.root',
          'hltThreshold_MET': float(_tmpMETThresh),
          'hltThreshold_METTypeOne': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT20': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT30': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT40': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT50': float(_tmpMETThresh),
        })

    for _tmpRef in [
      'GEN',
#      'Offline',
    ]:
      for (_tmpMC, effysMET) in [('VBFHToInv', effysMET_vbfh), ('TTbar', effysMET_ttbar)]:

        # MET (Raw)
        canvas = ROOT.TCanvas(tmpName(), tmpName(False))
        canvas.cd()
  
        h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)
  
        try:
          effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef].SetMarkerSize(1)
          effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef].SetLineWidth(2)
          effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef].SetMarkerColor(1)
          effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef].SetLineColor(1)
          effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef].SetLineStyle(1)
          effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef].Draw('lepz')
    
          effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef].SetLineWidth(2)
          effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef].SetMarkerColor(2)
          effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef].SetLineColor(2)
          effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef].SetLineStyle(1)
          effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef].Draw('lepz')
    
          effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
          effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
          effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
          effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
          effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
        except: pass
  
        topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
        topLabel.SetFillColor(0)
        topLabel.SetFillStyle(1001)
        topLabel.SetTextColor(ROOT.kBlack)
        topLabel.SetTextAlign(12)
        topLabel.SetTextFont(42)
        topLabel.SetTextSize(0.035)
        topLabel.SetBorderSize(0)
        topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
        topLabel.Draw('same')
  
        objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
        objLabel.SetFillColor(0)
        objLabel.SetFillStyle(1001)
        objLabel.SetTextColor(ROOT.kBlack)
        objLabel.SetTextAlign(32)
        objLabel.SetTextFont(42)
        objLabel.SetTextSize(0.035)
        objLabel.SetBorderSize(0)
        objLabel.AddText('200 PU (14 TeV)')
        objLabel.Draw('same')
  
        l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
        l1tRateLabel.SetFillColor(0)
        l1tRateLabel.SetFillStyle(1001)
        l1tRateLabel.SetTextColor(ROOT.kBlack)
        l1tRateLabel.SetTextAlign(12)
        l1tRateLabel.SetTextFont(42)
        l1tRateLabel.SetTextSize(0.035)
        l1tRateLabel.SetBorderSize(0)
        l1tRateLabel.AddText('HLT : PF+PUPPI p_{T}^{miss} > 120 GeV')
        l1tRateLabel.Draw('same')
  
        leg1 = ROOT.TLegend(0.65, 0.20, 0.94, 0.44)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        try:
          leg1.AddEntry(effysMET['PU200']['120']['MET_L1T_wrt_'+_tmpRef], 'L1T', 'lepx')
          leg1.AddEntry(effysMET['PU200']['120']['MET_HLT_wrt_'+_tmpRef], 'HLT', 'lepx')
          leg1.AddEntry(effysMET['PU200']['120']['MET_L1TpHLT_wrt_'+_tmpRef], 'L1T+HLT', 'lepx')
        except: pass
        leg1.Draw('same')
  
        h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
  
        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)
  
        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_METRaw_wrt'+_tmpRef+'_'+_tmpMC+'.'+_tmpExt)
  
        canvas.Close()
  
        print '\033[1m'+outputDir+'/triggerEff_METRaw_wrt'+_tmpRef+'_'+_tmpMC+'\033[0m'
  
        # METTypeOne (+MHT)
        for _tmpPU in [
          'PU140',
          'PU200',
        ]:
          for _tmpMET in [
            'METTypeOne',
            'METTypeOneMHT20',
            'METTypeOneMHT30',
            'METTypeOneMHT40',
            'METTypeOneMHT50',
          ]:
            for _tmpHLTthr in [
              '120',
              '130',
              '140',
              '150',
              '160',
            ]:
              canvas = ROOT.TCanvas(tmpName(), tmpName(False))
              canvas.cd()
  
              h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)
  
              try:
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef].SetMarkerColor(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef].SetLineColor(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef].Draw('lepz')
    
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef].SetMarkerColor(2)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef].SetLineColor(2)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef].Draw('lepz')
    
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(4)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef].SetLineColor(4)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
              except: pass
  
              topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
              topLabel.SetFillColor(0)
              topLabel.SetFillStyle(1001)
              topLabel.SetTextColor(ROOT.kBlack)
              topLabel.SetTextAlign(12)
              topLabel.SetTextFont(42)
              topLabel.SetTextSize(0.035)
              topLabel.SetBorderSize(0)
              topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
              topLabel.Draw('same')
  
              objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
              objLabel.SetFillColor(0)
              objLabel.SetFillStyle(1001)
              objLabel.SetTextColor(ROOT.kBlack)
              objLabel.SetTextAlign(32)
              objLabel.SetTextFont(42)
              objLabel.SetTextSize(0.035)
              objLabel.SetBorderSize(0)
              objLabel.AddText(_tmpPU[2:]+' PU (14 TeV)')
              objLabel.Draw('same')
  
              if 'MHT' in _tmpMET:
                l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.92, 0.88, 'NDC')
                l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss} & MHT > '+_tmpHLTthr+' GeV')
              else:
                l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
                l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss} > '+_tmpHLTthr+' GeV')
              l1tRateLabel.SetFillColor(0)
              l1tRateLabel.SetFillStyle(1001)
              l1tRateLabel.SetTextColor(ROOT.kBlack)
              l1tRateLabel.SetTextAlign(12)
              l1tRateLabel.SetTextFont(42)
              l1tRateLabel.SetTextSize(0.035)
              l1tRateLabel.SetBorderSize(0)
              l1tRateLabel.Draw('same')

              leg1 = ROOT.TLegend(0.65, 0.20, 0.94, 0.44)
              leg1.SetNColumns(1)
              leg1.SetTextFont(42)
              try:
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1T_wrt_'+_tmpRef], 'L1T', 'lepx')
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_HLT_wrt_'+_tmpRef], 'HLT', 'lepx')
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr][_tmpMET+'_L1TpHLT_wrt_'+_tmpRef], 'L1T+HLT', 'lepx')
              except: pass
              leg1.Draw('same')

              h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
              h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

              canvas.SetLogy(0)
              canvas.SetGrid(1, 1)

              for _tmpExt in EXTS:
                canvas.SaveAs(outputDir+'/triggerEff_'+_tmpMET+'_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpHLTthr+'_'+_tmpMC+'.'+_tmpExt)

              canvas.Close()

              print '\033[1m'+outputDir+'/triggerEff_'+_tmpMET+'_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpHLTthr+'_'+_tmpMC+'\033[0m'

        # MET (TypeOne vs TypeOne+MHT)
        for _tmpPU in [
          'PU140',
          'PU200',
        ]:
          for _tmpEff in [
            'HLT',
            'L1TpHLT',
          ]:
            for _tmpHLTthr in [
              '120',
              '130',
              '140',
              '150',
              '160',
            ]:
              canvas = ROOT.TCanvas(tmpName(), tmpName(False))
              canvas.cd()

              h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)

              try:
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlack)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlack)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')

                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kRed)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kRed)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')

                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlue)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlue)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')

                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kOrange)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kOrange)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')

                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kViolet)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kViolet)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
                effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
              except: pass

              topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
              topLabel.SetFillColor(0)
              topLabel.SetFillStyle(1001)
              topLabel.SetTextColor(ROOT.kBlack)
              topLabel.SetTextAlign(12)
              topLabel.SetTextFont(42)
              topLabel.SetTextSize(0.035)
              topLabel.SetBorderSize(0)
              topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
              topLabel.Draw('same')

              objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
              objLabel.SetFillColor(0)
              objLabel.SetFillStyle(1001)
              objLabel.SetTextColor(ROOT.kBlack)
              objLabel.SetTextAlign(32)
              objLabel.SetTextFont(42)
              objLabel.SetTextSize(0.035)
              objLabel.SetBorderSize(0)
              objLabel.AddText(_tmpPU[2:]+' PU (14 TeV)')
              objLabel.Draw('same')

              l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
              l1tRateLabel.SetFillColor(0)
              l1tRateLabel.SetFillStyle(1001)
              l1tRateLabel.SetTextColor(ROOT.kBlack)
              l1tRateLabel.SetTextAlign(12)
              l1tRateLabel.SetTextFont(42)
              l1tRateLabel.SetTextSize(0.035)
              l1tRateLabel.SetBorderSize(0)
              l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss} (+MHT)')
              l1tRateLabel.Draw('same')

              hltRateLabel = ROOT.TPaveText(0.165, 0.76, 0.65, 0.82, 'NDC')
              hltRateLabel.SetFillColor(0)
              hltRateLabel.SetFillStyle(1001)
              hltRateLabel.SetTextColor(ROOT.kBlack)
              hltRateLabel.SetTextAlign(12)
              hltRateLabel.SetTextFont(42)
              hltRateLabel.SetTextSize(0.035)
              hltRateLabel.SetBorderSize(0)
              hltRateLabel.AddText('HLT p_{T}^{miss} / MHT Threshold = '+_tmpHLTthr+' GeV')
#              hltRateLabel.Draw('same')

              leg1 = ROOT.TLegend(0.65, 0.20, 0.94, 0.64)
              leg1.SetNColumns(1)
              leg1.SetTextFont(42)
              try:
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr]['METTypeOne_'+_tmpEff+'_wrt_'+_tmpRef], 'Type-1', 'lepx')
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT20_'+_tmpEff+'_wrt_'+_tmpRef], 'Type-1 + MHT_{20}', 'lepx')
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT30_'+_tmpEff+'_wrt_'+_tmpRef], 'Type-1 + MHT_{30}', 'lepx')
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT40_'+_tmpEff+'_wrt_'+_tmpRef], 'Type-1 + MHT_{40}', 'lepx')
                leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr]['METTypeOneMHT50_'+_tmpEff+'_wrt_'+_tmpRef], 'Type-1 + MHT_{50}', 'lepx')
              except: pass
              leg1.Draw('same')
  
              _tmpYaxis = 'Efficiency'
              if _tmpEff == 'L1TpHLT': _tmpYaxis = 'L1T+HLT Efficiency'
              elif _tmpEff == 'HLT': _tmpYaxis = 'HLT Efficiency'
  
              h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];'+_tmpYaxis)
              h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
  
              canvas.SetLogy(0)
              canvas.SetGrid(1, 1)
  
              for _tmpExt in EXTS:
                canvas.SaveAs(outputDir+'/triggerEff_METTypeOneX_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpEff+'_'+_tmpHLTthr+'_'+_tmpMC+'.'+_tmpExt)
  
              canvas.Close()
  
              print '\033[1m'+outputDir+'/triggerEff_METTypeOneX_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpEff+'_'+_tmpHLTthr+'_'+_tmpMC+'\033[0m'
  
        # MET (TypeOne vs TypeOne+MHT vs 2018)
        for _tmpPU in [
          'PU140',
          'PU200',
        ]:
          canvas = ROOT.TCanvas(tmpName(), tmpName(False))
          canvas.cd()
  
          h0 = canvas.DrawFrame(0, 0.000, 800, 1.19)
  
          _thrMETTypeOne = '160'
          _thrMETTypeOneMHT = '140'
  
          effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef].SetMarkerSize(0)
          effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef].SetLineWidth(2)
          effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlack)
          effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef].SetLineColor(ROOT.kBlack)
          effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef].SetLineStyle(2)
          effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef].Draw('lepz')
  
          effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(0)
          effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
          effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlack)
          effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef].SetLineColor(ROOT.kBlack)
          effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
          effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
  
          try:
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef].SetMarkerSize(0)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef].SetMarkerColor(ROOT.kGreen+2)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef].SetLineColor(ROOT.kGreen+2)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef].SetLineStyle(2)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef].Draw('lepz')
    
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(0)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(ROOT.kRed)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef].SetLineColor(ROOT.kRed)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
    
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef].SetMarkerSize(0)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlue)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef].SetLineColor(ROOT.kBlue)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef].Draw('lepz')
    
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef].SetMarkerSize(0)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef].SetMarkerColor(ROOT.kViolet)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef].SetLineColor(ROOT.kViolet)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef].SetLineStyle(4)
            effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef].Draw('lepz')
          except: pass
  
          topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
          topLabel.SetFillColor(0)
          topLabel.SetFillStyle(1001)
          topLabel.SetTextColor(ROOT.kBlack)
          topLabel.SetTextAlign(12)
          topLabel.SetTextFont(42)
          topLabel.SetTextSize(0.035)
          topLabel.SetBorderSize(0)
          topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
          topLabel.Draw('same')
  
          objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
          objLabel.SetFillColor(0)
          objLabel.SetFillStyle(1001)
          objLabel.SetTextColor(ROOT.kBlack)
          objLabel.SetTextAlign(32)
          objLabel.SetTextFont(42)
          objLabel.SetTextSize(0.035)
          objLabel.SetBorderSize(0)
          objLabel.AddText(_tmpPU[2:]+' PU (14 TeV)')
          objLabel.Draw('same')
  
          l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
          l1tRateLabel.SetFillColor(0)
          l1tRateLabel.SetFillStyle(1001)
          l1tRateLabel.SetTextColor(ROOT.kBlack)
          l1tRateLabel.SetTextAlign(12)
          l1tRateLabel.SetTextFont(42)
          l1tRateLabel.SetTextSize(0.035)
          l1tRateLabel.SetBorderSize(0)
          l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss} (+MHT)')
          l1tRateLabel.Draw('same')
  
          leg1 = ROOT.TLegend(0.48, 0.20, 0.94, 0.45)
          leg1.SetNColumns(1)
          leg1.SetTextFont(42)
          leg1.AddEntry(effysMET_2018['120']['METMHT_L1T_wrt_'+_tmpRef], '[L1T] Run-2 (2018)', 'lepx')
          leg1.AddEntry(effysMET_2018['120']['METMHT_L1TpHLT_wrt_'+_tmpRef], '[L1T+HLT] Run-2 (2018), MET120 + MHT120', 'lepx')
          try:
            leg1.AddEntry(effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1T_wrt_'+_tmpRef], '[L1T] Phase-2, L1T MET118', 'lepx')
            leg1.AddEntry(effysMET[_tmpPU][_thrMETTypeOne]['METTypeOne_L1TpHLT_wrt_'+_tmpRef], '[L1T+HLT] Phase-2, Type-1 MET'+_thrMETTypeOne, 'lepx')
            leg1.AddEntry(effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_L1TpHLT_wrt_'+_tmpRef], '[L1T+HLT] Phase-2, Type-1 MET'+_thrMETTypeOneMHT+' + MHT'+_thrMETTypeOneMHT, 'lepx')
            leg1.AddEntry(effysMET[_tmpPU][_thrMETTypeOneMHT]['METTypeOneMHT30_HLT_wrt_'+_tmpRef], '[HLT] Phase-2, Type-1 MET'+_thrMETTypeOneMHT+' + MHT'+_thrMETTypeOneMHT, 'lepx')
          except: pass
          leg1.Draw('same')
  
          h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
  
          canvas.SetLogy(0)
          canvas.SetGrid(1, 1)

          for _tmpExt in EXTS:
            canvas.SaveAs(outputDir+'/triggerEff_METTypeOneXvs2018_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpMC+'.'+_tmpExt)

          canvas.Close()

          print '\033[1m'+outputDir+'/triggerEff_METTypeOneXvs2018_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpMC+'\033[0m'

      # MET (VBF-HiggsToInv vs TTbar)
      for _tmpEff in [
        'HLT',
        'L1TpHLT',
      ]:
        for _tmpHLTthr in [
          '120',
          '130',
          '140',
          '150',
          '160',
        ]:
          for _tmpMETType in [
            'METTypeOne',
            'METTypeOneMHT20',
            'METTypeOneMHT30',
            'METTypeOneMHT40',
            'METTypeOneMHT50',
          ]:
            canvas = ROOT.TCanvas(tmpName(), tmpName(False))
            canvas.cd()

            h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)

            try:
              effysMET['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
              effysMET['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
              effysMET['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlack)
              effysMET['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlack)
              effysMET['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(2)
              effysMET['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
            except: pass

            try:
              effysMET['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
              effysMET['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
              effysMET['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kRed)
              effysMET['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kRed)
              effysMET['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(2)
              effysMET['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
            except: pass

            try:
              effysMET['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
              effysMET['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
              effysMET['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlue)
              effysMET['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlue)
              effysMET['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(2)
              effysMET['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
            except: pass

            try:
              effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
              effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
              effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlack)
              effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlack)
              effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
              effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
            except: pass

            try:
              effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
              effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
              effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kRed)
              effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kRed)
              effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
              effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
            except: pass

            try:
              effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerSize(1)
              effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineWidth(2)
              effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlue)
              effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlue)
              effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].SetLineStyle(1)
              effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Draw('lepz')
            except: pass

            topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
            topLabel.SetFillColor(0)
            topLabel.SetFillStyle(1001)
            topLabel.SetTextColor(ROOT.kBlack)
            topLabel.SetTextAlign(12)
            topLabel.SetTextFont(42)
            topLabel.SetTextSize(0.035)
            topLabel.SetBorderSize(0)
            topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
            topLabel.Draw('same')

            objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
            objLabel.SetFillColor(0)
            objLabel.SetFillStyle(1001)
            objLabel.SetTextColor(ROOT.kBlack)
            objLabel.SetTextAlign(32)
            objLabel.SetTextFont(42)
            objLabel.SetTextSize(0.035)
            objLabel.SetBorderSize(0)
            objLabel.AddText('14 TeV')
            objLabel.Draw('same')

            l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
            l1tRateLabel.SetFillColor(0)
            l1tRateLabel.SetFillStyle(1001)
            l1tRateLabel.SetTextColor(ROOT.kBlack)
            l1tRateLabel.SetTextAlign(12)
            l1tRateLabel.SetTextFont(42)
            l1tRateLabel.SetTextSize(0.035)
            l1tRateLabel.SetBorderSize(0)
            l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss}'+' MHT'*('MHT' in _tmpMETType))
            l1tRateLabel.Draw('same')

            hltRateLabel = ROOT.TPaveText(0.165, 0.76, 0.65, 0.82, 'NDC')
            hltRateLabel.SetFillColor(0)
            hltRateLabel.SetFillStyle(1001)
            hltRateLabel.SetTextColor(ROOT.kBlack)
            hltRateLabel.SetTextAlign(12)
            hltRateLabel.SetTextFont(42)
            hltRateLabel.SetTextSize(0.035)
            hltRateLabel.SetBorderSize(0)
            hltRateLabel.AddText('HLT p_{T}^{miss} / MHT Threshold = '+_tmpHLTthr+' GeV')
#            hltRateLabel.Draw('same')

            try:
              leg1 = ROOT.TLegend(0.65, 0.60, 0.94, 0.81)
              leg1.SetNColumns(1)
              leg1.SetTextFont(42)
              leg1.AddEntry(effysMET_ttbar['NoPU'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef], 'No PU', 'lepx')
              leg1.AddEntry(effysMET_ttbar['PU140'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef], '140 PU', 'lepx')
              leg1.AddEntry(effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef], '200 PU', 'lepx')
              leg1.Draw('same')
            except: pass

            try:
              _htmp1 = effysMET_ttbar['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Clone()
              _htmp1.SetLineColor(1)
              _htmp1.SetLineStyle(1)
            except: pass

            try:
              _htmp2 = effysMET_vbfh['PU200'][_tmpHLTthr][_tmpMETType+'_'+_tmpEff+'_wrt_'+_tmpRef].Clone()
              _htmp2.SetLineColor(1)
              _htmp2.SetLineStyle(2)
            except: pass

            leg2 = ROOT.TLegend(0.75, 0.45, 0.94, 0.60)
            leg2.SetNColumns(1)
            leg2.SetTextFont(42)
            try: leg2.AddEntry(_htmp1, 't#bar{t}', 'l')
            except: pass
            try: leg2.AddEntry(_htmp2, 'VBF Higgs #rightarrow #nu#nu', 'l')
            except: pass
            leg2.Draw('same')

            _tmpYaxis = 'Efficiency'
            if _tmpEff == 'L1TpHLT': _tmpYaxis = 'L1T+HLT Efficiency'
            elif _tmpEff == 'HLT': _tmpYaxis = 'HLT Efficiency'

            h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];'+_tmpYaxis)
            h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

            canvas.SetLogy(0)
            canvas.SetGrid(1, 1)

            for _tmpExt in EXTS:
              canvas.SaveAs(outputDir+'/triggerEff_TTbarVsVBFHToInv_'+_tmpMETType+'_wrt'+_tmpRef+'_'+_tmpEff+'_'+_tmpHLTthr+'.'+_tmpExt)

            canvas.Close()

            print '\033[1m'+outputDir+'/triggerEff_TTbarVsVBFHToInv_'+_tmpMETType+'_wrt'+_tmpRef+'_'+_tmpEff+'_'+_tmpHLTthr+'\033[0m'

  ###
  ### Rates
  ###
  rateFiles = {

    'MinBias_14TeV': [
      'MinBias_14TeV_{:}',
    ],

    'QCD_Pt020to030_14TeV': ['QCD_Pt020to030_14TeV_{:}'],
    'QCD_Pt030to050_14TeV': ['QCD_Pt030to050_14TeV_{:}', 'QCD_Pt030to050_14TeV_{:}_ext1'],
    'QCD_Pt050to080_14TeV': ['QCD_Pt050to080_14TeV_{:}', 'QCD_Pt050to080_14TeV_{:}_ext1'],
    'QCD_Pt080to120_14TeV': ['QCD_Pt080to120_14TeV_{:}'],
    'QCD_Pt120to170_14TeV': ['QCD_Pt120to170_14TeV_{:}'],
    'QCD_Pt170to300_14TeV': ['QCD_Pt170to300_14TeV_{:}'],
    'QCD_Pt300to470_14TeV': ['QCD_Pt300to470_14TeV_{:}'],
    'QCD_Pt470to600_14TeV': ['QCD_Pt470to600_14TeV_{:}'],
    'QCD_Pt600toInf_14TeV': ['QCD_Pt600toInf_14TeV_{:}'],

    'WJetsToLNu_14TeV': [
      'WJetsToLNu_14TeV_{:}',
    ],

    'DYJetsToLL_M010to050_14TeV': [
      'DYJetsToLL_M010to050_14TeV_{:}',
    ],

    'DYJetsToLL_M050toInf_14TeV': [
      'DYJetsToLL_M050toInf_14TeV_{:}',
    ],
  }

  rateGroup = {

    'MB+QCD+V': [
      'MinBias_14TeV',
      'QCD_Pt020to030_14TeV',
      'QCD_Pt030to050_14TeV',
      'QCD_Pt050to080_14TeV',
      'QCD_Pt080to120_14TeV',
      'QCD_Pt120to170_14TeV',
      'QCD_Pt170to300_14TeV',
      'QCD_Pt300to470_14TeV',
      'QCD_Pt470to600_14TeV',
      'QCD_Pt600toInf_14TeV',
      'WJetsToLNu_14TeV',
      'DYJetsToLL_M010to050_14TeV',
      'DYJetsToLL_M050toInf_14TeV',
    ],

    'MB': [
      'MinBias_14TeV',
    ],

    'QCD': [
      'QCD_Pt020to030_14TeV',
      'QCD_Pt030to050_14TeV',
      'QCD_Pt050to080_14TeV',
      'QCD_Pt080to120_14TeV',
      'QCD_Pt120to170_14TeV',
      'QCD_Pt170to300_14TeV',
      'QCD_Pt300to470_14TeV',
      'QCD_Pt470to600_14TeV',
      'QCD_Pt600toInf_14TeV',
    ],

    'QCD_020': ['QCD_Pt020to030_14TeV'],
    'QCD_030': ['QCD_Pt030to050_14TeV'],
    'QCD_050': ['QCD_Pt050to080_14TeV'],
    'QCD_080': ['QCD_Pt080to120_14TeV'],
    'QCD_120': ['QCD_Pt120to170_14TeV'],
    'QCD_170': ['QCD_Pt170to300_14TeV'],
    'QCD_300': ['QCD_Pt300to470_14TeV'],
    'QCD_470': ['QCD_Pt470to600_14TeV'],
    'QCD_600': ['QCD_Pt600toInf_14TeV'],

    'Wln': [
      'WJetsToLNu_14TeV',
    ],

    'Zll': [
      'DYJetsToLL_M010to050_14TeV',
      'DYJetsToLL_M050toInf_14TeV',
    ],
  }

  rateSamples = []
  for _tmp in rateGroup:
    rateSamples += rateGroup[_tmp]
  rateSamples = sorted(list(set(rateSamples)))

  rates = {}
  rateHistos = {}
  rateDict = {}
  countDict = {}

  rateConfig = {
    'PU140': {
      'iLumiHzPerPb': 0.053,
      'hltThresholdSingleJet': 520,
      'hltThresholdHT': 1070,
      'hltThresholdMET': 110,
      'hltThresholdMETTypeOne': 140,
      'hltThresholdMETTypeOneMHT20': 140,
      'hltThresholdMETTypeOneMHT30': 140,
      'hltThresholdMETTypeOneMHT40': 140,
      'hltThresholdMETTypeOneMHT50': 140,
    },
    'PU200': {
      'iLumiHzPerPb': 0.075,
      'hltThresholdSingleJet': 520,
      'hltThresholdHT': 1070,
      'hltThresholdMET': 115,
      'hltThresholdMETTypeOne': 160,
      'hltThresholdMETTypeOneMHT20': 140,
      'hltThresholdMETTypeOneMHT30': 140,
      'hltThresholdMETTypeOneMHT40': 140,
      'hltThresholdMETTypeOneMHT50': 140,
    }
  }

  for _tmpReco in recoKeys:
    rates[_tmpReco] = {}
    rateDict[_tmpReco] = {}
    countDict[_tmpReco] = {}
    rateHistos[_tmpReco] = {}

    for _puTag in [
      'PU140',
      'PU200',
    ]:
      print '='*110
      print '='*110
      print '\033[1m'+'Rates ['+_puTag+']'+'\033[0m'
      print '='*110
      print '='*110

      rates[_tmpReco][_puTag] = {}
      for _tmp in rateSamples:
        rates[_tmpReco][_puTag][_tmp] = getRates(**{
          'fpaths': [inputDir+'/'+_tmpReco+'/Phase2HLTTDR_'+_tmp2.format(_puTag)+'.root' for _tmp2 in rateFiles[_tmp]],
          'instLumiHzPerPb': rateConfig[_puTag]['iLumiHzPerPb'],
          'qcd_weighted': not opts.no_qcd_weighted,
          'processName': _tmp,
          'hltThreshold_SingleJet': rateConfig[_puTag]['hltThresholdSingleJet'],
          'hltThreshold_HT': rateConfig[_puTag]['hltThresholdHT'],
          'hltThreshold_MET': rateConfig[_puTag]['hltThresholdMET'],
          'hltThreshold_METTypeOne': rateConfig[_puTag]['hltThresholdMETTypeOne'],
          'hltThreshold_METTypeOneMHT20': rateConfig[_puTag]['hltThresholdMETTypeOneMHT20'],
          'hltThreshold_METTypeOneMHT30': rateConfig[_puTag]['hltThresholdMETTypeOneMHT30'],
          'hltThreshold_METTypeOneMHT40': rateConfig[_puTag]['hltThresholdMETTypeOneMHT40'],
          'hltThreshold_METTypeOneMHT50': rateConfig[_puTag]['hltThresholdMETTypeOneMHT50'],
        })

      rateDict[_tmpReco][_puTag] = {}
      countDict[_tmpReco][_puTag] = {}
      for _tmpTrg in [
        'L1T_SinglePFPuppiJet230off2',
        'L1T_PFPuppiHT450off',
        'L1T_PFPuppiMET220off2',
        'HLT_AK4PFPuppiJet'+str(rateConfig[_puTag]['hltThresholdSingleJet']),
        'HLT_PFPuppiHT'+str(rateConfig[_puTag]['hltThresholdHT']),
        'HLT_PFPuppiMET'+str(rateConfig[_puTag]['hltThresholdMET']),
        'HLT_PFPuppiMETTypeOne'+str(rateConfig[_puTag]['hltThresholdMETTypeOne']),
        'HLT_PFPuppiMETTypeOneMHT20_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT20']),
        'HLT_PFPuppiMETTypeOneMHT30_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT30']),
        'HLT_PFPuppiMETTypeOneMHT40_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT40']),
        'HLT_PFPuppiMETTypeOneMHT50_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT50']),
      ]:
        rateDict[_tmpReco][_puTag][_tmpTrg] = {}
        countDict[_tmpReco][_puTag][_tmpTrg] = {}
        for _tmp1 in rateGroup:
          theRate, theRateErr2 = 0., 0.
          theCount, theCountErr2 = 0., 0.
          for _tmp2 in rateGroup[_tmp1]:
            if _tmpTrg in rates[_tmpReco][_puTag][_tmp2]['v_rates']:
              theRate += rates[_tmpReco][_puTag][_tmp2]['v_rates'][_tmpTrg][0]
              theRateErr2 += math.pow(rates[_tmpReco][_puTag][_tmp2]['v_rates'][_tmpTrg][1], 2)
            else:
              WARNING('invalid key "'+_tmpTrg+'" in rates["'+_tmpReco+'"]["'+_puTag+'"]["'+_tmp2+'"]["v_rates"]')
            if _tmpTrg in rates[_tmpReco][_puTag][_tmp2]['v_counts']:
              theCount += rates[_tmpReco][_puTag][_tmp2]['v_counts'][_tmpTrg][0]
              theCountErr2 += math.pow(rates[_tmpReco][_puTag][_tmp2]['v_counts'][_tmpTrg][1], 2)
            else:
              WARNING('invalid key "'+_tmpTrg+'" in rates["'+_tmpReco+'"]["'+_puTag+'"]["'+_tmp2+'"]["v_counts"]')
          rateDict[_tmpReco][_puTag][_tmpTrg][_tmp1] = [theRate, math.sqrt(theRateErr2)]
          countDict[_tmpReco][_puTag][_tmpTrg][_tmp1] = [theCount, math.sqrt(theCountErr2)]

      for _tmpL1T, _tmpHLT in [
        ['L1T_SinglePFPuppiJet230off2', 'HLT_AK4PFPuppiJet'+str(rateConfig[_puTag]['hltThresholdSingleJet'])],
        ['L1T_PFPuppiHT450off', 'HLT_PFPuppiHT'+str(rateConfig[_puTag]['hltThresholdHT'])],
        ['L1T_PFPuppiMET220off2', 'HLT_PFPuppiMET'+str(rateConfig[_puTag]['hltThresholdMET'])],
        ['L1T_PFPuppiMET220off2', 'HLT_PFPuppiMETTypeOne'+str(rateConfig[_puTag]['hltThresholdMETTypeOne'])],
        ['L1T_PFPuppiMET220off2', 'HLT_PFPuppiMETTypeOneMHT20_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT20'])],
        ['L1T_PFPuppiMET220off2', 'HLT_PFPuppiMETTypeOneMHT30_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT30'])],
        ['L1T_PFPuppiMET220off2', 'HLT_PFPuppiMETTypeOneMHT40_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT40'])],
        ['L1T_PFPuppiMET220off2', 'HLT_PFPuppiMETTypeOneMHT50_'+str(rateConfig[_puTag]['hltThresholdMETTypeOneMHT50'])],
      ]:
        print '-'*110
        print '\033[1m{:10}\033[0m | \033[1m{:47}\033[0m | \033[1m{:47}\033[0m'.format('Rate [Hz]', '[L1T] '+_tmpL1T, '[L1T+HLT] '+_tmpHLT)
        print '-'*110

        for _tmp1 in sorted(rateGroup.keys()):
          l1tRate = rateDict[_tmpReco][_puTag][_tmpL1T][_tmp1][0]
          l1tRateErr = rateDict[_tmpReco][_puTag][_tmpL1T][_tmp1][1]

          hltRate = rateDict[_tmpReco][_puTag][_tmpHLT][_tmp1][0]
          hltRateErr = rateDict[_tmpReco][_puTag][_tmpHLT][_tmp1][1]

          l1tCount = countDict[_tmpReco][_puTag][_tmpL1T][_tmp1][0]
          hltCount = countDict[_tmpReco][_puTag][_tmpHLT][_tmp1][0]

          if l1tCount < opts.minCountsForValidRate:
            l1tRate, l1tRateErr = -99., -99.

          if hltCount < opts.minCountsForValidRate:
            hltRate, hltRateErr = -99., -99.

          print '{:<10} | {:>11.2f} +/- {:>10.2f} [counts = {:9.1f}] | {:>11.2f} +/- {:>10.2f} [counts = {:9.1f}]'.format(_tmp1,
            l1tRate, l1tRateErr, l1tCount,
            hltRate, hltRateErr, hltCount
          )

      rateHistos[_tmpReco][_puTag] = {}
      for _tmpVar, _tmpSamples in {
#        # L1T
#        'l1tSlwPFPuppiJet': ['MB'],
#        'l1tPFPuppiHT'    : ['MB'],
#        'l1tPFPuppiHT_2'  : ['MB'],
#        'l1tPFPuppiMET'   : ['MB'],
        # HLT
        'hltAK4PFPuppiJet_woL1T'   : ['MB+QCD+V'],
        'hltAK4PFPuppiJet'         : ['MB+QCD+V'],
        'hltPFPuppiHT_woL1T'       : ['MB+QCD+V'],
        'hltPFPuppiHT'             : ['MB+QCD+V'],
        'hltPFPuppiMET_woL1T'      : ['MB+QCD+V'],
        'hltPFPuppiMET'            : ['MB+QCD+V'],
        'hltPFPuppiMETTypeOne'     : ['MB+QCD+V'],
        'hltPFPuppiMETTypeOneMHT20': ['MB+QCD+V'],
        'hltPFPuppiMETTypeOneMHT30': ['MB+QCD+V'],
        'hltPFPuppiMETTypeOneMHT40': ['MB+QCD+V'],
        'hltPFPuppiMETTypeOneMHT50': ['MB+QCD+V'],
      }.items():
        rateHistos[_tmpReco][_puTag][_tmpVar] = None
        for _tmp1 in _tmpSamples:
          for _tmp2 in rateGroup[_tmp1]:
            if _tmpVar not in rates[_tmpReco][_puTag][_tmp2]['t_rates']:
              WARNING('invalid key "'+_tmpVar+'" in rates["'+_tmpReco+'"]["'+_puTag+'"]["'+_tmp2+'"]["t_rates"]')
              continue
            h0 = rates[_tmpReco][_puTag][_tmp2]['t_rates'][_tmpVar]
            if rateHistos[_tmpReco][_puTag][_tmpVar]:
              rateHistos[_tmpReco][_puTag][_tmpVar].Add(h0)
            else:
              rateHistos[_tmpReco][_puTag][_tmpVar] = h0.Clone()

    print '='*50
    print '='*50
    print '\033[1m'+'Rate Plots'+'\033[0m'
    print '='*50
    print '='*50

    ## Single-Jet
    canvas = ROOT.TCanvas(tmpName(), tmpName(False))
    canvas.cd()

    h0 = canvas.DrawFrame(450, 20, 600, 349)

    h140 = rateHistos[_tmpReco]['PU140']['hltAK4PFPuppiJet'].Clone()
    h140.SetMarkerStyle(20)
    h140.SetMarkerSize(0.)
    h140.SetMarkerColor(ROOT.kGreen+2)
    h140.SetLineColor(ROOT.kGreen+2)
    h140.SetLineWidth(2)
    h140.SetLineStyle(1)

    h200 = rateHistos[_tmpReco]['PU200']['hltAK4PFPuppiJet'].Clone()
    h200.SetMarkerStyle(20)
    h200.SetMarkerSize(0.)
    h200.SetMarkerColor(ROOT.kOrange+2)
    h200.SetLineColor(ROOT.kOrange+2)
    h200.SetLineWidth(2)
    h200.SetLineStyle(1)

    h140tmp = h140.Clone()
    h140tmp.SetFillStyle(3002)
    h140tmp.SetFillColor(ROOT.kGreen-3)
    h140tmp.Draw('e2,same')
    h140.Draw('hist,same')

    h200tmp = h200.Clone()
    h200tmp.SetFillStyle(3002)
    h200tmp.SetFillColor(ROOT.kOrange)
    h200tmp.Draw('e2,same')
    h200.Draw('hist,same')

    topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
    topLabel.SetFillColor(0)
    topLabel.SetFillStyle(1001)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(0)
    topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
    objLabel.SetFillColor(0)
    objLabel.SetFillStyle(1001)
    objLabel.SetTextColor(ROOT.kBlack)
    objLabel.SetTextAlign(32)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.035)
    objLabel.SetBorderSize(0)
    objLabel.AddText('14 TeV')
    objLabel.Draw('same')

    l1tRateLabel = ROOT.TPaveText(0.65, 0.60, 0.94, 0.73, 'NDC')
    l1tRateLabel.SetFillColor(0)
    l1tRateLabel.SetFillStyle(1001)
    l1tRateLabel.SetTextColor(ROOT.kBlack)
    l1tRateLabel.SetTextAlign(22)
    l1tRateLabel.SetTextFont(42)
    l1tRateLabel.SetTextSize(0.0325)
    l1tRateLabel.SetBorderSize(0)
    l1tRateLabel.AddText('HLT : Single-Jet')
    l1tRateLabel.Draw('same')

#    hltTargetRateLine = ROOT.TLine(_tmp['xmin'], _tmp['hltTargetRateHz'], _tmp['xmax'], _tmp['hltTargetRateHz'])
#    hltTargetRateLine.SetLineWidth(2)
#    hltTargetRateLine.SetLineStyle(2)
#    hltTargetRateLine.SetLineColor(ROOT.kViolet-1)
#    hltTargetRateLine.Draw('same')

    leg1 = ROOT.TLegend(0.41, 0.73, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.AddEntry(h140tmp, 'PU 140, L = 5.3 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.AddEntry(h200tmp, 'PU 200, L = 7.5 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.Draw('same')

    canvas.SetLogy(1)
    canvas.SetGrid(1, 1)

    h0.SetTitle(';HLT Jet p_{T} Threshold [GeV];HLT Rate [Hz]')
    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
    h0.GetYaxis().SetNoExponent()
    h0.GetYaxis().SetMoreLogLabels()
    h0.Draw('axis,same')

    for _tmpExt in EXTS:
      canvas.SaveAs(outputDir+'/triggerRate_SingleJet'+'.'+_tmpExt)

    canvas.Close()

    print '\033[1m'+outputDir+'/triggerRate_SingleJet'+'\033[0m'

    ## HT
    canvas = ROOT.TCanvas(tmpName(), tmpName(False))
    canvas.cd()

    h0 = canvas.DrawFrame(900, 10, 1400, 449)

    h140 = rateHistos[_tmpReco]['PU140']['hltPFPuppiHT'].Clone()
    h140.SetMarkerStyle(20)
    h140.SetMarkerSize(0.)
    h140.SetMarkerColor(ROOT.kGreen+2)
    h140.SetLineColor(ROOT.kGreen+2)
    h140.SetLineWidth(2)
    h140.SetLineStyle(1)

    h200 = rateHistos[_tmpReco]['PU200']['hltPFPuppiHT'].Clone()
    h200.SetMarkerStyle(20)
    h200.SetMarkerSize(0.)
    h200.SetMarkerColor(ROOT.kOrange+2)
    h200.SetLineColor(ROOT.kOrange+2)
    h200.SetLineWidth(2)
    h200.SetLineStyle(1)

    h140tmp = h140.Clone()
    h140tmp.SetFillStyle(3002)
    h140tmp.SetFillColor(ROOT.kGreen-3)
    h140tmp.Draw('e2,same')
    h140.Draw('hist,same')

    h200tmp = h200.Clone()
    h200tmp.SetFillStyle(3002)
    h200tmp.SetFillColor(ROOT.kOrange)
    h200tmp.Draw('e2,same')
    h200.Draw('hist,same')

    topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
    topLabel.SetFillColor(0)
    topLabel.SetFillStyle(1001)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(0)
    topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
    objLabel.SetFillColor(0)
    objLabel.SetFillStyle(1001)
    objLabel.SetTextColor(ROOT.kBlack)
    objLabel.SetTextAlign(32)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.035)
    objLabel.SetBorderSize(0)
    objLabel.AddText('14 TeV')
    objLabel.Draw('same')

    l1tRateLabel = ROOT.TPaveText(0.48, 0.63, 0.94, 0.73, 'NDC')
    l1tRateLabel.SetFillColor(0)
    l1tRateLabel.SetFillStyle(1001)
    l1tRateLabel.SetTextColor(ROOT.kBlack)
    l1tRateLabel.SetTextAlign(22)
    l1tRateLabel.SetTextFont(42)
    l1tRateLabel.SetTextSize(0.0325)
    l1tRateLabel.SetBorderSize(0)
    l1tRateLabel.AddText('HLT : Jet H_{T} (p_{T} > 30 GeV, |#eta| < 2.4)')
    l1tRateLabel.Draw('same')

#    hltTargetRateLine = ROOT.TLine(_tmp['xmin'], _tmp['hltTargetRateHz'], _tmp['xmax'], _tmp['hltTargetRateHz'])
#    hltTargetRateLine.SetLineWidth(2)
#    hltTargetRateLine.SetLineStyle(2)
#    hltTargetRateLine.SetLineColor(ROOT.kViolet-1)
#    hltTargetRateLine.Draw('same')

    leg1 = ROOT.TLegend(0.41, 0.73, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.AddEntry(h140tmp, 'PU 140, L = 5.3 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.AddEntry(h200tmp, 'PU 200, L = 7.5 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.Draw('same')

    canvas.SetLogy(1)
    canvas.SetGrid(1, 1)

    h0.SetTitle(';HLT H_{T} Threshold [GeV];HLT Rate [Hz]')
    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
    h0.GetYaxis().SetNoExponent()
    h0.GetYaxis().SetMoreLogLabels()
    h0.GetXaxis().SetNdivisions(505)
    h0.Draw('axis,same')

    for _tmpExt in EXTS:
      canvas.SaveAs(outputDir+'/triggerRate_HT'+'.'+_tmpExt)

    canvas.Close()

    print '\033[1m'+outputDir+'/triggerRate_HT'+'\033[0m'

    ## MET (Raw)
    canvas = ROOT.TCanvas(tmpName(), tmpName(False))
    canvas.cd()

    h0 = canvas.DrawFrame(100, 10, 180, 1199)

    h140 = rateHistos[_tmpReco]['PU140']['hltPFPuppiMET'].Clone()
    h140.SetMarkerStyle(20)
    h140.SetMarkerSize(0.)
    h140.SetMarkerColor(ROOT.kGreen+2)
    h140.SetLineColor(ROOT.kGreen+2)
    h140.SetLineWidth(2)
    h140.SetLineStyle(1)

    h200 = rateHistos[_tmpReco]['PU200']['hltPFPuppiMET'].Clone()
    h200.SetMarkerStyle(20)
    h200.SetMarkerSize(0.)
    h200.SetMarkerColor(ROOT.kOrange+2)
    h200.SetLineColor(ROOT.kOrange+2)
    h200.SetLineWidth(2)
    h200.SetLineStyle(1)

    h140tmp = h140.Clone()
    h140tmp.SetFillStyle(3002)
    h140tmp.SetFillColor(ROOT.kGreen-3)
    h140tmp.Draw('e2,same')
    h140.Draw('hist,same')

    h200tmp = h200.Clone()
    h200tmp.SetFillStyle(3002)
    h200tmp.SetFillColor(ROOT.kOrange)
    h200tmp.Draw('e2,same')
    h200.Draw('hist,same')

    topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
    topLabel.SetFillColor(0)
    topLabel.SetFillStyle(1001)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(0)
    topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
    objLabel.SetFillColor(0)
    objLabel.SetFillStyle(1001)
    objLabel.SetTextColor(ROOT.kBlack)
    objLabel.SetTextAlign(32)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.035)
    objLabel.SetBorderSize(0)
    objLabel.AddText('14 TeV')
    objLabel.Draw('same')

    l1tRateLabel = ROOT.TPaveText(0.60, 0.63, 0.94, 0.73, 'NDC')
    l1tRateLabel.SetFillColor(0)
    l1tRateLabel.SetFillStyle(1001)
    l1tRateLabel.SetTextColor(ROOT.kBlack)
    l1tRateLabel.SetTextAlign(22)
    l1tRateLabel.SetTextFont(42)
    l1tRateLabel.SetTextSize(0.0325)
    l1tRateLabel.SetBorderSize(0)
    l1tRateLabel.AddText('HLT : Raw p_{T}^{miss}')
    l1tRateLabel.Draw('same')

#    hltTargetRateLine = ROOT.TLine(_tmp['xmin'], _tmp['hltTargetRateHz'], _tmp['xmax'], _tmp['hltTargetRateHz'])
#    hltTargetRateLine.SetLineWidth(2)
#    hltTargetRateLine.SetLineStyle(2)
#    hltTargetRateLine.SetLineColor(ROOT.kViolet-1)
#    hltTargetRateLine.Draw('same')

    leg1 = ROOT.TLegend(0.41, 0.73, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.AddEntry(h140tmp, 'PU 140, L = 5.3 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.AddEntry(h200tmp, 'PU 200, L = 7.5 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.Draw('same')

    canvas.SetLogy(1)
    canvas.SetGrid(1, 1)

    h0.SetTitle(';HLT p_{T}^{miss} Threshold [GeV];HLT Rate [Hz]')
    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
    h0.GetYaxis().SetNoExponent()
    h0.GetYaxis().SetMoreLogLabels()
    h0.Draw('axis,same')

    for _tmpExt in EXTS:
      canvas.SaveAs(outputDir+'/triggerRate_METRaw'+'.'+_tmpExt)

    canvas.Close()

    print '\033[1m'+outputDir+'/triggerRate_METRaw'+'\033[0m'

    ## MET (TypeOne)
    canvas = ROOT.TCanvas(tmpName(), tmpName(False))
    canvas.cd()

    h0 = canvas.DrawFrame(100, 25, 180, 4999)

    h140 = rateHistos[_tmpReco]['PU140']['hltPFPuppiMETTypeOne'].Clone()
    h140.SetMarkerStyle(20)
    h140.SetMarkerSize(0.)
    h140.SetMarkerColor(ROOT.kGreen+2)
    h140.SetLineColor(ROOT.kGreen+2)
    h140.SetLineWidth(2)
    h140.SetLineStyle(1)

    h200 = rateHistos[_tmpReco]['PU200']['hltPFPuppiMETTypeOne'].Clone()
    h200.SetMarkerStyle(20)
    h200.SetMarkerSize(0.)
    h200.SetMarkerColor(ROOT.kOrange+2)
    h200.SetLineColor(ROOT.kOrange+2)
    h200.SetLineWidth(2)
    h200.SetLineStyle(1)

    h140tmp = h140.Clone()
    h140tmp.SetFillStyle(3002)
    h140tmp.SetFillColor(ROOT.kGreen-3)
    h140tmp.Draw('e2,same')
    h140.Draw('hist,same')

    h200tmp = h200.Clone()
    h200tmp.SetFillStyle(3002)
    h200tmp.SetFillColor(ROOT.kOrange)
    h200tmp.Draw('e2,same')
    h200.Draw('hist,same')

    topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
    topLabel.SetFillColor(0)
    topLabel.SetFillStyle(1001)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(0)
    topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
    objLabel.SetFillColor(0)
    objLabel.SetFillStyle(1001)
    objLabel.SetTextColor(ROOT.kBlack)
    objLabel.SetTextAlign(32)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.035)
    objLabel.SetBorderSize(0)
    objLabel.AddText('14 TeV')
    objLabel.Draw('same')

    l1tRateLabel = ROOT.TPaveText(0.60, 0.63, 0.94, 0.73, 'NDC')
    l1tRateLabel.SetFillColor(0)
    l1tRateLabel.SetFillStyle(1001)
    l1tRateLabel.SetTextColor(ROOT.kBlack)
    l1tRateLabel.SetTextAlign(22)
    l1tRateLabel.SetTextFont(42)
    l1tRateLabel.SetTextSize(0.0325)
    l1tRateLabel.SetBorderSize(0)
    l1tRateLabel.AddText('HLT : Type-1 p_{T}^{miss}')
    l1tRateLabel.Draw('same')

    leg1 = ROOT.TLegend(0.41, 0.73, 0.94, 0.90)
    leg1.SetNColumns(1)
    leg1.SetTextFont(42)
    leg1.AddEntry(h140tmp, 'PU 140, L = 5.3 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.AddEntry(h200tmp, 'PU 200, L = 7.5 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
    leg1.Draw('same')

    l1tRateLabel.Draw('same')

    canvas.SetLogy(1)
    canvas.SetGrid(1, 1)

    h0.SetTitle(';HLT p_{T}^{miss} Threshold [GeV];HLT Rate [Hz]')
    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
    h0.GetYaxis().SetNoExponent()
    h0.GetYaxis().SetMoreLogLabels()
    h0.Draw('axis,same')

    for _tmpExt in EXTS:
      canvas.SaveAs(outputDir+'/triggerRate_METTypeOne'+'.'+_tmpExt)

    canvas.Close()

    print '\033[1m'+outputDir+'/triggerRate_METTypeOne'+'\033[0m'

    ## MET (TypeOne)
    for _metType in [
      'METTypeOneMHT20',
      'METTypeOneMHT30',
      'METTypeOneMHT40',
      'METTypeOneMHT50',
    ]:
      canvas = ROOT.TCanvas(tmpName(), tmpName(False))
      canvas.cd()

      h0 = canvas.DrawFrame(100, 18, 180, 3999)

      h140 = rateHistos[_tmpReco]['PU140']['hltPFPuppi'+_metType].Clone()
      h140.SetMarkerStyle(20)
      h140.SetMarkerSize(0.)
      h140.SetMarkerColor(ROOT.kGreen+2)
      h140.SetLineColor(ROOT.kGreen+2)
      h140.SetLineWidth(2)
      h140.SetLineStyle(1)

      h200 = rateHistos[_tmpReco]['PU200']['hltPFPuppi'+_metType].Clone()
      h200.SetMarkerStyle(20)
      h200.SetMarkerSize(0.)
      h200.SetMarkerColor(ROOT.kOrange+2)
      h200.SetLineColor(ROOT.kOrange+2)
      h200.SetLineWidth(2)
      h200.SetLineStyle(1)

      h140tmp = h140.Clone()
      h140tmp.SetFillStyle(3002)
      h140tmp.SetFillColor(ROOT.kGreen-3)
      h140tmp.Draw('e2,same')
      h140.Draw('hist,same')

      h200tmp = h200.Clone()
      h200tmp.SetFillStyle(3002)
      h200tmp.SetFillColor(ROOT.kOrange)
      h200tmp.Draw('e2,same')
      h200.Draw('hist,same')

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText('14 TeV')
      objLabel.Draw('same')
  
      l1tRateLabel = ROOT.TPaveText(0.57, 0.63, 0.94, 0.73, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(22)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.0325)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('HLT : Type-1 p_{T}^{miss} + MHT')
      l1tRateLabel.Draw('same')
  
      leg1 = ROOT.TLegend(0.41, 0.73, 0.94, 0.90)
      leg1.SetNColumns(1)
      leg1.SetTextFont(42)
      leg1.AddEntry(h140tmp, 'PU 140, L = 5.3 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
      leg1.AddEntry(h200tmp, 'PU 200, L = 7.5 #upoint 10^{34} cm^{-2} s^{-1}', 'lf')
      leg1.Draw('same')
  
      l1tRateLabel.Draw('same')
  
      canvas.SetLogy(1)
      canvas.SetGrid(1, 1)
  
      h0.SetTitle(';HLT p_{T}^{miss} Threshold [GeV];HLT Rate [Hz]')
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
      h0.GetYaxis().SetNoExponent()
      h0.GetYaxis().SetMoreLogLabels()
      h0.Draw('axis,same')
  
      for _tmpExt in EXTS:
        canvas.SaveAs(outputDir+'/triggerRate_'+_metType+'.'+_tmpExt)
  
      canvas.Close()
  
      print '\033[1m'+outputDir+'/triggerRate_'+_metType+'\033[0m'

    ## MET comparison (Raw vs TypeOne vs TypeOne+MHT)
    for _tmpPU in [
      'PU140',
      'PU200',
    ]:
      canvas = ROOT.TCanvas(tmpName(), tmpName(False))
      canvas.cd()

      if _tmpPU == 'PU140':
        h0 = canvas.DrawFrame(100, 12, 180, 799)
      else:
        h0 = canvas.DrawFrame(100, 25, 180, 9999)

      h1 = rateHistos[_tmpReco][_tmpPU]['hltPFPuppiMET'].Clone()
      h1.SetMarkerStyle(20)
      h1.SetMarkerSize(0.)
      h1.SetMarkerColor(ROOT.kGreen+2)
      h1.SetLineColor(ROOT.kGreen+2)
      h1.SetLineWidth(2)
      h1.SetLineStyle(1)
      h1tmp = h1.Clone()
      h1tmp.SetFillStyle(3002)
      h1tmp.SetFillColor(ROOT.kGreen-3)
#      h1tmp.Draw('e2,same')
#      h1.Draw('hist,same')

      h2 = rateHistos[_tmpReco][_tmpPU]['hltPFPuppiMETTypeOne'].Clone()
      h2.SetMarkerStyle(20)
      h2.SetMarkerSize(0.)
      h2.SetMarkerColor(ROOT.kBlack)
      h2.SetLineColor(ROOT.kBlack)
      h2.SetLineWidth(2)
      h2.SetLineStyle(1)
      h2tmp = h2.Clone()
      h2tmp.SetFillStyle(3002)
      h2tmp.SetFillColor(ROOT.kGray+1)
      h2tmp.Draw('e2,same')
      h2.Draw('hist,same')

      h3 = rateHistos[_tmpReco][_tmpPU]['hltPFPuppiMETTypeOneMHT20'].Clone()
      h3.SetMarkerStyle(20)
      h3.SetMarkerSize(0.)
      h3.SetMarkerColor(ROOT.kRed)
      h3.SetLineColor(ROOT.kRed)
      h3.SetLineWidth(2)
      h3.SetLineStyle(1)
      h3tmp = h3.Clone()
      h3tmp.SetFillStyle(3002)
      h3tmp.SetFillColor(ROOT.kRed)
      h3tmp.Draw('e2,same')
      h3.Draw('hist,same')

      h4 = rateHistos[_tmpReco][_tmpPU]['hltPFPuppiMETTypeOneMHT30'].Clone()
      h4.SetMarkerStyle(20)
      h4.SetMarkerSize(0.)
      h4.SetMarkerColor(ROOT.kBlue)
      h4.SetLineColor(ROOT.kBlue)
      h4.SetLineWidth(2)
      h4.SetLineStyle(1)
      h4tmp = h4.Clone()
      h4tmp.SetFillStyle(3002)
      h4tmp.SetFillColor(ROOT.kBlue)
      h4tmp.Draw('e2,same')
      h4.Draw('hist,same')

      h5 = rateHistos[_tmpReco][_tmpPU]['hltPFPuppiMETTypeOneMHT40'].Clone()
      h5.SetMarkerStyle(20)
      h5.SetMarkerSize(0.)
      h5.SetMarkerColor(ROOT.kOrange+2)
      h5.SetLineColor(ROOT.kOrange+2)
      h5.SetLineWidth(2)
      h5.SetLineStyle(1)
      h5tmp = h5.Clone()
      h5tmp.SetFillStyle(3002)
      h5tmp.SetFillColor(ROOT.kOrange)
      h5tmp.Draw('e2,same')
      h5.Draw('hist,same')

      h6 = rateHistos[_tmpReco][_tmpPU]['hltPFPuppiMETTypeOneMHT50'].Clone()
      h6.SetMarkerStyle(20)
      h6.SetMarkerSize(0.)
      h6.SetMarkerColor(ROOT.kViolet)
      h6.SetLineColor(ROOT.kViolet)
      h6.SetLineWidth(2)
      h6.SetLineStyle(1)
      h6tmp = h6.Clone()
      h6tmp.SetFillStyle(3002)
      h6tmp.SetFillColor(ROOT.kViolet)
      h6tmp.Draw('e2,same')
      h6.Draw('hist,same')

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText(_tmpPU[2:]+' PU (14 TeV)')
      objLabel.Draw('same')

      l1tRateLabel = ROOT.TPaveText(0.57, 0.43, 0.94, 0.53, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(22)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.0325)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('HLT : Type-1 p_{T}^{miss} (+MHT)')
      l1tRateLabel.Draw('same')

      puLabel = ROOT.TPaveText(0.165, 0.76, 0.43, 0.83, 'NDC')
      puLabel.SetFillColor(0)
      puLabel.SetFillStyle(1001)
      puLabel.SetTextColor(ROOT.kBlack)
      puLabel.SetTextAlign(12)
      puLabel.SetTextFont(42)
      puLabel.SetTextSize(0.0325)
      puLabel.SetBorderSize(0)
      puLabel.AddText('L = '+('7.5' if _tmpPU == 'PU200' else '5.3')+' #upoint 10^{34} cm^{-2} s^{-1}')
      puLabel.Draw('same')

      leg1 = ROOT.TLegend(0.63, 0.53, 0.94, 0.90)
      leg1.SetNColumns(1)
      leg1.SetTextFont(42)
#      leg1.AddEntry(h1tmp, 'Raw', 'lf')
      leg1.AddEntry(h2tmp, 'Type-1', 'lf')
      leg1.AddEntry(h3tmp, 'Type-1 + MHT_{20}', 'lf')
      leg1.AddEntry(h4tmp, 'Type-1 + MHT_{30}', 'lf')
      leg1.AddEntry(h5tmp, 'Type-1 + MHT_{40}', 'lf')
      leg1.AddEntry(h6tmp, 'Type-1 + MHT_{50}', 'lf')
      leg1.Draw('same')

      canvas.SetLogy(1)
      canvas.SetGrid(1, 1)

      h0.SetTitle(';HLT p_{T}^{miss} Threshold [GeV];HLT Rate [Hz]')
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
      h0.GetYaxis().SetNoExponent()
      h0.GetYaxis().SetMoreLogLabels()
      h0.Draw('axis,same')

      for _tmpExt in EXTS:
        canvas.SaveAs(outputDir+'/triggerRate_METTypeOneX_'+_tmpPU+'.'+_tmpExt)
      canvas.Close()

      print '\033[1m'+outputDir+'/triggerRate_METTypeOneX_'+_tmpPU+'\033[0m'

  print '='*50

## for _tmp1 in sorted(rateDict.keys()):
##   for _tmp2 in sorted(rateDict[_tmp1].keys()):
##     aRate, aRateErr2 = 0., 0.
##     for _tmp3 in ['QCD', 'Wln', 'Zll']:
##       aRate += rateDict[_tmp1][_tmp2][_tmp3][0]
##       aRateErr2 += math.pow(rateDict[_tmp1][_tmp2][_tmp3][1], 2)
##     print _tmp1, '  ', _tmp2, aRate, math.sqrt(aRateErr2)

## ## Output TFile
## ofile = ROOT.TFile('tmp.root', 'recreate')
## ofile.cd()
## 
## for _tmp0 in [effysJet, effysMET]:
##   for _tmp1 in sorted(_tmp0.keys()):
##     _odir = ofile.Get(_tmp1) if ofile.Get(_tmp1) else ofile.mkdir(_tmp1)
##     _odir.cd()
##     for _tmp2 in sorted(_tmp0[_tmp1].keys()):
##       _tmp0[_tmp1][_tmp2].Write()
## 
## ofile.Close()
