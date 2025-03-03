#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriverJES.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <cmath>
#include <cassert>
#include <sstream>
#include <algorithm>

JMETriggerAnalysisDriverJES::JMETriggerAnalysisDriverJES(const std::string& tfile,
                                                         const std::string& ttree,
                                                         const std::string& outputFilePath,
                                                         const std::string& outputFileMode)
    : JMETriggerAnalysisDriverJES(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriverJES::JMETriggerAnalysisDriverJES(const std::string& outputFilePath,
                                                         const std::string& outputFileMode)
    : AnalysisDriverBase(outputFilePath, outputFileMode) {}

//std::string JMETriggerAnalysisDriverJES::jetEtaString(float const jetEta) const {
//
//  std::ostringstream os;
//  os << std::fixed << std::setprecision(3) << std::abs(jetEta);
//
//  std::string ret((jetEta < 0.) ? "neg"+os.str() : "pos"+os.str());
//  std::replace(ret.begin(), ret.end(), '.', 'p');
//
//  return ret;
//}
//
//std::string JMETriggerAnalysisDriverJES::jetEtaBinLabel(float const jetEta) const {
//  assert(jetEtaBinEdges_.size() > 1);
//
//  uint theEtaIdx(0);
//  for(size_t etaIdx=0, lastEtaIdx=(jetEtaBinEdges_.size()-1); etaIdx<lastEtaIdx; ++etaIdx){
//
//    if((jetEtaBinEdges_.at(etaIdx) <= jetEta) and (jetEta < jetEtaBinEdges_.at(etaIdx+1))){
//      theEtaIdx = etaIdx;
//    }
//  }
//
//  if(jetEta >= jetEtaBinEdges_.back()){
//    theEtaIdx = jetEtaBinEdges_.size() - 2;
//  }
//
//  return "eta_"+jetEtaString(jetEtaBinEdges_.at(theEtaIdx))+"_"+jetEtaString(jetEtaBinEdges_.at(theEtaIdx+1));
//}

void JMETriggerAnalysisDriverJES::init() {
  //  jetEtaBinEdges_ = {
  //    -5.191,
  //    -4.716,
  //    -4.363,
  //    -4.013,
  //    -3.664,
  //    -3.314,
  //    -2.964,
  //    -2.650,
  //    -2.322,
  //    -2.043,
  //    -1.830,
  //    -1.653,
  //    -1.479,
  //    -1.305,
  //    -1.131,
  //    -0.957,
  //    -0.783,
  //    -0.609,
  //    -0.435,
  //    -0.261,
  //    -0.087,
  //     0.087,
  //     0.261,
  //     0.435,
  //     0.609,
  //     0.783,
  //     0.957,
  //     1.131,
  //     1.305,
  //     1.479,
  //     1.653,
  //     1.830,
  //     2.043,
  //     2.322,
  //     2.650,
  //     2.964,
  //     3.314,
  //     3.664,
  //     4.013,
  //     4.363,
  //     4.716,
  //     5.191,
  //  };

  jetCollectionsAK4_ = {
      "hltAK4CaloJets",
      "hltAK4PFClusterJets",
      "hltAK4PFJets",
      "hltAK4PFJetsCorrected",
      "hltAK4PFCHSJets",
      "hltAK4PFCHSJetsCorrected",
      "hltAK4PuppiJets",
      "hltAK4PuppiJetsCorrected",
  };

  jetCollectionsAK8_ = {
      "hltAK8CaloJets",
      "hltAK8PFClusterJets",
      "hltAK8PFJets",
      "hltAK8PFJetsCorrected",
      "hltAK8PFCHSJets",
      "hltAK8PFCHSJetsCorrected",
      "hltAK8PuppiJets",
      "hltAK8PuppiJetsCorrected",
  };

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});

  // histograms: Jets
  for (auto const& jetColl : jetCollectionsAK4_) {
    bookHistograms_Jets(jetColl, jetColl, {"GEN"});
  }

  for (auto const& jetColl : jetCollectionsAK8_) {
    bookHistograms_Jets(jetColl, jetColl, {"GEN"});
  }
}

