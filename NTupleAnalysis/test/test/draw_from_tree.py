import array
import ROOT

ROOT.gROOT.SetBatch()

#f0 = ROOT.TFile('output_run3trkGlobalPixelTracksIter0Test_v03/ntuples/HLT/Run3Winter20_DYToLL_M50_14TeV.root')
f0 = ROOT.TFile('output_run3trkGlobalPixelTracksIter0Test_v03/ntuples/HLT/Run3Winter20_QCD_Pt_15to3000_Flat_14TeV.root')

t0 = f0.Get('JMETriggerNTuple/Events')

bins = array.array('d', [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 120, 150, 180, 210, 240, 270, 300, 350, 400, 450, 500])

for (postFix, selCut) in [
  ('_nPVlo', 'hltPixelVertices_z@.size()<=30'),
  ('_nPVhi', 'hltPixelVertices_z@.size()> 30'),
]:

 h0 = ROOT.TH1D('h0', 'h0', len(bins)-1, bins)
 h0.Sumw2()

 h1 = ROOT.TH1D('h1', 'h1', len(bins)-1, bins)
 h1.Sumw2()

 t0.Draw('hltPFMET_pt'     +'>>h0', selCut, 'goff')
 t0.Draw('hltPuppiMETv1_pt'+'>>h1', selCut, 'goff')

 h0.SetLineColor(1)
 h1.SetLineColor(2)

 h0.SetLineWidth(2)
 h1.SetLineWidth(2)

# ratio = h1.Clone()
# ratio.Divide(h0)

 print h0.GetEntries()
 print h1.GetEntries()

 canvas = ROOT.TCanvas()
 canvas.cd()
 h0.Draw('hist,e0')
 h1.Draw('hist,e0,same')
# ratio.Draw('hist,e0')
 canvas.SaveAs('Run3_QCD_PuppiMET_over_PFMET'+postFix+'.pdf')
 canvas.Close()

f0.Close()
