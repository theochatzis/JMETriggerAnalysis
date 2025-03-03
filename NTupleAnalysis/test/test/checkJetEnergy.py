import array
import ROOT

ROOT.gROOT.SetBatch()

f0 = ROOT.TFile('output_hltRun3_trkSingleIterWithPatatrack_v02/ntuples/HLT/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV.root')
t0 = f0.Get('JMETriggerNTuple/Events')

for e0 in t0:
    for jet_i in range(len(e0.hltAK4PFJetsCorrected_pt)):
        jet_pt  = e0.hltAK4PFJetsCorrected_pt  [jet_i]
        jet_eta = e0.hltAK4PFJetsCorrected_eta [jet_i]
        jet_phi = e0.hltAK4PFJetsCorrected_phi [jet_i]
        jet_M   = e0.hltAK4PFJetsCorrected_mass[jet_i]

        p4 = ROOT.TLorentzVector()
        p4.SetPtEtaPhiM(jet_pt, jet_eta, jet_phi, jet_M)

        if p4.E() < 0.:
           print '{:} pt={:}={:} eta={:}={:} phi={:}={:} mass={:}={:} E={:}'.format(
             jet_i,
             jet_pt, p4.Pt(),
             jet_eta, p4.Eta(),
             jet_phi, p4.Phi(),
             jet_M, p4.M(),
             p4.E()
           )
           print '-'*100

#for (postFix, selCut) in [
#  ('_nPVlo', 'hltPixelVertices_z@.size()<=30'),
#  ('_nPVhi', 'hltPixelVertices_z@.size()> 30'),
#]:
#
# h0 = ROOT.TH1D('h0', 'h0', len(bins)-1, bins)
# h0.Sumw2()
#
# h1 = ROOT.TH1D('h1', 'h1', len(bins)-1, bins)
# h1.Sumw2()
#
# t0.Draw('hltPFMET_pt'     +'>>h0', selCut, 'goff')
# t0.Draw('hltPuppiMETv1_pt'+'>>h1', selCut, 'goff')
#
# h0.SetLineColor(1)
# h1.SetLineColor(2)
#
# h0.SetLineWidth(2)
# h1.SetLineWidth(2)
#
## ratio = h1.Clone()
## ratio.Divide(h0)
#
# print h0.GetEntries()
# print h1.GetEntries()
#
# canvas = ROOT.TCanvas()
# canvas.cd()
# h0.Draw('hist,e0')
# h1.Draw('hist,e0,same')
## ratio.Draw('hist,e0')
# canvas.SaveAs('Run3_QCD_PuppiMET_over_PFMET'+postFix+'.pdf')
# canvas.Close()

f0.Close()
