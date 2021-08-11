import ROOT

tf=ROOT.TFile.Open('Desktop/tmp/tmptmp.root')

thelist = [
# ('hltAK4PFJetsCorrected_HB_pt', 1, 20),
# ('hltAK4PFJetsCorrected_HGCal_pt', 2, 22),
# ('hltAK4PFJetsCorrected_HF1_pt', 4, 24),
# ('hltAK4PFJetsCorrected_HF2_pt', 6, 24),

 ('hltAK4PFJetsCorrected_HB_pt', 1, 20),
 ('hltAK4PFCHSJetsCorrected_HB_pt', 2, 22),
 ('hltAK4PuppiJetsCorrected_HB_pt', 4, 24),

# ('hltAK4PFJetsCorrected_EtaIncl_eta', 1, 20),
# ('hltAK4CaloJetsCorrected_EtaIncl_eta', 2, 24),
]

cache=[]
for _tmpIdx, _tmp in enumerate(thelist):
    hkeyDEN=_tmp[0]
    tmp=hkeyDEN.split('_')
    tmp = tmp[:-1]+['NotMatchedToGEN']+tmp[-1:]
    hkeyNUM='_'.join(tmp)
    den=tf.Get('NoSelection/'+hkeyDEN)
    num=tf.Get('NoSelection/'+hkeyNUM)

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
