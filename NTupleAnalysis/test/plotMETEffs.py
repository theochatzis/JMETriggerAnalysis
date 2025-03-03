#!/usr/bin/env python
import os
import ROOT

from common.plot_style import apply_style
from common.efficiency import get_efficiency_graph

outputDir = 'plots_metEffs'
os.makedirs(outputDir)

ROOT.gROOT.SetBatch()

apply_style(0)

def getEff(tree, hname, xnbins, xmin, xmax, var, cut):

  h0d = ROOT.TH1D(hname+'_den', hname+'_den', xnbins, xmin, xmax)
  h0d.Sumw2()
  tree.Draw(var+'>>'+hname+'_den', '', 'goff')

  h0n = ROOT.TH1D(hname+'_num', hname+'_num', xnbins, xmin, xmax)
  h0n.Sumw2()
  tree.Draw(var+'>>'+hname+'_num', cut, 'goff')

  geff = get_efficiency_graph(h0n, h0d)
  geff.UseCurrentStyle()
  geff.SetName(hname)
  geff.SetTitle(hname)

  return geff

for pfAlgo in [
# 'PF',
  'PFPuppi',
]:
 for key in [0]:

  if key == 0:
   inputNtuplesDir = 'output_hltPhase2_201007/ntuples'
   ntupleName = 'Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200'
   outputTag = pfAlgo
   reco0 = 'HLT_TRKv06'
   reco1 = 'HLT_TRKv07p2'
   reco2 = 'HLT_TRKv07p2_TICL'
   color0 = 1
   color1 = ROOT.kBlue
   color2 = ROOT.kRed
   legName0 = 'TRK-v6'
   legName1 = 'TRK-v7'
   legName2 = 'TRK-v7 + TICL'

  else:
   raise RuntimeError(key)

  f0 = ROOT.TFile.Open(inputNtuplesDir+'/'+reco0+'/'+ntupleName+'.root')
  f1 = ROOT.TFile.Open(inputNtuplesDir+'/'+reco1+'/'+ntupleName+'.root')
  f2 = ROOT.TFile.Open(inputNtuplesDir+'/'+reco2+'/'+ntupleName+'.root')

  t0 = f0.Get("JMETriggerNTuple/Events") if f0 else None
  t1 = f1.Get("JMETriggerNTuple/Events") if f1 else None
  t2 = f2.Get("JMETriggerNTuple/Events") if f2 else None

  canvases = []

  for _tmp in [
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_l1t105.pdf',
      'cut': 'l1t'+pfAlgo+'MET_pt > 105',
      'title': ';Offline (Raw)PFPuppi MET [GeV];Efficiency',
      'objLabel': 'PFPuppiMET: L1T>105',
      'topLabel': ntupleName,
      'var': 'offlinePFPuppiMET_Raw_pt',
      'xnbins': 50,
      'xmin': 0,
      'xmax': 500,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_l1t135.pdf',
      'cut': 'l1t'+pfAlgo+'MET_pt > 135',
      'title': ';Offline (Raw)PFPuppi MET [GeV];Efficiency',
      'objLabel': 'PFPuppiMET: L1T>135',
      'topLabel': ntupleName,
      'var': 'offlinePFPuppiMET_Raw_pt',
      'xnbins': 50,
      'xmin': 0,
      'xmax': 500,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_l1t135_hlt200.pdf',
      'cut': 'l1t'+pfAlgo+'MET_pt > 135 && hlt'+pfAlgo+'MET_pt > 200',
      'title': ';Offline (Raw)PFPuppi MET [GeV];Efficiency',
      'objLabel': 'PFPuppiMET: L1T>135 && HLT>200',
      'topLabel': ntupleName,
      'var': 'offlinePFPuppiMET_Raw_pt',
      'xnbins': 50,
      'xmin': 0,
      'xmax': 500,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_l1t135_hlt220.pdf',
      'cut': 'l1t'+pfAlgo+'MET_pt > 135 && hlt'+pfAlgo+'MET_pt > 220',
      'title': ';Offline (Raw)PFPuppi MET [GeV];Efficiency',
      'objLabel': 'PFPuppiMET: L1T>135 && HLT>220',
      'topLabel': ntupleName,
      'var': 'offlinePFPuppiMET_Raw_pt',
      'xnbins': 50,
      'xmin': 0,
      'xmax': 500,
      'logY': 0,
    },
    {
      'outputName': outputDir+'/'+ntupleName+'_'+outputTag+'_l1t105_hlt220.pdf',
      'cut': 'l1t'+pfAlgo+'MET_pt > 105 && hlt'+pfAlgo+'MET_pt > 220',
      'title': ';Offline (Raw)PFPuppi MET [GeV];Efficiency',
      'objLabel': 'PFPuppiMET: L1T>105 && HLT>220',
      'topLabel': ntupleName,
      'var': 'offlinePFPuppiMET_Raw_pt',
      'xnbins': 50,
      'xmin': 0,
      'xmax': 500,
      'logY': 0,
    },
  ]:
    g0 = None
    g1 = None
    g2 = None

    histoNamePostfix = '_'+str(len(canvases))

    if t0:
      g0 = getEff(t0, 'h0'+histoNamePostfix, _tmp['xnbins'], _tmp['xmin'], _tmp['xmax'], _tmp['var'], _tmp['cut'])
      g0.SetMarkerSize(0.5)
      g0.SetLineWidth(2)
      g0.SetMarkerColor(color0)
      g0.SetLineColor(color0)
      print 'g0'

    if t1:
      g1 = getEff(t1, 'h1'+histoNamePostfix, _tmp['xnbins'], _tmp['xmin'], _tmp['xmax'], _tmp['var'], _tmp['cut'])
      g1.SetMarkerSize(0.5)
      g1.SetLineWidth(2)
      g1.SetMarkerColor(color1)
      g1.SetLineColor(color1)
      print 'g1'

    if t2:
      g2 = getEff(t2, 'h2'+histoNamePostfix, _tmp['xnbins'], _tmp['xmin'], _tmp['xmax'], _tmp['var'], _tmp['cut'])
      g2.SetMarkerSize(0.5)
      g2.SetLineWidth(2)
      g2.SetMarkerColor(color2)
      g2.SetLineColor(color2)
      print 'g2'

    canvas = ROOT.TCanvas('c'+histoNamePostfix, 'c'+histoNamePostfix)
    canvas.cd()

    h0 = canvas.DrawFrame(_tmp['xmin'], 0., _tmp['xmax'], 1.15)

    for _tmp2 in [g0, g1, g2]:
      if _tmp2 is not None:
        _tmp2.Draw('lep')
  
    topLabel = ROOT.TPaveText(0.11, 0.93, 0.95, 0.98, 'NDC')
    topLabel.SetFillColor(0)
  # topLabel.SetFillStyle(3000)
    topLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(12)
    topLabel.SetTextFont(42)
    topLabel.SetTextSize(0.035)
    topLabel.SetBorderSize(10)
    topLabel.AddText(_tmp['topLabel'])
    topLabel.Draw('same')

    objLabel = ROOT.TPaveText(0.18, 0.84, 0.64, 0.91, 'NDC')
    objLabel.SetFillColor(0)
  # objLabel.SetFillStyle(3000)
    objLabel.SetTextColor(ROOT.kBlack)
    topLabel.SetTextAlign(11)
    objLabel.SetTextFont(42)
    objLabel.SetTextSize(0.0325)
    objLabel.SetBorderSize(0)
    objLabel.AddText(_tmp['objLabel'])
    objLabel.Draw('same')

    leg = ROOT.TLegend(0.65, 0.20, 0.95, 0.40)
    leg.SetNColumns(1)
    if g0: leg.AddEntry(g0, legName0, 'lep')
    if g1: leg.AddEntry(g1, legName1, 'lep')
    if g2: leg.AddEntry(g2, legName2, 'lep')
    leg.Draw('same')

    h0.SetTitle(_tmp['title'])
    h0.GetYaxis().SetTitleOffset(h0.GetYaxis().GetTitleOffset() * 1.0)
#    if _tmp['logY']:
#      h0.GetYaxis().SetRangeUser(1, hmax**(1./0.8))  
#    else:
#      h0.GetYaxis().SetRangeUser(0, hmax* (1./0.8))  

    canvas.SetLogy(_tmp['logY'])
    canvas.SetGrid(1, 1)

    canvas.SaveAs(_tmp['outputName'])
    canvases.append(canvas)
    canvas.Close()

  if f0: f0.Close()
  if f1: f1.Close()
  if f2: f2.Close()
