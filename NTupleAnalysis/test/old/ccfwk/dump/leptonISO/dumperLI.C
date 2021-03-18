#define dumperLI_cxx
// The class definition in dumperLI.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.

// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// Root > T->Process("dumperLI.C")
// Root > T->Process("dumperLI.C","some options")
// Root > T->Process("dumperLI.C+")
//

#include "dumperLI.h"
#include <TStyle.h>
#include <cmath>
#include <iostream>

void dumperLI::Begin(TTree * /*tree*/){
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

  return;
}

void dumperLI::addTH1F(TH1F** h, const std::string& name, const int xbin, const float xmin, const float xmax){

  *h = new TH1F(name.c_str(), name.c_str(), xbin, xmin, xmax);
  (*h)->SetDirectory(0);
  fOutput->Add(*h);

  return;
}

void dumperLI::addTH2F(TH2F** h, const std::string& name, const int xbin, const float xmin, const float xmax, const int ybin, const float ymin, const float ymax){

  *h = new TH2F(name.c_str(), name.c_str(), xbin, xmin, xmax, ybin, ymin, ymax);
  (*h)->SetDirectory(0);
  fOutput->Add(*h);

  return;
}

void dumperLI::SlaveBegin(TTree * /*tree*/){
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

  TString option = GetOption();

  addTH1F(&h_lep1_pt , "lep1_pt" , 360, 0, 1800);
  addTH1F(&h_lep1_eta, "lep1_eta", 60, -3, 3);
  addTH1F(&h_nPV, "nPV", 60, 0, 60);
  addTH1F(&h_MET, "MET", 360, 0, 1800);
  addTH1F(&h_HTlep, "HTlep", 360, 0, 3600);

  // 2D-cut
  addTH2F(&h_lep1_pt__vs__lep1_pTrel_dR010 , "lep1_pt__vs__lep1_pTrel_dR010" , 360, 0, 1800, 60, 0, 300);
  addTH2F(&h_lep1_eta__vs__lep1_pTrel_dR010, "lep1_eta__vs__lep1_pTrel_dR010", 60, -3, 3, 60, 0, 300);
  addTH2F(&h_lep1_nPV__vs__lep1_pTrel_dR010, "lep1_nPV__vs__lep1_pTrel_dR010", 60, 0, 60, 60, 0, 300);

  addTH2F(&h_lep1_pt__vs__lep1_pTrel_dR020, "lep1_pt__vs__lep1_pTrel_dR020", 360, 0, 1800, 60, 0, 300);
  addTH2F(&h_lep1_eta__vs__lep1_pTrel_dR020, "lep1_eta__vs__lep1_pTrel_dR020", 60, -3, 3, 60, 0, 300);
  addTH2F(&h_lep1_nPV__vs__lep1_pTrel_dR020, "lep1_nPV__vs__lep1_pTrel_dR020", 60, 0, 60, 60, 0, 300);

  addTH2F(&h_lep1_pt__vs__lep1_pTrel_dR030, "lep1_pt__vs__lep1_pTrel_dR030", 360, 0, 1800, 60, 0, 300);
  addTH2F(&h_lep1_eta__vs__lep1_pTrel_dR030, "lep1_eta__vs__lep1_pTrel_dR030", 60, -3, 3, 60, 0, 300);
  addTH2F(&h_lep1_nPV__vs__lep1_pTrel_dR030, "lep1_nPV__vs__lep1_pTrel_dR030", 60, 0, 60, 60, 0, 300);

  addTH2F(&h_lep1_pt__vs__lep1_pTrel_dR040, "lep1_pt__vs__lep1_pTrel_dR040", 360, 0, 1800, 60, 0, 300);
  addTH2F(&h_lep1_eta__vs__lep1_pTrel_dR040, "lep1_eta__vs__lep1_pTrel_dR040", 60, -3, 3, 60, 0, 300);
  addTH2F(&h_lep1_nPV__vs__lep1_pTrel_dR040, "lep1_nPV__vs__lep1_pTrel_dR040", 60, 0, 60, 60, 0, 300);

  // R010
  addTH2F(&h_lep1_pt__vs__lep1_R010iso_dbeta , "lep1_pt__vs__lep1_R010iso_dbeta" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_R010iso_dbeta, "lep1_eta__vs__lep1_R010iso_dbeta", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_R010iso_dbeta, "lep1_nPV__vs__lep1_R010iso_dbeta", 60, 0, 60, 240, 0, 1.2);

  addTH2F(&h_lep1_pt__vs__lep1_R010iso_pfwgt , "lep1_pt__vs__lep1_R010iso_pfwgt" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_R010iso_pfwgt, "lep1_eta__vs__lep1_R010iso_pfwgt", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_R010iso_pfwgt, "lep1_nPV__vs__lep1_R010iso_pfwgt", 60, 0, 60, 240, 0, 1.2);

  // R020
  addTH2F(&h_lep1_pt__vs__lep1_R020iso_dbeta , "lep1_pt__vs__lep1_R020iso_dbeta" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_R020iso_dbeta, "lep1_eta__vs__lep1_R020iso_dbeta", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_R020iso_dbeta, "lep1_nPV__vs__lep1_R020iso_dbeta", 60, 0, 60, 240, 0, 1.2);

  addTH2F(&h_lep1_pt__vs__lep1_R020iso_pfwgt , "lep1_pt__vs__lep1_R020iso_pfwgt" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_R020iso_pfwgt, "lep1_eta__vs__lep1_R020iso_pfwgt", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_R020iso_pfwgt, "lep1_nPV__vs__lep1_R020iso_pfwgt", 60, 0, 60, 240, 0, 1.2);

  // R030
  addTH2F(&h_lep1_pt__vs__lep1_R030iso_dbeta , "lep1_pt__vs__lep1_R030iso_dbeta" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_R030iso_dbeta, "lep1_eta__vs__lep1_R030iso_dbeta", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_R030iso_dbeta, "lep1_nPV__vs__lep1_R030iso_dbeta", 60, 0, 60, 240, 0, 1.2);

  addTH2F(&h_lep1_pt__vs__lep1_R030iso_pfwgt , "lep1_pt__vs__lep1_R030iso_pfwgt" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_R030iso_pfwgt, "lep1_eta__vs__lep1_R030iso_pfwgt", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_R030iso_pfwgt, "lep1_nPV__vs__lep1_R030iso_pfwgt", 60, 0, 60, 240, 0, 1.2);

  // MINI
  addTH2F(&h_lep1_pt__vs__lep1_MINIiso_dbeta , "lep1_pt__vs__lep1_MINIiso_dbeta" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_MINIiso_dbeta, "lep1_eta__vs__lep1_MINIiso_dbeta", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_MINIiso_dbeta, "lep1_nPV__vs__lep1_MINIiso_dbeta", 60, 0, 60, 240, 0, 1.2);

  addTH2F(&h_lep1_pt__vs__lep1_MINIiso_pfwgt , "lep1_pt__vs__lep1_MINIiso_pfwgt" , 360, 0, 1800, 240, 0, 1.2);
  addTH2F(&h_lep1_eta__vs__lep1_MINIiso_pfwgt, "lep1_eta__vs__lep1_MINIiso_pfwgt", 60, -3, 3, 240, 0, 1.2);
  addTH2F(&h_lep1_nPV__vs__lep1_MINIiso_pfwgt, "lep1_nPV__vs__lep1_MINIiso_pfwgt", 60, 0, 60, 240, 0, 1.2);

  return;
}

