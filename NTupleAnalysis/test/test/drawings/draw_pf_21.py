#!/usr/bin/env python
import ROOT

EXT = 'pdf'

ROOT.gROOT.SetBatch()

ROOT.gStyle.SetOptStat(0)

file0 = ROOT.TFile.Open('jmeAnalysis/ntuples_prod_v10_test10K_morePFplots/trkV2/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root')
file1 = ROOT.TFile.Open('jmeAnalysis/ntuples_prod_v10_test10K_morePFplots/trkV2_skimmedTracks/RelVal1100_2026D49_QCD_Pt15To7000_Flat_14TeV_PU200.root')

the_dict = {

  'HB_chargedHadrons': ['pt', 'eta'],
  'HB_neutralHadrons': ['pt', 'eta'],
  'HB_photons': ['pt', 'eta'],

  'HGCal_chargedHadrons': ['pt', 'eta'],
  'HGCal_neutralHadrons': ['pt', 'eta'],
  'HGCal_photons': ['pt', 'eta'],
}

for pfcands_tag in ['hltPFCands']: #, 'hltPuppiCands']:

    for _tmp in the_dict:

        for _tmp2 in the_dict[_tmp]:

            h0 = file0.Get('PFCandidateHistograms_'+pfcands_tag+'_'+_tmp+'/pfcand_'+_tmp2)
            h1 = file1.Get('PFCandidateHistograms_'+pfcands_tag+'_'+_tmp+'/pfcand_'+_tmp2)

            h0.SetLineColor(1)
            h1.SetLineColor(2)

            h0.SetLineStyle(1)
            h1.SetLineStyle(1)

            h0.SetLineWidth(2)
            h1.SetLineWidth(2)

            h0.Rebin(2)
            h1.Rebin(2)

            canv = ROOT.TCanvas()

            canv.SetRightMargin(0.05)
            canv.SetLeftMargin(0.12)

            canv.cd()
    
            h0.Rebin(2)
            h1.Rebin(2)
    
            h0.Scale(1./h0.Integral())
            h1.Scale(1./h1.Integral())
    
            h1.Draw("hist,e0")
            h0.Draw("hist,e0,same")
    
            h1.SetTitle(';PFCandidate '+_tmp2+';a.u. (norm to 1)')
            h1.GetYaxis().SetRangeUser(0.00005, 1.2*max(h0.GetMaximum(), h1.GetMaximum()))
    
            h1.GetYaxis().SetTitleSize(0.05)
    
            leg = ROOT.TLegend(0.12, 0.91, 0.95, 0.99)
            leg.SetNColumns(2)
            leg.AddEntry(h0, _tmp+', trkV2', 'le')
            leg.AddEntry(h1, _tmp+', skimmedTracks', 'le')
            leg.Draw('same')

            canv.SetLogy()

            canv.SaveAs(pfcands_tag+'_'+_tmp+'_'+_tmp2+'.'+EXT)
            canv.Close()

    # ---

    the_dict2 = {

      'trkV2': file0,
      'trkV2_skimmedTracks': file1,
    }

    for _tmp_tag in the_dict2:

        for _tmp in ['HB', 'HGCal']:

            h0c = the_dict2[_tmp_tag].Get('PFCandidateHistograms_'+pfcands_tag+'_'+_tmp+'_chargedHadrons/pfcand_mult')
            h0n = the_dict2[_tmp_tag].Get('PFCandidateHistograms_'+pfcands_tag+'_'+_tmp+'_neutralHadrons/pfcand_mult')
            h0p = the_dict2[_tmp_tag].Get('PFCandidateHistograms_'+pfcands_tag+'_'+_tmp+'_photons/pfcand_mult')

            h0c.SetLineColor(1)
            h0n.SetLineColor(2)
            h0p.SetLineColor(4)

            h0c.SetLineStyle(1)
            h0n.SetLineStyle(1)
            h0p.SetLineStyle(1)

            h0c.SetLineWidth(2)
            h0n.SetLineWidth(2)
            h0p.SetLineWidth(2)

            h0c.Rebin(2)
            h0n.Rebin(2)
            h0p.Rebin(2)

            canv = ROOT.TCanvas()

            canv.SetRightMargin(0.05)
            canv.SetLeftMargin(0.12)

            canv.cd()

            h0c.Rebin(2)
            h0n.Rebin(2)
            h0p.Rebin(2)

            h0c.Draw("hist,e0")
            h0n.Draw("hist,e0,same")
            h0p.Draw("hist,e0,same")

            h0c.SetTitle(_tmp+' '+_tmp_tag+';number of PFCandidates;Events')
            h0c.GetXaxis().SetRangeUser(0, 5000)
            h0c.GetYaxis().SetRangeUser(0.001, 1.2*max(h0c.GetMaximum(), h0n.GetMaximum(), h0p.GetMaximum()))

            leg = ROOT.TLegend(0.65, 0.65, 0.99, 0.99)
            leg.SetNColumns(1)
            leg.AddEntry(h0c, 'PF Charged Hadrons', 'le')
            leg.AddEntry(h0n, 'PF Neutral Hadrons', 'le')
            leg.AddEntry(h0p, 'PF Photons', 'le')
            leg.Draw('same')

            canv.SaveAs(pfcands_tag+'_mults_'+_tmp_tag+'_'+_tmp+'.'+EXT)
            canv.Close()
