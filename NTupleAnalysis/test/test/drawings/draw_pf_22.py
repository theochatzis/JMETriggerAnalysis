#!/usr/bin/env python
import ROOT

ROOT.gROOT.SetBatch()

ROOT.gStyle.SetOptStat(0)

file0 = ROOT.TFile.Open("ntuples_prod_v10_test50K_copyTH1s/trkV2/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root")
file1 = ROOT.TFile.Open("ntuples_prod_v10_test50K_copyTH1s/trkV2_skimmedTracks/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root")

h00 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult_h").Clone()
h10 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult_h").Clone()
h01 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").Clone()
h11 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").Clone()
h02 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult_h0").Clone()
h12 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult_h0").Clone()

norm0 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").GetEntries()
norm1 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_mult").GetEntries()

h00.SetLineColor(1)
h10.SetLineColor(1)
h02.SetLineColor(2)
h12.SetLineColor(2)
h01.SetLineColor(ROOT.kViolet)
h11.SetLineColor(ROOT.kViolet)

h00.SetLineStyle(1)
h10.SetLineStyle(3)
h01.SetLineStyle(1)
h11.SetLineStyle(3)
h02.SetLineStyle(1)
h12.SetLineStyle(3)

h00.SetLineWidth(2)
h10.SetLineWidth(2)
h01.SetLineWidth(2)
h11.SetLineWidth(2)
h02.SetLineWidth(2)
h12.SetLineWidth(2)

h00.Rebin(2)
h10.Rebin(2)
h01.Rebin(2)
h11.Rebin(2)
h02.Rebin(2)
h12.Rebin(2)

canv = ROOT.TCanvas()

canv.SetRightMargin(0.05)
canv.SetLeftMargin(0.12)

canv.cd()

#h0.Rebin(2)
#h1.Rebin(2)

h00.Scale(1./norm0)
h10.Scale(1./norm1)
h01.Scale(1./norm0)
h11.Scale(1./norm1)
h02.Scale(1./norm0)
h12.Scale(1./norm1)

h11.Draw("hist,e0")
h01.Draw("hist,e0,same")
h10.Draw("hist,e0,same")
h00.Draw("hist,e0,same")
h12.Draw("hist,e0,same")
h02.Draw("hist,e0,same")

h11.SetTitle('multiplicity of PFChargedHadrons, PFNeutralHadrons, and All PFCands;number of PF candidates;a.u.')
h11.GetYaxis().SetRangeUser(0.001, 20)

leg = ROOT.TLegend(0.20, 0.50, 0.99, 0.90)
leg.SetNColumns(2)
leg.AddEntry(h00, 'trkV2, Charged PF Hadrons', 'le')
leg.AddEntry(h10, 'skimmedTracks, Charged PF Hadrons', 'le')
leg.AddEntry(h02, 'trkV2, Neutral PF Hadrons', 'le')
leg.AddEntry(h12, 'skimmedTracks, Neutral PF Hadrons', 'le')
leg.AddEntry(h01, 'trkV2, All PFCands', 'le')
leg.AddEntry(h11, 'skimmedTracks, All PFCands', 'le')
leg.Draw('same')

canv.SetLogy()
canv.SaveAs('hltPFCand_mults.pdf')
canv.Close()

# ---

h0 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_particleId").Clone()
h1 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_particleId").Clone()

h0.SetLineColor(1)
h1.SetLineColor(2)

h0.SetLineStyle(1)
h1.SetLineStyle(1)

h0.SetLineWidth(2)
h1.SetLineWidth(2)

canv = ROOT.TCanvas()

canv.SetRightMargin(0.05)
canv.SetLeftMargin(0.12)

canv.cd()

#h0.Rebin(2)
#h1.Rebin(2)

h0.Scale(1./norm0)
h1.Scale(1./norm1)

h0.Draw("hist,e0")
h1.Draw("hist,e0,same")

