#!/usr/bin/env python
import array
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
    'TDR_PU140': 'output_hltPhase2_201209_tdrDraft2_deltaR02_v3/harvesting/HLT_TRKv06p1_TICL/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU140.root',
    'TDR_PU200': 'output_hltPhase2_201209_tdrDraft2_deltaR02_v3/harvesting/HLT_TRKv06p1_TICL/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root',
  }

  for _fileTag in fileDict:
    _tmpTFile = ROOT.TFile.Open(fileDict[_fileTag])

    if not _tmpTFile:
      WARNING('failed to open target TFile: '+_tmpFilePath)
      continue
    print _fileTag

    for _tmpMinGENMET in [
      100,
      150,
      200,
      250,
#      300,
    ]:
     print 'Min GEN-MET: ', _tmpMinGENMET
     binEdges_MET = array.array('d', [_tmpMinGENMET, 800])
     for _tmpMHT in ['MHT30']:
      eff = {'HLT': {}, 'L1TpHLT': {}}
      for _tmpHLTThr in [
        120,
#        130,
        140,
#        150,
        160,
        180,
      ]:
       _tmp_num = _tmpTFile.Get('NoSelection/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppi'+_tmpMHT+'_pt')
       _tmp_num = _tmp_num.ProjectionX(tmpName(), _tmp_num.GetYaxis().FindBin(_tmpHLTThr+0.01), _tmp_num.GetNbinsY()+1, _tmp_num.GetZaxis().FindBin(_tmpHLTThr+0.01), _tmp_num.GetNbinsZ()+1)
       _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)
       _tmp_num.SetBinContent(0, 0.)
       _tmp_num.SetBinError(0, 0.)

       _tmp_den = _tmpTFile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__GEN_pt')
       _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
       _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)
       _tmp_den.SetBinContent(0, 0.)
       _tmp_den.SetBinError(0, 0.)

       eff['HLT'][_tmpHLTThr] = get_efficiency(_tmp_num, _tmp_den)

       _tmp_num = _tmpTFile.Get('L1T_PFPuppiMET220off2/genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppi'+_tmpMHT+'_pt')
       _tmp_num = _tmp_num.ProjectionX(tmpName(), _tmp_num.GetYaxis().FindBin(_tmpHLTThr+0.01), _tmp_num.GetNbinsY()+1, _tmp_num.GetZaxis().FindBin(_tmpHLTThr+0.01), _tmp_num.GetNbinsZ()+1)
       _tmp_num = _tmp_num.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)
       _tmp_num.SetBinContent(0, 0.)
       _tmp_num.SetBinError(0, 0.)

       _tmp_den = _tmpTFile.Get('NoSelection/hltPFPuppiMETTypeOne_pt__vs__GEN_pt')
       _tmp_den = _tmp_den.ProjectionY(tmpName(), 0, -1)
       _tmp_den = _tmp_den.Rebin(len(binEdges_MET)-1, tmpName(), binEdges_MET)
       _tmp_den.SetBinContent(0, 0.)
       _tmp_den.SetBinError(0, 0.)

       eff['L1TpHLT'][_tmpHLTThr] = get_efficiency(_tmp_num, _tmp_den)

       print '{:> 5.1f} {:> 5.3f} {:> 5.3f}'.format(_tmpHLTThr, eff['HLT'][_tmpHLTThr][0], eff['L1TpHLT'][_tmpHLTThr][0])

