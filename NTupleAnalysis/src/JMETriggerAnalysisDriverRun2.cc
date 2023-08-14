#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriverRun2.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <cmath>

JMETriggerAnalysisDriverRun2::JMETriggerAnalysisDriverRun2(const std::string& tfile,
                                                           const std::string& ttree,
                                                           const std::string& outputFilePath,
                                                           const std::string& outputFileMode)
    : JMETriggerAnalysisDriverRun2(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriverRun2::JMETriggerAnalysisDriverRun2(const std::string& outputFilePath,
                                                           const std::string& outputFileMode)
    : AnalysisDriverBase(outputFilePath, outputFileMode) {}

bool JMETriggerAnalysisDriverRun2::jetBelongsToCategory(const std::string& categLabel,
                                                        const float jetPt,
                                                        const float jetAbsEta,
                                                        const float jetPhi,
                                                        const float jetEta) const {
  bool ret(false);
  if (categLabel == "_EtaIncl") {
    ret = (jetAbsEta < 5.0);
  } else if (categLabel == "_EtaInclPt0") {
    ret = (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_EtaInclPt1") {
    ret = (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.);
  } else if (categLabel == "_EtaInclPt2") {
    ret = (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_EtaInclPt3") {
    ret = (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.);
  } else if (categLabel == "_EtaInclPt4") {
    ret = (jetAbsEta < 5.0) and (2000. <= jetPt);
  }

  else if (categLabel == "_HB") {
    ret = (jetAbsEta < 1.3);
  } else if (categLabel == "_HBPt0") {
    ret = (jetAbsEta < 1.3) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HBPt1") {
    ret = (jetAbsEta < 1.3) and (60. <= jetPt) and (jetPt < 110.);
  } else if (categLabel == "_HBPt2") {
    ret = (jetAbsEta < 1.3) and (110. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HBPt3") {
    ret = (jetAbsEta < 1.3) and (400. <= jetPt) and (jetPt < 2000.);
  } else if (categLabel == "_HBPt4") {
    ret = (jetAbsEta < 1.3) and (2000. <= jetPt);
  }

  else if (categLabel == "_HE1") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5);
  } else if (categLabel == "_HE1Pt0") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HE1Pt1") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (60. <= jetPt) and (jetPt < 110.);
  } else if (categLabel == "_HE1Pt2") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (110. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HE1Pt3") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (400. <= jetPt) and (jetPt < 2000.);
  } else if (categLabel == "_HE1Pt4") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (2000. <= jetPt);
  }

  else if (categLabel == "_HE2") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0);
  } else if (categLabel == "_HE2Pt0") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HE2Pt1") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt < 110.);
  } else if (categLabel == "_HE2Pt2") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (110. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HE2Pt3") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (400. <= jetPt) and (jetPt < 2000.);
  } else if (categLabel == "_HE2Pt4") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (2000. <= jetPt);
  }

  else if (categLabel == "_HF") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0);
  } else if (categLabel == "_HFPt0") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HFPt1") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.);
  } else if (categLabel == "_HFPt2") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HFPt3") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.);
  } else if (categLabel == "_HFPt4") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (2000. <= jetPt);
  }

  return ret;
}

