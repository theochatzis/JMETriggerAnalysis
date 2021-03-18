import ROOT

filee = ROOT.TFile.Open('tmp.root')

h1 = filee.Get('offlineMETsPuppi_Type1_pt_minusGEN:genMetTrue_pt')
h1p = h1.ProfileY('aa', 1, -1, 's')
h1p.SetLineColor(1)

h2 = filee.Get('offlineMETsPuppi_Type1_pt_minusGEN:genMetTrue_pt')

for idx in range(1, 1+h2.GetNbinsY()):
    _tmp = h2.ProjectionX('_tmp'+str(idx), idx, idx, 's')
    _tmp.SetDirectory(0)
    print idx, _tmp.GetRMS()
    del _tmp

h2 = filee.Get('offlineMETsPuppi_Type1_pt_minusGEN:genMetTrue_pt')
h2p = h2.ProfileY('aaa', 1, -1, 's')
print h2p.GetEntries()
tmp = h2p.GetEntries()
for idx in range(1, h2p.GetNbinsX()+1):
    print idx, h2p.GetBinContent(idx), h2p.GetBinError(idx)
#    h2p.SetBinContent(idx, h2p.GetBinError(idx))
#    h2p.SetBinEntries(idx, 1)
#
#    h2p.SetBinError(idx, 0)
#    h2p.SetBinEntries(idx, 1)
#
#    print '', idx, h2p.GetBinContent(idx), h2p.GetBinError(idx)
h2p.SetEntries(tmp)
print h2p.GetEntries()
h2p.SetLineColor(2)

#h1p.Draw()
#h2p.Draw('same')

key


if '_minusGEN:':

   key_varX = key.split('_minusGEN:')[0]
   key_varY = key.split('_minusGEN:')[1]

   h_name1 = key_varX+'_minusGEN_RMS_wrt_'+key_varY
   if h_name1 in h1s: KILL('aaa '+h_name1)

   tmp_h1_RMS = tmp_h2.ProjectionY(h_name1)
   tmp_h1_RMS.SetDirectory(0)
   tmp_h1_RMS.Reset()

   # RMS of X in bins of Y
   tmp_h2 = th2s[key]
   for _idx in range(1, 1+tmp_h2.GetNbinsY()):
       _htmp = h2.ProjectionX('_htmp'+str(idx), idx, idx, 'e')
       _htmp.SetDirectory(0)
       tmp_h1_RMS.SetBinContent(_idx, _tmp.GetRMS())
       tmp_h1_RMS.SetBinError(_idx, _tmp.GetRMSError())
       del _tmp

   if key_varX+'_overGEN:'+key_varY:

   h_name2 = key_varX+'_minusGEN_RMSScaledByResponse_wrt_'+key_varY
   if h_name2 in h1s: KILL('aaa '+h_name2)


offlineMETsPuppi_Type1_pt_minusGEN_RMSScaledByResponse_wrt_genMetTrue_pt
