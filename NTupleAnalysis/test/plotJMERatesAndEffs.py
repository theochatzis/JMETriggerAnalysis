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

L1T_SingleJet = 'L1T_SinglePFPuppiJet200off'
L1T_HT = 'L1T_PFPuppiHT450off'

COUNTER = 0
def tmpName():
  global COUNTER
  COUNTER += 1
  return 'tmp'+str(COUNTER)

def getRateFactor(processName):
  if   processName == 'MinBias_14TeV'             : return 30.903 * 1e6
  elif processName == 'QCD_Pt020to030_14TeV'      : return 0.075 * 436000000.0
  elif processName == 'QCD_Pt030to050_14TeV'      : return 0.075 * 118400000.0
  elif processName == 'QCD_Pt050to080_14TeV'      : return 0.075 *  17650000.0
  elif processName == 'QCD_Pt080to120_14TeV'      : return 0.075 *   2671000.0
  elif processName == 'QCD_Pt120to170_14TeV'      : return 0.075 *    469700.0
  elif processName == 'QCD_Pt170to300_14TeV'      : return 0.075 *    121700.0
  elif processName == 'QCD_Pt300to470_14TeV'      : return 0.075 *      8251.0
  elif processName == 'QCD_Pt470to600_14TeV'      : return 0.075 *       686.4
  elif processName == 'QCD_Pt600toInf_14TeV'      : return 0.075 *       244.8
  elif processName == 'WJetsToLNu_14TeV'          : return 0.075 *     56990.0
  elif processName == 'DYJetsToLL_M010to050_14TeV': return 0.075 *     16880.0
  elif processName == 'DYJetsToLL_M050toInf_14TeV': return 0.075 *      5795.0
  else:
    raise RuntimeError(processName)

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

