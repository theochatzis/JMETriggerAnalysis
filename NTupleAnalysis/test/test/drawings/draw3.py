#!/usr/bin/env python
import ROOT

ROOT.gROOT.SetBatch()

#ROOT.gStyle.SetOptStat(0)

file0 = ROOT.TFile.Open("test_skimTracks_histos_QCD_PU200.root")
#file1 = ROOT.TFile.Open("out_V2_newGT.root")
h0 = file0.Get("TrackHistograms_generalTracksOriginal/track_mult")
h1 = file0.Get("TrackHistograms_generalTracks/track_mult")

h0.SetLineColor(1)
h1.SetLineColor(2)

h0.SetLineWidth(2)
h1.SetLineWidth(2)

canv = ROOT.TCanvas()

canv.cd()

#h0.Rebin(2)
#h1.Rebin(2)

h1.Draw("hist,e0")
h0.Draw("hist,e0,same")

#h1.GetYaxis().SetRangeUser(0.1, 1300)

leg = ROOT.TLegend(0.30, 0.70, 0.70, 0.90)
leg.AddEntry(h0, 'generalTracks', 'le')
leg.AddEntry(h1, 'generalTracks + skimming', 'le')
leg.Draw('same')

canv.SaveAs('generalTracks_skim_mult.pdf')
canv.Close()
