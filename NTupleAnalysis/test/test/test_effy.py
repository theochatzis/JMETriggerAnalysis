#!/usr/bin/env python
import ROOT
from common.efficiency import *

if __name__ == '__main__':
   ROOT.gROOT.SetBatch()

   tfile = ROOT.TFile.Open('tmptmptmp/outputs/EGamma_Run2018D.root')

   plots = [
#     ('HLT_PFMET200_NotCleaned'          , 'offlineMETs_Type1_pt', ROOT.kBlack, 1),
#     ('HLT_PFMET200_HBHECleaned'         , 'offlineMETs_Type1_pt', ROOT.kRed, 1),

      ('HLT_PFMET200_HBHE_BeamHaloCleaned', 'offlineMETs'     +'_Type1_pt', ROOT.kBlue, 1),
      ('HLT_PFMET200_HBHE_BeamHaloCleaned', 'offlineMETsPuppi'+'_Type1_pt', ROOT.kBlue, 2),

      ('HLT_PFMET250_HBHECleaned', 'offlineMETs'     +'_Type1_pt', ROOT.kOrange+1, 1),
      ('HLT_PFMET250_HBHECleaned', 'offlineMETsPuppi'+'_Type1_pt', ROOT.kOrange+1, 2),

      ('HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned', 'offlineMETs'     +'_Type1_pt', ROOT.kRed+0, 1),
      ('HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned', 'offlineMETsPuppi'+'_Type1_pt', ROOT.kRed+0, 2),
   ]

   canvas = ROOT.TCanvas()
   canvas.SetGrid(1,1)
   canvas.SetTickx(1)
   canvas.SetTicky(1)

   graphs = []
   firstDraw = True
   for _tmp in plots:
       hnum = tfile.Get(_tmp[0]+'_pass/' +_tmp[1])
       hden = tfile.Get(_tmp[0]+'_total/'+_tmp[1])
       geff = get_efficiency_graph(hnum, hden)

       geff.SetMarkerSize(1.0)
       geff.SetMarkerStyle(19+_tmp[3])
       geff.SetMarkerColor(_tmp[2])
       geff.SetLineColor(_tmp[2])
       geff.SetLineWidth(2)
       geff.SetLineStyle(_tmp[3])
       graphs.append(geff)
       if firstDraw:
          geff.Draw('alep')
          firstDraw = False
       else:
          geff.Draw('lep')

   canvas.SaveAs('tmp.pdf')
   canvas.Close()
   tfile.Close()
