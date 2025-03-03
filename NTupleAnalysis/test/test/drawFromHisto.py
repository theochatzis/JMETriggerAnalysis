import glob
import ROOT

ROOT.gROOT.SetBatch()
hists = []
canvas = ROOT.TCanvas()
canvas.SetLogy()
hn = None

#files = sorted(glob.glob('Desktop/output_run3trkSingleTrkIterV01_harvesting/HLT*/Run3Winter20_DYToLL_M50_14TeV.root'))
#postfix = ''

files = sorted(glob.glob('Desktop/output_run3trkSingleTrkIterV01_harvesting/HLT*/Run3Winter20_VBF*14TeV.root'))
postfix = '_overGEN'

#offline = 'offlinePFMET_Raw'
offline = 'offlinePuppiMET_Raw'

#algo = 'PF'
#algo = 'PFCHSv1'
#algo = 'PFCHSv2'
#algo = 'PuppiV1'
#algo = 'PuppiV2'
#algo = 'PuppiV3'
algo = 'PuppiV4'

plots = [
  (files[0], 'NoSelection/'+offline+'_pt'+postfix, ROOT.kPink+1),
  (files[0], 'NoSelection/hlt'+algo+'MET_pt'  +postfix, 1),
  (files[1], 'NoSelection/hlt'+algo+'MET_pt'  +postfix, 2),
  (files[2], 'NoSelection/hlt'+algo+'MET_pt'  +postfix, 3),
  (files[3], 'NoSelection/hlt'+algo+'MET_pt'  +postfix, 4),
]

index = 0
for _tmp in plots:
    print _tmp
    index += 1
    tfile = ROOT.TFile.Open(_tmp[0])
    h00 = tfile.Get(_tmp[1])
    h0 = h00.Clone()
    h0.SetDirectory(0)
    h0.SetLineColor(_tmp[2])
    if not hn:
       hn = h00.Clone()
       hn.SetDirectory(0)
#    h0.Divide(hn)
    h0.Draw('hist,e0'+(index != 1)*',same')
    hists.append(h0)
    tfile.Close()
canvas.SaveAs('tmp.root')
canvas.Close()