###
###    for _etaTag in binEdges:
###      if _etaTag not in graphs: graphs[_etaTag] = {}
###      _binEdges = array.array('d', binEdges[_etaTag])
###
###      _htmpNum = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_MatchedTohltPFPuppiCorr_pt')
###      _htmpDen = getHistogram(_tmpTFile, 'NoSelection/ak4GenJetsNoNu_'+_etaTag+'_pt')
###      _htmpNum = _htmpNum.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
###      _htmpDen = _htmpDen.Rebin(len(_binEdges)-1, tmpName(), _binEdges)
###
###      graphs[_etaTag][_fileTag] = get_efficiency_graph(_htmpNum, _htmpDen)
###      graphs[_etaTag][_fileTag].UseCurrentStyle()
###
###      for _tmpn in range(graphs[_etaTag][_fileTag].GetN()):
###        graphs[_etaTag][_fileTag].SetPointEXhigh(_tmpn, 0.)
###        graphs[_etaTag][_fileTag].SetPointEXlow(_tmpn, 0.)
###
###  for _etaTag in graphs:
###    canvas = ROOT.TCanvas(tmpName(), tmpName(False))
###    canvas.cd()
###
###    h0 = canvas.DrawFrame(30., 0.0001, 600., 1.2)
###
###    graphsByEta = graphs[_etaTag]
###
###    gDR02NoPU = graphs[_etaTag]['NoPU_dR02_TDR']
###    gDR02PU200 = graphs[_etaTag]['PU200_dR02_TDR']
###    gDR02PU200PuppiLowAB = graphs[_etaTag]['PU200_dR02_LowPuppiAB']
###    gDR02PU200PuppiLowABPt0 = graphs[_etaTag]['PU200_dR02_LowPuppiAB_Pt0']
###    gDR06PU200PuppiLowABPt0 = graphs[_etaTag]['PU200_dR06_LowPuppiAB_Pt0']
###
###    try:
###      gDR02NoPU.SetMarkerStyle(20)
###      gDR02NoPU.SetMarkerSize(1)
###      gDR02NoPU.SetLineWidth(2)
###      gDR02NoPU.SetLineStyle(1)
###      gDR02NoPU.SetLineColor(1)
###      gDR02NoPU.SetMarkerColor(1)
###      gDR02NoPU.Draw('lepz')
###
###      gDR02PU200.SetMarkerStyle(21)
###      gDR02PU200.SetMarkerSize(1)
###      gDR02PU200.SetLineWidth(2)
###      gDR02PU200.SetLineStyle(1)
###      gDR02PU200.SetLineColor(2)
###      gDR02PU200.SetMarkerColor(2)
###      gDR02PU200.Draw('lepz')
###    
###      gDR02PU200PuppiLowAB.SetMarkerStyle(33)
###      gDR02PU200PuppiLowAB.SetMarkerSize(1.5)
###      gDR02PU200PuppiLowAB.SetLineWidth(2)
###      gDR02PU200PuppiLowAB.SetLineStyle(1)
###      gDR02PU200PuppiLowAB.SetLineColor(4)
###      gDR02PU200PuppiLowAB.SetMarkerColor(4)
###      gDR02PU200PuppiLowAB.Draw('lepz')
###
###      gDR02PU200PuppiLowABPt0.SetMarkerStyle(20)
###      gDR02PU200PuppiLowABPt0.SetMarkerSize(1)
###      gDR02PU200PuppiLowABPt0.SetLineWidth(2)
###      gDR02PU200PuppiLowABPt0.SetLineStyle(1)
###      gDR02PU200PuppiLowABPt0.SetLineColor(ROOT.kViolet+1)
###      gDR02PU200PuppiLowABPt0.SetMarkerColor(ROOT.kViolet+1)
####      gDR02PU200PuppiLowABPt0.Draw('lepz')
###
###      gDR06PU200PuppiLowABPt0.SetMarkerStyle(21)
###      gDR06PU200PuppiLowABPt0.SetMarkerSize(1)
###      gDR06PU200PuppiLowABPt0.SetLineWidth(2)
###      gDR06PU200PuppiLowABPt0.SetLineStyle(1)
###      gDR06PU200PuppiLowABPt0.SetLineColor(ROOT.kGreen+1)
###      gDR06PU200PuppiLowABPt0.SetMarkerColor(ROOT.kGreen+1)
###      gDR06PU200PuppiLowABPt0.Draw('lepz')
###    except: pass
###
###    topLabel = ROOT.TPaveText(0.15, 0.93, 0.55, 0.98, 'NDC')
###    topLabel.SetFillColor(0)
###    topLabel.SetFillStyle(1001)
###    topLabel.SetTextColor(ROOT.kBlack)
###    topLabel.SetTextAlign(12)
###    topLabel.SetTextFont(42)
###    topLabel.SetTextSize(0.035)
###    topLabel.SetBorderSize(0)
###    topLabel.AddText('#font[62]{CMS} #font[52]{Phase-2 Simulation}')
####    topLabel.Draw('same')
###
###    objLabel = ROOT.TPaveText(0.80, 0.93, 0.96, 0.98, 'NDC')
###    objLabel.SetFillColor(0)
###    objLabel.SetFillStyle(1001)
###    objLabel.SetTextColor(ROOT.kBlack)
###    objLabel.SetTextAlign(32)
###    objLabel.SetTextFont(42)
###    objLabel.SetTextSize(0.035)
###    objLabel.SetBorderSize(0)
###    objLabel.AddText('14 TeV')
###    objLabel.Draw('same')
###
###    l1tRateLabel = ROOT.TPaveText(0.165, 0.85, 0.45, 0.90, 'NDC')
###    l1tRateLabel.SetFillColor(0)
###    l1tRateLabel.SetFillStyle(1001)
###    l1tRateLabel.SetTextColor(ROOT.kBlack)
###    l1tRateLabel.SetTextAlign(12)
###    l1tRateLabel.SetTextFont(42)
###    l1tRateLabel.SetTextSize(0.035)
###    l1tRateLabel.SetBorderSize(0)
###    l1tRateLabel.AddText('AK4 PF+PUPPI Jets ('+_etaTag+')')
###    l1tRateLabel.Draw('same')
###
###    hltRateLabel = ROOT.TPaveText(0.165, 0.80, 0.45, 0.85, 'NDC')
###    hltRateLabel.SetFillColor(0)
###    hltRateLabel.SetFillStyle(1001)
###    hltRateLabel.SetTextColor(ROOT.kBlack)
###    hltRateLabel.SetTextAlign(12)
###    hltRateLabel.SetTextFont(42)
###    hltRateLabel.SetTextSize(0.035)
###    hltRateLabel.SetBorderSize(0)
###    hltRateLabel.AddText('p_{T}^{HLT} > 20 GeV')
####    hltRateLabel.Draw('same')
###
###    hltTargetRateLine = ROOT.TLine(30, 1, 600, 1)
###    hltTargetRateLine.SetLineWidth(2)
###    hltTargetRateLine.SetLineStyle(2)
###    hltTargetRateLine.SetLineColor(ROOT.kGray)
###    hltTargetRateLine.Draw('same')
###
###    leg1 = ROOT.TLegend(0.25, 0.17, 0.90, 0.50)
###    leg1.SetNColumns(1)
###    leg1.SetTextFont(42)
###    leg1.AddEntry(gDR02NoPU, 'NoPU (#DeltaR<0.2)', 'l')
###    leg1.AddEntry(gDR02PU200, 'PU200 (#DeltaR<0.2)', 'l')
###    leg1.AddEntry(gDR02PU200PuppiLowAB, 'PU200 (#DeltaR<0.2) PUPPI-LowAB', 'l')
####    leg1.AddEntry(gDR02PU200PuppiLowABPt0, 'PU200 (#DeltaR<0.2) PUPPI-LowAB, p_{T}^{HLT}>0 GeV', 'l')
###    leg1.AddEntry(gDR06PU200PuppiLowABPt0, 'PU200 (#DeltaR<0.6) PUPPI-LowAB', 'l')
###
###    leg1.Draw('same')
###
###    h0.SetTitle(';GEN Jet p_{T} [GeV];Jet-Finding Efficiency')
###    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
###  
###    canvas.SetLogx(1)
###    canvas.SetLogy(0)
###    canvas.SetGrid(1, 1)
###  
###    h0.GetXaxis().SetNoExponent()
###    h0.GetXaxis().SetMoreLogLabels()
###
###    for _tmpExt in exts:
###      canvas.SaveAs('tmp__genMatchEff_'+_etaTag+'.'+_tmpExt)
###  
###    canvas.Close()
