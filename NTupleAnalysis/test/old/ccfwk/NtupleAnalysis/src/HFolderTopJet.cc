#include <inc/HFolderTopJet.h>
#include <inc/utils.h>

#include <iostream>
#include <sstream>
#include <iomanip>

nak::HFolderTopJet::HFolderTopJet(TFile& file, const std::string& dname): HFolderBASE(file, dname) {

  book_TH1F("nJet", 12, 0, 12);
  book_TH1F("nCSVL", 8, 0, 8);
  book_TH1F("nCSVM", 8, 0, 8);
  book_TH1F("nCSVT", 8, 0, 8);
  book_TH1F("nJPL", 8, 0, 8);
  book_TH1F("nJPM", 8, 0, 8);
  book_TH1F("nJPT", 8, 0, 8);

  book_TH1F("M_1", 180, 0, 360);
  book_TH1F("Msd_1", 180, 0, 360);
  book_TH1F("Mmin_1", 120, 0, 240);
  book_TH1F("pt_1", 900, 0, 1800);
  book_TH1F("eta_1", 52, -2.6, 2.6);
  book_TH1F("phi_1", 66, -3.3, 3.3);
  book_TH1F("CSV_1", 80, -2, 2);
  book_TH1F("JP_1", 60, 0, 3);
  book_TH1F("tau2_1", 40, 0, 2);
  book_TH1F("tau3_1", 40, 0, 2);
  book_TH1F("tau32_1", 40, 0, 2);
  book_TH1F("nSubjet_1", 6, 0, 6);
  book_TH1F("istagged_1", 2, 0, 2);

  book_TH1F("M_2", 120, 0, 240);
  book_TH1F("Msd_2", 120, 0, 240);
  book_TH1F("Mmin_2", 120, 0, 240);
  book_TH1F("pt_2", 600, 0, 1200);
  book_TH1F("eta_2", 52, -2.6, 2.6);
  book_TH1F("phi_2", 66, -3.3, 3.3);
  book_TH1F("CSV_2", 80, -2, 2);
  book_TH1F("JP_2", 60, 0, 3);
  book_TH1F("tau2_2", 40, 0, 2);
  book_TH1F("tau3_2", 40, 0, 2);
  book_TH1F("tau32_2", 40, 0, 2);
  book_TH1F("nSubjet_2", 6, 0, 6);
  book_TH1F("istagged_2", 2, 0, 2);

  book_TH1F("M_tag1", 180, 0, 360);
  book_TH1F("Msd_tag1", 180, 0, 360);
  book_TH1F("Mmin_tag1", 120, 0, 240);
  book_TH1F("pt_tag1", 900, 0, 1800);
  book_TH1F("eta_tag1", 52, -2.6, 2.6);
  book_TH1F("phi_tag1", 66, -3.3, 3.3);
  book_TH1F("CSV_tag1", 80, -2, 2);
  book_TH1F("JP_tag1", 60, 0, 3);
  book_TH1F("CSVmax_sj_tag1", 80, -2, 2);
  book_TH1F("JPmax_sj_tag1", 60, 0, 3);
  book_TH1F("tau2_tag1", 40, 0, 2);
  book_TH1F("tau3_tag1", 40, 0, 2);
  book_TH1F("tau32_tag1", 40, 0, 2);
  book_TH1F("nSubjet_tag1", 6, 0, 6);
  book_TH1F("minDRsj_tag1", 30, 0, 3);
  book_TH1F("M_sj1_tag1", 120, 0, 240);
  book_TH1F("pt_sj1_tag1", 240, 0, 960);
  book_TH1F("eta_sj1_tag1", 52, -2.6, 2.6);
  book_TH1F("CSV_sj1_tag1", 80, -2, 2);
  book_TH1F("JP_sj1_tag1", 60, 0, 3);
  book_TH1F("M_sj2_tag1", 120, 0, 240);
  book_TH1F("pt_sj2_tag1", 120, 0, 480);
  book_TH1F("eta_sj2_tag1", 52, -2.6, 2.6);
  book_TH1F("CSV_sj2_tag1", 80, -2, 2);
  book_TH1F("JP_sj2_tag1", 60, 0, 3);
  book_TH1F("M_sj3_tag1", 120, 0, 240);
  book_TH1F("pt_sj3_tag1", 120, 0, 480);
  book_TH1F("eta_sj3_tag1", 52, -2.6, 2.6);
  book_TH1F("CSV_sj3_tag1", 80, -2, 2);
  book_TH1F("JP_sj3_tag1", 60, 0, 3);

  book_TH1F("M_tag2", 180, 0, 360);
  book_TH1F("Msd_tag2", 180, 0, 360);
  book_TH1F("Mmin_tag2", 120, 0, 240);
  book_TH1F("pt_tag2", 600, 0, 1200);
  book_TH1F("eta_tag2", 52, -2.6, 2.6);
  book_TH1F("phi_tag2", 66, -3.3, 3.3);
  book_TH1F("CSV_tag2", 80, -2, 2);
  book_TH1F("JP_tag2", 60, 0, 3);
  book_TH1F("CSVmax_sj_tag2", 80, -2, 2);
  book_TH1F("JPmax_sj_tag2", 60, 0, 3);
  book_TH1F("tau2_tag2", 40, 0, 2);
  book_TH1F("tau3_tag2", 40, 0, 2);
  book_TH1F("tau32_tag2", 40, 0, 2);
  book_TH1F("nSubjet_tag2", 6, 0, 6);
  book_TH1F("minDRsj_tag2", 30, 0, 3);
  book_TH1F("M_sj1_tag2", 120, 0, 240);
  book_TH1F("pt_sj1_tag2", 240, 0, 960);
  book_TH1F("eta_sj1_tag2", 52, -2.6, 2.6);
  book_TH1F("CSV_sj1_tag2", 80, -2, 2);
  book_TH1F("JP_sj1_tag2", 60, 0, 3);
  book_TH1F("M_sj2_tag2", 120, 0, 240);
  book_TH1F("pt_sj2_tag2", 120, 0, 480);
  book_TH1F("eta_sj2_tag2", 52, -2.6, 2.6);
  book_TH1F("CSV_sj2_tag2", 80, -2, 2);
  book_TH1F("JP_sj2_tag2", 60, 0, 3);
  book_TH1F("M_sj3_tag2", 120, 0, 240);
  book_TH1F("pt_sj3_tag2", 120, 0, 480);
  book_TH1F("eta_sj3_tag2", 52, -2.6, 2.6);
  book_TH1F("CSV_sj3_tag2", 80, -2, 2);
  book_TH1F("JP_sj3_tag2", 60, 0, 3);

  CSVL_wp = 0.244;
  CSVM_wp = 0.679;
  CSVT_wp = 0.898;

  JPL_wp = 0.275;
  JPM_wp = 0.545;
  JPT_wp = 0.790;
}

