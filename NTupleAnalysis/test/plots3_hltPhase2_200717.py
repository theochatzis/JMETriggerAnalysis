#!/usr/bin/env python
import os
import ROOT
from common.plot import *

if __name__ == '__main__':

   ROOT.gROOT.SetBatch()

#   ## 1
#   for AN_TAG in [
#     'PuppiMod0_v01',
#     'PuppiMod1_v01',
#     'PuppiMod2_v01',
#   ]:
#     INPUT_DIR = '/nfs/dust/cms/user/missirol/test/jmeTrigger/phase2/area_01/CMSSW_11_1_2_PuppiMod2/src/NTupleAnalysis/JMETrigger/test/output_hltPhase2_200717_'+AN_TAG+'/harvesting'
#
#     OUT_DIR = 'plots2_hltPhase2_200717/'+AN_TAG
#
#     os.makedirs(OUT_DIR)
#  
#     for reco_label in [
#       'HLT_TRKv06',
#       'HLT_TRKv06_TICL',
#     ]:
#       _file0 = ROOT.TFile.Open(INPUT_DIR+'/'+reco_label+'/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
#       if not _file0: continue
#
#       for [algoName_i, algoTitle_i] in [
#         ['PF', 'PF'],
#         ['Puppi', 'Puppi'],
#       ]:
#         h0 = _file0.Get('NoSelection/offline'+algoName_i+'MET_Raw_pt')
#         h0.Scale(1., 'width')
#         h0.SetLineColor(1)
#         h0.SetLineWidth(2)
#         h0.SetStats(0)
#    
#         h1 = _file0.Get('NoSelection/l1t'+algoName_i+'MET_pt')
#         h1.Scale(1., 'width')
#         h1.SetLineColor(2)
#         h1.SetLineWidth(2)
#       
#         h2 = _file0.Get('NoSelection/hlt'+algoName_i+'MET_pt')
#         h2.Scale(1., 'width')
#         h2.SetLineColor(4)
#         h2.SetLineWidth(2)
#       
#         canvas = ROOT.TCanvas('canvas', 'canvas', 750, 750)
#         canvas.cd()
#         canvas.SetGrid(1,1)
#    
#         canvas.SetTopMargin(0.10)
#         canvas.SetBottomMargin(0.15)
#         canvas.SetRightMargin(0.05)
#         canvas.SetLeftMargin(0.15)
#    
#         h0.Draw('hist,e0')
#         h1.Draw('hist,e0,same')
#         h2.Draw('hist,e0,same')
#    
#         h0.SetTitle(';MET [GeV];Events / Bin width')
#         h0.GetXaxis().SetRangeUser(0, 500.)
#         h0.GetXaxis().SetTitleSize(0.05)
#         h0.GetXaxis().SetTitleOffset(1.2)
#         h0.GetYaxis().SetTitleSize(0.05)
#         h0.GetYaxis().SetTitleOffset(1.4)
#    
#         leg = ROOT.TLegend(0.6, 0.6, 0.95, 0.9)
#         leg.SetFillColor(0)
#         leg.AddEntry(h0, 'Offline ('+algoTitle_i+')', 'le')
#         leg.AddEntry(h1, 'L1T ('+algoTitle_i+')', 'le')
#         leg.AddEntry(h2, 'HLT ('+algoTitle_i+')', 'le')
#         leg.Draw('same')
#       
#         label1 = get_pavetext(0.6, 0.91, 0.95, 0.99, 0.035, reco_label)
#         label1.SetFillColor(0)
#         label1.Draw('same')
#    
#         label2 = get_pavetext(0.1, 0.91, 0.50, 0.99, 0.035, 'QCD Pt-Flat [PU200]')
#         label2.SetFillColor(0)
#         label2.Draw('same')
#    
#         canvas.SaveAs(OUT_DIR+'/FakeMET_'+algoName_i+'_pt_'+reco_label+'.pdf')
#         canvas.SetLogy(1)
#         canvas.SaveAs(OUT_DIR+'/FakeMET_'+algoName_i+'_pt_'+reco_label+'_logY.pdf')
#         canvas.Close()
#
#       _file0.Close()
#
#     # MET resolution
#     for reco_label in [
#       'HLT_TRKv06',
#       'HLT_TRKv06_TICL',
#     ]:
#       _file1 = ROOT.TFile.Open(INPUT_DIR+'/'+reco_label+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root')
#       if not _file1: continue
#
#       for [algoName_i, algoTitle_i] in [
#         ['PF', 'PF'],
#         ['Puppi', 'Puppi'],
#       ]:
#         for [varName_i, varTitle_i] in [
#           ['pt_overGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<p_{T} / p^{GEN}_{T}>'],
#           ['pt_paraToGENMinusGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];#sigma(#Deltap^{#parallel}_{T}) / <p_{T} / p^{GEN}_{T}>'],
#           ['pt_perpToGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];#sigma(p^{#perp}_{T}) / <p_{T} / p^{GEN}_{T}>'],
#         ]:       
#           h0 = _file1.Get('NoSelection/offline'+algoName_i+'MET_Raw_'+varName_i)
#           h0.SetLineColor(1)
#           h0.SetLineWidth(2)
#           h0.SetMarkerSize(1)
#           h0.SetMarkerStyle(20)
#           h0.SetMarkerColor(1)
#           h0.SetStats(0)
#
#           h1 = _file1.Get('NoSelection/l1t'+algoName_i+'MET_'+varName_i)
#           h1.SetLineColor(2)
#           h1.SetLineWidth(2)
#           h1.SetMarkerSize(1)
#           h1.SetMarkerStyle(20)
#           h1.SetMarkerColor(2)
#      
#           h2 = _file1.Get('NoSelection/hlt'+algoName_i+'MET_'+varName_i)
#           h2.SetLineColor(4)
#           h2.SetLineWidth(2)
#           h2.SetMarkerSize(1)
#           h2.SetMarkerStyle(20)
#           h2.SetMarkerColor(4)
#  
#           canvas = ROOT.TCanvas('canvas', 'canvas', 750, 750)
#           canvas.cd()
#           canvas.SetGrid(1,1)
#      
#           canvas.SetTopMargin(0.10)
#           canvas.SetBottomMargin(0.15)
#           canvas.SetRightMargin(0.05)
#           canvas.SetLeftMargin(0.15)
#    
#           h0.Draw('lp,e0')
#           h1.Draw('lp,e0,same')
#           h2.Draw('lp,e0,same')
#    
#           h0.SetTitle(varTitle_i)
#           h0.GetXaxis().SetRangeUser(0, 500.)
#           if 'RMSOverMean' in varName_i:
#              h0.GetYaxis().SetRangeUser(0.1, 100.)
#           else:
#              h0.GetYaxis().SetRangeUser(0.001, 5.)
#           h0.GetXaxis().SetTitleSize(0.05)
#           h0.GetXaxis().SetTitleOffset(1.2)
#           h0.GetYaxis().SetTitleSize(0.05)
#           h0.GetYaxis().SetTitleOffset(1.4)
#  
#           if 'RMSOverMean' in varName_i:
#              leg = ROOT.TLegend(0.6, 0.2, 0.95, 0.5)
#           else:
#              leg = ROOT.TLegend(0.6, 0.6, 0.95, 0.9)
#           leg.SetFillColor(0)
#           leg.AddEntry(h0, 'Offline ('+algoTitle_i+')', 'lep')
#           leg.AddEntry(h1, 'L1T ('+algoTitle_i+')', 'lep')
#           leg.AddEntry(h2, 'HLT ('+algoTitle_i+')', 'lep')
#           leg.Draw('same')
#
#           label1 = get_pavetext(0.6, 0.91, 0.95, 0.99, 0.035, reco_label)
#           label1.SetFillColor(0)
#           label1.Draw('same')
#      
#           label2 = get_pavetext(0.1, 0.91, 0.50, 0.99, 0.035, 'VBF H#rightarrowInv [PU200]')
#           label2.SetFillColor(0)
#           label2.Draw('same')
#    
#           canvas.SaveAs(OUT_DIR+'/RealMET_'+algoName_i+'_'+varName_i+'_'+reco_label+'.pdf')
#           canvas.SetLogy(1)
#           canvas.SaveAs(OUT_DIR+'/RealMET_'+algoName_i+'_'+varName_i+'_'+reco_label+'_logY.pdf')
#           canvas.Close()
#
#       _file1.Close()
#
#   ## 2
#   AN_TAG0 = 'PuppiMod0_v01'
#   AN_TAG1 = 'PuppiMod1_v01'
#   AN_TAG2 = 'PuppiMod2_v01'
#
#   INPUT_DIR0 = '/nfs/dust/cms/user/missirol/test/jmeTrigger/phase2/area_01/CMSSW_11_1_2_PuppiMod2/src/NTupleAnalysis/JMETrigger/test/output_hltPhase2_200717_'+AN_TAG0+'/harvesting'
#   INPUT_DIR1 = '/nfs/dust/cms/user/missirol/test/jmeTrigger/phase2/area_01/CMSSW_11_1_2_PuppiMod2/src/NTupleAnalysis/JMETrigger/test/output_hltPhase2_200717_'+AN_TAG1+'/harvesting'
#   INPUT_DIR2 = '/nfs/dust/cms/user/missirol/test/jmeTrigger/phase2/area_01/CMSSW_11_1_2_PuppiMod2/src/NTupleAnalysis/JMETrigger/test/output_hltPhase2_200717_'+AN_TAG2+'/harvesting'
#
#   OUT_DIR = 'plots2_hltPhase2_200717/compare'
#   os.makedirs(OUT_DIR)
#
#   for reco_label in [
#     'HLT_TRKv06',
#     'HLT_TRKv06_TICL',
#   ]:
#     _file0 = ROOT.TFile.Open(INPUT_DIR0+'/'+reco_label+'/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
#     _file1 = ROOT.TFile.Open(INPUT_DIR1+'/'+reco_label+'/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
#     _file2 = ROOT.TFile.Open(INPUT_DIR2+'/'+reco_label+'/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
#
#     if not _file0: continue
#     if not _file1: continue
#     if not _file2: continue
#
#     for [algoName_i, algoTitle_i] in [
#       ['PF', 'PF'],
#       ['Puppi', 'Puppi'],
#     ]:
#       h0 = _file0.Get('NoSelection/hlt'+algoName_i+'MET_pt')
#       h0.Scale(1., 'width')
#       h0.SetLineColor(1)
#       h0.SetLineWidth(2)
#       h0.SetStats(0)
#  
#       h1 = _file1.Get('NoSelection/hlt'+algoName_i+'MET_pt')
#       h1.Scale(1., 'width')
#       h1.SetLineColor(2)
#       h1.SetLineWidth(2)
#
#       h2 = _file2.Get('NoSelection/hlt'+algoName_i+'MET_pt')
#       h2.Scale(1., 'width')
#       h2.SetLineColor(4)
#       h2.SetLineWidth(2)
#
#       canvas = ROOT.TCanvas('canvas', 'canvas', 750, 750)
#       canvas.cd()
#       canvas.SetGrid(1,1)
#  
#       canvas.SetTopMargin(0.10)
#       canvas.SetBottomMargin(0.15)
#       canvas.SetRightMargin(0.05)
#       canvas.SetLeftMargin(0.15)
#  
#       h0.Draw('hist,e0')
#       h1.Draw('hist,e0,same')
#       h2.Draw('hist,e0,same')
#  
#       h0.SetTitle(';MET [GeV];Events / Bin width')
#       h0.GetXaxis().SetRangeUser(0, 500.)
#       h0.GetXaxis().SetTitleSize(0.05)
#       h0.GetXaxis().SetTitleOffset(1.2)
#       h0.GetYaxis().SetTitleSize(0.05)
#       h0.GetYaxis().SetTitleOffset(1.4)
#  
#       leg = ROOT.TLegend(0.6, 0.6, 0.95, 0.9)
#       leg.SetFillColor(0)
#       leg.AddEntry(h0, '11_1_2', 'le')
#       leg.AddEntry(h1, '+ Puppi B-Tuned', 'le')
#       leg.AddEntry(h2, '+ Puppi "PU12"', 'le')
#       leg.Draw('same')
#     
#       label1 = get_pavetext(0.6, 0.91, 0.95, 0.99, 0.035, reco_label)
#       label1.SetFillColor(0)
#       label1.Draw('same')
#  
#       label2 = get_pavetext(0.1, 0.91, 0.50, 0.99, 0.035, 'QCD Pt-Flat [PU200]')
#       label2.SetFillColor(0)
#       label2.Draw('same')
#  
#       canvas.SaveAs(OUT_DIR+'/FakeMET_'+algoName_i+'_pt_'+reco_label+'.pdf')
#       canvas.SetLogy(1)
#       canvas.SaveAs(OUT_DIR+'/FakeMET_'+algoName_i+'_pt_'+reco_label+'_logY.pdf')
#       canvas.Close()
#
#     _file0.Close()
#     _file1.Close()
#     _file2.Close()
#
#   # MET resolution
#   for reco_label in [
#     'HLT_TRKv06',
#     'HLT_TRKv06_TICL',
#   ]:
#     _file0 = ROOT.TFile.Open(INPUT_DIR0+'/'+reco_label+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root')
#     _file1 = ROOT.TFile.Open(INPUT_DIR1+'/'+reco_label+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root')
#     _file2 = ROOT.TFile.Open(INPUT_DIR2+'/'+reco_label+'/Phase2HLTTDR_VBF_HToInvisible_14TeV_PU200.root')
#
#     if not _file0: continue
#     if not _file1: continue
#     if not _file2: continue
#
#     for [algoName_i, algoTitle_i] in [
#       ['PF', 'PF'],
#       ['Puppi', 'Puppi'],
#     ]:
#       for [varName_i, varTitle_i] in [
#         ['pt_overGEN_Mean_wrt_GEN_pt', ';GEN MET [GeV];<p_{T} / p^{GEN}_{T}>'],
#         ['pt_paraToGENMinusGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];#sigma(#Deltap^{#parallel}_{T}) / <p_{T} / p^{GEN}_{T}>'],
#         ['pt_perpToGEN_RMSOverMean_wrt_GEN_pt', ';GEN MET [GeV];#sigma(p^{#perp}_{T}) / <p_{T} / p^{GEN}_{T}>'],
#       ]:
#         h0 = _file0.Get('NoSelection/hlt'+algoName_i+'MET_'+varName_i)
#         h0.SetLineColor(1)
#         h0.SetLineWidth(2)
#         h0.SetMarkerSize(1)
#         h0.SetMarkerStyle(20)
#         h0.SetMarkerColor(1)
#         h0.SetStats(0)
#
#         h1 = _file1.Get('NoSelection/hlt'+algoName_i+'MET_'+varName_i)
#         h1.SetLineColor(2)
#         h1.SetLineWidth(2)
#         h1.SetMarkerSize(1)
#         h1.SetMarkerStyle(20)
#         h1.SetMarkerColor(2)
#
#         h2 = _file2.Get('NoSelection/hlt'+algoName_i+'MET_'+varName_i)
#         h2.SetLineColor(4)
#         h2.SetLineWidth(2)
#         h2.SetMarkerSize(1)
#         h2.SetMarkerStyle(20)
#         h2.SetMarkerColor(4)
#
#         canvas = ROOT.TCanvas('canvas', 'canvas', 750, 750)
#         canvas.cd()
#         canvas.SetGrid(1,1)
#    
#         canvas.SetTopMargin(0.10)
#         canvas.SetBottomMargin(0.15)
#         canvas.SetRightMargin(0.05)
#         canvas.SetLeftMargin(0.15)
#  
#         h0.Draw('lp,e0')
#         h1.Draw('lp,e0,same')
#         h2.Draw('lp,e0,same')
#  
#         h0.SetTitle(varTitle_i)
#         h0.GetXaxis().SetRangeUser(0, 500.)
#         if 'RMSOverMean' in varName_i:
#            h0.GetYaxis().SetRangeUser(0.1, 100.)
#         else:
#            h0.GetYaxis().SetRangeUser(0.001, 5.)
#         h0.GetXaxis().SetTitleSize(0.05)
#         h0.GetXaxis().SetTitleOffset(1.2)
#         h0.GetYaxis().SetTitleSize(0.05)
#         h0.GetYaxis().SetTitleOffset(1.4)
#
#         if 'RMSOverMean' in varName_i:
#            leg = ROOT.TLegend(0.6, 0.2, 0.95, 0.5)
#         else:
#            leg = ROOT.TLegend(0.6, 0.6, 0.95, 0.9)
#         leg.SetFillColor(0)
#         leg.AddEntry(h0, '11_1_2', 'lep')
#         leg.AddEntry(h1, '+ Puppi B-Tuned', 'lep')
#         leg.AddEntry(h2, '+ Puppi "PU12"', 'lep')
#         leg.Draw('same')
#
#         label1 = get_pavetext(0.6, 0.91, 0.95, 0.99, 0.035, reco_label)
#         label1.SetFillColor(0)
#         label1.Draw('same')
#    
#         label2 = get_pavetext(0.1, 0.91, 0.50, 0.99, 0.035, 'VBF H#rightarrowInv [PU200]')
#         label2.SetFillColor(0)
#         label2.Draw('same')
#  
#         canvas.SaveAs(OUT_DIR+'/RealMET_'+algoName_i+'_'+varName_i+'_'+reco_label+'.pdf')
#         canvas.SetLogy(1)
#         canvas.SaveAs(OUT_DIR+'/RealMET_'+algoName_i+'_'+varName_i+'_'+reco_label+'_logY.pdf')
#         canvas.Close()
#
#     _file0.Close()
#     _file1.Close()
#     _file2.Close()





   ## 1
   INPUT_DIR = '/nfs/dust/cms/user/missirol/test/jmeTrigger/phase2/area_01/CMSSW_11_1_2_PuppiMod2/src/NTupleAnalysis/JMETrigger/test'

   OUT_DIR = 'tmp_plots3_hltPhase2_200717/jets_compare'

   os.makedirs(OUT_DIR)

   for reco_label in [
     'HLT_TRKv06',
   ]:
     for [varName, varTitle] in [
       ['JetsCorrected_EtaIncl_pt0_cumul', ';Jet p_{T} threshold [GeV];Event Counts'],
       ['JetsCorrected_HB_pt0_cumul'     , ';Jet p_{T} threshold [GeV];Event Counts'],
       ['JetsCorrected_HGCal_pt0_cumul'  , ';Jet p_{T} threshold [GeV];Event Counts'],
       ['JetsCorrected_HF1_pt0_cumul'    , ';Jet p_{T} threshold [GeV];Event Counts'],
       ['JetsCorrected_HF2_pt0_cumul'    , ';Jet p_{T} threshold [GeV];Event Counts'],
     ]:
       _file0 = ROOT.TFile.Open(INPUT_DIR+'/output_hltPhase2_200717_PuppiMod0_v02/harvesting/'+reco_label+'/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
       if not _file0: continue

       _file1 = ROOT.TFile.Open(INPUT_DIR+'/output_hltPhase2_200717_PuppiMod1_v02/harvesting/'+reco_label+'/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
       if not _file1: continue

       _file2 = ROOT.TFile.Open(INPUT_DIR+'/output_hltPhase2_200717_PuppiMod1_v02/harvesting/'+reco_label+'_TICL/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_PU200.root')
       if not _file2: continue

       for [algoName_i, algoTitle_i] in [
#        ['PF', 'PF'],
         ['Puppi', 'Puppi'],
       ]:
         h0 = _file0.Get('NoSelection/offlineAK4'+algoName_i+varName)
         h0.SetLineColor(1)
         h0.SetMarkerColor(1)
         h0.SetLineWidth(2)
         if h0.InheritsFrom('TH1'):
            h0.SetStats(0)

         h1 = _file0.Get('NoSelection/l1tAK4'+algoName_i+varName)
         h1.SetLineColor(2)
         h1.SetMarkerColor(2)
         h1.SetLineWidth(2)

         h20 = _file0.Get('NoSelection/hltAK4'+algoName_i+varName)
         h20.SetLineColor(4)
         h20.SetMarkerColor(4)
         h20.SetLineWidth(2)

         h21 = _file1.Get('NoSelection/hltAK4'+algoName_i+varName)
         h21.SetLineColor(ROOT.kGray+1)
         h21.SetMarkerColor(ROOT.kGray+1)
         h21.SetLineWidth(2)

         h22 = _file2.Get('NoSelection/hltAK4'+algoName_i+varName)
         h22.SetLineColor(ROOT.kOrange+1)
         h22.SetMarkerColor(ROOT.kOrange+1)
         h22.SetLineWidth(2)

         if not h0.InheritsFrom('TH1'):
            h0.SetMarkerSize(1.5)
            h1.SetMarkerSize(1.5)
            h20.SetMarkerSize(1.5)
            h21.SetMarkerSize(1.5)
            h22.SetMarkerSize(1.5)

         canvas = ROOT.TCanvas('canvas', 'canvas', 750, 750)
         canvas.cd()
         canvas.SetGrid(1,1)

         canvas.SetTopMargin(0.10)
         canvas.SetBottomMargin(0.15)
         canvas.SetRightMargin(0.05)
         canvas.SetLeftMargin(0.15)

         draw_opt1, draw_opt2, draw_optLeg = 'epa', 'ep', 'ep'
         if h0.InheritsFrom('TH1'):
            draw_opt1, draw_opt2, draw_optLeg = 'hist,e0', 'hist,e0,same', 'lep'

         h0.Draw(draw_opt1)
         h1.Draw(draw_opt2)
         h20.Draw(draw_opt2)
         h21.Draw(draw_opt2)
         h22.Draw(draw_opt2)

         hmin, hmax = 1e6, 1.

         hmin, hmax = min(hmin, h0 .GetMinimum()), max(hmax, h0 .GetMaximum())
         hmin, hmax = min(hmin, h1 .GetMinimum()), max(hmax, h1 .GetMaximum())
         hmin, hmax = min(hmin, h20.GetMinimum()), max(hmax, h20.GetMaximum())
         hmin, hmax = min(hmin, h21.GetMinimum()), max(hmax, h21.GetMaximum())
         hmin, hmax = min(hmin, h22.GetMinimum()), max(hmax, h22.GetMaximum())
         hmin = max(hmin, 0.1)

         print hmin, hmax

         h0.SetTitle(varTitle)
         h0.GetXaxis().SetRangeUser(30., 1000.)
         h0.GetYaxis().SetRangeUser(0.8*hmin, 1.2*hmax)
         h0.GetXaxis().SetTitleSize(0.05)
         h0.GetXaxis().SetTitleOffset(1.2)
         h0.GetYaxis().SetTitleSize(0.05)
         h0.GetYaxis().SetTitleOffset(1.4)

         if 'eff' in h0.GetName():
            leg = ROOT.TLegend(0.35, 0.6, 0.75, 0.9)
         else:
            leg = ROOT.TLegend(0.6, 0.6, 0.95, 0.9)

         leg.SetFillColor(0)
         leg.AddEntry(h0, 'Offline ('+algoTitle_i+')', draw_optLeg)
         leg.AddEntry(h1, 'L1T ('+algoTitle_i+')', draw_optLeg)
         leg.AddEntry(h20, 'HLT ('+algoTitle_i+')', draw_optLeg)
         leg.AddEntry(h21, 'HLT ('+algoTitle_i+') + B-Tuned', draw_optLeg)
         leg.AddEntry(h22, 'HLT ('+algoTitle_i+') + B-Tuned + TICL', draw_optLeg)
         leg.Draw('same')

         label1 = get_pavetext(0.6, 0.91, 0.95, 0.99, 0.035, reco_label)
         label1.SetFillColor(0)
         label1.Draw('same')
    
         label2 = get_pavetext(0.1, 0.91, 0.50, 0.99, 0.035, 'QCD Pt-Flat [PU200]')
         label2.SetFillColor(0)
         label2.Draw('same')

         canvas.SetLogx(1)

         canvas.SaveAs(OUT_DIR+'/AK4'+algoName_i+varName+'.pdf')
#        canvas.SetLogy(1)
#        canvas.SaveAs(OUT_DIR+'/AK4'+algoName_i+varName+'_logY.pdf')
         canvas.Close()

       _file0.Close()
       _file1.Close()
       _file2.Close()
