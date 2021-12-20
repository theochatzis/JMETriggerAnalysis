#!/usr/bin/env python
import glob
import sys
import ROOT

ROOT.gROOT.SetBatch()

def valid_tfile(path):
    _tfile = ROOT.TFile.Open(path)
    _ret = (_tfile and (not _tfile.IsZombie()) and (not _tfile.TestBit(ROOT.TFile.kRecovered)))
    _tfile.Close()
    return _ret

input_tag = sys.argv[1]

input_files = glob.glob(input_tag+'/job_*/out.root')
output_file = input_tag+'.root'

input_files_max = int(sys.argv[2])

jet_n20 = ROOT.TH1D('jet_n20', 'jet_n20', 15, 0, 15)
jet_n30 = ROOT.TH1D('jet_n30', 'jet_n30', 15, 0, 15)
jet_n40 = ROOT.TH1D('jet_n40', 'jet_n40', 15, 0, 15)

jet_pt = ROOT.TH1D('jet_pt', 'jet_pt', 300, 0, 300)
jet_eta = ROOT.TH1D('jet_eta', 'jet_eta', 100, -5, 5)
jet_phi = ROOT.TH1D('jet_phi', 'jet_phi', 100, -3.1416, 3.1416)
jet_jesc = ROOT.TH1D('jet_jesc', 'jet_jesc', 300, -10, 10)

jet_pt_pos = ROOT.TH1D('jet_pt_pos', 'jet_pt_pos', 300, 0, 300)
jet_eta_pos = ROOT.TH1D('jet_eta_pos', 'jet_eta_pos', 100, -5, 5)
jet_phi_pos = ROOT.TH1D('jet_phi_pos', 'jet_phi_pos', 100, -3.1416, 3.1416)
jet_jesc_pos = ROOT.TH1D('jet_jesc_pos', 'jet_jesc_pos', 300, -10, 10)

jet_pt_neg = ROOT.TH1D('jet_pt_neg', 'jet_pt_neg', 300, 0, 300)
jet_eta_neg = ROOT.TH1D('jet_eta_neg', 'jet_eta_neg', 100, -5, 5)
jet_phi_neg = ROOT.TH1D('jet_phi_neg', 'jet_phi_neg', 100, -3.1416, 3.1416)
jet_jesc_neg = ROOT.TH1D('jet_jesc_neg', 'jet_jesc_neg', 300, -10, 10)

t0 = ROOT.TChain('JMETriggerNTuple/Events')
for _tmp in input_files[:input_files_max]:
    if valid_tfile(_tmp): t0.Add(_tmp)
#    else: print _tmp

t0.SetBranchStatus('*', False)
t0.SetBranchStatus('hltAK4PFJetsCorrected_*', True)

for evt in t0:

    jetn20 = 0
    jetn30 = 0
    jetn40 = 0

    for j_idx in range(len(evt.hltAK4PFJetsCorrected_pt)):
        j_pt = evt.hltAK4PFJetsCorrected_pt[j_idx]
        j_eta = evt.hltAK4PFJetsCorrected_eta[j_idx]
        j_phi = evt.hltAK4PFJetsCorrected_phi[j_idx]
        j_jesc = evt.hltAK4PFJetsCorrected_jesc[j_idx]

        if abs(j_eta) < 5.0:
           if j_pt > 20.: jetn20 += 1
           if j_pt > 30.: jetn30 += 1
           if j_pt > 40.: jetn40 += 1

        jet_pt.Fill(j_pt)
        jet_eta.Fill(j_eta)
        jet_phi.Fill(j_phi)
        jet_jesc.Fill(j_jesc)

        if j_jesc >= 0.:
           jet_pt_pos.Fill(j_pt)
           jet_eta_pos.Fill(j_eta)
           jet_phi_pos.Fill(j_phi)
           jet_jesc_pos.Fill(j_jesc)
        else:
           jet_pt_neg.Fill(j_pt)
           jet_eta_neg.Fill(j_eta)
           jet_phi_neg.Fill(j_phi)
           jet_jesc_neg.Fill(j_jesc)

    jet_n20.Fill(jetn20)
    jet_n30.Fill(jetn30)
    jet_n40.Fill(jetn40)

#h0 = ROOT.TH1D('h0', 'h0', 120, 0, 3)
#h1 = ROOT.TH1D('h1', 'h1', 120, 0, 3)
#
#t0.Draw(draw_var+'>>h0', '', 'goff')
#t1.Draw(draw_var+'>>h1', '', 'goff')
#
#h0.SetLineColor(1)
#h1.SetLineColor(2)
#
#h0.Draw('hist,e0')
#h1.Draw('hist,e0,same')

ofile = ROOT.TFile(output_file, 'recreate')

jet_n20.Write()
jet_n30.Write()
jet_n40.Write()

jet_pt.Write()
jet_eta.Write()
jet_phi.Write()
jet_jesc.Write()

jet_pt_pos.Write()
jet_eta_pos.Write()
jet_phi_pos.Write()
jet_jesc_pos.Write()

jet_pt_neg.Write()
jet_eta_neg.Write()
jet_phi_neg.Write()
jet_jesc_neg.Write()

ofile.Close()
