#!/usr/bin/env python3
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

    _tmp_num = _tfile.Get('HLT_PFHT'+hltThreshold_HT+'/offlineAK4PFCHSJetsCorrected_Eta2p5_HT')

    _tmp_den = _tfile.Get('NoSelection/offlineAK4PFCHSJetsCorrected_Eta2p5_HT')

    ret['PF_HT_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PF_HT_wrt_'+_tmpRef].SetName('PF_HT_wrt_'+_tmpRef)

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

#    _tmp_num = _tfile.Get('20to40_HLT/offlinePFPuppiMET_Raw_pt')
#    _tmp_den = _tfile.Get('20to40/offlinePFPuppiMET_Raw_pt')

    ret['PuppiMET_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PuppiMET_wrt_'+_tmpRef].SetName('PuppiMET_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFMET'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFMET_Raw_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFMET_Raw_pt')

#    _tmp_num = _tfile.Get('20to40_HLT/offlinePFMET_Raw_pt')
#    _tmp_den = _tfile.Get('20to40/offlinePFMET_Raw_pt')

    ret['PFMET_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PFMET_wrt_'+_tmpRef].SetName('PFMET_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFMETTypeOne'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFPuppiMET_Type1_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFPuppiMET_Type1_pt')

#    _tmp_num = _tfile.Get('20to40_HLT_TypeOne/offlinePFPuppiMET_Raw_pt')
#    _tmp_den = _tfile.Get('20to40/offlinePFPuppiMET_Raw_pt')

    ret['PuppiMETTypeOne_wrt_'+_tmpRef] = get_efficiency_graph(_tmp_num, _tmp_den)
    ret['PuppiMETTypeOne_wrt_'+_tmpRef].SetName('PuppiMETTypeOne_wrt_'+_tmpRef)

    _tmp_num = _tfile.Get('HLT_PFMETTypeOne'+hltThreshold_MET+'_PFMHT'+hltThreshold_MET+'_IDTight'+'/offlinePFMET_Type1_pt')

    _tmp_den = _tfile.Get('NoSelection/offlinePFMET_Type1_pt')

#    _tmp_num = _tfile.Get('20to40_HLT_TypeOne/offlinePFMET_Raw_pt')
#    _tmp_den = _tfile.Get('20to40/offlinePFMET_Raw_pt')

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

  outputDir = opts.output
  MKDIRP(opts.output, verbose = (opts.verbosity > 0), dry_run = opts.dry_run)

  ## SingleJet

  for _tmpJetThresh in ['140', '320', '500']:
    print ('='*110)
    print ('\033[1m'+_tmpJetThresh+'\033[0m')
    print ('='*110)
    print ('\033[1m'+'Jet Efficiency Plots'+'\033[0m')
    print ('='*110)

    effysJet = {}

    effysJet[_tmpJetThresh] = {}

    for _tmpReco in ['12_2_0_pre2', '12_3_0_pre6', '12_3_0_pre6_HBHE']:
      effysJet[_tmpJetThresh][_tmpReco] = getJetEfficiencies(
        fpath = inputDir+'/'+_tmpReco+'/QCD_Pt15to7000_TuneCP5_14TeV-pythia8.root',
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
          effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(1)
          effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(1)
          effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(2)
          effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(2)
          effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')

          effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerSize(1)
          effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineWidth(2)
          effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetMarkerColor(4)
          effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineColor(4)
          effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef].SetLineStyle(1)
          effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef].Draw('lepz')
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
        l1tRateLabel.AddText('SingleJet'+_tmpJetThresh)
        l1tRateLabel.Draw('same')

        leg1 = ROOT.TLegend(0.55, 0.20, 0.84, 0.44)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.035)
        leg1.SetEntrySeparation(0.4) 

        try:
          leg1.AddEntry(effysJet[_tmpJetThresh]['12_2_0_pre2'][_tmpType+'_SingleJet_wrt_'+_tmpRef], '12_2_0_pre2', 'lp')
          leg1.AddEntry(effysJet[_tmpJetThresh]['12_3_0_pre6'][_tmpType+'_SingleJet_wrt_'+_tmpRef], '12_3_0_pre6', 'lp')
          leg1.AddEntry(effysJet[_tmpJetThresh]['12_3_0_pre6_HBHE'][_tmpType+'_SingleJet_wrt_'+_tmpRef], '12_3_0_pre6+HBHE', 'lp')
        except: pass
        leg1.Draw('same')

        h0.SetTitle(';'+_tmpRef+' Jet p_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+'_'+_tmpJetThresh+'.'+_tmpExt)

        canvas.Close()

        print ('\033[1m'+outputDir+'/triggerEff_'+_tmpType+'_SingleJet_wrt'+_tmpRef+'_'+_tmpJetThresh+'\033[0m')     
    

  ## HT
  for _tmpHTThresh in ['780', '890', '1050']:
    print ('='*110)
    print ('\033[1m'+_tmpHTThresh+'\033[0m')
    print ('='*110)
    print ('\033[1m'+'HT Efficiency Plots'+'\033[0m')
    print ('='*110)

    effysHT = {}

    effysHT[_tmpHTThresh] = {}

    for _tmpReco in ['12_2_0_pre2', '12_3_0_pre6', '12_3_0_pre6_HBHE']:
      effysHT[_tmpHTThresh][_tmpReco] = getHTEfficiencies(
        fpath = inputDir+'/'+_tmpReco+'/QCD_Pt15to7000_TuneCP5_14TeV-pythia8.root',
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
          effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(1)
          effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(1)
          effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')

          effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(2)
          effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(2)
          effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')
  
          effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerSize(1)
          effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineWidth(2)
          effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef].SetMarkerColor(4)
          effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineColor(4)
          effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef].SetLineStyle(1)
          effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef].Draw('lepz')
  
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
        l1tRateLabel.AddText('HT'+_tmpHTThresh)
        l1tRateLabel.Draw('same')

        leg1 = ROOT.TLegend(0.55, 0.20, 0.84, 0.44)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.035)
        leg1.SetEntrySeparation(0.4)
        try:
          leg1.AddEntry(effysHT[_tmpHTThresh]['12_2_0_pre2'][_tmpType+'_HT_wrt_'+_tmpRef], '12_2_0_pre2', 'lp')
          leg1.AddEntry(effysHT[_tmpHTThresh]['12_3_0_pre6'][_tmpType+'_HT_wrt_'+_tmpRef], '12_3_0_pre6', 'lp')
          leg1.AddEntry(effysHT[_tmpHTThresh]['12_3_0_pre6_HBHE'][_tmpType+'_HT_wrt_'+_tmpRef], '12_3_0_pre6+HBHE', 'lp')
        except: pass
        leg1.Draw('same')

        h0.SetTitle(';'+_tmpRef+' H_{T} [GeV];Efficiency')
        h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        for _tmpExt in EXTS:
          canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+'_HT_wrt'+_tmpRef+'_'+_tmpHTThresh+'.'+_tmpExt)

        canvas.Close()

        print ('\033[1m'+outputDir+'/triggerEff_'+_tmpType+'_HT_wrt'+_tmpRef+'_'+_tmpHTThresh+'\033[0m')


  ## MET

  for _tmpMETThresh in ['120', '140']:
    print ('='*110)
    print ('\033[1m'+_tmpMETThresh+'\033[0m')
    print ('='*110)
    print ('\033[1m'+'MET Efficiency Plots'+'\033[0m')
    print ('='*110)

    effysMET = {}

    effysMET[_tmpMETThresh] = {}

    for _tmpReco in ['12_2_0_pre2', '12_3_0_pre6', '12_3_0_pre6_HBHE']:
      effysMET[_tmpMETThresh][_tmpReco] = getMETEfficiencies(
        fpath = inputDir+'/'+_tmpReco+'/VBFHToInvisible_M125_TuneCP5_14TeV-powheg-pythia8.root',
          hltThreshold_MET = _tmpMETThresh,
      )

    for _tmpRef in [
      'Offline',
    ]:

      for _tmpType in [
        'PF',
        'Puppi',
      ]:

        for _tmpAlgo in [
          'MET',
          'METTypeOne',
        ]:

          # MET
          canvas = ROOT.TCanvas(tmpName(), tmpName(False))
          canvas.cd()
  
          h0 = canvas.DrawFrame(0, 0.0001, 500, 1.19)
  
          try:
            effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerColor(1)
            effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineColor(1)
            effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].Draw('lepz')
    
            effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerColor(2)
            effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineColor(2)
            effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].Draw('lepz')

            effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerSize(1)
            effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineWidth(2)
            effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetMarkerColor(4)
            effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineColor(4)
            effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].SetLineStyle(1)
            effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef].Draw('lepz')
    
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
          l1tRateLabel.AddText('HLT_PF'+_tmpAlgo+_tmpMETThresh+'_PFMHT'+_tmpMETThresh+'_IDTight')
          l1tRateLabel.Draw('same')

          leg1 = ROOT.TLegend(0.55, 0.20, 0.84, 0.44)
          leg1.SetNColumns(1)
          leg1.SetTextFont(42)
          leg1.SetTextSize(0.035)
          leg1.SetEntrySeparation(0.4)
          try:
            leg1.AddEntry(effysMET[_tmpMETThresh]['12_2_0_pre2'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef], '12_2_0_pre2', 'lp')
            leg1.AddEntry(effysMET[_tmpMETThresh]['12_3_0_pre6'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef], '12_3_0_pre6', 'lp')
            leg1.AddEntry(effysMET[_tmpMETThresh]['12_3_0_pre6_HBHE'][_tmpType+_tmpAlgo+'_wrt_'+_tmpRef], '12_3_0_pre6+HBHE', 'lp')
          except: pass
          leg1.Draw('same')
  
          h0.SetTitle(';'+_tmpRef+' p_{T}^{miss} [GeV];Efficiency')
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
  
          canvas.SetLogy(0)
          canvas.SetGrid(1, 1)
  
          for _tmpExt in EXTS:
            canvas.SaveAs(outputDir+'/triggerEff_'+_tmpType+_tmpAlgo+'_wrt'+_tmpRef+'_'+_tmpMETThresh+'.'+_tmpExt)
  
          canvas.Close()
  
          print ('\033[1m'+outputDir+'/triggerEff_'+_tmpType+_tmpAlgo+'_wrt'+_tmpRef+'_'+_tmpMETThresh+'\033[0m')
 