void JMETriggerAnalysisDriverRun2::init() {
  jetCategoryLabels_ = {
      "_EtaIncl",
      //  "_EtaInclPt0",
      //  "_EtaInclPt1",
      //  "_EtaInclPt2",
      //  "_EtaInclPt3",
      //  "_EtaInclPt4",

      "_HB",
      //  "_HBPt0",
      //  "_HBPt1",
      //  "_HBPt2",
      //  "_HBPt3",
      //  "_HBPt4",

      "_HE1",
      //  "_HE1Pt0",
      //  "_HE1Pt1",
      //  "_HE1Pt2",
      //  "_HE1Pt3",
      //  "_HE1Pt4",

      "_HE2",
      //  "_HE2Pt0",
      //  "_HE2Pt1",
      //  "_HE2Pt2",
      //  "_HE2Pt3",
      //  "_HE2Pt4",

      "_HF",
      //  "_HFPt0",
      //  "_HFPt1",
      //  "_HFPt2",
      //  "_HFPt3",
      //  "_HFPt4",
  };

  //!! jetletponclesaning, pt, eta, pfid, hltmatching

  auto const& opt_era(getOption("era"));

  if (opt_era == "2016") {
    hltPaths_PFMET_ = {
        "HLT_PFMET170_NotCleaned",
        "HLT_PFMET170_HBHECleaned",
        "HLT_PFMET170_BeamHaloCleaned",
        "HLT_PFMET170_HBHE_BeamHaloCleaned",
        "HLT_PFMETTypeOne190_HBHE_BeamHaloCleaned",
    };
  } else if (opt_era == "2017") {
    hltPaths_PFMET_ = {
        "HLT_PFMET200_NotCleaned",
        "HLT_PFMET200_HBHECleaned",
        "HLT_PFMET200_HBHE_BeamHaloCleaned",
        "HLT_PFMET250_HBHECleaned",
        "HLT_PFMET300_HBHECleaned",
        "HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned",
    };
  } else if (opt_era == "2018") {
    hltPaths_PFMET_ = {
        "HLT_PFMET200_NotCleaned",
        "HLT_PFMET200_HBHECleaned",
        "HLT_PFMET200_HBHE_BeamHaloCleaned",
        "HLT_PFMET250_HBHECleaned",
        "HLT_PFMET300_HBHECleaned",
        "HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned",
    };
  } else {
    throw std::runtime_error("JMETriggerAnalysisDriverRun2::init -- invalid value for option \"era\": " + opt_era);
  }

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});

  // histograms: MET
  for (std::string const& metColl : {
           "offlineMETs_Raw",
           "offlineMETs_Type1",
           "offlineMETsPuppi_Raw",
           "offlineMETsPuppi_Type1",
       }) {
    for (std::string const& metHLT : hltPaths_PFMET_) {
      bookHistograms_MET(metHLT + "_total", metColl);
      bookHistograms_MET(metHLT + "_pass", metColl);
    }
  }
}

void JMETriggerAnalysisDriverRun2::analyze() {
  H1("eventsProcessed")->Fill(0.5, 1.);

  // single-electron trigger
  auto const& opt_era(getOption("era"));

  if (opt_era == "2016") {
    auto const& ele_trig(value<bool>("HLT_Ele27_WPTight_Gsf"));
    if (not ele_trig) {
      return;
    }
  } else if (opt_era == "2017") {
    auto const& ele_trig(value<bool>("HLT_Ele32_WPTight_Gsf_L1DoubleEG") and
                         value<bool>("Flag_ele32DoubleL1ToSingleL1"));
    if (not ele_trig) {
      return;
    }
  } else if (opt_era == "2018") {
    auto const& ele_trig(value<bool>("HLT_Ele32_WPTight_Gsf"));
    if (not ele_trig) {
      return;
    }
  } else {
    throw std::runtime_error("JMETriggerAnalysisDriverRun2::analyze -- invalid value for option \"era\": " + opt_era);
  }

  // electron selection
  size_t nElectronsVeto(0), nElectronsGood(0);
  auto const& electrons_pt(vector<float>("offlineElectrons_pt"));
  auto const& electrons_etaSC(vector<float>("offlineElectrons_etaSC"));
  auto const& electrons_phi(vector<float>("offlineElectrons_phi"));
  auto const& electrons_id(vector<uint>("offlineElectrons_id"));

  if ((electrons_pt.size() != electrons_etaSC.size()) or (electrons_pt.size() != electrons_phi.size()) or
      (electrons_pt.size() != electrons_id.size())) {
    throw std::runtime_error("electrons_pt size");
  }

  //  size_t goodElectronIdx(0);
  for (size_t eleIdx = 0; eleIdx < electrons_pt.size(); ++eleIdx) {
    auto const& pt(electrons_pt.at(eleIdx));
    auto const& absEtaSC(std::abs(electrons_etaSC.at(eleIdx)));
    auto const& id(electrons_id.at(eleIdx));

    if ((1.4442 < absEtaSC) and (absEtaSC < 1.566)) {
      continue;
    }

    auto const isVeto((pt > 20.) and (absEtaSC < 2.5) and (id & (1 << 1)));
    auto const isGood((pt > 35.) and (absEtaSC < 2.5) and (id & (1 << 2)));

    if (isVeto) {
      ++nElectronsVeto;
    }
    if (isGood) {
      ++nElectronsGood;
      //      goodElectronIdx = eleIdx;
    }
  }

  if (nElectronsVeto > 1) {
    return;
  }
  if (nElectronsGood != 1) {
    return;
  }

  // veto on muons
  size_t nMuonsVeto(0);  //, nMuonsGood(0);
  auto const& muons_pt(vector<float>("offlineMuons_pt"));
  auto const& muons_eta(vector<float>("offlineMuons_eta"));
  auto const& muons_pfIso(vector<float>("offlineMuons_pfIso"));
  auto const& muons_id(vector<uint>("offlineMuons_id"));

  if ((muons_pt.size() != muons_eta.size()) or (muons_pt.size() != muons_pfIso.size()) or
      (muons_pt.size() != muons_id.size())) {
    throw std::runtime_error("muons_pt size");
  }

  //  size_t goodMuonIdx(0);
  for (size_t muoIdx = 0; muoIdx < muons_pt.size(); ++muoIdx) {
    auto const& pt(muons_pt.at(muoIdx));
    auto const& absEta(std::abs(muons_eta.at(muoIdx)));
    auto const& pfIso(muons_pfIso.at(muoIdx));
    auto const& id(muons_id.at(muoIdx));

    auto const isVeto((pt > 20.) and (absEta < 2.4) and (id & (1 << 0)) and (pfIso < 0.25));
    //    auto const isGood((pt > 35.) and (absEta < 2.4) and (id & (1 << 1)) and (pfIso < 0.12));

    if (isVeto) {
      ++nMuonsVeto;
    }
    //    if(isGood){ ++nMuonsGood; goodMuonIdx = muoIdx; }
  }

  if (nMuonsVeto > 0) {
    return;
  }

  //  auto const& electronPhi(electrons_phi.at(goodElectronIdx));

  for (std::string const& metColl :
       {"offlineMETs_Raw", "offlineMETs_Type1", "offlineMETsPuppi_Raw", "offlineMETsPuppi_Type1"}) {
    //    auto const& metPhi(vector<float>(metColl+"_phi").at(0));
    //
    //    // cut on deltaPhi(electron, MET)
    //    if(utils::deltaPhi(electronPhi, metPhi) > (6. * M_PI / 5.)){
    //      continue;
    //    }

    for (auto const& metHLT : hltPaths_PFMET_) {
      auto const& metHLT_flagL1TSeedPrescaledOrMasked(value<bool>("Flag_" + metHLT + "_L1TSeedPrescaledOrMasked"));
      if (metHLT_flagL1TSeedPrescaledOrMasked) {
        continue;
      }

      auto const& metHLT_flagHLTPathPrescaled(value<bool>("Flag_" + metHLT + "_HLTPathPrescaled"));
      if (metHLT_flagHLTPathPrescaled) {
        continue;
      }

      fillHistoDataMET fhDataMET;
      fhDataMET.metCollection = metColl;
      fillHistograms_MET(metHLT + "_total", fhDataMET);

      auto const& metHLTAccept(value<bool>(metHLT));
      if (not metHLTAccept) {
        continue;
      }

      fillHistograms_MET(metHLT + "_pass", fhDataMET);
    }
  }
}

