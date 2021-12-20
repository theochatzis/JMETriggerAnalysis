#!/usr/bin/env python
import ROOT

ROOT.gROOT.SetBatch()

ROOT.gStyle.SetOptStat(0)

file0 = ROOT.TFile.Open("ntuples_prod_v10_test50K/trkV2/PhaseIITDRSpring19_QCD_Pt_15to3000_Flat_14TeV_PU200.root")
file1 = ROOT.TFile.Open("ntuples_prod_v10_test50K_copyTH1s/trkV2_skimmedTracks/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root")

h00 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult_h").Clone()
h10 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult_h").Clone()
h01 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").Clone()
h11 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").Clone()

norm00 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").GetEntries()
norm10 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").GetEntries()
norm01 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").GetEntries()
norm11 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").GetEntries()

h00.SetLineColor(1)
h10.SetLineColor(2)
h01.SetLineColor(1)
h11.SetLineColor(2)

h00.SetLineStyle(3)
h10.SetLineStyle(3)
h01.SetLineStyle(1)
h11.SetLineStyle(1)

h00.SetLineWidth(2)
h10.SetLineWidth(2)
h01.SetLineWidth(2)
h11.SetLineWidth(2)

canv = ROOT.TCanvas()

canv.SetRightMargin(0.05)
canv.SetLeftMargin(0.12)

canv.cd()

#h0.Rebin(2)
#h1.Rebin(2)

h00.Scale(1./norm00)
h10.Scale(1./norm10)
h01.Scale(1./norm01)
h11.Scale(1./norm11)

h11.Draw("hist,e0")
h01.Draw("hist,e0,same")
h10.Draw("hist,e0,same")
h00.Draw("hist,e0,same")

h11.SetTitle('multiplicity of ChargedPFHadrons (dashed) and all PFCands (solid);number of PF candidates;a.u.')
h11.GetYaxis().SetRangeUser(0.001, 0.15)

leg = ROOT.TLegend(0.40, 0.40, 0.90, 0.90)
leg.AddEntry(h00, 'Charged PF Hadrons, trkV2', 'le')
leg.AddEntry(h10, 'Charged PF Hadrons, skimmedTracks', 'le')
leg.AddEntry(h01, 'All PFCands, trkV2', 'le')
leg.AddEntry(h11, 'All PFCands, skimmedTracks', 'le')
leg.Draw('same')

canv.SaveAs('pfCand_mult_handall.pdf')
canv.Close()
