#include <inc/HFolderLepton.h>
#include <inc/utils.h>

#include <iostream>
#include <sstream>
#include <iomanip>

nak::HFolderLepton::HFolderLepton(TFile& file, const std::string& dname): HFolderBASE(file, dname){

  book_TH1F("pt", 500, 0, 500);
  book_TH1F("eta", 52, -2.6, 2.6);
  book_TH1F("etaSC", 52, -2.6, 2.6);
  book_TH1F("phi", 66, -3.3, 3.3);
  book_TH1F("PFIso", 200, 0, 2);
}

void nak::HFolderLepton::Fill(const xtt::Lepton& lepton_, const float w_){

  H1("pt")->Fill(lepton_.pt, w_);
  H1("eta")->Fill(lepton_.eta, w_);
//!!  H1("etaSC")->Fill(lepton_.scEta, w_);
  H1("phi")->Fill(lepton_.phi, w_);
//!!  H1("PFIso")->Fill(lepton_.PFIso, w_);

  return;
}