void JMETriggerAnalysisDriverRun2::bookHistograms_Jets(const std::string& dir,
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

  std::vector<float> binEdges_numberOfDaughters(121);
  for (uint idx = 0; idx < 121; ++idx) {
    binEdges_numberOfDaughters.at(idx) = 2. * idx;
  }

  std::vector<float> binEdges_energyFrac(21);
  for (uint idx = 0; idx < 21; ++idx) {
    binEdges_energyFrac.at(idx) = 0.05 * idx;
  }

  std::vector<float> binEdges_dauMult1(61);
  for (uint idx = 0; idx < 61; ++idx) {
    binEdges_dauMult1.at(idx) = idx;
  }

  std::vector<float> binEdges_dauMult2(13);
  for (uint idx = 0; idx < 13; ++idx) {
    binEdges_dauMult2.at(idx) = idx;
  }

  std::vector<float> binEdges_dRmatch(26);
  for (uint idx = 0; idx < 26; ++idx) {
    binEdges_dRmatch.at(idx) = 0.2 * idx;
  }

  std::vector<float> binEdges_response(51);
  for (uint idx = 0; idx < 51; ++idx) {
    binEdges_response.at(idx) = 0.1 * idx;
  }

  for (auto const& catLabel : jetCategoryLabels_) {
    addTH1D(dirPrefix + jetType + catLabel + "_njets", binEdges_njets);
    addTH1D(dirPrefix + jetType + catLabel + "_pt", binEdges_pt);
    addTH1D(dirPrefix + jetType + catLabel + "_pt0", binEdges_pt);
    addTH1D(dirPrefix + jetType + catLabel + "_eta", binEdges_eta);
    addTH2D(dirPrefix + jetType + catLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
    addTH1D(dirPrefix + jetType + catLabel + "_phi", binEdges_phi);
    addTH1D(dirPrefix + jetType + catLabel + "_mass", binEdges_mass);
    addTH1D(dirPrefix + jetType + catLabel + "_numberOfDaughters", binEdges_numberOfDaughters);
    addTH1D(dirPrefix + jetType + catLabel + "_chargedHadronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix + jetType + catLabel + "_neutralHadronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix + jetType + catLabel + "_electronEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix + jetType + catLabel + "_photonEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix + jetType + catLabel + "_muonEnergyFraction", binEdges_energyFrac);
    addTH1D(dirPrefix + jetType + catLabel + "_chargedHadronMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix + jetType + catLabel + "_neutralHadronMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix + jetType + catLabel + "_electronMultiplicity", binEdges_dauMult2);
    addTH1D(dirPrefix + jetType + catLabel + "_photonMultiplicity", binEdges_dauMult1);
    addTH1D(dirPrefix + jetType + catLabel + "_muonMultiplicity", binEdges_dauMult2);

    for (auto const& matchLabel : matchLabels) {
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_njets", binEdges_njets);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_eta", binEdges_eta);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_phi", binEdges_phi);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_mass", binEdges_mass);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_numberOfDaughters",
              binEdges_numberOfDaughters);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_chargedHadronEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_neutralHadronEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_electronEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_photonEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_muonEnergyFraction", binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_chargedHadronMultiplicity",
              binEdges_dauMult1);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_neutralHadronMultiplicity",
              binEdges_dauMult1);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_electronMultiplicity", binEdges_dauMult2);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_photonMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_muonMultiplicity", binEdges_dauMult2);

      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_dRmatch", binEdges_dRmatch);

      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt__vs__" + matchLabel + "_pt",
              binEdges_pt,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0__vs__" + matchLabel + "_pt",
              binEdges_pt,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0__vs__" + matchLabel + "_eta",
              binEdges_pt,
              binEdges_eta);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__" + matchLabel + "_eta",
              binEdges_eta,
              binEdges_eta);

      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel, binEdges_response);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
                  matchLabel + "_pt",
              binEdges_response,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
                  matchLabel + "_eta",
              binEdges_response,
              binEdges_eta);

      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel, binEdges_response);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel + "__vs__" +
                  matchLabel + "_pt",
              binEdges_response,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel + "__vs__" +
                  matchLabel + "_eta",
              binEdges_response,
              binEdges_eta);

      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel,
              binEdges_response);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel + "__vs__" +
                  matchLabel + "_pt",
              binEdges_response,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel + "__vs__" +
                  matchLabel + "_eta",
              binEdges_response,
              binEdges_eta);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel + "__vs__" +
                  matchLabel + "_mass",
              binEdges_response,
              binEdges_mass);

      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_njets", binEdges_njets);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_pt", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_pt0", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_eta", binEdges_eta);
      addTH2D(
          dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_phi", binEdges_phi);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_mass", binEdges_mass);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_numberOfDaughters",
              binEdges_numberOfDaughters);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_chargedHadronEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_neutralHadronEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_electronEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_photonEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_muonEnergyFraction",
              binEdges_energyFrac);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_chargedHadronMultiplicity",
              binEdges_dauMult1);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_neutralHadronMultiplicity",
              binEdges_dauMult1);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_electronMultiplicity",
              binEdges_dauMult2);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_photonMultiplicity", binEdges_dauMult1);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_muonMultiplicity", binEdges_dauMult2);
    }
  }
}