void JMETriggerAnalysisDriverJES::analyze() {
  H1("eventsProcessed")->Fill(0.5, 1.);

  //// AK4 Jets
  float const minAK4JetPt(30.);
  float const minAK4JetPt_GEN(20.);
  float const maxAK4JetDeltaRmatch_GEN(0.2);

  for (auto const& jetLabel : jetCollectionsAK4_) {
    fillHistoDataJets fhDataAK4Jets;
    fhDataAK4Jets.jetCollection = jetLabel;
    fhDataAK4Jets.jetPtMin = minAK4JetPt;
    fhDataAK4Jets.matches.emplace_back(
        fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));
    fillHistograms_Jets(jetLabel, fhDataAK4Jets);
  }

  //// AK8 Jets
  float const minAK8JetPt(90.);
  float const minAK8JetPt_GEN(60.);
  float const maxAK8JetDeltaRmatch_GEN(0.2);

  for (auto const& jetLabel : jetCollectionsAK8_) {
    fillHistoDataJets fhDataAK8Jets;
    fhDataAK8Jets.jetCollection = jetLabel;
    fhDataAK8Jets.jetPtMin = minAK8JetPt;
    fhDataAK8Jets.matches.emplace_back(
        fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));
    fillHistograms_Jets(jetLabel, fhDataAK8Jets);
  }
}

void JMETriggerAnalysisDriverJES::bookHistograms_Jets(const std::string& dir,
                                                      const std::string& jetType,
                                                      const std::vector<std::string>& matchLabels) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }

  std::vector<float> binEdges_njets(121);
  for (uint idx = 0; idx < 121; ++idx) {
    binEdges_njets.at(idx) = idx;
  }

  const std::vector<float> binEdges_pt({0,   10,  20,  30,  40,  50,  60,  70,  80,  90,  100, 120, 140, 160,
                                        180, 200, 220, 240, 260, 280, 300, 400, 500, 600, 700, 800, 1000});

  std::vector<float> binEdges_eta(101);
  for (uint idx = 0; idx < 101; ++idx) {
    binEdges_eta.at(idx) = -5.0 + 0.1 * idx;
  }

  std::vector<float> binEdges_phi(41);
  for (uint idx = 0; idx < 41; ++idx) {
    binEdges_phi.at(idx) = M_PI * (0.05 * idx - 1.);
  }

  const std::vector<float> binEdges_mass(
      {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600});

  std::vector<float> binEdges_dRmatch(26);
  for (uint idx = 0; idx < 26; ++idx) {
    binEdges_dRmatch.at(idx) = 0.2 * idx;
  }

  std::vector<float> binEdges_response(51);
  for (uint idx = 0; idx < 51; ++idx) {
    binEdges_response.at(idx) = 0.1 * idx;
  }

  addTH1D(dirPrefix + jetType + "_njets", binEdges_njets);
  addTH1D(dirPrefix + jetType + "_pt", binEdges_pt);
  addTH1D(dirPrefix + jetType + "_eta", binEdges_eta);
  addTH2D(dirPrefix + jetType + "_eta__vs__pt", binEdges_eta, binEdges_pt);
  addTH1D(dirPrefix + jetType + "_phi", binEdges_phi);
  addTH1D(dirPrefix + jetType + "_mass", binEdges_mass);

  for (auto const& matchLabel : matchLabels) {
    addTH1D(dirPrefix + jetType + "_NotMatchedTo" + matchLabel + "_njets", binEdges_njets);
    addTH1D(dirPrefix + jetType + "_NotMatchedTo" + matchLabel + "_pt", binEdges_pt);
    addTH1D(dirPrefix + jetType + "_NotMatchedTo" + matchLabel + "_eta", binEdges_eta);
    addTH2D(dirPrefix + jetType + "_NotMatchedTo" + matchLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
    addTH1D(dirPrefix + jetType + "_NotMatchedTo" + matchLabel + "_phi", binEdges_phi);
    addTH1D(dirPrefix + jetType + "_NotMatchedTo" + matchLabel + "_mass", binEdges_mass);

    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_njets", binEdges_njets);
    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_pt", binEdges_pt);
    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_eta", binEdges_eta);
    addTH2D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_phi", binEdges_phi);
    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_mass", binEdges_mass);
    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_dRmatch", binEdges_dRmatch);
    addTH2D(
        dirPrefix + jetType + "_MatchedTo" + matchLabel + "_pt__vs__" + matchLabel + "_pt", binEdges_pt, binEdges_pt);
    addTH2D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_eta__vs__" + matchLabel + "_eta",
            binEdges_eta,
            binEdges_eta);
    addTH1D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel, binEdges_response);
    addTH2D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_pt",
            binEdges_response,
            binEdges_pt);
    addTH2D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_eta",
            binEdges_response,
            binEdges_eta);

    addTH3D(dirPrefix + jetType + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__pt__vs__eta",
            binEdges_response,
            binEdges_pt,
            binEdges_eta);

    //    for(size_t etaIdx=0, lastEtaIdx=(jetEtaBinEdges_.size()-1); etaIdx<lastEtaIdx; ++etaIdx){
    //      auto const etaBinLabel(jetEtaBinLabel(jetEtaBinEdges_.at(etaIdx)));
    //      addTH2D(dirPrefix+jetType+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt__"+etaBinLabel, binEdges_response, binEdges_pt);
    //    }
  }
}

