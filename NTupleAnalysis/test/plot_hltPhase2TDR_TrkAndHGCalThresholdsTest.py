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

def getHistogram(tfile, key):
  h0 = tfile.Get(key)
  if not h0:
    return None

  hret = h0.Clone()
  hret.SetDirectory(0)
  hret.UseCurrentStyle()

  return hret

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

  parser.add_argument('-e', '--exts', dest='exts', nargs='+', default=['pdf', 'png', 'C', 'root'],
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

  theStyle = get_style(0)
  theStyle.cd()

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir

  recoKeys = [
    'HLT_TRKv06p1_TICL',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p00',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p25',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p50',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p75',
    'HLT_75e33_TrkAndHGCalThresholdsTest_2p00',
  ]

  recoLabels = {
    'HLT_TRKv06p1_TICL': 'HLT (TDR)',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p00': 'HLT (F=1.00)',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p25': 'HLT (F=1.25)',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p50': 'HLT (F=1.50)',
    'HLT_75e33_TrkAndHGCalThresholdsTest_1p75': 'HLT (F=1.75)',
    'HLT_75e33_TrkAndHGCalThresholdsTest_2p00': 'HLT (F=2.00)',
  }

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  print '='*50
  print '='*50
  print '\033[1m'+'Efficiency Plots'+'\033[0m'
  print '='*50
  print '='*50

  ## MET
  effysMET_vbfh = {}
  for _tmpPU in [
    'NoPU',
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
      effysMET_vbfh[_tmpPU][_tmpMETThresh] = {}
      for _tmpReco in recoKeys:
        effysMET_vbfh[_tmpPU][_tmpMETThresh][_tmpReco] = getMETEfficiencies(**{
          'fpath': inputDir+'/'+_tmpReco+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_'+_tmpPU+'.root',
          'hltThreshold_MET': float(_tmpMETThresh),
          'hltThreshold_METTypeOne': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT20': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT30': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT40': float(_tmpMETThresh),
          'hltThreshold_METTypeOneMHT50': float(_tmpMETThresh),
        })

  for _tmpRef in [
    'GEN',
#    'Offline',
  ]:
    for (_tmpMC, effysMET) in [('VBFHToInv', effysMET_vbfh)]:
        # METTypeOne (+MHT)
        for _tmpPU in [
          'NoPU',
          'PU140',
          'PU200',
        ]:
          for _tmpMET in [
            'MET',
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
              for _tmpTrgType in [
                'HLT',
                'L1TpHLT',
              ]:
                canvas = ROOT.TCanvas(tmpName(), tmpName(False))
                canvas.cd()

                h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)

                try:
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_TRKv06p1_TICL'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerSize(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_TRKv06p1_TICL'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineWidth(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_TRKv06p1_TICL'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kGray)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_TRKv06p1_TICL'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineColor(ROOT.kGray)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_TRKv06p1_TICL'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineStyle(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_TRKv06p1_TICL'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].Draw('lepz')
  
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerSize(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineWidth(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kGreen+1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineColor(ROOT.kGreen+1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineStyle(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].Draw('lepz')
  
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p25'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerSize(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p25'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineWidth(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p25'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlue)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p25'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlue)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p25'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineStyle(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p25'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].Draw('lepz')
  
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p50'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerSize(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p50'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineWidth(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p50'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kViolet)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p50'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineColor(ROOT.kViolet)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p50'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineStyle(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p50'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].Draw('lepz')
  
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p75'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerSize(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p75'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineWidth(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p75'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kBlack)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p75'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineColor(ROOT.kBlack)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p75'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineStyle(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_1p75'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].Draw('lepz')
  
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_2p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerSize(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_2p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineWidth(2)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_2p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetMarkerColor(ROOT.kRed)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_2p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineColor(ROOT.kRed)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_2p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].SetLineStyle(1)
                  effysMET[_tmpPU][_tmpHLTthr]['HLT_75e33_TrkAndHGCalThresholdsTest_2p00'][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef].Draw('lepz')
                except: pass

                topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
                topLabel.SetFillColor(0)
                topLabel.SetFillStyle(1001)
                topLabel.SetTextColor(ROOT.kBlack)
                topLabel.SetTextAlign(12)
                topLabel.SetTextFont(42)
                topLabel.SetTextSize(0.035)
                topLabel.SetBorderSize(0)
                topLabel.AddText('#font[52]{Phase-2 Simulation}')#('#font[61]{CMS} #font[52]{Phase-2 Simulation}')
                topLabel.Draw('same')

                objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
                objLabel.SetFillColor(0)
                objLabel.SetFillStyle(1001)
                objLabel.SetTextColor(ROOT.kBlack)
                objLabel.SetTextAlign(32)
                objLabel.SetTextFont(42)
                objLabel.SetTextSize(0.035)
                objLabel.SetBorderSize(0)
                objLabel.AddText(_tmpPU+' (14 TeV)')
                objLabel.Draw('same')

                if 'MHT' in _tmpMET:
                  l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.92, 0.88, 'NDC')
                  l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss} & MHT > '+_tmpHLTthr+' GeV')
                elif 'TypeOne' in _tmpMET:
                  l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
                  l1tRateLabel.AddText('HLT : PF+PUPPI Type-1 p_{T}^{miss} > '+_tmpHLTthr+' GeV')
                else:
                  l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.65, 0.88, 'NDC')
                  l1tRateLabel.AddText('HLT : PF+PUPPI Raw p_{T}^{miss} > '+_tmpHLTthr+' GeV')
                l1tRateLabel.SetFillColor(0)
                l1tRateLabel.SetFillStyle(1001)
                l1tRateLabel.SetTextColor(ROOT.kBlack)
                l1tRateLabel.SetTextAlign(12)
                l1tRateLabel.SetTextFont(42)
                l1tRateLabel.SetTextSize(0.035)
                l1tRateLabel.SetBorderSize(0)
                l1tRateLabel.Draw('same')

                outputFileName = outputDir+'/triggerEff_'+_tmpTrgType+'_'+_tmpMET+'_wrt'+_tmpRef+'_'+_tmpPU+'_'+_tmpHLTthr+'_'+_tmpMC

                leg1 = ROOT.TLegend(0.70, 0.20, 0.94, 0.55)
                leg1.SetNColumns(1)
                leg1.SetTextFont(42)
                try:
                  for _tmpReco in recoKeys:
                    leg1.AddEntry(effysMET[_tmpPU][_tmpHLTthr][_tmpReco][_tmpMET+'_'+_tmpTrgType+'_wrt_'+_tmpRef], recoLabels[_tmpReco], 'lepx')
                except:
                  print 'error in TLegend of '+outputFileName

                leg1.Draw('same')

                h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
                h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

                canvas.SetLogy(0)
                canvas.SetGrid(1, 1)

                for _tmpExt in EXTS:
                  canvas.SaveAs(outputFileName+'.'+_tmpExt)

                canvas.Close()

                print '\033[1m'+outputFileName+'\033[0m'