void JMETriggerAnalysisDriverRun2::bookHistograms_MET(const std::string& dir,
                                                      const std::string& metType,
                                                      const std::vector<std::string>& matchLabels) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }

  const std::vector<float> binEdges_pt({0,   20,  40,  60,  80,  100, 120, 140, 160, 180, 200, 220, 240, 260, 280,
                                        300, 320, 340, 360, 380, 400, 420, 440, 480, 540, 600, 700, 800, 1000});

  std::vector<float> binEdges_phi(41);
  for (uint idx = 0; idx < 41; ++idx) {
    binEdges_phi.at(idx) = M_PI * (0.05 * idx - 1.);
  }

  std::vector<float> binEdges_sumEt(121);
  for (uint idx = 0; idx < 121; ++idx) {
    binEdges_sumEt.at(idx) = 50. * idx;
  }

  addTH1D(dirPrefix + metType + "_pt", binEdges_pt);
  addTH1D(dirPrefix + metType + "_phi", binEdges_phi);
  addTH1D(dirPrefix + metType + "_sumEt", binEdges_sumEt);

  if (matchLabels.empty()) {
    return;
  }

  std::vector<float> binEdges_response(51);
  for (uint idx = 0; idx < 51; ++idx) {
    binEdges_response.at(idx) = 0.1 * idx;
  }

  std::vector<float> binEdges_deltaPhi(21);
  for (uint idx = 0; idx < 21; ++idx) {
    binEdges_deltaPhi.at(idx) = M_PI * 0.05 * idx;
  }

  std::vector<float> binEdges_deltaPt(61);
  for (uint idx = 0; idx < 61; ++idx) {
    binEdges_deltaPt.at(idx) = -240 + 8. * idx;
  }

  for (auto const& matchLabel : matchLabels) {
    addTH1D(dirPrefix + metType + "_pt_over" + matchLabel, binEdges_response);
    addTH1D(dirPrefix + metType + "_deltaPhi" + matchLabel, binEdges_deltaPhi);
    addTH1D(dirPrefix + metType + "_sumEt_over" + matchLabel, binEdges_response);
    addTH1D(dirPrefix + metType + "_pt_paraTo" + matchLabel, binEdges_deltaPt);
    addTH1D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel, binEdges_deltaPt);
    addTH1D(dirPrefix + metType + "_pt_perpTo" + matchLabel, binEdges_deltaPt);

    addTH2D(dirPrefix + metType + "_pt__vs__" + matchLabel + "_pt", binEdges_pt, binEdges_pt);
    addTH2D(dirPrefix + metType + "_phi__vs__" + matchLabel + "_phi", binEdges_phi, binEdges_phi);
    addTH2D(dirPrefix + metType + "_sumEt__vs__" + matchLabel + "_sumEt", binEdges_sumEt, binEdges_sumEt);

    addTH2D(
        dirPrefix + metType + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_response, binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_response,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_response,
            binEdges_sumEt);

    addTH2D(
        dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_deltaPhi, binEdges_pt);
    addTH2D(dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPhi,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPhi,
            binEdges_sumEt);

    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_pt",
            binEdges_response,
            binEdges_pt);
    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_response,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_response,
            binEdges_sumEt);

    addTH2D(
        dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPt,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPt,
            binEdges_sumEt);

    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel + "_pt",
            binEdges_deltaPt,
            binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPt,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPt,
            binEdges_sumEt);

    addTH2D(
        dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPt,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPt,
            binEdges_sumEt);
  }
}

