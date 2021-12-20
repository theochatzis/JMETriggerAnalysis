#!/usr/bin/env python
import ROOT

ROOT.gROOT.SetBatch()

ROOT.gStyle.SetOptStat(0)

for puTag in ['PU200', 'NoPU']:

    for regTag in ['HB', 'HGCal']:

        file0 = ROOT.TFile.Open('output_hltPhase2_200423_v02/harvesting/HLT_TRKv00_TICL/Phase2HLTTDR_QCD_Pt_15to3000_Flat_14TeV_'+puTag+'.root')
#       file0 = ROOT.TFile.Open('output_hltPhase2_200423_v02/harvesting/HLT_TRKv00_TICL/Phase2HLTTDR_VBF_HToInvisible_14TeV_'+puTag+'.root')

        h0 = file0.Get('NoSelection/hltAK4PFJetsCorrected_'+regTag+'_phi')
        h1 = file0.Get('NoSelection/hltAK4PFCHSJetsCorrected_'+regTag+'_phi')
        h2 = file0.Get('NoSelection/hltAK4PuppiJetsCorrected_'+regTag+'_phi')

        h00 = h0.Clone()
        h01 = h1.Clone()
        h02 = h2.Clone()

        h00.SetLineColor(1)
        h01.SetLineColor(2)
        h02.SetLineColor(4)

        h00.SetLineStyle(1)
        h01.SetLineStyle(1)
        h02.SetLineStyle(1)
    
        h00.SetLineWidth(2)
        h01.SetLineWidth(2)
        h02.SetLineWidth(2)

        h00.SetMarkerSize(0)
        h01.SetMarkerSize(0)
        h02.SetMarkerSize(0)

        canv = ROOT.TCanvas()

        canv.SetRightMargin(0.05)
        canv.SetLeftMargin(0.12)
    
        canv.cd()

        h00.Scale(1./h00.Integral())
        h01.Scale(1./h01.Integral())
        h02.Scale(1./h02.Integral())

        h00.Draw('hist,e0')
        h01.Draw('hist,e0,same')
        h02.Draw('hist,e0,same')

        h00.SetTitle('['+puTag+'] ['+regTag+'] hltAK4JetsCorrected;#phi;a.u.')
        h00.GetYaxis().SetRangeUser(0.001, 0.07)

        leg = ROOT.TLegend(0.15, 0.80, 0.95, 0.90)
        leg.SetNColumns(3)
        leg.AddEntry(h00, 'AK4PF'   , 'le')
        leg.AddEntry(h01, 'AK4PFCHS', 'le')
        leg.AddEntry(h02, 'AK4Puppi', 'le')
        leg.Draw('same')

        canv.SaveAs('plots_200505/hltAK4_phi_'+regTag+'_'+puTag+'.pdf')
        canv.Close()

        file0.Close()
