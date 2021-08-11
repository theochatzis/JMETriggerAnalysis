#!/usr/bin/env python
import ROOT

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
  if not h0: return None
  hret = h0.Clone()
  hret.SetDirectory(0)
  hret.UseCurrentStyle()
  return hret

if __name__ == '__main__':

  ROOT.gROOT.SetBatch()

  theStyle = get_style(0)
  theStyle.cd()

  exts = [
    'pdf',
    'png',
    'root',
  ]

  fileDict = {
    'NoPU' : 'output_hltPhase2_210427_HFtestCalo/harvesting/HLT_TRKv06p1_TICL/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_NoPU.root',
    'PU140': 'output_hltPhase2_210427_HFtestCalo/harvesting/HLT_TRKv06p1_TICL/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU140.root',
    'PU200': 'output_hltPhase2_210427_HFtestCalo/harvesting/HLT_TRKv06p1_TICL/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root',
  }

#  binEdges = {
#    'HB': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
#    'HGCal': [30, 40, 50, 60, 80, 100, 120, 140, 160, 200, 250, 300, 350, 400, 500, 600],
#    'HF': [30, 40, 50, 60, 80, 120, 240, 600],
#    'HF1': [30, 40, 50, 60, 80, 120, 240, 600],
#    'HF2': [30, 40, 50, 60, 80, 120, 240, 600],
#  }

  etaLabels = {
    'EtaIncl': '|#eta| < 5.0',
    'HB': '|#eta| < 1.5',
    'HGCal': '1.5 < |#eta| < 3.0',
    'HF' : '3.0 < |#eta| < 5.0',
    'HF1': '3.0 < |#eta| < 4.0',
    'HF2': '4.0 < |#eta| < 5.0',
    'HF3': '3.0 < |#eta| < 3.2',
    'HF4': '3.2 < |#eta| < 5.0',
  }

  for _jetTag in [
    'l1tSlwPFPuppiJetsCorrected',
    'hltAK4CaloJets',
    'hltAK4PFJets',
    'hltAK4PFPuppiJets',
    'hltAK4PFPuppiJetsCorrected',
  ]:
    for _etaTag in [
      'HB',
      'HGCal',
      'HF',
      'HF1',
      'HF2',
      'HF3',
      'HF4',
    ]:
      for _fomTag in [
        'Mean',
        'RMSOverMean',
      ]:
        graphs = {}
        for _fileTag in fileDict:
          _tmpTFile = ROOT.TFile.Open(fileDict[_fileTag])

          if not _tmpTFile:
            WARNING('failed to open target TFile: '+_tmpFilePath)
            continue

          graphs[_fileTag] = getHistogram(_tmpTFile, 'NoSelection/'+_jetTag+'_'+_etaTag+'_MatchedToGEN_pt_overGEN_'+_fomTag+'_wrt_GEN_pt')
          if graphs[_fileTag] is not None:
            graphs[_fileTag].UseCurrentStyle()

        if len([_tmp for _tmp in graphs if graphs[_tmp] is not None]) == 0: continue

        canvas = ROOT.TCanvas(tmpName(), tmpName(False))
        canvas.cd()

        if _fomTag == 'RMSOverMean':
          h0 = canvas.DrawFrame(30., 0.0001, 800., 0.8)
        elif _fomTag == 'Mean':
          h0 = canvas.DrawFrame(30., 0.0001, 800., 2)

        gNoPU = graphs['NoPU']
        gPU140 = graphs['PU140']
        gPU200 = graphs['PU200']

        try:
          gNoPU.SetMarkerStyle(20)
          gNoPU.SetMarkerSize(1)
          gNoPU.SetLineWidth(2)
          gNoPU.SetLineStyle(1)
          gNoPU.SetLineColor(1)
          gNoPU.SetMarkerColor(1)
          gNoPU.Draw('ep,same')
        except: pass

        try:
          gPU140.SetMarkerStyle(21)
          gPU140.SetMarkerSize(1)
          gPU140.SetLineWidth(2)
          gPU140.SetLineStyle(1)
          gPU140.SetLineColor(2)
          gPU140.SetMarkerColor(2)
          gPU140.Draw('ep,same')
        except: pass

        try:
          gPU200.SetMarkerStyle(21)
          gPU200.SetMarkerSize(1)
          gPU200.SetLineWidth(2)
          gPU200.SetLineStyle(1)
          gPU200.SetLineColor(4)
          gPU200.SetMarkerColor(4)
          gPU200.Draw('ep,same')
        except: pass

        topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
        topLabel.SetFillColor(0)
        topLabel.SetFillStyle(1001)
        topLabel.SetTextColor(ROOT.kBlack)
        topLabel.SetTextAlign(12)
        topLabel.SetTextFont(42)
        topLabel.SetTextSize(0.035)
        topLabel.SetBorderSize(0)
        topLabel.AddText(_jetTag)
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

        l1tRateLabel = ROOT.TPaveText(0.74, 0.80, 0.94, 0.85, 'NDC')
        l1tRateLabel.SetFillColor(0)
        l1tRateLabel.SetFillStyle(1001)
        l1tRateLabel.SetTextColor(ROOT.kBlack)
        l1tRateLabel.SetTextAlign(12)
        l1tRateLabel.SetTextFont(42)
        l1tRateLabel.SetTextSize(0.035)
        l1tRateLabel.SetBorderSize(0)
        l1tRateLabel.AddText(etaLabels[_etaTag])
        l1tRateLabel.Draw('same')

        hltRateLabel = ROOT.TPaveText(0.74, 0.85, 0.94, 0.90, 'NDC')
        hltRateLabel.SetFillColor(0)
        hltRateLabel.SetFillStyle(1001)
        hltRateLabel.SetTextColor(ROOT.kBlack)
        hltRateLabel.SetTextAlign(12)
        hltRateLabel.SetTextFont(42)
        hltRateLabel.SetTextSize(0.035)
        hltRateLabel.SetBorderSize(0)
        hltRateLabel.AddText('p_{T}^{HLT} > 30 GeV')
        hltRateLabel.Draw('same')

        hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
        hltTargetRateLine.SetLineWidth(2)
        hltTargetRateLine.SetLineStyle(2)
        hltTargetRateLine.SetLineColor(ROOT.kGray)
#        hltTargetRateLine.Draw('same')

        leg1 = ROOT.TLegend(0.74, 0.55, 0.94, 0.80)
        leg1.SetNColumns(1)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.040)
        try: leg1.AddEntry(gNoPU, 'NoPU', 'l')
        except: pass
        try: leg1.AddEntry(gPU140, 'PU140', 'l')
        except: pass
        try: leg1.AddEntry(gPU200, 'PU200', 'l')
        except: pass
        leg1.Draw('same')

        if _fomTag == 'RMSOverMean':
          h0.SetTitle(';GEN Jet p_{T} [GeV];Jet Response RMS/Mean')
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
        elif _fomTag == 'Mean':
          h0.SetTitle(';GEN Jet p_{T} [GeV];Jet Response Mean')
          h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)

        canvas.SetLogx(1)
        canvas.SetLogy(0)
        canvas.SetGrid(1, 1)

        h0.GetXaxis().SetNoExponent()
        h0.GetXaxis().SetMoreLogLabels()

        for _tmpExt in exts:
          canvas.SaveAs('tmp__jet_'+_fomTag+'_'+_jetTag+'_'+_etaTag+'.'+_tmpExt)

        canvas.Close()