void JMETriggerAnalysisDriverRun2::fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhData) {
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

  auto const* v_numberOfDaughters(this->vector_ptr<uint>(fhData.jetCollection + "_numberOfDaughters"));

  if (not(v_pt and v_eta and v_phi and v_mass)) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriverRun2::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData.jetCollection + "_pt/eta/phi/mass" << std::endl;
    }
    return;
  }

  for (auto const& catLabel : jetCategoryLabels_) {
    std::vector<size_t> jetIndices;
    jetIndices.reserve(v_pt->size());
    int indexMaxPtJet(-1);
    float jetPtMax(-1.);
    for (size_t idx = 0; idx < v_pt->size(); ++idx) {
      if (v_pt->at(idx) <= fhData.jetPtMin) {
        continue;
      }

      if (jetBelongsToCategory(catLabel, v_pt->at(idx), std::abs(v_eta->at(idx)), v_phi->at(idx), v_eta->at(idx))) {
        jetIndices.emplace_back(idx);
        if ((jetIndices.size() == 1) or (v_pt->at(idx) > jetPtMax)) {
          jetPtMax = v_pt->at(idx);
          indexMaxPtJet = idx;
        }
      }
    }

    for (auto const jetIdx : jetIndices) {
      H1(dirPrefix + fhData.jetCollection + catLabel + "_pt")->Fill(v_pt->at(jetIdx));
      H1(dirPrefix + fhData.jetCollection + catLabel + "_eta")->Fill(v_eta->at(jetIdx));
      H2(dirPrefix + fhData.jetCollection + catLabel + "_eta__vs__pt")->Fill(v_eta->at(jetIdx), v_pt->at(jetIdx));
      H1(dirPrefix + fhData.jetCollection + catLabel + "_phi")->Fill(v_phi->at(jetIdx));
      H1(dirPrefix + fhData.jetCollection + catLabel + "_mass")->Fill(v_mass->at(jetIdx));

      if (v_numberOfDaughters) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_numberOfDaughters")->Fill(v_numberOfDaughters->at(jetIdx));
      }
    }

    H1(dirPrefix + fhData.jetCollection + catLabel + "_njets")->Fill(0.01 + jetIndices.size());

    if (indexMaxPtJet >= 0) {
      H1(dirPrefix + fhData.jetCollection + catLabel + "_pt0")->Fill(v_pt->at(indexMaxPtJet));
    }
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
        std::cout << "JMETriggerAnalysisDriverRun2::fillHistograms_Jets(\"" << dir
                  << "\", const fillHistoDataJets&) -- "
                  << "branches not available (histograms will not be filled): " << matchJetColl + "_pt/eta/phi/mass"
                  << std::endl;
      }
      continue;
    }

    std::map<size_t, size_t> mapMatchIndeces;
    for (size_t idx = 0; idx < v_pt->size(); ++idx) {
      if (v_pt->at(idx) <= fhData.jetPtMin) {
        continue;
      }

      int indexBestMatch(-1);
      float dR2min(matchJetDeltaRMin * matchJetDeltaRMin);
      for (size_t idxMatch = 0; idxMatch < v_match_pt->size(); ++idxMatch) {
        if (v_match_pt->at(idxMatch) <= matchJetPtMin) {
          continue;
        }

        auto const dR2(
            utils::deltaR2(v_eta->at(idx), v_phi->at(idx), v_match_eta->at(idxMatch), v_match_phi->at(idxMatch)));
        if (dR2 < dR2min) {
          dR2min = dR2;
          indexBestMatch = idxMatch;
        }
      }

      if (indexBestMatch >= 0) {
        mapMatchIndeces.insert(std::make_pair(idx, indexBestMatch));
      }
    }

    for (auto const& catLabel : jetCategoryLabels_) {
      std::vector<size_t> jetIndices;
      jetIndices.reserve(v_pt->size());
      for (size_t idx = 0; idx < v_pt->size(); ++idx) {
        if (v_pt->at(idx) <= fhData.jetPtMin) {
          continue;
        }

        if (jetBelongsToCategory(catLabel, v_pt->at(idx), std::abs(v_eta->at(idx)), v_phi->at(idx), v_eta->at(idx))) {
          jetIndices.emplace_back(idx);
        }
      }

      size_t nJetsMatched(0), nJetsNotMatched(0);
      int indexMaxPtJetWithMatch(-1), indexMaxPtJetWithNoMatch(-1);
      float maxPtJetPtWithMatch(-1.), maxPtJetPtWithNoMatch(-1.);

      for (auto const jetIdx : jetIndices) {
        auto const jetPt(v_pt->at(jetIdx));
        auto const jetEta(v_eta->at(jetIdx));
        auto const jetPhi(v_phi->at(jetIdx));
        auto const jetMass(v_mass->at(jetIdx));

        auto const hasMatch(mapMatchIndeces.find(jetIdx) != mapMatchIndeces.end());

        if (hasMatch) {
          ++nJetsMatched;

          if ((nJetsMatched == 1) or (jetPt > maxPtJetPtWithMatch)) {
            maxPtJetPtWithMatch = jetPt;
            indexMaxPtJetWithMatch = jetIdx;
          }

          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt")->Fill(jetPt);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_eta")->Fill(jetEta);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__pt")
              ->Fill(jetEta, jetPt);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_phi")->Fill(jetPhi);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass")->Fill(jetMass);

          if (v_numberOfDaughters) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_numberOfDaughters")
                ->Fill(v_numberOfDaughters->at(jetIdx));
          }

          auto const jetMatchIdx(mapMatchIndeces.at(jetIdx));
          auto const jetMatchPt(v_match_pt->at(jetMatchIdx));
          auto const jetMatchEta(v_match_eta->at(jetMatchIdx));
          auto const jetMatchPhi(v_match_phi->at(jetMatchIdx));
          auto const jetMatchMass(v_match_mass->at(jetMatchIdx));

          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt__vs__" + matchLabel + "_pt")
              ->Fill(jetPt, jetMatchPt);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__" + matchLabel +
             "_eta")
              ->Fill(jetEta, jetMatchEta);

          auto const dR2match(utils::deltaR2(jetEta, jetPhi, jetMatchEta, jetMatchPhi));
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_dRmatch")->Fill(sqrt(dR2match));

          if (jetMatchPt != 0.) {
            auto const jetPtRatio(jetPt / jetMatchPt);
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel)
                ->Fill(jetPtRatio);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__" + matchLabel + "_pt")
                ->Fill(jetPtRatio, jetMatchPt);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__" + matchLabel + "_eta")
                ->Fill(jetPtRatio, jetMatchEta);
          }

          if (jetMatchMass != 0.) {
            auto const jetMassRatio(jetMass / jetMatchMass);
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel)
                ->Fill(jetMassRatio);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel +
               "__vs__" + matchLabel + "_pt")
                ->Fill(jetMassRatio, jetMatchMass);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel +
               "__vs__" + matchLabel + "_eta")
                ->Fill(jetMassRatio, jetMatchEta);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel +
               "__vs__" + matchLabel + "_mass")
                ->Fill(jetMassRatio, jetMatchMass);
          }
        } else {
          ++nJetsNotMatched;

          if ((nJetsNotMatched == 1) or (jetPt > maxPtJetPtWithNoMatch)) {
            maxPtJetPtWithNoMatch = jetPt;
            indexMaxPtJetWithNoMatch = jetIdx;
          }

          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_pt")->Fill(jetPt);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_eta")->Fill(jetEta);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_eta__vs__pt")
              ->Fill(jetEta, jetPt);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_phi")->Fill(jetPhi);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_mass")->Fill(jetMass);

          if (v_numberOfDaughters) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_numberOfDaughters")
                ->Fill(v_numberOfDaughters->at(jetIdx));
          }
        }
      }

      H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_njets")->Fill(0.01 + nJetsMatched);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_njets")
          ->Fill(0.01 + nJetsNotMatched);

      if (indexMaxPtJetWithMatch >= 0) {
        auto const maxPtJetPt(v_pt->at(indexMaxPtJetWithMatch));
        auto const maxPtJetMatchPt(v_match_pt->at(mapMatchIndeces.at(indexMaxPtJetWithMatch)));
        auto const maxPtJetMatchEta(v_match_eta->at(mapMatchIndeces.at(indexMaxPtJetWithMatch)));
        H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0")->Fill(maxPtJetPt);
        H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0__vs__" + matchLabel + "_pt")
            ->Fill(maxPtJetPt, maxPtJetMatchPt);
        H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0__vs__" + matchLabel + "_eta")
            ->Fill(maxPtJetPt, maxPtJetMatchEta);
        if (maxPtJetMatchPt != 0.) {
          auto const maxPtJetPtRatio(maxPtJetPt / maxPtJetMatchPt);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel)
              ->Fill(maxPtJetPtRatio);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel +
             "__vs__" + matchLabel + "_pt")
              ->Fill(maxPtJetPtRatio, maxPtJetMatchPt);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel +
             "__vs__" + matchLabel + "_eta")
              ->Fill(maxPtJetPtRatio, maxPtJetMatchEta);
        }
      }

      if (indexMaxPtJetWithNoMatch >= 0) {
        auto const maxPtJetPt(v_pt->at(indexMaxPtJetWithNoMatch));
        H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_pt0")->Fill(maxPtJetPt);
      }
    }
  }
}

