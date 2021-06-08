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

#    _tmp_num = _tfile.Get('HLT_PFJet'+hltThreshold_SingleJet+'/offlineAK4PFJetsCorrected_EtaIncl_MatchedToHLT_pt')
#
#    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFJetsCorrected_EtaIncl_MatchedToHLT_pt')
#
#    ret['PF_SingleJet_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#    ret['PF_SingleJet_wrt_'+_tmpRef].SetName('PF_SingleJet_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getHTEfficiencies(fpath, hltThreshold_HT):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  # HT
  binEdges_HT = array.array('d', [50.*_tmpIdx for _tmpIdx in range(44+1)])

  for _tmpRef in _tmpRefs:

    _tmp_num = _tfile.Get('HLT_PFHT'+hltThreshold_HT+'/offlineAK4PFPuppiJetsCorrected_Eta2p5_HT')

    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFPuppiJetsCorrected_Eta2p5_HT')

    ret['Puppi_HT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['Puppi_HT_wrt_'+_tmpRef].SetName('Puppi_HT_wrt_'+_tmpRef)

#    _tmp_num = _tfile.Get('HLT_PFHT'+hltThreshold_HT+'/offlineAK4PFJetsCorrected_Eta2p5_HT')
#
#    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFJetsCorrected_Eta2p5_HT')
#
#    ret['PF_HT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
#    ret['PF_HT_wrt_'+_tmpRef].SetName('PF_HT_wrt_'+_tmpRef)

  _tfile.Close()

  return ret

def getMETEfficiencies(fpath, hltThreshold_MET):
  ret = {}

  _tfile = ROOT.TFile.Open(fpath)
  if not _tfile:
    WARNING('failed to open target TFile: '+fpath)
    return ret

  _tmpRefs = [
    'Offline',
  ]

  for _tmpRef in _tmpRefs:

    _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFPuppiMET_Raw_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFPuppiMET_Raw_pt')

    ret['PuppiMET_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PuppiMET_wrt_'+_tmpRef].SetName('PuppiMET_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFMET_Raw_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFMET_Raw_pt')

    ret['PFMET_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PFMET_wrt_'+_tmpRef].SetName('PFMET_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFMETTypeOne'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFPuppiMET_Type1_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFPuppiMET_Type1_pt')

    ret['PuppiMETTypeOne_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PuppiMETTypeOne_wrt_'+_tmpRef].SetName('PuppiMETTypeOne_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFMETTypeOne'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFMET_Type1_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFMET_Type1_pt')

    ret['PFMETTypeOne_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PFMETTypeOne_wrt_'+_tmpRef].SetName('PFMETTypeOne_wrt_'+_tmpRef)

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
    '07June',
  ]

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  for _tmpReco in recoKeys:
    print '='*110
    print '\033[1m'+_tmpReco+'\033[0m'
    print '='*110
    print '\033[1m'+'Efficiency Plots'+'\033[0m'
    print '='*110

    ## SingleJet
    effysJet = {}
    for _tmpPU in [
      'PU',
      'NoPU',
    ]:
      effysJet[_tmpPU] = {}
      for _tmpJetThresh in ['140', '320', '500']:
        effysJet[_tmpPU][_tmpJetThresh] = getJetEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Run3Winter20_QCD_PtFlat15to3000_14TeV_'+_tmpPU+'.root',
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
          effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(1)
          effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(1)
          effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(2)
          effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(2)
          effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(4)
          effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(4)
          effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')
        except: pass

        try:
          effysJet['NoPU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['NoPU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['NoPU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(1)
          effysJet['NoPU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(1)
          effysJet['NoPU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(2)
          effysJet['NoPU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['NoPU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['NoPU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['NoPU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(2)
          effysJet['NoPU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(2)
          effysJet['NoPU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(2)
          effysJet['NoPU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(4)
          effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(4)
          effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(2)
          effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')
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

        leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.44)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.040)
        leg1.SetEntrySeparation(0.4) 
        try:
          leg1.AddEntry(effysJet['PU']['140'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'HLT_PFJet140 ', 'lp')
          leg1.AddEntry(effysJet['PU']['320'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'HLT_PFJet320 ', 'lp')
          leg1.AddEntry(effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef], 'HLT_PFJet500 ', 'lp')
        except: pass
        leg1.Draw('same')

        try:
          _htmpPU140 = effysJet['PU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Clone()
          _htmpPU140.SetLineColor(1)
          _htmpPU140.SetLineStyle(2)
        except: pass

        try:
          _htmpPU200 = effysJet['NoPU']['500'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Clone()
          _htmpPU200.SetLineColor(1)
          _htmpPU200.SetLineStyle(1)
        except: pass

        leg2 = ROOT.TLegend(0.70, 0.46, 0.94, 0.61)
        leg2.SetNColumns(1)
        leg2.SetTextFont(42)
        leg2.SetTextSize(0.040)
        try:
          leg2.AddEntry(_htmpPU140, 'PU', 'l')
        except: pass
        try:
          leg2.AddEntry(_htmpPU200, 'NoPU', 'l')
        except: pass
        leg2.Draw('same')

        h0.SetTitle(';'+_tmpRef+' Jet p_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+'.'+_tmpExt)

        canvas.Close()

        print '\033[1m'+outputDir+'/triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+'\033[0m'

    ## HT
    effysHT = {}
    for _tmpPU in ['PU', 'NoPU']:
      effysHT[_tmpPU] = {}
      for _tmpHTThresh in ['780', '890', '1050']:
        effysHT[_tmpPU][_tmpHTThresh] = getHTEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Run3Winter20_QCD_PtFlat15to3000_14TeV_'+_tmpPU+'.root',
          hltThreshold_HT = _tmpHTThresh,
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

        h0 = canvas.DrawFrame(600, 0.0001, 2000, 1.19)

        try:
          effysHT['PU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT['PU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT['PU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(1)
          effysHT['PU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(1)
          effysHT['PU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT['PU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')

          effysHT['PU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT['PU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT['PU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(2)
          effysHT['PU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(2)
          effysHT['PU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT['PU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')
  
          effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(4)
          effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(4)
          effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')
  
        except: pass

        try:  
          effysHT['NoPU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT['NoPU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT['NoPU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(1)
          effysHT['NoPU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(1)
          effysHT['NoPU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(2)
          effysHT['NoPU']['780'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')

          effysHT['NoPU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT['NoPU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT['NoPU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(2)
          effysHT['NoPU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(2)
          effysHT['NoPU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(2)
          effysHT['NoPU']['890'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')
  
          effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(4)
          effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(4)
          effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(2)
          effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')
  
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

        leg1 = ROOT.TLegend(0.60, 0.20, 0.94, 0.44)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.040)
        leg1.SetEntrySeparation(0.4)
        try:
          leg1.AddEntry(effysHT['PU'][ '780'][_tmpType+'_HT_wrt_'+_tmpRef], 'HLT_PFHT780', 'lp')
          leg1.AddEntry(effysHT['PU'][ '890'][_tmpType+'_HT_wrt_'+_tmpRef], 'HLT_PFHT890', 'lp')
          leg1.AddEntry(effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef], 'HLT_PFHT1050', 'lp')
        except: pass
        leg1.Draw('same')

        leg2 = ROOT.TLegend(0.70, 0.46, 0.94, 0.61)
        leg2.SetNColumns(1)
        leg2.SetTextFont(42)
        leg2.SetTextSize(0.040)
        try:
          _htmpPU140 = effysHT['PU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].Clone()
          _htmpPU140.SetLineColor(1)
          _htmpPU140.SetLineStyle(2)
          leg2.AddEntry(_htmpPU140, 'PU', 'l')
        except: pass
        try:
          _htmpPU200 = effysHT['NoPU']['1050'][_tmpType+'_HT_wrt_'+_tmpRef].Clone()
          _htmpPU200.SetLineColor(1)
          _htmpPU200.SetLineStyle(1)
          leg2.AddEntry(_htmpPU200, 'NoPU', 'l')
        except: pass
        leg2.Draw('same')

        h0.SetTitle(';'+_tmpRef+' H_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+'_HT_wrt'+_tmpRef+'.'+_tmpExt)

        canvas.Close()

        print '\033[1m'+outputDir+'/triggerEff_'+_tmpType+'_HT_wrt'+_tmpRef+'\033[0m'

    ## MET
    effysMET = {}
    for _tmpPU in [
      'PU',
    ]:
      effysMET[_tmpPU] = {}
      for _tmpMETThresh in [
        '120',
        '140',
      ]:
        effysMET[_tmpPU][_tmpMETThresh] = getMETEfficiencies(
          fpath = inputDir+'/'+_tmpReco+'/Run3Winter20_VBF_HToInvisible_14TeV_'+_tmpPU+'.root',
          hltThreshold_MET = _tmpMETThresh,
        )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'PF',
        'Puppi',
      ]:

        for _tmpReco in [
          'MET',
          'METTypeOne',
        ]:

          # MET
          canvas = ROOT.TCanvas(tmpName(), tmpName(False))
          canvas.cd()
  
          h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)
  
          try:
            effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetMarkerColor(1)
            effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetLineColor(1)
            effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].Draw('lepz')
    
            effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetMarkerColor(2)
            effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetLineColor(2)
            effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef].Draw('lepz')
    
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

          if _tmpReco == 'MET':
            printlabel = 'Raw '+_tmpType
          else:
            printlabel = 'Type-1 '+_tmpType

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
            leg1.AddEntry(effysMET['PU']['120'][_tmpType+_tmpReco+'_wrt_'+_tmpRef], 'HLT_PF'+_tmpReco+'120_PFMHT120_IDTight', 'lp')
            leg1.AddEntry(effysMET['PU']['140'][_tmpType+_tmpReco+'_wrt_'+_tmpRef], 'HLT_PF'+_tmpReco+'140_PFMHT140_IDTight', 'lp')
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
 
