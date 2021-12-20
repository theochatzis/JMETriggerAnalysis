import ROOT

tf=ROOT.TFile.Open('tmptmptmp.root')

thelist = [
  (['NoSelection/'                +'hltAK4PuppiJetsCorrected_EtaIncl_MatchedToGEN_pt0__vs__GEN_pt',
    'HLT_AK4PuppiJetCorrected100/'+'hltAK4PuppiJetsCorrected_EtaIncl_MatchedToGEN_pt0__vs__GEN_pt'], 2, 20)

# ('hltAK4PFJetsCorrected_HB_pt', 1, 20),
# ('hltAK4PFJetsCorrected_HGCal_pt', 2, 22),
# ('hltAK4PFJetsCorrected_HF1_pt', 4, 24),
# ('hltAK4PFJetsCorrected_HF2_pt', 6, 24),

# ('hltAK4PFJetsCorrected_HB_pt', 1, 20),
# ('hltAK4PFCHSJetsCorrected_HB_pt', 2, 22),
# ('hltAK4PuppiJetsCorrected_HB_pt', 4, 24),

# ('hltAK4PFJetsCorrected_EtaIncl_eta', 1, 20),
# ('hltAK4CaloJetsCorrected_EtaIncl_eta', 2, 24),
]

cache=[]
for _tmpIdx, _tmp in enumerate(thelist):
    hkeyDEN=_tmp[0][0]
    hkeyNUM=_tmp[0][1]
    den0=tf.Get(hkeyDEN)
    num0=tf.Get(hkeyNUM)

    den = den0.ProjectionY('den')
    num = num0.ProjectionY('num')

    ratio=num.Clone()
    den2=den.Clone()
    for _tmp2 in range(2+den2.GetNbinsX()): den2.SetBinError(_tmp2,0.)
    ratio.Divide(den2)
    ratio.SetMarkerColor(_tmp[1])
    ratio.SetMarkerStyle(_tmp[2])
    ratio.SetMarkerSize(1)
    ratio.SetLineColor(_tmp[1])
    ratio.SetLineWidth(2)
    ratio.Draw('lep'+',same'*_tmpIdx)
    cache+=[(num, den, ratio)]