void JMETriggerAnalysisDriverRun2::fillHistograms_MET(const std::string& dir, const fillHistoDataMET& fhData) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }

  auto const* v_pt(this->vector_ptr<float>(fhData.metCollection + "_pt"));
  auto const* v_phi(this->vector_ptr<float>(fhData.metCollection + "_phi"));
  auto const* v_sumEt(this->vector_ptr<float>(fhData.metCollection + "_sumEt"));

  if (not(v_pt and v_phi and v_sumEt)) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriverRun2::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): " << fhData.metCollection + "_pt/phi/sumEt"
                << std::endl;
    }
    return;
  }

  if (not((v_pt->size() == 1) and (v_phi->size() == 1) and (v_sumEt->size() == 1))) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriverRun2::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData.metCollection + "_pt/phi/sumEt" << std::endl;
    }
    return;
  }

  auto const metPt(v_pt->at(0));
  auto const metPhi(v_phi->at(0));
  auto const metSumEt(v_sumEt->at(0));

  H1(dirPrefix + fhData.metCollection + "_pt")->Fill(metPt);
  H1(dirPrefix + fhData.metCollection + "_phi")->Fill(metPhi);
  H1(dirPrefix + fhData.metCollection + "_sumEt")->Fill(metSumEt);

  for (auto const& fhDataMatch : fhData.matches) {
    auto const matchLabel(fhDataMatch.label);
    auto const matchMetColl(fhDataMatch.metCollection);

    auto const* v_match_pt(this->vector_ptr<float>(matchMetColl + "_pt"));
    auto const* v_match_phi(this->vector_ptr<float>(matchMetColl + "_phi"));
    auto const* v_match_sumEt(this->vector_ptr<float>(matchMetColl + "_sumEt"));

    if (not(v_match_pt and v_match_phi and v_match_sumEt)) {
      if (verbosity_ >= 0) {
        std::cout << "JMETriggerAnalysisDriverRun2::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                  << "branches not available (histograms will not be filled): " << matchMetColl + "_pt/phi/sumEt"
                  << std::endl;
      }
      continue;
    }

    if (not((v_match_pt->size() == 1) and (v_match_phi->size() == 1) and (v_match_sumEt->size() == 1))) {
      if (verbosity_ >= 0) {
        std::cout << "JMETriggerAnalysisDriverRun2::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                  << "MET branches have invalid size (histograms will not be filled): "
                  << matchMetColl + "_pt/phi/sumEt" << std::endl;
      }
      continue;
    }

    auto const metMatchPt(v_match_pt->at(0));
    auto const metMatchPhi(v_match_phi->at(0));
    auto const metMatchSumEt(v_match_sumEt->at(0));

    if (metMatchPt != 0.) {
      auto const metPtRatio(metPt / metMatchPt);
      H2(dirPrefix + fhData.metCollection + "_pt__vs__" + matchLabel + "_pt")->Fill(metPt, metMatchPt);
      H1(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel)->Fill(metPtRatio);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_pt")
          ->Fill(metPtRatio, metMatchPt);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_phi")
          ->Fill(metPtRatio, metMatchPhi);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt")
          ->Fill(metPtRatio, metMatchSumEt);
    }

    if (metMatchSumEt != 0.) {
      auto const metSumEtRatio(metSumEt / metMatchSumEt);
      H2(dirPrefix + fhData.metCollection + "_sumEt__vs__" + matchLabel + "_sumEt")->Fill(metSumEt, metMatchSumEt);
      H1(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel)->Fill(metSumEtRatio);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_pt")
          ->Fill(metSumEtRatio, metMatchPt);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_phi")
          ->Fill(metSumEtRatio, metMatchPhi);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt")
          ->Fill(metSumEtRatio, metMatchSumEt);
    }

    auto const metDeltaPhiMatch(utils::deltaPhi(metPhi, metMatchPhi));
    H2(dirPrefix + fhData.metCollection + "_phi__vs__" + matchLabel + "_phi")->Fill(metPhi, metMatchPhi);
    H1(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel)->Fill(metDeltaPhiMatch);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_pt")
        ->Fill(metDeltaPhiMatch, metMatchPt);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_phi")
        ->Fill(metDeltaPhiMatch, metMatchPhi);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_sumEt")
        ->Fill(metDeltaPhiMatch, metMatchSumEt);

    auto const metParaToMatch(metPt *
                              (std::cos(metPhi) * std::cos(metMatchPhi) + std::sin(metPhi) * std::sin(metMatchPhi)));
    H1(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel)->Fill(metParaToMatch);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_pt")
        ->Fill(metParaToMatch, metMatchPt);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_phi")
        ->Fill(metParaToMatch, metMatchPhi);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_sumEt")
        ->Fill(metParaToMatch, metMatchSumEt);

    auto const metParaToMatchMinusMatch(metParaToMatch - metMatchPt);
    H1(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel)
        ->Fill(metParaToMatchMinusMatch);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel +
       "_pt")
        ->Fill(metParaToMatchMinusMatch, metMatchPt);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel +
       "_phi")
        ->Fill(metParaToMatchMinusMatch, metMatchPhi);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel +
       "_sumEt")
        ->Fill(metParaToMatchMinusMatch, metMatchSumEt);

    auto const metPerpToMatch(metPt *
                              (std::cos(metPhi) * std::sin(metMatchPhi) - std::sin(metPhi) * std::cos(metMatchPhi)));
    H1(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel)->Fill(metPerpToMatch);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_pt")
        ->Fill(metPerpToMatch, metMatchPt);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_phi")
        ->Fill(metPerpToMatch, metMatchPhi);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_sumEt")
        ->Fill(metPerpToMatch, metMatchSumEt);
  }
}