void JMETriggerAnalysisDriverJES::fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhData) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }

  auto const* v_pt(this->vector_ptr<float>(fhData.jetCollection + "_pt"));
  auto const* v_eta(this->vector_ptr<float>(fhData.jetCollection + "_eta"));
  auto const* v_phi(this->vector_ptr<float>(fhData.jetCollection + "_phi"));
  auto const* v_mass(this->vector_ptr<float>(fhData.jetCollection + "_mass"));

  if (not(v_pt and v_eta and v_phi and v_mass)) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriverJES::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData.jetCollection + "_pt/eta/phi/mass" << std::endl;
    }
    return;
  }

  std::vector<size_t> jetIndices;
  jetIndices.reserve(v_pt->size());
  for (size_t idx = 0; idx < v_pt->size(); ++idx) {
    if (v_pt->at(idx) > fhData.jetPtMin) {
      jetIndices.emplace_back(idx);
    }
  }

  uint const njets(jetIndices.size());
  H1(dirPrefix + fhData.jetCollection + "_njets")->Fill(0.01 + njets);

  for (auto const jetIdx : jetIndices) {
    H1(dirPrefix + fhData.jetCollection + "_pt")->Fill(v_pt->at(jetIdx));
    H1(dirPrefix + fhData.jetCollection + "_eta")->Fill(v_eta->at(jetIdx));
    H2(dirPrefix + fhData.jetCollection + "_eta__vs__pt")->Fill(v_eta->at(jetIdx), v_pt->at(jetIdx));
    H1(dirPrefix + fhData.jetCollection + "_phi")->Fill(v_phi->at(jetIdx));
    H1(dirPrefix + fhData.jetCollection + "_mass")->Fill(v_mass->at(jetIdx));
  }

  for (auto const& fhDataMatch : fhData.matches) {
    auto const matchLabel(fhDataMatch.label);
    auto const matchJetColl(fhDataMatch.jetCollection);
    auto const matchJetPtMin(fhDataMatch.jetPtMin);
    auto const matchJetDeltaRMin(fhDataMatch.jetDeltaRMin);

    auto const* v_match_pt(this->vector_ptr<float>(matchJetColl + "_pt"));
    auto const* v_match_eta(this->vector_ptr<float>(matchJetColl + "_eta"));
    auto const* v_match_phi(this->vector_ptr<float>(matchJetColl + "_phi"));
    auto const* v_match_mass(this->vector_ptr<float>(matchJetColl + "_mass"));

    if (not(v_match_pt and v_match_eta and v_match_phi and v_match_mass)) {
      if (verbosity_ >= 0) {
        std::cout << "JMETriggerAnalysisDriverJES::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
                  << "branches not available (histograms will not be filled): " << matchJetColl + "_pt/eta/phi/mass"
                  << std::endl;
      }
      continue;
    }

    size_t nJetsMatched(0), nJetsNotMatched(0);

    std::map<size_t, size_t> mapMatchIndeces;
    for (auto const jetIdx : jetIndices) {
      int indexBestMatch(-1);
      float dR2min(matchJetDeltaRMin * matchJetDeltaRMin);
      for (size_t idxMatch = 0; idxMatch < v_match_pt->size(); ++idxMatch) {
        if (v_match_pt->at(idxMatch) <= matchJetPtMin) {
          continue;
        }

        auto const dR2(
            utils::deltaR2(v_eta->at(jetIdx), v_phi->at(jetIdx), v_match_eta->at(idxMatch), v_match_phi->at(idxMatch)));
        if (dR2 < dR2min) {
          dR2min = dR2;
          indexBestMatch = idxMatch;
        }
      }

      if (indexBestMatch >= 0) {
        mapMatchIndeces.insert(std::make_pair(jetIdx, indexBestMatch));
        ++nJetsMatched;
      } else {
        ++nJetsNotMatched;
      }
    }

    H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_njets")->Fill(0.01 + nJetsMatched);
    H1(dirPrefix + fhData.jetCollection + "_NotMatchedTo" + matchLabel + "_njets")->Fill(0.01 + nJetsNotMatched);

    for (auto const jetIdx : jetIndices) {
      auto const jetPt(v_pt->at(jetIdx));
      auto const jetEta(v_eta->at(jetIdx));
      auto const jetPhi(v_phi->at(jetIdx));
      auto const jetMass(v_mass->at(jetIdx));

      auto const hasMatch(mapMatchIndeces.find(jetIdx) != mapMatchIndeces.end());

      if (hasMatch) {
        H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_pt")->Fill(jetPt);
        H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_eta")->Fill(jetEta);
        H2(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_eta__vs__pt")->Fill(jetEta, jetPt);
        H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_phi")->Fill(jetPhi);
        H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_mass")->Fill(jetMass);

        auto const jetMatchIdx(mapMatchIndeces.at(jetIdx));

        auto const jetMatchPt(v_match_pt->at(jetMatchIdx));
        auto const jetMatchEta(v_match_eta->at(jetMatchIdx));
        auto const jetMatchPhi(v_match_phi->at(jetMatchIdx));

        auto const dR2match(utils::deltaR2(jetEta, jetPhi, jetMatchEta, jetMatchPhi));
        H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_dRmatch")->Fill(sqrt(dR2match));

        H2(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_pt__vs__" + matchLabel + "_pt")
            ->Fill(jetPt, jetMatchPt);
        H2(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_eta__vs__" + matchLabel + "_eta")
            ->Fill(jetEta, jetMatchEta);

        if (jetMatchPt != 0.) {
          auto const jetPtRatio(jetPt / jetMatchPt);
          H1(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel)->Fill(jetPtRatio);
          H2(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
             matchLabel + "_pt")
              ->Fill(jetPtRatio, jetMatchPt);
          H2(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
             matchLabel + "_eta")
              ->Fill(jetPtRatio, jetMatchEta);

          H3(dirPrefix + fhData.jetCollection + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
             "__vs__pt__vs__eta")
              ->Fill(jetPtRatio, jetPt, jetEta);

          //          auto const etaBinLabel(jetEtaBinLabel(jetEta));
          //          H2(dirPrefix+fhData.jetCollection+"_MatchedTo"+matchLabel+"_pt_over"+matchLabel+"__vs__"+matchLabel+"_pt__"+etaBinLabel)->Fill(jetPtRatio, jetMatchPt);
        }
      } else {
        H1(dirPrefix + fhData.jetCollection + "_NotMatchedTo" + matchLabel + "_pt")->Fill(jetPt);
        H1(dirPrefix + fhData.jetCollection + "_NotMatchedTo" + matchLabel + "_eta")->Fill(jetEta);
        H2(dirPrefix + fhData.jetCollection + "_NotMatchedTo" + matchLabel + "_eta__vs__pt")->Fill(jetEta, jetPt);
        H1(dirPrefix + fhData.jetCollection + "_NotMatchedTo" + matchLabel + "_phi")->Fill(jetPhi);
        H1(dirPrefix + fhData.jetCollection + "_NotMatchedTo" + matchLabel + "_mass")->Fill(jetMass);
      }
    }
  }
}
