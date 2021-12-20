import ROOT

if True:
  ROOT.gROOT.SetBatch()

  f0 = ROOT.TFile.Open('output_hltRun3_testTRK_210331_v01/ntuples/HLT_Run3TRK/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU.root')
  f1 = ROOT.TFile.Open('output_hltRun3_testTRK_210331_v01/ntuples/HLT_Run3TRKWithPU/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

#  t0.AddFriend(t1, 't1')

#  t0.Scan('hltParticleFlow_pdgId:hltParticleFlow_pt:hltParticleFlow_eta:hltParticleFlow_phi:hltPFPuppi_pt/hltParticleFlow_pt:t1.hltPFPuppi_pt/t1.hltParticleFlow_pt')
  # -----------------------------------------------

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';Number of hltVerticesPF;Events', 30, 0, 30)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltVerticesPF_z@.size()>>h0', '', 'goff')

  h1 = ROOT.TH1D('h1', ';Number of hltVerticesPF;Events', 30, 0, 30)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltVerticesPF_z@.size()>>h1', '', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy()

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltVerticesPF_n.pdf')
  c0.Close()
  # -----------------------------------------------

  f0 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRK.root')
  f1 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRKWithPU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';PUPPI weight;Entries', 100, 0, 1)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltPFPuppi_pt/hltParticleFlow_pt>>h0', 'hltPFPuppi_pt>-0.00001', 'goff')

  h1 = ROOT.TH1D('h1', ';PUPPI weight;Entries', 100, 0, 1)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltPFPuppi_pt/hltParticleFlow_pt>>h1', 'hltPFPuppi_pt>-0.00001', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy()

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltPFPuppi_weight.pdf')
  c0.Close()
  # -----------------------------------------------

  f0 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRK.root')
  f1 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRKWithPU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';Number of PFCands;Events', 40, 0, 4000)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltParticleFlow_pt@.size()>>h0', '', 'goff')

  h1 = ROOT.TH1D('h1', ';Number of PFCands;Events', 40, 0, 4000)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltParticleFlow_pt@.size()>>h1', '', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy(0)

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltParticleFlow_n.pdf')
  c0.Close()
  # -----------------------------------------------

  f0 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRK.root')
  f1 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRKWithPU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';hltParticleFlow p_{T} [GeV];Entries', 100, 0, 10)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltParticleFlow_pt>>h0', '', 'goff')

  h1 = ROOT.TH1D('h1', ';hltParticleFlow p_{T} [GeV];Entries', 100, 0, 10)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltParticleFlow_pt>>h1', '', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy(1)

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltParticleFlow_pt.pdf')
  c0.Close()
  # -----------------------------------------------

  f0 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRK.root')
  f1 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRKWithPU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';hltParticleFlow #eta;Entries', 100, -5, 5)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltParticleFlow_eta>>h0', '', 'goff')

  h1 = ROOT.TH1D('h1', ';hltParticleFlow #eta;Entries', 100, -5, 5)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltParticleFlow_eta>>h1', '', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy(0)

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltParticleFlow_eta.pdf')
  c0.Close()
  # -----------------------------------------------

  f0 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRK.root')
  f1 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRKWithPU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';hltPFPuppi p_{T} [GeV];Entries', 100, 0, 10)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltPFPuppi_pt>>h0', 'hltPFPuppi_pt>0.00001', 'goff')

  h1 = ROOT.TH1D('h1', ';hltPFPuppi p_{T} [GeV];Entries', 100, 0, 10)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltPFPuppi_pt>>h1', 'hltPFPuppi_pt>0.00001', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy(1)

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltPFPuppi_pt.pdf')
  c0.Close()
  # -----------------------------------------------

  f0 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRK.root')
  f1 = ROOT.TFile.Open('../../NTuplizers/test/out_HLT_Run3TRKWithPU.root')

  t0 = f0.Get('JMETriggerNTuple/Events')
  t1 = f1.Get('JMETriggerNTuple/Events')

  c0 = ROOT.TCanvas('c0', 'c0', 800, 600)
  c0.SetTopMargin(0.10)
  c0.SetLeftMargin(0.12)
  c0.SetRightMargin(0.03)
  c0.SetBottomMargin(0.10)

  h0 = ROOT.TH1D('h0', ';hltPFPuppi #eta;Entries', 100, -5, 5)
  h0.SetStats(0)
  h0.SetLineColor(ROOT.kBlue)
  h0.SetLineWidth(2)
  t0.Draw('hltPFPuppi_eta>>h0', 'hltPFPuppi_pt>0.00001', 'goff')

  h1 = ROOT.TH1D('h1', ';hltPFPuppi #eta;Entries', 100, -5, 5)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kGreen+1)
  h1.SetLineWidth(2)
  t1.Draw('hltPFPuppi_eta>>h1', 'hltPFPuppi_pt>0.00001', 'goff')

  c0.cd()
  h0.Draw('hist,e0')
  h1.Draw('hist,e0,same')
  h0.GetXaxis().SetTitleOffset(1.1 * h0.GetXaxis().GetTitleOffset())
  c0.SetLogy(0)

  leg = ROOT.TLegend(0.60, 0.75, 0.90, 0.95)
  leg.AddEntry(h0, 'HLT Run-3 TRK', 'le')
  leg.AddEntry(h1, 'HLT Run-3 TRK-WithPU', 'le')
  leg.Draw('same')

  c0.SaveAs('hltPFPuppi_eta.pdf')
  c0.Close()
  # -----------------------------------------------