Bool_t dumperLI::Process(Long64_t entry){
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // It can be passed to either dumperLI::GetEntry() or TBranch::GetEntry()
   // to read either all or the required parts of the data. When processing
   // keyed objects with PROOF, the object is already loaded and is available
   // via the fObject pointer.
   //
   // This function should contain the "body" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

  fChain->GetTree()->GetEntry(entry);

  if(channel_ == "muon"){
    if(!(MUO_ == 1 && ELE_ == 0)) return 0;
    if(!(fabs(lep1_pdgID) == 13)) return 0;
  }
  else if(channel_ == "elec"){
    if(!(MUO_ == 0 && ELE_ == 1)) return 0;
    if(!(fabs(lep1_pdgID) == 11)) return 0;
  }
  else std::abort();

  const float pt    = lep1_pt;
  const float eta   = (fabs(lep1_pdgID) == 13) ? lep1_eta : lep1_scEta;
  const int   nPV   = EVT_nPV[0];
  const float MET   = MET_pt[0];
  const float HTlep = MET_pt[0] + lep1_pt;

  std::vector<TLorentzVector> JETS_AK4;
  int jetN_pt030_eta2p4(0), jetN_pt050_eta2p4(0), jetN_pt200_eta2p4(0);
  for(int j=0; j<JET_AK4_; ++j){

    bool cond_2dcut_jet = JET_AK4_pt[j] > 50. && fabs(JET_AK4_eta[j]) < 2.4;

    if(cond_2dcut_jet){
      TLorentzVector tlv;
      tlv.SetPtEtaPhiM(JET_AK4_pt[j], JET_AK4_eta[j], JET_AK4_phi[j], JET_AK4_M[j]);
      JETS_AK4.push_back(tlv);
    }

    if(JET_AK4_pt[j] >  30. && fabs(JET_AK4_eta[j]) < 2.4) ++jetN_pt030_eta2p4;
    if(JET_AK4_pt[j] >  50. && fabs(JET_AK4_eta[j]) < 2.4) ++jetN_pt050_eta2p4;
    if(JET_AK4_pt[j] > 200. && fabs(JET_AK4_eta[j]) < 2.4) ++jetN_pt200_eta2p4;
  }

  if(!(jetN_pt050_eta2p4 >= 2)) return 0;
  if(!(jetN_pt200_eta2p4 >= 1)) return 0;
  if(!(MET    >  50.)) return 0;
  if(!(HTlep  > 150.)) return 0;

  h_lep1_pt->Fill(pt);
  h_lep1_eta->Fill(eta);
  h_nPV->Fill(nPV);
  h_MET->Fill(MET);
  h_HTlep->Fill(HTlep);

  // iso
  const float isoR010_dbeta = (lep1_R010_CH_stand + fmaxf(0., lep1_R010_NH_stand+lep1_R010_Ph_stand-.5*lep1_R010_PU_stand)) / pt;
  const float isoR020_dbeta = (lep1_R020_CH_stand + fmaxf(0., lep1_R020_NH_stand+lep1_R020_Ph_stand-.5*lep1_R020_PU_stand)) / pt;
  const float isoR030_dbeta = (lep1_R030_CH_stand + fmaxf(0., lep1_R030_NH_stand+lep1_R030_Ph_stand-.5*lep1_R030_PU_stand)) / pt;
  const float isoMINI_dbeta = (lep1_MINI_CH_stand + fmaxf(0., lep1_MINI_NH_stand+lep1_MINI_Ph_stand-.5*lep1_MINI_PU_stand)) / pt;

  h_lep1_pt__vs__lep1_R010iso_dbeta ->Fill(pt,  isoR010_dbeta);
  h_lep1_eta__vs__lep1_R010iso_dbeta->Fill(eta, isoR010_dbeta);
  h_lep1_nPV__vs__lep1_R010iso_dbeta->Fill(nPV, isoR010_dbeta);

  h_lep1_pt__vs__lep1_R020iso_dbeta ->Fill(pt,  isoR020_dbeta);
  h_lep1_eta__vs__lep1_R020iso_dbeta->Fill(eta, isoR020_dbeta);
  h_lep1_nPV__vs__lep1_R020iso_dbeta->Fill(nPV, isoR020_dbeta);

  h_lep1_pt__vs__lep1_R030iso_dbeta ->Fill(pt,  isoR030_dbeta);
  h_lep1_eta__vs__lep1_R030iso_dbeta->Fill(eta, isoR030_dbeta);
  h_lep1_nPV__vs__lep1_R030iso_dbeta->Fill(nPV, isoR030_dbeta);

  h_lep1_pt__vs__lep1_MINIiso_dbeta ->Fill(pt,  isoMINI_dbeta);
  h_lep1_eta__vs__lep1_MINIiso_dbeta->Fill(eta, isoMINI_dbeta);
  h_lep1_nPV__vs__lep1_MINIiso_dbeta->Fill(nPV, isoMINI_dbeta);

  const float isoR010_pfwgt = (lep1_R010_CH_stand + lep1_R010_NH_pfwgt+lep1_R010_Ph_pfwgt) / pt;
  const float isoR020_pfwgt = (lep1_R020_CH_stand + lep1_R020_NH_pfwgt+lep1_R020_Ph_pfwgt) / pt;
  const float isoR030_pfwgt = (lep1_R030_CH_stand + lep1_R030_NH_pfwgt+lep1_R030_Ph_pfwgt) / pt;
  const float isoMINI_pfwgt = (lep1_MINI_CH_stand + lep1_MINI_NH_pfwgt+lep1_MINI_Ph_pfwgt) / pt;

  h_lep1_pt__vs__lep1_R010iso_pfwgt ->Fill(pt,  isoR010_pfwgt);
  h_lep1_eta__vs__lep1_R010iso_pfwgt->Fill(eta, isoR010_pfwgt);
  h_lep1_nPV__vs__lep1_R010iso_pfwgt->Fill(nPV, isoR010_pfwgt);

  h_lep1_pt__vs__lep1_R020iso_pfwgt ->Fill(pt,  isoR020_pfwgt);
  h_lep1_eta__vs__lep1_R020iso_pfwgt->Fill(eta, isoR020_pfwgt);
  h_lep1_nPV__vs__lep1_R020iso_pfwgt->Fill(nPV, isoR020_pfwgt);

  h_lep1_pt__vs__lep1_R030iso_pfwgt ->Fill(pt,  isoR030_pfwgt);
  h_lep1_eta__vs__lep1_R030iso_pfwgt->Fill(eta, isoR030_pfwgt);
  h_lep1_nPV__vs__lep1_R030iso_pfwgt->Fill(nPV, isoR030_pfwgt);

  h_lep1_pt__vs__lep1_MINIiso_pfwgt ->Fill(pt,  isoMINI_pfwgt);
  h_lep1_eta__vs__lep1_MINIiso_pfwgt->Fill(eta, isoMINI_pfwgt);
  h_lep1_nPV__vs__lep1_MINIiso_pfwgt->Fill(nPV, isoMINI_pfwgt);

  // 2D-cut
  TLorentzVector lepton;
  if     (fabs(lep1_pdgID) == 13) lepton.SetPtEtaPhiM(MUO_pt[0], MUO_eta[0], MUO_phi[0], MUO_M[0]);
  else if(fabs(lep1_pdgID) == 11) lepton.SetPtEtaPhiM(ELE_pt[0], ELE_eta[0], ELE_phi[0], ELE_M[0]);

  const float dR_min = dRmin(lepton, JETS_AK4);
  const float pT_rel = pTrel(lepton, JETS_AK4);

  const float pTrel_dR010 = (dR_min > 0.1) ? 9999. : pT_rel;
  const float pTrel_dR020 = (dR_min > 0.2) ? 9999. : pT_rel;
  const float pTrel_dR030 = (dR_min > 0.3) ? 9999. : pT_rel;
  const float pTrel_dR040 = (dR_min > 0.4) ? 9999. : pT_rel;

  h_lep1_pt__vs__lep1_pTrel_dR010 ->Fill(pt,  pTrel_dR010);
  h_lep1_eta__vs__lep1_pTrel_dR010->Fill(eta, pTrel_dR010);
  h_lep1_nPV__vs__lep1_pTrel_dR010->Fill(nPV, pTrel_dR010);

  h_lep1_pt__vs__lep1_pTrel_dR020 ->Fill(pt,  pTrel_dR020);
  h_lep1_eta__vs__lep1_pTrel_dR020->Fill(eta, pTrel_dR020);
  h_lep1_nPV__vs__lep1_pTrel_dR020->Fill(nPV, pTrel_dR020);

  h_lep1_pt__vs__lep1_pTrel_dR030 ->Fill(pt,  pTrel_dR030);
  h_lep1_eta__vs__lep1_pTrel_dR030->Fill(eta, pTrel_dR030);
  h_lep1_nPV__vs__lep1_pTrel_dR030->Fill(nPV, pTrel_dR030);

  h_lep1_pt__vs__lep1_pTrel_dR040 ->Fill(pt,  pTrel_dR040);
  h_lep1_eta__vs__lep1_pTrel_dR040->Fill(eta, pTrel_dR040);
  h_lep1_nPV__vs__lep1_pTrel_dR040->Fill(nPV, pTrel_dR040);

  return kTRUE;
}

