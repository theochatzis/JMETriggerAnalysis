#include <inc/HFolderXObj.h>
#include <inc/utils.h>

#include <iostream>
#include <sstream>
#include <iomanip>

nak::HFolderXObj::HFolderXObj(TFile& file, const std::string& dname): HFolderBASE(file, dname) {

  book_TH1F("weight", 120, -1, 11);
  book_TH1F("nPV", 60, 0, 60);

  book_TH1F("MET_pt", 168, 0, 840);
  book_TH1F("MET_phi", 66, -3.3, 3.3);
  book_TH1F("MET_px", 144, -360, 360);
  book_TH1F("MET_py", 144, -360, 360);
  book_TH1F("HTlep", 210, 0, 2100);
  book_TH1F("HTjet", 210, 0, 2100);
  book_TH1F("HTtot", 300, 0, 3000);

  book_TH1F("minDR_ljet", 50, 0, 5);
  book_TH1F("pTrel_ljet", 150, 0, 150);
  book_TH2F("minDR_VS_pTrel_ljet", 50, 0, 5, 150, 0, 150);
  book_TH2F("MET_VS_dphi_lMET", 60, 0, 300, 32, 0, 3.2);
  book_TH2F("MET_VS_dphi_jMET", 60, 0, 300, 32, 0, 3.2);
  book_TH2F("lep_VS_jet_triangcut", 2, 0, 2, 2, 0, 2);
}

void nak::HFolderXObj::Fill(const int npv_, const xtt::Particle& lepton_, const xtt::MET& met_,
 const std::vector<xtt::Jet>& jets_, const std::vector<xtt::MergedJet>& topjets_, const float w_){

  float dRmin_lj(dRmin      (lepton_, jets_));
  float pTrel_lj(pTrel_dRmin(lepton_, jets_));

  Fill(npv_, lepton_, met_, jets_, topjets_, dRmin_lj, pTrel_lj, w_);

  return;
}

void nak::HFolderXObj::Fill(const int npv_, const xtt::Particle& lepton_, const xtt::MET& met_,
 const std::vector<xtt::Jet>& jets_, const std::vector<xtt::MergedJet>& topjets_, const float minDR_, const float pTrel_, const float w_){

  H1("weight")->Fill(w_);
  H1("nPV")->Fill(npv_, w_);

  H1("MET_pt")->Fill(met_.pt, w_);
  H1("MET_phi")->Fill(met_.phi, w_);
  H1("MET_px")->Fill(met_.px(), w_);
  H1("MET_py")->Fill(met_.py(), w_);

  double HTlep = met_.pt+lepton_.pt;
  H1("HTlep")->Fill(HTlep, w_);

  double HTjet = 0.;
  for(unsigned int i=0; i<jets_.size(); ++i) HTjet += jets_.at(i).pt;
  H1("HTjet")->Fill(HTjet, w_);

  H1("HTtot")->Fill(HTlep+HTjet, w_);

  H1("minDR_ljet")->Fill(minDR_, w_);
  H1("pTrel_ljet")->Fill(pTrel_, w_);
  H2("minDR_VS_pTrel_ljet")->Fill(minDR_, pTrel_, w_);

  if(jets_.size()){

    double dphi_lMET = fabs(met_.p4().DeltaPhi(lepton_.p4()));
    double dphi_jMET = fabs(met_.p4().DeltaPhi(jets_.at(0).p4()));

    double k = 1.5/75.;
    bool tc_l_pass(1), tc_j_pass(1);
    if(dphi_lMET >    k* met_.pt + 1.5) tc_l_pass = 0;
    if(dphi_lMET < -1*k* met_.pt + 1.5) tc_l_pass = 0;
    if(dphi_jMET >    k* met_.pt + 1.5) tc_j_pass = 0;
    if(dphi_jMET < -1*k* met_.pt + 1.5) tc_j_pass = 0;

    H2("MET_VS_dphi_lMET")->Fill(met_.pt, dphi_lMET, w_);
    H2("MET_VS_dphi_jMET")->Fill(met_.pt, dphi_jMET, w_);
    H2("lep_VS_jet_triangcut")->Fill(tc_l_pass, tc_j_pass, w_);
  }

  return;
}
