#!/usr/bin/env python
import glob
import ROOT

def valid_tfile(path):
    _tfile = ROOT.TFile.Open(path)
    _ret = (_tfile and (not _tfile.IsZombie()) and (not _tfile.TestBit(ROOT.TFile.kRecovered)))
    _tfile.Close()
    return _ret

max_files = 1000

#draw_var = 'hltPFMET_pt/genMetTrue_pt'
#draw_var = 'hltPFMETTypeOne_pt/genMetTrue_pt'
#draw_var = 'hltPuppiMET_pt/genMetTrue_pt'
draw_var = 'hltPuppiMETTypeOne_pt/genMetTrue_pt'

t0 = ROOT.TChain('JMETriggerNTuple/Events')
for _tmp in glob.glob('out_prod_v04/VBF_HToInvisible_M125_14TeV_PU200/job_*/out.root')[:max_files]:
    if valid_tfile(_tmp): t0.Add(_tmp)
    else: print _tmp

t1 = ROOT.TChain('JMETriggerNTuple/Events')
for _tmp in glob.glob('out_prod_v05/VBF_HToInvisible_M125_14TeV_PU200/job_*/out.root')[:max_files]:
    if valid_tfile(_tmp): t1.Add(_tmp)
    else: print _tmp

h0 = ROOT.TH1D('h0', 'h0', 120, 0, 3)
h1 = ROOT.TH1D('h1', 'h1', 120, 0, 3)

t0.Draw(draw_var+'>>h0', '', 'goff')
t1.Draw(draw_var+'>>h1', '', 'goff')

h0.SetLineColor(1)
h1.SetLineColor(2)

h0.Draw('hist,e0')
h1.Draw('hist,e0,same')
