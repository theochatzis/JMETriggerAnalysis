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

def getJetEfficiencies(fpath, hltThreshold_SingleJet):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  # SingleJet
  binEdges_pT = array.array('d', [_tmp*20 for _tmp in range(35)] + [700+_tmp*50 for _tmp in range(6+1)])

  for _tmpRef in _tmpRefs:

    _tmp_num = _tfile.Get('HLT_PFJet'+hltThreshold_SingleJet+'/offlineAK4PFPuppiJetsCorrected_EtaIncl_MatchedToHLT_pt')

    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFPuppiJetsCorrected_EtaIncl_MatchedToHLT_pt')

    ret['Puppi_SingleJet_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['Puppi_SingleJet_wrt_'+_tmpRef].SetName('Puppi_SingleJet_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFJet'+hltThreshold_SingleJet+'/offlineAK4PFCHSJetsCorrected_EtaIncl_MatchedToHLT_pt')

    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFCHSJetsCorrected_EtaIncl_MatchedToHLT_pt')

    ret['PF_SingleJet_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PF_SingleJet_wrt_'+_tmpRef].SetName('PF_SingleJet_wrt_'+_tmpRef)

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

  parser.add_argument('--no-qcd-weighted', dest='no_qcd_weighted', action='store_true',
                      help='input histograms do not include weights for MB+QCD merging')

  parser.add_argument('--minCountsForValidRate', dest='minCountsForValidRate', action='store', type=float, default=-1.0,
                      help='minimum number of counts to consider a sample valid for trigger rate estimates')

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

#  ROOT.TH1.AddDirectory(False)

  theStyle = get_style(0)
  theStyle.cd()

  EXTS = list(set(opts.exts))

  ### args validation ---

  inputDir = opts.inputDir

#  recoKeys = [
#    '30Nov_OldJEC_GRun',
#    '30Nov_OldJEC_Run3TRK'
#  ]

  tmpPUs = [
    'PU',
#    'NoPU',
  ]

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

#  for _tmpReco in recoKeys:
  for _tmpPU in tmpPUs:
    print ('='*110)
#    print '\033[1m'+_tmpReco+'\033[0m'
    print ('='*110)
    print ('\033[1m'+'Efficiency Plots'+'\033[0m')
    print ('='*110)

    recoKeys = [
      'GRun',
      'Run3TRK'
    ]

    ## SingleJet
    effysJet = {}
    for _tmpReco in recoKeys:
      effysJet[_tmpReco] = {}
      for _tmpJetThresh in ['140', '320', '500']:
        effysJet[_tmpReco][_tmpJetThresh] = getJetEfficiencies(
          fpath = inputDir+_tmpReco+'/harvesting/outputs/Run3Winter21_QCD_PtFlat15to7000_14TeV_'+_tmpPU+'.root',
          hltThreshold_SingleJet = _tmpJetThresh,
        )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'PF',
        'Puppi',
      ]:

        canvas = ROOT.TCanvas(tmpName(), tmpName(False))
        canvas.cd()

        h0 = canvas.DrawFrame(100, 0.0001, 1000, 1.19)

        try:
          effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(1)
          effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(1)
          effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(2)
          effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(2)
          effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(4)
          effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(4)
          effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')
        except: pass

        try:
          effysJet['Run3TRK']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['Run3TRK']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['Run3TRK']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(1)
          effysJet['Run3TRK']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(1)
          effysJet['Run3TRK']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(2)
          effysJet['Run3TRK']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['Run3TRK']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['Run3TRK']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['Run3TRK']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(2)
          effysJet['Run3TRK']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(2)
          effysJet['Run3TRK']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(2)
          effysJet['Run3TRK']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(4)
          effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(4)
          effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(2)
          effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')
        except: pass

        topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
        topLabel.SetFillColor(0)
        topLabel.SetFillStyle(1001)
        topLabel.SetTextColor(ROOT.kBlack)
        topLabel.SetTextAlign(12)
        topLabel.SetTextFont(42)
        topLabel.SetTextSize(0.035)
        topLabel.SetBorderSize(0)
        topLabel.AddText('#font[61]{CMS} #font[52]{Run-3 Simulation}')
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

        l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.70, 0.88, 'NDC')
        l1tRateLabel.SetFillColor(0)
        l1tRateLabel.SetFillStyle(1001)
        l1tRateLabel.SetTextColor(ROOT.kBlack)
        l1tRateLabel.SetTextAlign(12)
        l1tRateLabel.SetTextFont(42)
        l1tRateLabel.SetTextSize(0.035)
        l1tRateLabel.SetBorderSize(0)
        l1tRateLabel.AddText('Offline Jet |#eta| < 5.0')
        l1tRateLabel.Draw('same')

        leg1 = ROOT.TLegend(0.55, 0.20, 0.94, 0.44)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.040)
        leg1.SetEntrySeparation(0.4) 
        try:
          leg1.AddEntry(effysJet['GRun']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'HLT_PFJet140 ', 'lp')
          leg1.AddEntry(effysJet['GRun']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'HLT_PFJet320 ', 'lp')
          leg1.AddEntry(effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'HLT_PFJet500 ', 'lp')
        except: pass
        leg1.Draw('same')

        try:
          _htmpPU140 = effysJet['GRun']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Clone()
          _htmpPU140.SetLineColor(1)
          _htmpPU140.SetLineStyle(2)
        except: pass

        try:
          _htmpPU200 = effysJet['Run3TRK']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Clone()
          _htmpPU200.SetLineColor(1)
          _htmpPU200.SetLineStyle(1)
        except: pass

        leg2 = ROOT.TLegend(0.60, 0.46, 0.94, 0.61)
        leg2.SetNColumns(1)
        leg2.SetTextFont(42)
        leg2.SetTextSize(0.040)
        try:
          leg2.AddEntry(_htmpPU140, 'GRun', 'l')
        except: pass
        try:
          leg2.AddEntry(_htmpPU200, 'Run-3 TRK', 'l')
        except: pass
        leg2.Draw('same')

        h0.SetTitle(';'+_tmpRef+' Jet p_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/TRK_triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+_tmpPU+'.'+_tmpExt)

        canvas.Close()

        print ('\033[1m'+outputDir+'/TRK_triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+_tmpPU+'\033[0m')

