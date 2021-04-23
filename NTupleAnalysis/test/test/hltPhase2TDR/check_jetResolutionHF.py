import ROOT

f0 = ROOT.TFile.Open("output_hltPhase2_201209_tdrDraft2_deltaR02_v3/harvesting/HLT_TRKv06p1_TICL/Phase2HLTTDR_QCD_PtFlat15to3000_14TeV_PU200.root")
h2 = f0.Get("NoSelection/hltAK4PFPuppiJetsCorrected_HF_MatchedToGEN_pt_overGEN__vs__GEN_pt")

binEdges = [
   40,
   60,
   80,
  100,
  120,
  140,
  160,
  240,
  340,
  600,
]

for binEdge_i in range(len(binEdges)-1):
  h2proj_i = h2.ProjectionX("h2proj_i", h2.GetYaxis().FindBin(binEdges[binEdge_i]*1.00001), h2.GetYaxis().FindBin(binEdges[binEdge_i+1]/1.00001))
  h2proj_i_ent = h2proj_i.GetEntries()
  h2proj_i_mean = h2proj_i.GetMean()
  h2proj_i_rms = h2proj_i.GetRMS()
  h2proj_i_rOm = -1. if h2proj_i_mean == 0 else h2proj_i_rms/h2proj_i_mean
  print '[{:> 5.0f}, {:> 5.0f}] e={:> 7.1f} m={:>5.5f} r={:>5.5f} r/m={:5.5f}'.format(binEdges[binEdge_i], binEdges[binEdge_i+1], h2proj_i_ent, h2proj_i_mean, h2proj_i_rms, h2proj_i_rOm)
