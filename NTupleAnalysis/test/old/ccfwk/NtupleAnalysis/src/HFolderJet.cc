#include <inc/HFolderJet.h>
#include <inc/utils.h>

#include <iostream>
#include <sstream>
#include <iomanip>
#include <algorithm>

nak::HFolderJet::HFolderJet(TFile& file, const std::string& dname): HFolderBASE(file, dname) {

  book_TH1F("jetN_pt030", 12, 0, 12);
  book_TH1F("jetN_pt050", 12, 0, 12);
  book_TH1F("jetN_pt100", 12, 0, 12);
  book_TH1F("jetN_pt200", 12, 0, 12);

  book_TH1F("jetN_CSVL", 8, 0, 8);
  book_TH1F("jetN_CSVM", 8, 0, 8);
  book_TH1F("jetN_CSVT", 8, 0, 8);
  book_TH1F("jetN_CSVIVFL", 8, 0, 8);
  book_TH1F("jetN_CSVIVFM", 8, 0, 8);
  book_TH1F("jetN_CSVIVFT", 8, 0, 8);
  book_TH1F("jetN_JPL", 8, 0, 8);
  book_TH1F("jetN_JPM", 8, 0, 8);
  book_TH1F("jetN_JPT", 8, 0, 8);

  book_TH1F("jet1__M", 180, 0, 360);
  book_TH1F("jet1__pt", 900, 0, 1800);
  book_TH1F("jet1__eta", 60, -3, 3);
  book_TH1F("jet1__phi", 60, -3.15, 3.15);
  book_TH1F("jet1__CSV", 80, -2, 2);
  book_TH1F("jet1__CSVIVF", 80, -2, 2);
  book_TH1F("jet1__JP", 60, 0, 3);

  book_TH1F("jet2__M", 120, 0, 240);
  book_TH1F("jet2__pt", 600, 0, 1200);
  book_TH1F("jet2__eta", 60, -3, 3);
  book_TH1F("jet2__phi", 60, -3.15, 3.15);
  book_TH1F("jet2__CSV", 80, -2, 2);
  book_TH1F("jet2__CSVIVF", 80, -2, 2);
  book_TH1F("jet2__JP", 60, 0, 3);

  book_TH1F("jet3__M", 84, 0, 168);
  book_TH1F("jet3__pt", 360, 0, 720);
  book_TH1F("jet3__eta", 60, -3, 3);
  book_TH1F("jet3__phi", 60, -3.15, 3.15);
  book_TH1F("jet3__CSV", 80, -2, 2);
  book_TH1F("jet3__CSVIVF", 80, -2, 2);
  book_TH1F("jet3__JP", 60, 0, 3);

  book_TH1F("jet4__M", 60, 0, 120);
  book_TH1F("jet4__pt", 210, 0, 420);
  book_TH1F("jet4__eta", 60, -3, 3);
  book_TH1F("jet4__phi", 60, -3.15, 3.15);
  book_TH1F("jet4__CSV", 80, -2, 2);
  book_TH1F("jet4__CSVIVF", 80, -2, 2);
  book_TH1F("jet4__JP", 60, 0, 3);

  CSVL_wp = 0.244;
  CSVM_wp = 0.679;
  CSVT_wp = 0.898;

  JPL_wp = 0.275;
  JPM_wp = 0.545;
  JPT_wp = 0.790;
}

void nak::HFolderJet::Fill(const std::vector<xtt::Jet>& jets_, const float w_){

  int jetN_pt030(0), jetN_pt050(0), jetN_pt100(0), jetN_pt200(0);
  int jetN_CSVIVFL(0), jetN_CSVIVFM(0), jetN_CSVIVFT(0);
  int jetN_CSVL(0), jetN_CSVM(0), jetN_CSVT(0);
  int jetN_JPL(0), jetN_JPM(0), jetN_JPT(0);

  for(unsigned int i=0; i<jets_.size(); ++i){

    if(jets_.at(i).pt >  30.) ++jetN_pt030;
    if(jets_.at(i).pt >  50.) ++jetN_pt050;
    if(jets_.at(i).pt > 100.) ++jetN_pt100;
    if(jets_.at(i).pt > 200.) ++jetN_pt200;

    if(jets_.at(i).btagCSVIVF > CSVIVFL_wp) ++jetN_CSVIVFL;
    if(jets_.at(i).btagCSVIVF > CSVIVFM_wp) ++jetN_CSVIVFM;
    if(jets_.at(i).btagCSVIVF > CSVIVFT_wp) ++jetN_CSVIVFT;

    if(jets_.at(i).btagCSV > CSVL_wp) ++jetN_CSVL;
    if(jets_.at(i).btagCSV > CSVM_wp) ++jetN_CSVM;
    if(jets_.at(i).btagCSV > CSVT_wp) ++jetN_CSVT;

    if(jets_.at(i).btagJP  >  JPL_wp) ++jetN_JPL;
    if(jets_.at(i).btagJP  >  JPM_wp) ++jetN_JPM;
    if(jets_.at(i).btagJP  >  JPT_wp) ++jetN_JPT;
  }

  H1("jetN_pt030")->Fill(jetN_pt030, w_);
  H1("jetN_pt050")->Fill(jetN_pt050, w_);
  H1("jetN_pt100")->Fill(jetN_pt100, w_);
  H1("jetN_pt200")->Fill(jetN_pt200, w_);

  H1("jetN_CSVIVFL")->Fill(jetN_CSVIVFL, w_);
  H1("jetN_CSVIVFM")->Fill(jetN_CSVIVFM, w_);
  H1("jetN_CSVIVFT")->Fill(jetN_CSVIVFT, w_);

  H1("jetN_CSVL")->Fill(jetN_CSVL, w_);
  H1("jetN_CSVM")->Fill(jetN_CSVM, w_);
  H1("jetN_CSVT")->Fill(jetN_CSVT, w_);

  H1("jetN_JPL") ->Fill(jetN_JPL, w_);
  H1("jetN_JPM") ->Fill(jetN_JPM, w_);
  H1("jetN_JPT") ->Fill(jetN_JPT, w_);

  for(int i=0; i<std::min(3, int(jets_.size())); ++i){

    std::stringstream idx;
    idx << i+1;

    H1("jet"+idx.str()+"__M")->Fill(jets_.at(i).M, w_);
    H1("jet"+idx.str()+"__pt")->Fill(jets_.at(i).pt, w_);
    H1("jet"+idx.str()+"__eta")->Fill(jets_.at(i).eta, w_);
    H1("jet"+idx.str()+"__phi")->Fill(jets_.at(i).phi, w_);
    H1("jet"+idx.str()+"__CSVIVF")->Fill(jets_.at(i).btagCSVIVF, w_);
    H1("jet"+idx.str()+"__CSV")->Fill(jets_.at(i).btagCSV, w_);
    H1("jet"+idx.str()+"__JP")->Fill(jets_.at(i).btagJP, w_);
  }

  return;
}