float dumperLI::dRmin(const TLorentzVector& v1, const std::vector<TLorentzVector>& v2s){

  float minDR(-1.);
  for(unsigned int i=0; i<v2s.size(); ++i){

    float dr(v1.DeltaR(v2s.at(i)));
    if(!i || dr < minDR){ minDR = dr; }
  }

  if(minDR == -1.) std::abort();

  return minDR;
}

float dumperLI::pTrel(const TLorentzVector& v1, const std::vector<TLorentzVector>& v2s){

  float minDR(-1.), ptrel(-1.);
  for(unsigned int i=0; i<v2s.size(); ++i){

    float dr(v1.DeltaR(v2s.at(i)));
    if(!i || dr < minDR){ minDR = dr; ptrel = v1.P() * sin(v1.Angle(v2s.at(i).Vect())); }
  }

  if(minDR == -1. || ptrel == -1.) std::abort();

  return ptrel;
}

void dumperLI::SlaveTerminate(){
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.

  return;
}

void dumperLI::Terminate(){
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

//  std::string oprex_ = "/home/mm/phd/analysis/Z1.tt.ljets_13TeV/work/ttbsm_ljets/filebox/nak/leptonISO/";
//  std::string ofile_ = "dump/dump_LI.MC.Zp_M3000w01p__phys14_pu20bx25.root";

  TFile ofile(output_file_.c_str(), "recreate");
  fOutput->Write();
  ofile.Close();

  return;
}
