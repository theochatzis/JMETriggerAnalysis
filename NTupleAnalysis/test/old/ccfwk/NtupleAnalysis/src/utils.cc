#include <inc/utils.h>

#include <iostream>
#include <cstdlib>
#include <string>
#include <sstream>
#include <limits>

void util::KILL(const std::string& log_){

  std::cerr << "@@@ FATAL -- "+log_+"\n";
  std::cerr << "@@@ Stopping execution.\n";
  std::abort();

  return;
}

void util::WARNING(const std::string& log_){

  std::cerr << "@@@ WARNING -- "+log_+"\n";

  return;
}

std::string util::int_to_str(int n){

  std::ostringstream ss;
  ss << n;

  return ss.str();
}

bool util::int_le_ge(int min, int n, int max){

  return (min <= n) && (n <= max);
}

float util::f_infty(){

  return std::numeric_limits<float>::infinity();
}

std::vector<std::string> util::string_tokens(const std::string& str, const std::string& delimiter){

  std::vector<std::string> toks; {

    std::size_t last(0), next(0);
    while((next = str.find(delimiter, last)) != std::string::npos){

      std::string substr = str.substr(last, next-last);
      if(substr != "") toks.push_back(substr);

      last = next + delimiter.size();
    }

    if(str.substr(last) != "") toks.push_back(str.substr(last));
  }

  return toks;
}

std::string util::get_option_from_string(const std::string& opts, const std::string& arg_str){

  std::string val_str("");

  std::vector<std::string> opt_ls = util::string_tokens(opts, " ");
  for(unsigned int i=0; i<opt_ls.size(); ++i){

    const std::string& opt0 = opt_ls.at(i);
    std::vector<std::string> opt0_pair = util::string_tokens(opt0, "=");

    if(opt0_pair.size() == 2){

      std::string arg(opt0_pair.at(0)), val(opt0_pair.at(1));
      if(arg == arg_str) val_str = val;
    }
    else util::KILL("get_option_from_string -- invalid format for option: "+opt0);
  }

  return val_str;
}

// analysis-specific selections

bool lepton_2Dcut(const xtt::Particle& lep_, const std::vector<xtt::Jet>& jets_){

  float dRmin_lj = 0.4;
  float pTrel_lj = 25.;

  return (dRmin(lep_, jets_) > dRmin_lj || pTrel_dRmin(lep_, jets_) > pTrel_lj);
}

bool triangular_cut(const xtt::MET& met_, const xtt::Particle& p_){

  float dphi(fabs(met_.p4().DeltaPhi(p_.p4())));

  float a(1.5), b(75.);

  return (fabs(dphi-a) < (a/b) * met_.pt);
}

bool topjet_tag(const xtt::MergedJet& topj_){

  if(!(topj_.subjets1.size() >= 3)) return false;
  if(!(topj_.M > 140. && topj_.M < 250.)) return false;
  if(!(topjet_mmin(topj_) > 50.)) return false;
  if(!(topj_.Tau3 < .7 * topj_.Tau2)) return false;

  return true;
}

float topjet_mmin(const xtt::MergedJet& topj_){

  float mmin(0.);
  for(unsigned int i=0; i<topj_.subjets1.size(); ++i){
    for(unsigned int j=i+1; j<topj_.subjets1.size(); ++j){

      float mjj = (topj_.subjets1.at(i).p4() + topj_.subjets1.at(j).p4()).M();
      if(mjj < mmin || !(i*j)) mmin = mjj;
    }
  }

  return mmin;
}

float topjet_minDRsubjets(const xtt::MergedJet& topj_){

  float minDR(0.);
  for(unsigned int i=0; i<topj_.subjets1.size(); ++i){
    for(unsigned int j=i+1; j<topj_.subjets1.size(); ++j){

      float dr = topj_.subjets1.at(i).p4().DeltaR(topj_.subjets1.at(j).p4());
      if(dr < minDR || !(i*j)) minDR = dr;
    }
  }

  return minDR;
}

float topjet_max_subjet_btag(const std::string& bdisc_, const xtt::MergedJet& topj_){

  float maxDisc(0.);
  for(unsigned int i=0; i<topj_.subjets1.size(); ++i){

    float disc(0.);
    if(bdisc_ == "CSV") disc = topj_.subjets1.at(i).btagCSV;
    else if(bdisc_ == "JP") disc = topj_.subjets1.at(i).btagJP;
    else util::KILL("topjet_max_subjet_btag() -- undefined label for b-tag discriminator ('CSV' or 'JP'): "+bdisc_);

    if(disc > maxDisc || !i) maxDisc = disc;
  }

  return maxDisc;
}

std::vector<xtt::MergedJet> get_toptag_jets(const std::vector<xtt::MergedJet>& topjets_){

  std::vector<xtt::MergedJet> toptags;

  for(unsigned int i=0; i<topjets_.size(); ++i){

    const xtt::MergedJet& itopj = topjets_.at(i);
    if(topjet_tag(itopj)) toptags.push_back(itopj);
  }

  return toptags;
}

void util::boost_x1_to_x2CM(TLorentzVector& x1, const TLorentzVector& x2){

  if(!x2.E()) return;

  x1.Boost(-x2.Px()/x2.E(), -x2.Py()/x2.E(), -x2.Pz()/x2.E());

  return;
}

float util::cosThetaX(const TLorentzVector& tprod, const TLorentzVector& top, const TLorentzVector& ttbar0){

  TLorentzVector top_in_ttbarCM = top;
  TLorentzVector tprod_in_topCM = tprod;
  TLorentzVector ttbar          = ttbar0;

  util::boost_x1_to_x2CM(top_in_ttbarCM, ttbar);
  util::boost_x1_to_x2CM(tprod_in_topCM, ttbar);
  util::boost_x1_to_x2CM(tprod_in_topCM, top_in_ttbarCM);

  float thetaX = tprod_in_topCM.Angle(top_in_ttbarCM.Vect());

  return cos(thetaX);
}

float util::cosThetaCS(const TLorentzVector& top, const TLorentzVector& ttbar0){

  const float sqrt_s = 13000.;

  TLorentzVector proton1       (         0.,          0.,   .5*sqrt_s,  .5*sqrt_s);
  TLorentzVector proton2       (         0.,          0.,  -.5*sqrt_s,  .5*sqrt_s);
  TLorentzVector top_in_ttbarCM(   top.Px(),    top.Py(),    top.Pz(),    top.E());
  TLorentzVector ttbar         (ttbar0.Px(), ttbar0.Py(), ttbar0.Pz(), ttbar0.E());

  util::boost_x1_to_x2CM(proton1       , ttbar);
  util::boost_x1_to_x2CM(proton2       , ttbar);
  util::boost_x1_to_x2CM(top_in_ttbarCM, ttbar);

  float thetaCS = top_in_ttbarCM.Angle((proton1+proton2).Vect());

  return cos(thetaCS);
}
