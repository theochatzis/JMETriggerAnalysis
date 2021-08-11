#include <inc/HFolderBASE.h>
#include <inc/utils.h>

#include <iostream>
#include <sstream>
#include <iomanip>

nak::HFolderBASE::HFolderBASE(TFile& file, const std::string& dname){

  name_ = dname;

  d0 = (name_ == "") ? ((TDirectory*) &file) : file.mkdir(name_.c_str());
}

nak::HFolderBASE::~HFolderBASE(){

//  Clear();
}

void nak::HFolderBASE::book_TH1F(const std::string& name_, const int xnbins_, const float xmin_, const float xmax_){

  if(h1.find(name_) != h1.end()) util::KILL("HFolderBASE::book_TH1F -- already existing histogram key: "+name_);
  else {

    h1[name_] = new TH1F(name_.c_str(), name_.c_str(), xnbins_, xmin_, xmax_);
    h1[name_]->SetDirectory(d0);

    key_v.push_back(name_);
  }

  return;
}

void nak::HFolderBASE::book_TH2F(const std::string& name_, const int xnbins_, const float xmin_, const float xmax_, const int ynbins_, const float ymin_, const float ymax_){

  if(h2.find(name_) != h2.end()) util::KILL("HFolderBASE::book_TH2F -- already existing histogram key: "+name_);
  else {

    h2[name_] = new TH2F(name_.c_str(), name_.c_str(), xnbins_, xmin_, xmax_, ynbins_, ymin_, ymax_);
    h2[name_]->SetDirectory(d0);

    key_v.push_back(name_);
  }

  return;
}

TH1F* nak::HFolderBASE::H1(const std::string& key_){

  TH1F* h(0);

  if(h1.find(key_) != h1.end()) h = h1[key_];
  else util::KILL("HFolderBASE::H1 -- histogram key not found: "+key_);

  return h;
}

TH2F* nak::HFolderBASE::H2(const std::string& key_){

  TH2F* h(0);

  if(h2.find(key_) != h2.end()) h = h2[key_];
  else util::KILL("HFolderBASE::H2 -- histogram key not found: "+key_);

  return h;
}

//std::string nak::HFolderBASE::BinWidth(const TH1F& h_){
//
//  double xRange = h_.GetXaxis()->GetXmax() - h_.GetXaxis()->GetXmin();
//  double binw = floor(xRange/h_.GetNbinsX()*100+0.5)/100;
//
//  std::ostringstream sstrm;
//  sstrm << binw;
//  std::string binw_str = sstrm.str();
//
//  return binw_str;
//}

void nak::HFolderBASE::Write(){

  for(unsigned int k=0; k<key_v.size(); ++k){

    d0->cd();

    const std::string& key = key_v.at(k);

    if(h1.find(key) != h1.end()){

      if(!h1[key]->GetSumw2N()) h1[key]->Sumw2();
      h1[key]->Write();
    }

    else if(h2.find(key) != h2.end()){

      if(!h2[key]->GetSumw2N()) h2[key]->Sumw2();
      h2[key]->Write();
    }

    else util::KILL("HFolderBASE::Write() -- no object associated to key: "+key);
  }

  d0->Close();

  return;
}

void nak::HFolderBASE::Clear(){

  key_v.clear();

  for(h1_itr ih1=h1.begin(); ih1!=h1.end(); ++ih1){

    if(ih1->second) delete ih1->second;
    ih1->second = 0;
  }

  for(h2_itr ih2=h2.begin(); ih2!=h2.end(); ++ih2){

    if(ih2->second) delete ih2->second;
    ih2->second = 0;
  }

  return;
}