def getRates(fpath, processName, hltThreshold_SingleJet, hltThreshold_HT, hltThreshold_MET, hltThreshold_MET2):
  global L1T_SingleJet, L1T_HT

  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)

  _eventsProcessed = _tfile.Get('eventsProcessed')
  ret['v_eventsProcessed'] = _eventsProcessed.GetEntries()

  rateFactor = getRateFactor(processName) / ret['v_eventsProcessed']

  ret['t_rates'] = {}
  ret['v_rates'] = {}
  ret['v_counts'] = {}

  # SingleJet
  ret['t_rates']['l1tSlwPFPuppiJet'] = getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)

  ret['t_rates']['hltAK4PFPuppiJet_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)
  ret['t_rates']['hltAK4PFPuppiJet'] = getRateHistogram(_tfile.Get(L1T_SingleJet+'/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0'), rateFactor)

  _tmp = _tfile.Get(L1T_SingleJet+'/l1tSlwPFPuppiJetsCorrected_EtaIncl_pt0')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] [L1T_SingleJet] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts'][L1T_SingleJet] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get(L1T_SingleJet+'/hltAK4PFPuppiJetsCorrected_EtaIncl_pt0')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_SingleJet)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_AK4PFPuppiJet'+str(hltThreshold_SingleJet)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_AK4PFPuppiJet'+str(hltThreshold_SingleJet)] = [_tmp_integ, _tmp_integErr.value]

  # HT
  ret['t_rates']['l1tPFPuppiHT'] = getRateHistogram(_tfile.Get('NoSelection/l1tPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['l1tPFPuppiHT_2'] = getRateHistogram(_tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_Eta2p4_HT'), rateFactor)

  ret['t_rates']['hltPFPuppiHT_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['hltPFPuppiHT'] = getRateHistogram(_tfile.Get(L1T_HT+'/hltPFPuppiHT_sumEt'), rateFactor)

  _tmp = _tfile.Get(L1T_HT+'/l1tPFPuppiHT_sumEt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] [L1T_HT] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts'][L1T_HT] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get(L1T_HT+'/hltPFPuppiHT_sumEt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_HT)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_PFPuppiHT'+str(hltThreshold_HT)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_PFPuppiHT'+str(hltThreshold_HT)] = [_tmp_integ, _tmp_integErr.value]

  # MET
  ret['t_rates']['l1tPFPuppiMET'] = getRateHistogram(_tfile.Get('NoSelection/l1tPFPuppiMET_pt'), rateFactor)

  ret['t_rates']['hltPFPuppiMET_woL1T'] = getRateHistogram(_tfile.Get('NoSelection/hltPFPuppiHT_sumEt'), rateFactor)
  ret['t_rates']['hltPFPuppiMET'] = getRateHistogram(_tfile.Get('L1T_PFPuppiMET200off/hltPFPuppiMET_pt'), rateFactor)
  ret['t_rates']['hltPFPuppiMET2'] = getRateHistogram(_tfile.Get('L1T_PFPuppiMET245off/hltPFPuppiMET_pt'), rateFactor)

  _tmp = _tfile.Get('L1T_PFPuppiMET200off/l1tPFPuppiMET_pt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] ['L1T_PFPuppiMET200off'] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['L1T_PFPuppiMET200off'] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get('L1T_PFPuppiMET200off/hltPFPuppiMET_pt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_MET)), -1, _tmp_integErr)
  ret['v_rates'] ['HLT_PFPuppiMET'+str(hltThreshold_MET)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['HLT_PFPuppiMET'+str(hltThreshold_MET)] = [_tmp_integ, _tmp_integErr.value]

  _tmp = _tfile.Get('L1T_PFPuppiMET245off/l1tPFPuppiMET_pt')
  _tmp_integErr = ctypes.c_double(0.)
  _tmp_integ = _tmp.IntegralAndError(0, -1, _tmp_integErr)
  ret['v_rates'] ['L1T_PFPuppiMET245off'] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
  ret['v_counts']['L1T_PFPuppiMET245off'] = [_tmp_integ, _tmp_integErr.value]

  if hltThreshold_MET2 != hltThreshold_MET:
    _tmp = _tfile.Get('L1T_PFPuppiMET245off/hltPFPuppiMET_pt')
    _tmp_integErr = ctypes.c_double(0.)
    _tmp_integ = _tmp.IntegralAndError(_tmp.GetXaxis().FindBin(float(hltThreshold_MET)), -1, _tmp_integErr)
    ret['v_rates'] ['HLT_PFPuppiMET'+str(hltThreshold_MET2)] = [rateFactor * _tmp_integ, rateFactor * _tmp_integErr.value]
    ret['v_counts']['HLT_PFPuppiMET'+str(hltThreshold_MET2)] = [_tmp_integ, _tmp_integErr.value]

  ## common
  for _tmp1 in ret:
    if not _tmp1.startswith('t_'):
      continue
    for _tmp2 in ret[_tmp1]:
      if ret[_tmp1][_tmp2].InheritsFrom('TH1'):
        ret[_tmp1][_tmp2].SetDirectory(0)
        ret[_tmp1][_tmp2].UseCurrentStyle()

  _tfile.Close()

  return ret

def getJetEfficiencies(fpath, hltThreshold_SingleJet, hltThreshold_HT):
  global L1T_SingleJet, L1T_HT

  ret = {}

  _tfile = ROOT.TFile.Open(fpath)

  # SingleJet
  for _tmpRef in ['GEN', 'Offline']:
    _tmp_num = _tfile.Get(L1T_SingleJet+'/l1tSlwPFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['SingleJet_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1T_wrt_'+_tmpRef].SetName('SingleJet_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_SingleJet), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['SingleJet_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_HLT_wrt_'+_tmpRef].SetName('SingleJet_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get(L1T_SingleJet+'/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_SingleJet), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_MatchedTo'+_tmpRef+'_pt0__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['SingleJet_L1TpHLT_wrt_'+_tmpRef].SetName('SingleJet_L1TpHLT_wrt_'+_tmpRef)

  # HT
  for _tmpRef in ['GEN', 'Offline']:

    _tmp_num = _tfile.Get(L1T_HT+'/l1tSlwPFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tSlwPFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1T_wrt_'+_tmpRef].SetName('HT_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_HLT_wrt_'+_tmpRef].SetName('HT_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get(L1T_HT+'/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_HT), -1)

    _tmp_den = _tfile.Get('NoSelection/hltAK4PFPuppiJetsCorrected_EtaIncl_HT__vs__'+_tmpRef+'_HT')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['HT_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['HT_L1TpHLT_wrt_'+_tmpRef].SetName('HT_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getMETEfficiencies(fpath, hltThreshold_MET, hltThreshold_MET2):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)

  for _tmpRef in ['GEN', 'Offline']:
    # MET
    _tmp_num = _tfile.Get('L1T_PFPuppiMET200off/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_L1T_wrt_'+_tmpRef].SetName('MET_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_HLT_wrt_'+_tmpRef].SetName('MET_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiMET200off/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET_L1TpHLT_wrt_'+_tmpRef].SetName('MET_L1TpHLT_wrt_'+_tmpRef)

    # MET2
    _tmp_num = _tfile.Get('L1T_PFPuppiMET245off/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), 0, -1)

    _tmp_den = _tfile.Get('NoSelection/l1tPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET2_L1T_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET2_L1T_wrt_'+_tmpRef].SetName('MET_L1T_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET2), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET2_HLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET2_HLT_wrt_'+_tmpRef].SetName('MET_HLT_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('L1T_PFPuppiMET245off/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_num = _tmp_num.ProjectionY(tmpName(), _tmp_num.GetXaxis().FindBin(hltThreshold_MET2), -1)

    _tmp_den = _tfile.Get('NoSelection/hltPFPuppiMET_pt__vs__'+_tmpRef+'_pt')
    _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)

    ret['MET2_L1TpHLT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['MET2_L1TpHLT_wrt_'+_tmpRef].SetName('MET_L1TpHLT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

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

  apply_style(0)

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir

  hltThresholds = {
  
    'HLT_TRKv06p1': {
  
      'SingleJet': 470,
      'HT': 970,
      'MET': 120,
      'MET2': 120,
    },
  
    'HLT_TRKv07p2': {

      'SingleJet': 480,
      'HT': 1030,
      'MET': 120,
      'MET2': 120,
    },

    'HLT_TRKv06p1_TICL': {

      'SingleJet': 470,
      'HT': 1000,
      'MET': 150,
      'MET2': 150,
    },

    'HLT_TRKv07p2_TICL': {

      'SingleJet': 490,
      'HT': 1370,
      'MET': 230,
      'MET2': 230,
    },

    'HLT_TRKv06p1_TICLv2': {

      'SingleJet': 470,
      'HT': 980,
      'MET': 130,
      'MET2': 130,
    },

    'HLT_TRKv07p2_TICLv2': {

      'SingleJet': 480,
      'HT': 1050,
      'MET': 150,
      'MET2': 150,
    },
  }

  rateGroup = {
  
    'MB': [
      'MinBias_14TeV',
    ],
  
    'QCD': [
#      'QCD_Pt020to030_14TeV',
#      'QCD_Pt030to050_14TeV',
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

  QCDSamples = [
#    'QCD_020',
#    'QCD_030',
    'QCD_050',
    'QCD_080',
    'QCD_120',
    'QCD_170',
    'QCD_300',
    'QCD_470',
    'QCD_600',
  ]

  rateSamples = []
  for _tmp in rateGroup:
    rateSamples += rateGroup[_tmp]
  rateSamples = sorted(list(set(rateSamples)))

  rates = {}
  rateHistos = {}
  effys = {}
  effysJet = {}
  effysMET = {}

  rateDict = {}
  countDict = {}

  for _tmpReco in sorted(hltThresholds.keys()):
    print '='*110
    print '='*110
    print '\033[1m'+_tmpReco+'\033[0m'
    print '='*110
    print '='*110
  
    hltThresholdSingleJet = hltThresholds[_tmpReco]['SingleJet']
    hltThresholdHT = hltThresholds[_tmpReco]['HT']
    hltThresholdMET = hltThresholds[_tmpReco]['MET']
    hltThresholdMET2 = hltThresholds[_tmpReco]['MET2']
  
    hltPath_SingleJet = 'HLT_AK4PFPuppiJet'+str(hltThresholdSingleJet)
    hltPath_HT = 'HLT_PFPuppiHT'+str(hltThresholdHT)
    hltPath_MET = 'HLT_PFPuppiMET'+str(hltThresholdMET)
    hltPath_MET2 = 'HLT_PFPuppiMET'+str(hltThresholdMET2)
  
    rates[_tmpReco] = {}
    for _tmp in rateSamples:
      rates[_tmpReco][_tmp] = getRates(
        fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_'+_tmp+'_PU200.root',
        processName = _tmp,
        hltThreshold_SingleJet = hltThresholdSingleJet,
        hltThreshold_HT = hltThresholdHT,
        hltThreshold_MET = hltThresholdMET,
        hltThreshold_MET2 = hltThresholdMET2,
      )
  
    rateDict[_tmpReco] = {}
    countDict[_tmpReco] = {}
    for _tmpTrg in [
      L1T_SingleJet,
      hltPath_SingleJet,
  
      L1T_HT,
      hltPath_HT,
  
      'L1T_PFPuppiMET200off',
      hltPath_MET,
  
      'L1T_PFPuppiMET245off',
      hltPath_MET2,
    ]:
      rateDict[_tmpReco][_tmpTrg] = {}
      countDict[_tmpReco][_tmpTrg] = {}
      for _tmp1 in rateGroup:
        theRate, theRateErr2 = 0., 0.
        theCount, theCountErr2 = 0., 0.
        for _tmp2 in rateGroup[_tmp1]:
          theRate += rates[_tmpReco][_tmp2]['v_rates'][_tmpTrg][0]
          theRateErr2 += math.pow(rates[_tmpReco][_tmp2]['v_rates'][_tmpTrg][1], 2)
          theCount += rates[_tmpReco][_tmp2]['v_counts'][_tmpTrg][0]
          theCountErr2 += math.pow(rates[_tmpReco][_tmp2]['v_counts'][_tmpTrg][1], 2)
        rateDict[_tmpReco][_tmpTrg][_tmp1] = [theRate, math.sqrt(theRateErr2)]
        countDict[_tmpReco][_tmpTrg][_tmp1] = [theCount, math.sqrt(theCountErr2)]
  
    for _tmpL1T, _tmpHLT in [
      [L1T_SingleJet, hltPath_SingleJet],
      [L1T_HT, hltPath_HT],
      ['L1T_PFPuppiMET200off', hltPath_MET],
      ['L1T_PFPuppiMET245off', hltPath_MET2],
    ]:
      print '-'*110
      print '\033[1m{:10}\033[0m | \033[1m{:47}\033[0m | \033[1m{:47}\033[0m'.format('Rate [Hz]', '[L1T] '+_tmpL1T, '[L1T+HLT] '+_tmpHLT)
      print '-'*110

      for _tmp1 in sorted(rateGroup.keys()):

        l1tRate    = rateDict[_tmpReco][_tmpL1T][_tmp1][0]
        l1tRateErr = rateDict[_tmpReco][_tmpL1T][_tmp1][1]

        hltRate    = rateDict[_tmpReco][_tmpHLT][_tmp1][0]
        hltRateErr = rateDict[_tmpReco][_tmpHLT][_tmp1][1]

        l1tCount = countDict[_tmpReco][_tmpL1T][_tmp1][0]
        hltCount = countDict[_tmpReco][_tmpHLT][_tmp1][0]

        if l1tCount < opts.minCountsForValidRate:
          l1tRate, l1tRateErr = -99., -99.

        if hltCount < opts.minCountsForValidRate:
          hltRate, hltRateErr = -99., -99.

        print '{:<10} | {:>11.2f} +/- {:>10.2f} [counts = {:9.1f}] | {:>11.2f} +/- {:>10.2f} [counts = {:9.1f}]'.format(_tmp1,
          l1tRate, l1tRateErr, l1tCount,
          hltRate, hltRateErr, hltCount
        )

    rateHistos[_tmpReco] = {}

    for _tmpVar, _tmpSamples in {
      # L1T
      'l1tSlwPFPuppiJet': ['MB'],
      'l1tPFPuppiHT'    : ['MB'],
      'l1tPFPuppiHT_2'  : ['MB'],
      'l1tPFPuppiMET'   : ['MB'],

      # HLT
      'hltAK4PFPuppiJet_woL1T': QCDSamples+['Wln', 'Zll'],
      'hltAK4PFPuppiJet'      : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiHT_woL1T'    : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiHT'          : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiMET_woL1T'   : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiMET'         : QCDSamples+['Wln', 'Zll'],
      'hltPFPuppiMET2'        : QCDSamples+['Wln', 'Zll'],
    }.items():
      rateHistos[_tmpReco][_tmpVar] = None
      for _tmp1 in _tmpSamples:
        for _tmp2 in rateGroup[_tmp1]:
          h0 = rates[_tmpReco][_tmp2]['t_rates'][_tmpVar]
          if rateHistos[_tmpReco][_tmpVar]:
            rateHistos[_tmpReco][_tmpVar].Add(h0)
          else:
            rateHistos[_tmpReco][_tmpVar] = h0.Clone()

    effysJet[_tmpReco] = getJetEfficiencies(
      fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
      hltThreshold_SingleJet = hltThresholdSingleJet,
      hltThreshold_HT = hltThresholdHT,
    )

    effysMET[_tmpReco] = getMETEfficiencies(
      fpath = inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root',
      hltThreshold_MET = hltThresholdMET,
      hltThreshold_MET2 = hltThresholdMET2,
    )

  ### Plots
  if not opts.no_plots:

    outputDir = opts.output
    MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

    canvasCount = 0

    print '='*50
    print '='*50
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*50
    print '='*50

    for _tmpReco in sorted(hltThresholds.keys()):

      hltThresholdSingleJet = hltThresholds[_tmpReco]['SingleJet']
      hltThresholdHT = hltThresholds[_tmpReco]['HT']
      hltThresholdMET = hltThresholds[_tmpReco]['MET']
      hltThresholdMET2 = hltThresholds[_tmpReco]['MET2']

      hltPath_SingleJet = 'HLT_AK4PFPuppiJet'+str(hltThresholdSingleJet)
      hltPath_HT = 'HLT_PFPuppiHT'+str(hltThresholdHT)
      hltPath_MET = 'HLT_PFPuppiMET'+str(hltThresholdMET)
      hltPath_MET2 = 'HLT_PFPuppiMET'+str(hltThresholdMET2)

      for _tmpRef in ['GEN', 'Offline']:

        for _tmp in [
          {
            'l1tPathKey': L1T_SingleJet,
            'hltPathKey': hltPath_SingleJet,
            'outputName': outputDir+'/effy_SingleJet_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' Jet p_{T} [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'QCD_PtFlat_PU200',
            'xmin': 0,
            'xmax': 1000,
            'logY': 0,
            'graphs': [
              {'graph': effysJet[_tmpReco]['SingleJet_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysJet[_tmpReco]['SingleJet_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['SingleJet'])},
              {'graph': effysJet[_tmpReco]['SingleJet_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['SingleJet'])},
            ],
          },
          {
            'l1tPathKey': L1T_HT,
            'hltPathKey': hltPath_HT,
            'outputName': outputDir+'/effy_HT_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' H_{T} [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'QCD_PtFlat_PU200',
            'xmin': 0,
            'xmax': 2000,
            'logY': 0,
            'graphs': [
              {'graph': effysJet[_tmpReco]['HT_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysJet[_tmpReco]['HT_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['HT'])},
              {'graph': effysJet[_tmpReco]['HT_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['HT'])},
            ],
          },
          {
            'l1tPathKey': 'L1T_PFPuppiMET200off',
            'hltPathKey': hltPath_MET,
            'outputName': outputDir+'/effy_MET_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' MET [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'VBF_HiggsToInvisible_PU200',
            'xmin': 0,
            'xmax': 600,
            'logY': 0,
            'graphs': [
              {'graph': effysMET[_tmpReco]['MET_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysMET[_tmpReco]['MET_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['MET'])},
              {'graph': effysMET[_tmpReco]['MET_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['MET'])},
            ],
          },
          {
            'l1tPathKey': 'L1T_PFPuppiMET245off',
            'hltPathKey': hltPath_MET2,
            'outputName': outputDir+'/effy_MET2_wrt'+_tmpRef+'_'+_tmpReco,
            'outputExts': EXTS,
            'title': ';'+_tmpRef+' MET [GeV];Efficiency',
            'objLabel': _tmpReco,
            'topLabel': 'VBF_HiggsToInvisible_PU200',
            'xmin': 0,
            'xmax': 600,
            'logY': 0,
            'graphs': [
              {'graph': effysMET[_tmpReco]['MET2_L1T_wrt_'+_tmpRef], 'color': 2, 'legName': 'L1T'},
              {'graph': effysMET[_tmpReco]['MET2_HLT_wrt_'+_tmpRef], 'color': 1, 'legName': 'HLT'+str(hltThresholds[_tmpReco]['MET2'])},
              {'graph': effysMET[_tmpReco]['MET2_L1TpHLT_wrt_'+_tmpRef], 'color': 4, 'legName': 'L1T + HLT'+str(hltThresholds[_tmpReco]['MET2'])},
            ],
          },
        ]:
          canvasCount += 1
          canvasNamePostfix = '_'+str(canvasCount)

          theEffys = []
          for _tmpIdx in range(len(_tmp['graphs'])):
            g0 = _tmp['graphs'][_tmpIdx]['graph']
            g0.SetMarkerSize(0.5)
            g0.SetLineWidth(2)
            g0.SetMarkerColor(_tmp['graphs'][_tmpIdx]['color'])
            g0.SetLineColor(_tmp['graphs'][_tmpIdx]['color'])
            g0.SetName(_tmp['graphs'][_tmpIdx]['legName'])
            theEffys += [g0]

          canvas = ROOT.TCanvas('c'+canvasNamePostfix, 'c'+canvasNamePostfix)
          canvas.cd()

          h0 = canvas.DrawFrame(_tmp['xmin'], 0.0001, _tmp['xmax'], 1.19)

          for _tmp2 in theEffys:
            if _tmp2 is not None:
              _tmp2.Draw('lepz')

          topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
          topLabel.SetFillColor(0)
          topLabel.SetFillStyle(1001)
          topLabel.SetTextColor(ROOT.kBlack)
          topLabel.SetTextAlign(12)
          topLabel.SetTextFont(42)
          topLabel.SetTextSize(0.035)
          topLabel.SetBorderSize(0)
          topLabel.AddText(_tmp['topLabel'])
          topLabel.Draw('same')

          objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
          objLabel.SetFillColor(0)
          objLabel.SetFillStyle(1001)
          objLabel.SetTextColor(ROOT.kBlack)
          objLabel.SetTextAlign(32)
          objLabel.SetTextFont(42)
          objLabel.SetTextSize(0.035)
          objLabel.SetBorderSize(0)
          objLabel.AddText(_tmp['objLabel'])
          objLabel.Draw('same')

          l1tRateVal = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][0]
          l1tRateErr = rateDict[_tmpReco][_tmp['l1tPathKey']]['MB'][1]

          hltRateVal = 0.
          hltRateErr2 = 0.
          for _tmpSample in QCDSamples+['Wln', 'Zll']:
            hltRateVal += rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][0]
            hltRateErr2 += math.pow(rateDict[_tmpReco][_tmp['hltPathKey']][_tmpSample][1], 2)

          l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.65, 0.90, 'NDC')
          l1tRateLabel.SetFillColor(0)
          l1tRateLabel.SetFillStyle(1001)
          l1tRateLabel.SetTextColor(ROOT.kBlack)
          l1tRateLabel.SetTextAlign(12)
          l1tRateLabel.SetTextFont(42)
          l1tRateLabel.SetTextSize(0.0325)
          l1tRateLabel.SetBorderSize(0)
          l1tRateLabel.AddText('L1T Rate = {:4.1f} +/- {:4.1f} kHz (MB)'.format(l1tRateVal/1000., l1tRateErr/1000.))
          l1tRateLabel.Draw('same')

          hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.65, 0.85, 'NDC')
          hltRateLabel.SetFillColor(0)
          hltRateLabel.SetFillStyle(1001)
          hltRateLabel.SetTextColor(ROOT.kBlack)
          hltRateLabel.SetTextAlign(12)
          hltRateLabel.SetTextFont(42)
          hltRateLabel.SetTextSize(0.0325)
          hltRateLabel.SetBorderSize(0)
          hltRateLabel.AddText('L1T+HLT Rate = {:4.1f} +/- {:4.1f} Hz (QCD + V+jets)'.format(hltRateVal, math.sqrt(hltRateErr2)))
          hltRateLabel.Draw('same')

          leg = ROOT.TLegend(0.65, 0.20, 0.95, 0.40)
          leg.SetNColumns(1)
          for _tmpGr in theEffys:
            leg.AddEntry(_tmpGr, _tmpGr.GetName(), 'lepx')
          leg.Draw('same')

          h0.SetTitle(_tmp['title'])
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

          canvas.SetLogy(_tmp['logY'])
          canvas.SetGrid(1, 1)

          for _tmpExt in _tmp['outputExts']:
            canvas.SaveAs(_tmp['outputName']+'.'+_tmpExt)

          canvas.Close()

          print '\033[1m'+_tmp['outputName']+'\033[0m'

    print '='*50
    print '='*50
    print '\033[1m'+'Rate Plots'+'\033[0m'
    print '='*50
    print '='*50

    for _tmp in [
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1'][L1T_SingleJet]['MB'],
        'hltTargetRateHz': 75,
        'outputName': outputDir+'/rate_SingleJet',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi Jet p_{T} Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':  400,
        'xmax':  550,
        'ymin':   11,
        'ymax':  299,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltAK4PFPuppiJet'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltAK4PFPuppiJet'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltAK4PFPuppiJet'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltAK4PFPuppiJet'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltAK4PFPuppiJet'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltAK4PFPuppiJet'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1'][L1T_HT]['MB'],
        'hltTargetRateHz': 75,
        'outputName': outputDir+'/rate_HT',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi H_{T} Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':  900,
        'xmax': 1400,
        'ymin':    2,
        'ymax':  299,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltPFPuppiHT'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltPFPuppiHT'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltPFPuppiHT'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltPFPuppiHT'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltPFPuppiHT'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltPFPuppiHT'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1']['L1T_PFPuppiMET200off']['MB'],
        'hltTargetRateHz': 225,
        'outputName': outputDir+'/rate_MET',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi MET Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':    0,
        'xmax':  260,
        'ymin':    2,
        'ymax': 2999,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltPFPuppiMET'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltPFPuppiMET'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltPFPuppiMET'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltPFPuppiMET'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltPFPuppiMET'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltPFPuppiMET'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
      {
        'l1tRateTuple': rateDict['HLT_TRKv06p1']['L1T_PFPuppiMET245off']['MB'],
        'hltTargetRateHz': 225,
        'outputName': outputDir+'/rate_MET2',
        'outputExts': EXTS,
        'title': ';HLT PF+Puppi MET Threshold [GeV];L1T+HLT Rate [Hz]',
        'objLabel': '',
        'topLabel': 'MC: QCD + V+jets',
        'xmin':    0,
        'xmax':  260,
        'ymin':    2,
        'ymax': 2999,
        'logY': 1,
        'histos': [
          {'histo': rateHistos['HLT_TRKv06p1']       ['hltPFPuppiMET2'], 'color': 1, 'lineStyle': 1, 'legName': 'TRK-v6.1 + simPF'  },
          {'histo': rateHistos['HLT_TRKv06p1_TICL']  ['hltPFPuppiMET2'], 'color': 2, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLold'},
          {'histo': rateHistos['HLT_TRKv06p1_TICLv2']['hltPFPuppiMET2'], 'color': 4, 'lineStyle': 1, 'legName': 'TRK-v6.1 + TICLnew'},
          {'histo': rateHistos['HLT_TRKv07p2']       ['hltPFPuppiMET2'], 'color': 1, 'lineStyle': 2, 'legName': 'TRK-v7.2 + simPF'  },
          {'histo': rateHistos['HLT_TRKv07p2_TICL']  ['hltPFPuppiMET2'], 'color': 2, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLold'},
          {'histo': rateHistos['HLT_TRKv07p2_TICLv2']['hltPFPuppiMET2'], 'color': 4, 'lineStyle': 2, 'legName': 'TRK-v7.2 + TICLnew'},
        ],
      },
    ]:
      canvasCount += 1
      canvasNamePostfix = '_'+str(canvasCount)

      theRates = []
      for _tmpIdx in range(len(_tmp['histos'])):
        h0 = _tmp['histos'][_tmpIdx]['histo']
        h0.SetMarkerSize(0.5)
        h0.SetLineWidth(2)
        h0.SetMarkerColor(_tmp['histos'][_tmpIdx]['color'])
        h0.SetLineColor(_tmp['histos'][_tmpIdx]['color'])
        h0.SetLineStyle(_tmp['histos'][_tmpIdx]['lineStyle'])
        h0.SetName(_tmp['histos'][_tmpIdx]['legName'])
        theRates += [h0]

      canvas = ROOT.TCanvas('c'+canvasNamePostfix, 'c'+canvasNamePostfix)
      canvas.cd()

      h0 = canvas.DrawFrame(_tmp['xmin'], _tmp['ymin'], _tmp['xmax'], _tmp['ymax'])

      for _tmp2 in theRates:
        if _tmp2 is not None:
          _tmp2.Draw('hist,e,same')

      topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
      topLabel.SetFillColor(0)
      topLabel.SetFillStyle(1001)
      topLabel.SetTextColor(ROOT.kBlack)
      topLabel.SetTextAlign(12)
      topLabel.SetTextFont(42)
      topLabel.SetTextSize(0.035)
      topLabel.SetBorderSize(0)
      topLabel.AddText(_tmp['topLabel'])
      topLabel.Draw('same')

      objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
      objLabel.SetFillColor(0)
      objLabel.SetFillStyle(1001)
      objLabel.SetTextColor(ROOT.kBlack)
      objLabel.SetTextAlign(32)
      objLabel.SetTextFont(42)
      objLabel.SetTextSize(0.035)
      objLabel.SetBorderSize(0)
      objLabel.AddText(_tmp['objLabel'])
      objLabel.Draw('same')

      l1tRateVal = _tmp['l1tRateTuple'][0]
      l1tRateErr = _tmp['l1tRateTuple'][1]

      l1tRateLabel = ROOT.TPaveText(0.50, 0.85, 0.94, 0.90, 'NDC')
      l1tRateLabel.SetFillColor(0)
      l1tRateLabel.SetFillStyle(1001)
      l1tRateLabel.SetTextColor(ROOT.kBlack)
      l1tRateLabel.SetTextAlign(12)
      l1tRateLabel.SetTextFont(42)
      l1tRateLabel.SetTextSize(0.0325)
      l1tRateLabel.SetBorderSize(0)
      l1tRateLabel.AddText('L1T Rate = {:4.1f} +/- {:4.1f} kHz (MB)'.format(l1tRateVal/1000., l1tRateErr/1000.))
      l1tRateLabel.Draw('same')

      hltTargetRateLine = ROOT.TLine(_tmp['xmin'], _tmp['hltTargetRateHz'], _tmp['xmax'], _tmp['hltTargetRateHz'])
      hltTargetRateLine.SetLineWidth(2)
      hltTargetRateLine.SetLineStyle(2)
      hltTargetRateLine.SetLineColor(ROOT.kViolet-1)
      hltTargetRateLine.Draw('same')

      hltTargetRateLabel = ROOT.TPaveText(0.50, 0.80, 0.94, 0.85, 'NDC')
      hltTargetRateLabel.SetFillColor(0)
      hltTargetRateLabel.SetFillStyle(1001)
      hltTargetRateLabel.SetTextColor(ROOT.kViolet-1)
      hltTargetRateLabel.SetTextAlign(32)
      hltTargetRateLabel.SetTextFont(42)
      hltTargetRateLabel.SetTextSize(0.0325)
      l1tRateLabel.SetBorderSize(0)
      hltTargetRateLabel.AddText('Target HLT Rate: '+str(_tmp['hltTargetRateHz'])+' Hz')
      hltTargetRateLabel.Draw('same')

      leg = ROOT.TLegend(0.165, 0.17, 0.50, 0.55)
      leg.SetNColumns(1)
      for _tmpRate in theRates:
        leg.AddEntry(_tmpRate, _tmpRate.GetName(), 'le')
      leg.Draw('same')

      h0.SetTitle(_tmp['title'])
      h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

      canvas.SetLogy(_tmp['logY'])
      canvas.SetGrid(1, 1)

      for _tmpExt in _tmp['outputExts']:
        canvas.SaveAs(_tmp['outputName']+'.'+_tmpExt)

      canvas.Close()

      print '\033[1m'+_tmp['outputName']+'\033[0m'

    print '='*50



for _tmp1 in sorted(rateDict.keys()):
  for _tmp2 in sorted(rateDict[_tmp1].keys()):
    aRate, aRateErr2 = 0., 0.
    for _tmp3 in QCDSamples+['Wln', 'Zll']:
      aRate += rateDict[_tmp1][_tmp2][_tmp3][0]
      aRateErr2 += math.pow(rateDict[_tmp1][_tmp2][_tmp3][1], 2)
    print _tmp1, '  ', _tmp2, aRate, math.sqrt(aRateErr2)

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