h0.SetTitle('PFCandidate ID;;a.u.')
h0.GetYaxis().SetRangeUser(0.1, 1e5-1)

h0.GetXaxis().SetLabelSize(0.075)
h0.GetXaxis().SetBinLabel(1, 'X')
h0.GetXaxis().SetBinLabel(2, 'h')
h0.GetXaxis().SetBinLabel(3, 'e')
h0.GetXaxis().SetBinLabel(4, '#mu')
h0.GetXaxis().SetBinLabel(5, '#gamma')
h0.GetXaxis().SetBinLabel(6, 'h0')
h0.GetXaxis().SetBinLabel(7, 'hHF')
h0.GetXaxis().SetBinLabel(8, 'e/#gamma HF')

leg = ROOT.TLegend(0.69, 0.79, 0.99, 0.99)
leg.AddEntry(h0, 'trkV2', 'le')
leg.AddEntry(h1, 'skimmedTracks', 'le')
leg.Draw('same')

canv.SetTickx()
canv.SetTicky()
canv.SetLogx(0)
canv.SetLogy()

canv.SaveAs('hltPFCand_particleId.pdf')
canv.Close()

# ---

h0 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_eta").Clone()
h1 = file1.Get("PFCandidateHistograms_hltPFCands/pfcand_eta").Clone()

h0.SetLineColor(1)
h1.SetLineColor(2)

h0.SetLineStyle(1)
h1.SetLineStyle(1)

h0.SetLineWidth(2)
h1.SetLineWidth(2)

canv = ROOT.TCanvas()

canv.SetRightMargin(0.05)
canv.SetLeftMargin(0.12)

canv.cd()

#h0.Rebin(2)
#h1.Rebin(2)

h0.Scale(1./norm0)
h1.Scale(1./norm1)

h1.Draw("hist,e0")
h0.Draw("hist,e0,same")

h1.SetTitle(';PFCandidate #eta;a.u.')
#h1.GetYaxis().SetRangeUser(0.0001, 0.01)
#h1.GetXaxis().SetLabelSize(0.075)

leg = ROOT.TLegend(0.45, 0.75, 0.75, 0.95)
leg.AddEntry(h0, 'trkV2', 'le')
leg.AddEntry(h1, 'skimmedTracks', 'le')
leg.Draw('same')

canv.SetTickx()
canv.SetTicky()
canv.SetLogx(0)
canv.SetLogy(0)

canv.SaveAs('hltPFCand_eta.pdf')
canv.Close()

# ---

h0 = file0.Get("PFCandidateHistograms_hltPFCands/pfcand_eta").Clone()
h1 = file0.Get("PFCandidateHistograms_offlinePFCands/pfcand_eta").Clone()

h0.SetLineColor(1)
h1.SetLineColor(4)

h0.SetLineStyle(1)
h1.SetLineStyle(1)

h0.SetLineWidth(2)
h1.SetLineWidth(2)

canv = ROOT.TCanvas()

canv.SetRightMargin(0.05)
canv.SetLeftMargin(0.12)

canv.cd()

#h0.Rebin(2)
#h1.Rebin(2)

h0.Scale(1./norm0)
h1.Scale(1./norm0)

h1.Draw("hist,e0")
h0.Draw("hist,e0,same")

h1.SetTitle(';PFCandidate #eta;a.u.')
#h1.GetYaxis().SetRangeUser(0.0001, 0.01)
#h1.GetXaxis().SetLabelSize(0.075)

leg = ROOT.TLegend(0.45, 0.75, 0.75, 0.95)
leg.AddEntry(h0, 'trkV2', 'le')
leg.AddEntry(h1, 'Offline', 'le')
leg.Draw('same')

canv.SetTickx()
canv.SetTicky()
canv.SetLogx(0)
canv.SetLogy(0)

canv.SaveAs('hltPFCand_vsOffline_eta.pdf')
canv.Close()
