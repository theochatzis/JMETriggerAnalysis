{
//  TFile* f0 = TFile::Open("../../NTuplizers/test/out_HLT_Run3TRK.root");
//  TFile* f1 = TFile::Open("../../NTuplizers/test/out_HLT_Run3TRKWithPU.root");
//
//  TFile* f0 = TFile::Open("output_hltRun3_testTRK_210331_v01/ntuples/HLT_Run3TRK/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU.root");
//  TFile* f1 = TFile::Open("output_hltRun3_testTRK_210331_v01/ntuples/HLT_Run3TRKWithPU/Run3Winter20_QCD_PtFlat15to3000_14TeV_PU.root");

  TFile* f0 = TFile::Open("output_hltRun3_testTRK_210331_v01/ntuples/HLT_Run3TRK/Run3Winter20_VBF_HToInvisible_14TeV_PU.root");
  TFile* f1 = TFile::Open("output_hltRun3_testTRK_210331_v01/ntuples/HLT_Run3TRKWithPU/Run3Winter20_VBF_HToInvisible_14TeV_PU.root");

  TTree* t0 = (TTree*) f0->Get("JMETriggerNTuple/Events");
  TTree* t1 = (TTree*) f1->Get("JMETriggerNTuple/Events");

  t0->SetLineColor(1);
  t0->SetLineWidth(2);

  t1->SetLineColor(2);
  t1->SetLineWidth(2);

  t0->AddFriend(t1, "t1");

//  t0->Scan("hltParticleFlow_pdgId:hltParticleFlow_pt:hltParticleFlow_eta:hltParticleFlow_phi:hltPFPuppi_pt/hltParticleFlow_pt:t1.hltPFPuppi_pt/t1.hltParticleFlow_pt");
}
