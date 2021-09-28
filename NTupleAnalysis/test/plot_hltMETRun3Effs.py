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


def getMETEfficiencies(fpath, hltThreshold_MET):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  _metTypes = [
    'PFMET_Raw',
    'PFPuppiMET_Raw',
    'PFMET_Type1',
    'PFPuppiMET_Type1',
  ]

  for _tmpRef in _tmpRefs:

    for _metType in _metTypes:

      _hltType = 'HLT'
      if _metType == 'PFMET_Type1' or _metType == 'PFPuppiMET_Type1':
        _hltType == 'HLT_TypeOne'

      _tmp_num = _tfile.Get('PU0to20_'+_hltType+'/offline'+_metType+'_pt')
      _tmp_den = _tfile.Get('PU0to20/offline'+_metType+'_pt')
  
      ret['PU0to20_'+_metType+'_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
      ret['PU0to20_'+_metType+'_wrt_'+_tmpRef].SetName('PU0to20_'+_metType+'_wrt_'+_tmpRef)    
  
      _tmp_num = _tfile.Get('PU20to40_'+_hltType+'/offline'+_metType+'_pt')
      _tmp_den = _tfile.Get('PU20to40/offline'+_metType+'_pt')
  
      ret['PU20to40_'+_metType+'_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
      ret['PU20to40_'+_metType+'_wrt_'+_tmpRef].SetName('PU20to40_'+_metType+'_wrt_'+_tmpRef)
  
      _tmp_num = _tfile.Get('PUgt40_'+_hltType+'/offline'+_metType+'_pt')
      _tmp_den = _tfile.Get('PUgt40/offline'+_metType+'_pt')
  
      ret['PUgt40_'+_metType+'_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
      ret['PUgt40_'+_metType+'_wrt_'+_tmpRef].SetName('PUgt40_'+_metType+'_wrt_'+_tmpRef)


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

  recoKeys = [
    '25June_withoutThreshold',
  ]

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  for _tmpReco in recoKeys:
    print '='*110
    print '\033[1m'+_tmpReco+'\033[0m'
    print '='*110
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*110


    ## MET
    effysMET = {}
    for _tmpPU in [
      'PU',
    ]:
      effysMET[_tmpPU] = {}
      for _tmpMETThresh in [
        '0to20',
        '20to40',
        'gt40',
      ]:
        effysMET[_tmpPU][_tmpMETThresh] = getMETEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Run3Winter20_VBF_HToInvisible_14TeV_'+_tmpPU+'.root',
          hltThreshold_MET = _tmpMETThresh,
        )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'PFMET',
        'PFPuppiMET',
      ]:

        for _tmpReco in [
          'Raw',
          'Type1',
        ]:

          # MET
          canvas = ROOT.TCanvas(tmpName(), tmpName(False))
          canvas.cd()
  
          h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)
  
          try:
            effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetMarkerColor(1)
            effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineColor(1)
            effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].Draw('lepz')
    
            effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetMarkerColor(2)
            effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineColor(2)
            effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].Draw('lepz')

            effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetMarkerColor(3)
            effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineColor(3)
            effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef].Draw('lepz')
    
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

          if _tmpReco == 'Raw' and _tmpType == "PFMET":
            printlabel = 'Raw PF, HLT_PFMET120_PFMHT120_IDTight'
          if _tmpReco == 'Raw' and _tmpType == "PFPuppiMET":
            printlabel = 'Raw Puppi, HLT_PFMET120_PFMHT120_IDTight'
          if _tmpReco == 'Type1' and _tmpType == "PFMET":
            printlabel = 'Type-1 PF, HLT_PFMETTypeOne120_PFMHT120_IDTight'
          if _tmpReco == 'Type1' and _tmpType == "PFPuppiMET":
            printlabel = 'Type-1 Puppi, HLT_PFMETTypeOne120_PFMHT120_IDTight'

          l1tRateLabel = ROOT.TPaveText(0.165, 0.82, 0.70, 0.88, 'NDC')
          l1tRateLabel.SetFillColor(0)
          l1tRateLabel.SetFillStyle(1001)
          l1tRateLabel.SetTextColor(ROOT.kBlack)
          l1tRateLabel.SetTextAlign(12)
          l1tRateLabel.SetTextFont(42)
          l1tRateLabel.SetTextSize(0.035)
          l1tRateLabel.SetBorderSize(0)
          l1tRateLabel.AddText(printlabel)
          l1tRateLabel.Draw('same')
  
          leg1 = ROOT.TLegend(0.45, 0.20, 0.94, 0.44)
          leg1.SetNColumns(1)
          leg1.SetTextFont(42)
          try:
            leg1.AddEntry(effysMET['PU']['0to20']['PU0to20_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef], 'PU 0-20', 'lp')
            leg1.AddEntry(effysMET['PU']['20to40']['PU20to40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef], 'PU 20-40', 'lp')
            leg1.AddEntry(effysMET['PU']['gt40']['PUgt40_'+_tmpType+'_'+_tmpReco+'_wrt_'+_tmpRef], 'PU > 40', 'lp')
          except: pass
          leg1.Draw('same')
  
          h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
  
          canvas.SetLogy(0)
          canvas.SetGrid(1, 1)
  
          for _tmpExt in EXTS:
            canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+_tmpReco+'_wrt'+_tmpRef+'.'+_tmpExt)
  
          canvas.Close()
  
          print '\033[1m'+outputDir+'/triggerEff_'+_tmpType+_tmpReco+'_wrt'+_tmpRef+'\033[0m'
 