void nak::HFolderTopJet::Fill(const std::vector<xtt::MergedJet>& tjets_, const float w_){

  H1("nJet")->Fill(tjets_.size(), w_);

  int nCSVL(0), nCSVM(0), nCSVT(0), nJPL(0), nJPM(0), nJPT(0);
  for(unsigned int i=0; i<tjets_.size(); ++i){

    if(tjets_.at(i).btagCSV > CSVL_wp) ++nCSVL;
    if(tjets_.at(i).btagCSV > CSVM_wp) ++nCSVM;
    if(tjets_.at(i).btagCSV > CSVT_wp) ++nCSVT;
    if(tjets_.at(i).btagJP > JPL_wp) ++nJPL;
    if(tjets_.at(i).btagJP > JPM_wp) ++nJPM;
    if(tjets_.at(i).btagJP > JPT_wp) ++nJPT;
  }

  H1("nCSVL")->Fill(nCSVL, w_);
  H1("nCSVM")->Fill(nCSVM, w_);
  H1("nCSVT")->Fill(nCSVT, w_);
  H1("nJPL")->Fill(nJPL, w_);
  H1("nJPM")->Fill(nJPM, w_);
  H1("nJPT")->Fill(nJPT, w_);

  for(unsigned int i=0; i<tjets_.size(); ++i){
    if(i > 1) break;

    std::stringstream idx;
    idx << i+1;

    H1("M_"+idx.str())->Fill(tjets_.at(i).M, w_);
    H1("Msd_"+idx.str())->Fill(tjets_.at(i).Msoftdrop, w_);
    H1("Mmin_"+idx.str())->Fill(topjet_mmin(tjets_.at(i)), w_);
    H1("pt_"+idx.str())->Fill(tjets_.at(i).pt, w_);
    H1("eta_"+idx.str())->Fill(tjets_.at(i).eta, w_);
    H1("phi_"+idx.str())->Fill(tjets_.at(i).phi, w_);
    H1("CSV_"+idx.str())->Fill(tjets_.at(i).btagCSV, w_);
    H1("JP_"+idx.str())->Fill(tjets_.at(i).btagJP, w_);
    H1("tau2_"+idx.str())->Fill(tjets_.at(i).Tau2, w_);
    H1("tau3_"+idx.str())->Fill(tjets_.at(i).Tau3, w_);
    if(tjets_.at(i).Tau2) H1("tau32_"+idx.str())->Fill(tjets_.at(i).Tau3/tjets_.at(i).Tau2, w_);
    H1("nSubjet_"+idx.str())->Fill(tjets_.at(i).subjets1.size(), w_);
    H1("istagged_"+idx.str())->Fill(topjet_tag(tjets_.at(i)), w_);
  }

  std::vector<xtt::MergedJet> toptagjets;
  toptagjets.reserve(tjets_.size());
  for(unsigned int i=0; i<tjets_.size(); ++i)
    if(topjet_tag(tjets_.at(i))) toptagjets.push_back(tjets_.at(i));

  for(unsigned int i=0; i<toptagjets.size(); ++i){
    if(i > 1) break;

    std::stringstream idx;
    idx << i+1;

    H1("M_tag"+idx.str())->Fill(toptagjets.at(i).M, w_);
    H1("Msd_tag"+idx.str())->Fill(toptagjets.at(i).Msoftdrop, w_);
    H1("Mmin_tag"+idx.str())->Fill(topjet_mmin(toptagjets.at(i)), w_);
    H1("pt_tag"+idx.str())->Fill(toptagjets.at(i).pt, w_);
    H1("eta_tag"+idx.str())->Fill(toptagjets.at(i).eta, w_);
    H1("phi_tag"+idx.str())->Fill(toptagjets.at(i).phi, w_);
    H1("CSV_tag"+idx.str())->Fill(toptagjets.at(i).btagCSV, w_);
    H1("JP_tag"+idx.str())->Fill(toptagjets.at(i).btagJP, w_);
    H1("CSVmax_sj_tag"+idx.str())->Fill(topjet_max_subjet_btag("CSV", toptagjets.at(i)), w_);
    H1("JPmax_sj_tag"+idx.str())->Fill(topjet_max_subjet_btag("JP", toptagjets.at(i)), w_);
    H1("tau2_tag"+idx.str())->Fill(toptagjets.at(i).Tau2, w_);
    H1("tau3_tag"+idx.str())->Fill(toptagjets.at(i).Tau3, w_);
    if(toptagjets.at(i).Tau2) H1("tau32_tag"+idx.str())->Fill(toptagjets.at(i).Tau3/toptagjets.at(i).Tau2, w_);
    H1("nSubjet_tag"+idx.str())->Fill(toptagjets.at(i).subjets1.size(), w_);
    H1("minDRsj_tag"+idx.str())->Fill(topjet_minDRsubjets(toptagjets.at(i)), w_);

    for(unsigned int j=0; j<toptagjets.at(i).subjets1.size(); ++j){
      if(j > 2) break;

      std::stringstream jdx;
      jdx << j+1;

      H1("M_sj"+jdx.str()+"_tag"+idx.str())->Fill(toptagjets.at(i).subjets1.at(j).M, w_);
      H1("pt_sj"+jdx.str()+"_tag"+idx.str())->Fill(toptagjets.at(i).subjets1.at(j).pt, w_);
      H1("eta_sj"+jdx.str()+"_tag"+idx.str())->Fill(toptagjets.at(i).subjets1.at(j).eta, w_);
      H1("CSV_sj"+jdx.str()+"_tag"+idx.str())->Fill(toptagjets.at(i).subjets1.at(j).btagCSV, w_);
      H1("JP_sj"+jdx.str()+"_tag"+idx.str())->Fill(toptagjets.at(i).subjets1.at(j).btagJP, w_);
    }
  }

  return;
}
