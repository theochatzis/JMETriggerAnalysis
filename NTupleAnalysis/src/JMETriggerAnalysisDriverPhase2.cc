#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriverPhase2.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <utility>
#include <cmath>
#include <Math/GenVector/LorentzVector.h>
#include <Math/GenVector/PtEtaPhiM4D.h>

JMETriggerAnalysisDriverPhase2::JMETriggerAnalysisDriverPhase2(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriverPhase2(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriverPhase2::JMETriggerAnalysisDriverPhase2(const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriver(outputFilePath, outputFileMode) {}

bool JMETriggerAnalysisDriverPhase2::jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta) const {

  bool ret(false);
  if(categLabel == "_EtaIncl"){ ret = (jetAbsEta < 5.0); }
  else if(categLabel == "_EtaInclPt0"){ ret = (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_EtaInclPt1"){ ret = (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_EtaInclPt2"){ ret = (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_EtaInclPt3"){ ret = (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_EtaInclPt4"){ ret = (jetAbsEta < 5.0) and (2000. <= jetPt); }

  else if(categLabel == "_Eta2p4"){ ret = (jetAbsEta < 2.4); }
  else if(categLabel == "_Eta2p4Pt0"){ ret = (jetAbsEta < 2.4) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_Eta2p4Pt1"){ ret = (jetAbsEta < 2.4) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_Eta2p4Pt2"){ ret = (jetAbsEta < 2.4) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_Eta2p4Pt3"){ ret = (jetAbsEta < 2.4) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_Eta2p4Pt4"){ ret = (jetAbsEta < 2.4) and (2000. <= jetPt); }

  else if(categLabel == "_HB"){ ret = (jetAbsEta < 1.5); }
  else if(categLabel == "_HBPt0"){ ret = (jetAbsEta < 1.5) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HBPt1"){ ret = (jetAbsEta < 1.5) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HBPt2"){ ret = (jetAbsEta < 1.5) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HBPt3"){ ret = (jetAbsEta < 1.5) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HBPt4"){ ret = (jetAbsEta < 1.5) and (2000. <= jetPt); }

  else if(categLabel == "_HGCal"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if(categLabel == "_HGCalPt0"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HGCalPt1"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HGCalPt2"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HGCalPt3"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HGCalPt4"){ ret = (1.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (2000. <= jetPt); }

  else if(categLabel == "_HF"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if(categLabel == "_HFPt0"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HFPt1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HFPt2"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HFPt3"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HFPt4"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (2000. <= jetPt); }

  else if(categLabel == "_HF1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0); }
  else if(categLabel == "_HF1Pt0"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HF1Pt1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HF1Pt2"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HF1Pt3"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HF1Pt4"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (2000. <= jetPt); }

  else if(categLabel == "_HF2"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if(categLabel == "_HF2Pt0"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.); }
  else if(categLabel == "_HF2Pt1"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 110.); }
  else if(categLabel == "_HF2Pt2"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (110. <= jetPt) and (jetPt < 400.); }
  else if(categLabel == "_HF2Pt3"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt) and (jetPt < 2000.); }
  else if(categLabel == "_HF2Pt4"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (2000. <= jetPt); }

  return ret;
}

void JMETriggerAnalysisDriverPhase2::init(){

  jetCategoryLabels_ = {
    "_EtaIncl",
//  "_EtaInclPt0",
//  "_EtaInclPt1",
//  "_EtaInclPt2",
//  "_EtaInclPt3",
//  "_EtaInclPt4",

    "_Eta2p4",
//  "_Eta2p4Pt0",
//  "_Eta2p4Pt1",
//  "_Eta2p4Pt2",
//  "_Eta2p4Pt3",
//  "_Eta2p4Pt4",

    "_HB",
//  "_HBPt0",
//  "_HBPt1",
//  "_HBPt2",
//  "_HBPt3",
//  "_HBPt4",

    "_HGCal",
//  "_HGCalPt0",
//  "_HGCalPt1",
//  "_HGCalPt2",
//  "_HGCalPt3",
//  "_HGCalPt4",

    "_HF",
//  "_HFPt0",
//  "_HFPt1",
//  "_HFPt2",
//  "_HFPt3",
//  "_HFPt4",

//  "_HF1",
//  "_HF1Pt0",
//  "_HF1Pt1",
//  "_HF1Pt2",
//  "_HF1Pt3",
//  "_HF1Pt4",

//  "_HF2",
//  "_HF2Pt0",
//  "_HF2Pt1",
//  "_HF2Pt2",
//  "_HF2Pt3",
//  "_HF2Pt4",
  };

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});
  addTH1D("weight", 100, -5, 5);

  labelMap_jetAK4_.clear();
  labelMap_jetAK4_ = {
    {"ak4GenJetsNoNu", {
      {"l1tCaloCorr"    , "l1tAK4CaloJetsCorrected"},
      {"l1tPFCorr"      , "l1tAK4PFJetsCorrected"},
      {"l1tPFPuppiCorr2", "l1tAK4PFPuppiJetsCorrected"},
      {"l1tPFPuppiCorr" , "l1tSlwPFPuppiJetsCorrected"},
//    {"hltCalo"        , "hltAK4CaloJets"},
//    {"hltPFCluster"   , "hltAK4PFClusterJets"},
//    {"hltPF"          , "hltAK4PFJets"},
      {"hltPFCorr"      , "hltAK4PFJetsCorrected"},
//    {"hltPFCHS"       , "hltAK4PFCHSJets"},
      {"hltPFCHSCorr"   , "hltAK4PFCHSJetsCorrected"},
      {"hltPFPuppi"     , "hltAK4PFPuppiJets"},
      {"hltPFPuppiCorr" , "hltAK4PFPuppiJetsCorrected"},
//      {"offlPFPuppiCorr", "offlineAK4PFPuppiJetsCorrected"},
    }},

//    {"l1tAK4CaloJetsCorrected"   , {{"GEN", "ak4GenJetsNoNu"}}},
//    {"l1tAK4PFJetsCorrected"     , {{"GEN", "ak4GenJetsNoNu"}}},
//    {"l1tAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"l1tSlwPFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},//, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},

//  {"hltAK4CaloJets"            , {{"GEN", "ak4GenJetsNoNu"}}},
//  {"hltAK4PFClusterJets"       , {{"GEN", "ak4GenJetsNoNu"}}},
//  {"hltAK4PFJets"              , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFJetsCorrected"     , {{"GEN", "ak4GenJetsNoNu"}}},
//  {"hltAK4PFCHSJets"           , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFCHSJetsCorrected"  , {{"GEN", "ak4GenJetsNoNu"}}},//, {"Offline", "offlineAK4PFCHSJetsCorrected"}}},
//  {"hltAK4PFPuppiJets"         , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},//, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},

//    {"offlineAK4PFCHSJetsCorrected"  , {{"GEN", "ak4GenJetsNoNu"}}},
//    {"offlineAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},
  };

  labelMap_jetAK8_.clear();
  labelMap_jetAK8_ = {
    {"ak8GenJetsNoNu", {
//    {"hltCalo"        , "hltAK8CaloJets"},
//    {"hltPFCluster"   , "hltAK8PFClusterJets"},
//    {"hltPF"          , "hltAK8PFJets"},
      {"hltPFCorr"      , "hltAK8PFJetsCorrected"},
//    {"hltPFCHS"       , "hltAK8PFCHSJets"},
      {"hltPFCHSCorr"   , "hltAK8PFCHSJetsCorrected"},
//    {"hltPFPuppi"     , "hltAK8PFPuppiJets"},
      {"hltPFPuppiCorr" , "hltAK8PFPuppiJetsCorrected"},
//      {"offlPFPuppiCorr", "offlineAK8PFPuppiJetsCorrected"},
    }},

//  {"hltAK8CaloJets"            , {{"GEN", "ak8GenJetsNoNu"}}},
//  {"hltAK8PFClusterJets"       , {{"GEN", "ak8GenJetsNoNu"}}},
//  {"hltAK8PFJets"              , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFJetsCorrected"     , {{"GEN", "ak8GenJetsNoNu"}}},
//  {"hltAK8PFCHSJets"           , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFCHSJetsCorrected"  , {{"GEN", "ak8GenJetsNoNu"}}}, //, {"Offline", "offlineAK8PFCHSJetsCorrected"}}},
//  {"hltAK8PFPuppiJets"         , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFPuppiJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}}}, //, {"Offline", "offlineAK8PFPuppiJetsCorrected"}}},

//    {"offlineAK8PFCHSJetsCorrected"  , {{"GEN", "ak8GenJetsNoNu"}}},
//    {"offlineAK8PFPuppiJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}}},
  };

  labelMap_MET_.clear();
  labelMap_MET_ = {
    {"genMETCalo", {}},
    {"genMETTrue", {}},

    {"l1tCaloMET"   , {{"GEN", "genMETCalo"}}},
    {"l1tPFMET"     , {{"GEN", "genMETTrue"}}},//, {"Offline", "offlinePFMET_Raw"}}},
    {"l1tPFPuppiMET", {{"GEN", "genMETTrue"}}},//, {"Offline", "offlinePFPuppiMET_Raw"}}},

//    {"hltPFClusterMET"     , {{"GEN", "genMETCalo"}}},
//    {"hltPFMETNoMu"        , {{"GEN", "genMETCalo"}}},
    {"hltPFMET"            , {{"GEN", "genMETTrue"}}},//, {"Offline", "offlinePFMET_Raw"}}},
    {"hltPFCHSMET"         , {{"GEN", "genMETTrue"}}},
    {"hltPFSoftKillerMET"  , {{"GEN", "genMETTrue"}}},
//    {"hltPFPuppiMETNoMu"   , {{"GEN", "genMETCalo"}}},
    {"hltPFPuppiMET"       , {{"GEN", "genMETTrue"}}},//, {"Offline", "offlinePFPuppiMET_Raw"}}},
    {"hltPFPuppiMETv0"     , {{"GEN", "genMETTrue"}}},//, {"Offline", "offlinePuppiMET_Raw"}}},
    {"hltPFPuppiMETTypeOne", {{"GEN", "genMETTrue"}}},//, {"Offline", "offlinePuppiMET_Raw"}}},

//    {"offlinePFMET_Raw"       , {{"GEN", "genMETTrue"}}},
//    {"offlinePFMET_Type1"     , {{"GEN", "genMETTrue"}}},
//    {"offlinePFPuppiMET_Raw"  , {{"GEN", "genMETTrue"}}},
//    {"offlinePFPuppiMET_Type1", {{"GEN", "genMETTrue"}}},
  };

  for(auto const& selLabel : {
    "NoSelection",
  }){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "l1tSlwPFJetsCorrected");
//    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFJetsCorrected");

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "l1tSlwPFPuppiJetsCorrected");
//    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiHT", "l1tPFPuppiHT", true);

    // histograms: AK8 Jets
    for(auto const& jetLabel : labelMap_jetAK8_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }

    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "l1tPFMET");
//    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "offlinePFMET_Raw");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "l1tPFPuppiMET");
//    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "offlinePFPuppiMET_Raw");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMETTypeOne", "l1tPFPuppiMET");
//    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMETTypeOne", "offlinePFPuppiMET_Type1");

    bookHistograms_METMHT(selLabel);
  }

  l1tSeeds_1Jet_ = {
    "L1T_SinglePFPuppiJet200off",
    "L1T_SinglePFPuppiJet200off2",
    "L1T_SinglePFPuppiJet230off2",
//    "L1T_SinglePFPuppiJet280off2",
//    "L1T_SinglePFPuppiJet320off2",
//    "L1T_SinglePFPuppiJet350off2",
//    "L1T_SinglePFPuppiJet380off2",
//    "L1T_SinglePFPuppiJet400off2",
//    "L1T_SinglePFPuppiJet420off2",
  };

  for(auto const& selLabel : l1tSeeds_1Jet_){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }
  }

  l1tSeeds_HT_ = {
    "L1T_PFPuppiHT450off",
//    "L1T_PFPuppiHT450off2",
//    "L1T_PFPuppiHT500off2",
//    "L1T_PFPuppiHT550off2",
//    "L1T_PFPuppiHT600off2",
//    "L1T_PFPuppiHT650off2",
//    "L1T_PFPuppiHT700off2",
//    "L1T_PFPuppiHT750off2",
//    "L1T_PFPuppiHT800off2",
  };

  for(auto const& selLabel : l1tSeeds_HT_){

    for(auto const& jetLabel : labelMap_jetAK4_){
      if(jetLabel.first.find("GenJets") != std::string::npos) continue;

      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "l1tSlwPFJetsCorrected");
//    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFJetsCorrected");

    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "l1tSlwPFPuppiJetsCorrected");
//    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiHT", "l1tPFPuppiHT", true);
  }

  l1tSeeds_MET_ = {
    "L1T_PFPuppiMET200off",
    "L1T_PFPuppiMET200off2",
    "L1T_PFPuppiMET220off2",
//    "L1T_PFPuppiMET250off2",
  };

  for(auto const& selLabel : l1tSeeds_MET_){
    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }

    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "l1tPFMET");
//    bookHistograms_MET_2DMaps(selLabel, "hltPFMET", "offlinePFMET_Raw");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "l1tPFPuppiMET");
//    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMET", "offlinePFPuppiMET_Raw");

    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMETTypeOne", "l1tPFPuppiMET");
//    bookHistograms_MET_2DMaps(selLabel, "hltPFPuppiMETTypeOne", "offlinePFPuppiMET_Type1");

    bookHistograms_METMHT(selLabel);
  }
}

void JMETriggerAnalysisDriverPhase2::analyze(){
  H1("eventsProcessed")->Fill(0.5);

  float wgt(1.f);
  std::string const tfileName = theFile_->GetName();
  auto const tfileBasename = tfileName.substr(tfileName.find_last_of("/\\") + 1);
  if(utils::stringContains(tfileBasename, "MinBias") or
     (utils::stringContains(tfileBasename, "QCD") and not utils::stringContains(tfileBasename, "Flat"))){
    if(utils::stringContains(tfileBasename, "PU200"))
      wgt = value<double>("qcdWeightPU200");
    else if(utils::stringContains(tfileBasename, "PU140"))
      wgt = value<double>("qcdWeightPU140");
    else
      throw std::runtime_error("failed to determine weight choice from TFile basename: "+tfileName);
  }
  H1("weight")->Fill(wgt);

  //// AK4 Jets
  const float minAK4JetPt(30.);
  const float minAK4JetPtRef(20.);
  const float maxAK4JetDeltaRmatchRef(0.1);

  // Single-Jet
  for(auto const& jetLabel : labelMap_jetAK4_){
    auto const isGENJets = (jetLabel.first.find("GenJets") != std::string::npos);

    auto const jetPt1 = isGENJets ? minAK4JetPtRef : minAK4JetPt;
    auto const jetPt2 = isGENJets ? minAK4JetPtRef * 0.75 : minAK4JetPtRef;

    fillHistoDataJets fhDataAK4Jets;
    fhDataAK4Jets.jetCollection = jetLabel.first;
    fhDataAK4Jets.jetPtMin = jetPt1;
    fhDataAK4Jets.jetAbsEtaMax = 5.0;
    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK4Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK4JetDeltaRmatchRef));
    }

    fillHistograms_Jets("NoSelection", fhDataAK4Jets, wgt);

    if(jetLabel.first.find("l1t") == 0) continue;

    for(auto const& selLabel : l1tSeeds_1Jet_){
      auto const l1tSeed = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : l1tSingleJetSeed(selLabel);
      if(not l1tSeed){
        continue;
      }

      fillHistograms_Jets(selLabel, fhDataAK4Jets, wgt);
    }

    if(isGENJets) continue;

    for(auto const& selLabel : l1tSeeds_HT_){
      auto const l1tSeed = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : l1tHTSeed(selLabel);
      if(not l1tSeed){
        continue;
      }

      fillHistograms_Jets(selLabel, fhDataAK4Jets, wgt);
    }
  }

  // HT
  for(std::string const& jetType : {"PF", "PFPuppi"}){

    fillHistoDataJets fhDataL1TSLWJets;
    fhDataL1TSLWJets.jetCollection = "l1tSlw"+jetType+"JetsCorrected";
    fhDataL1TSLWJets.jetPtMin = minAK4JetPt;
    fhDataL1TSLWJets.jetAbsEtaMax = 2.4;

    fillHistoDataJets fhDataHLTAK4Jets;
    fhDataHLTAK4Jets.jetCollection = "hltAK4"+jetType+"JetsCorrected";
    fhDataHLTAK4Jets.jetPtMin = minAK4JetPt;
    fhDataHLTAK4Jets.jetAbsEtaMax = 5.0;

//    fillHistoDataJets fhDataOffAK4Jets;
//    fhDataOffAK4Jets.jetCollection = "offlineAK4"+jetType+"JetsCorrected";
//    fhDataOffAK4Jets.jetPtMin = minAK4JetPt;
//    fhDataOffAK4Jets.jetAbsEtaMax = 5.0;

    fillHistograms_Jets_2DMaps("NoSelection", fhDataHLTAK4Jets, fhDataL1TSLWJets, wgt);
//    fillHistograms_Jets_2DMaps("NoSelection", fhDataHLTAK4Jets, fhDataOffAK4Jets, wgt);

    fillHistoDataMET fhDataHLTHT;
    fhDataHLTHT.metCollection = "hlt"+jetType+"HT";

    fillHistoDataMET fhDataL1THT;
    fhDataL1THT.metCollection = "l1t"+jetType+"HT";

    fillHistograms_MET_2DMaps("NoSelection", fhDataHLTHT, fhDataL1THT, true, wgt);

    for(auto const& selLabel : l1tSeeds_HT_){
      auto const l1tSeed = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : l1tHTSeed(selLabel);
      if(not l1tSeed){
        continue;
      }

      fillHistograms_Jets_2DMaps(selLabel, fhDataHLTAK4Jets, fhDataL1TSLWJets, wgt);
//      fillHistograms_Jets_2DMaps(selLabel, fhDataHLTAK4Jets, fhDataOffAK4Jets, wgt);

      if(jetType == "PFPuppi"){
        fillHistograms_MET_2DMaps(selLabel, fhDataHLTHT, fhDataL1THT, true, wgt);
      }
    }
  }

  //// AK8 Jets
  const float minAK8JetPt(90.);
  const float minAK8JetPtRef(60.);
  const float maxAK8JetDeltaRmatchRef(0.1);

  for(auto const& jetLabel : labelMap_jetAK8_){
    auto const isGENJets = (jetLabel.first.find("GenJets") != std::string::npos);

    auto const jetPt1 = isGENJets ? minAK8JetPtRef : minAK8JetPt;
    auto const jetPt2 = isGENJets ? minAK8JetPtRef * 0.75 : minAK8JetPtRef;

    fillHistoDataJets fhDataAK8Jets;
    fhDataAK8Jets.jetCollection = jetLabel.first;
    fhDataAK8Jets.jetPtMin = jetPt1;
    fhDataAK8Jets.jetAbsEtaMax = 5.0;

    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK8Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK8JetDeltaRmatchRef));
    }

    fillHistograms_Jets("NoSelection", fhDataAK8Jets, wgt);
  }

  //// MET
  for(auto const& metLabel : labelMap_MET_){
    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel.first;
    for(auto const& metRefs : metLabel.second){
      fhDataMET.matches.emplace_back(fillHistoDataMET::Match(metRefs.first, metRefs.second));
    }

    fillHistograms_MET("NoSelection", fhDataMET, wgt);

    for(auto const& selLabel : l1tSeeds_MET_){
      auto const l1tSeed = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : l1tMETSeed(selLabel);
      if(l1tSeed){
        fillHistograms_MET(selLabel, fhDataMET, wgt);
      }
    }
  }

  std::vector<std::vector<std::string>> metTypes({
    {"l1tPFMET", "hltPFMET", "offlinePFMET_Raw"},
    {"l1tPFPuppiMET", "hltPFPuppiMET", "offlinePFPuppiMET_Raw"},
    {"l1tPFPuppiMET", "hltPFPuppiMETTypeOne", "offlinePFPuppiMET_Type1"},
  });

  for(auto const& metType : metTypes){

    fillHistoDataMET fhDataL1TMET;
    fhDataL1TMET.metCollection = metType.at(0);

    fillHistoDataMET fhDataHLTMET;
    fhDataHLTMET.metCollection = metType.at(1);

//    fillHistoDataMET fhDataOffMET;
//    fhDataOffMET.metCollection = metType.at(2);

    fillHistograms_MET_2DMaps("NoSelection", fhDataHLTMET, fhDataL1TMET, false, wgt);
//    fillHistograms_MET_2DMaps("NoSelection", fhDataHLTMET, fhDataOffMET, false, wgt);

    for(auto const& selLabel : l1tSeeds_MET_){
      auto const l1tSeed = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : l1tMETSeed(selLabel);
      if(l1tSeed){
        fillHistograms_MET_2DMaps(selLabel, fhDataHLTMET, fhDataL1TMET, false, wgt);
//        fillHistograms_MET_2DMaps(selLabel, fhDataHLTMET, fhDataOffMET, false, wgt);
      }
    }
  }

  //// MET+MHT
  fillHistograms_METMHT("NoSelection", wgt);

  for(auto const& selLabel : l1tSeeds_MET_){
    auto const l1tSeed = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : l1tMETSeed(selLabel);
    if(l1tSeed){
      fillHistograms_METMHT(selLabel, wgt);
    }
  }
}

void JMETriggerAnalysisDriverPhase2::bookHistograms_Jets_2DMaps(const std::string& dir, const std::string& jetType1, const std::string& jetType2){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_HT(221);
  for(uint idx=0; idx<binEdges_HT.size(); ++idx){ binEdges_HT.at(idx) = idx * 10.; }

  addTH2D(dirPrefix+jetType1+"_HT__vs__"+jetType2+"_HT", binEdges_HT, binEdges_HT);
}

void JMETriggerAnalysisDriverPhase2::bookHistograms_MET_2DMaps(const std::string& dir, const std::string& metType1, const std::string& metType2, bool const book1D){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_pt(81);
  for(uint idx=0; idx<binEdges_pt.size(); ++idx){ binEdges_pt.at(idx) = idx * 10.; }

  std::vector<float> binEdges_phi(41);
  for(uint idx=0; idx<binEdges_phi.size(); ++idx){ binEdges_phi.at(idx) = M_PI*(0.05*idx - 1.); }

  std::vector<float> binEdges_sumEt(221);
  for(uint idx=0; idx<binEdges_sumEt.size(); ++idx){ binEdges_sumEt.at(idx) = idx * 10.; }

  if(book1D){
    addTH1D(dirPrefix+metType1+"_pt", binEdges_pt);
    addTH1D(dirPrefix+metType1+"_phi", binEdges_phi);
    addTH1D(dirPrefix+metType1+"_sumEt", binEdges_sumEt);

    addTH1D(dirPrefix+metType2+"_pt", binEdges_pt);
    addTH1D(dirPrefix+metType2+"_phi", binEdges_phi);
    addTH1D(dirPrefix+metType2+"_sumEt", binEdges_sumEt);
  }

  addTH2D(dirPrefix+metType1+"_pt__vs__"+metType2+"_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+metType1+"_phi__vs__"+metType2+"_phi", binEdges_phi, binEdges_phi);
  addTH2D(dirPrefix+metType1+"_sumEt__vs__"+metType2+"_sumEt", binEdges_sumEt, binEdges_sumEt);
}

void JMETriggerAnalysisDriverPhase2::fillHistograms_Jets_2DMaps(const std::string& dir, const fillHistoDataJets& fhData1, const fillHistoDataJets& fhData2, float const weight){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt1(this->vector_ptr<float>(fhData1.jetCollection+"_pt"));
  auto const* v_eta1(this->vector_ptr<float>(fhData1.jetCollection+"_eta"));

  if(not (v_pt1 and v_eta1)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_Jets_2DMaps(\"" << dir << "\", const fillHistoDataJets&, const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData1.jetCollection+"_pt/eta" << std::endl;
    }
    return;
  }

  auto const* v_pt2(this->vector_ptr<float>(fhData2.jetCollection+"_pt"));
  auto const* v_eta2(this->vector_ptr<float>(fhData2.jetCollection+"_eta"));

  if(not (v_pt2 and v_eta2)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_Jets_2DMaps(\"" << dir << "\", const fillHistoDataJets&, const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData2.jetCollection+"_pt/eta" << std::endl;
    }
    return;
  }

  float sumPt1(0.);
  for(size_t idx=0; idx<v_pt1->size(); ++idx){
    if(v_pt1->at(idx) > fhData1.jetPtMin and std::abs(v_eta1->at(idx)) < fhData1.jetAbsEtaMax){
      sumPt1 += v_pt1->at(idx);
    }
  }

  float sumPt2(0.);
  for(size_t idx=0; idx<v_pt2->size(); ++idx){
    if(v_pt2->at(idx) > fhData2.jetPtMin and std::abs(v_eta2->at(idx)) < fhData2.jetAbsEtaMax){
      sumPt2 += v_pt2->at(idx);
    }
  }

  H2(dirPrefix+fhData1.jetCollection+"_HT__vs__"+fhData2.jetCollection+"_HT")->Fill(sumPt1, sumPt2, weight);
}

void JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(const std::string& dir, const fillHistoDataMET& fhData1, const fillHistoDataMET& fhData2, bool const fill1D, float const weight){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt1(this->vector_ptr<float>(fhData1.metCollection+"_pt"));
  if(not v_pt1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData1.metCollection+"_pt" << std::endl;
    }
    return;
  }
  else if(v_pt1->size() != 1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData1.metCollection+"_pt" << std::endl;
    }
    return;
  }

  auto const* v_pt2(this->vector_ptr<float>(fhData2.metCollection+"_pt"));
  if(not v_pt2){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData2.metCollection+"_pt" << std::endl;
    }
    return;
  }
  else if(v_pt2->size() != 1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverPhase2::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData2.metCollection+"_pt" << std::endl;
    }
    return;
  }

  auto const* v_phi1(this->vector_ptr<float>(fhData1.metCollection+"_phi"));
  auto const* v_phi2(this->vector_ptr<float>(fhData2.metCollection+"_phi"));

  auto const* v_sumEt1(this->vector_ptr<float>(fhData1.metCollection+"_sumEt"));
  auto const* v_sumEt2(this->vector_ptr<float>(fhData2.metCollection+"_sumEt"));

  auto const met1_pt(v_pt1->at(0)), met1_phi(v_phi1->at(0)), met1_sumEt(v_sumEt1->at(0));
  auto const met2_pt(v_pt2->at(0)), met2_phi(v_phi2->at(0)), met2_sumEt(v_sumEt2->at(0));

  if(fill1D){
    H1(dirPrefix+fhData1.metCollection+"_pt")->Fill(met1_pt, weight);
    H1(dirPrefix+fhData1.metCollection+"_phi")->Fill(met1_phi, weight);
    H1(dirPrefix+fhData1.metCollection+"_sumEt")->Fill(met1_sumEt, weight);

    H1(dirPrefix+fhData2.metCollection+"_pt")->Fill(met2_pt, weight);
    H1(dirPrefix+fhData2.metCollection+"_phi")->Fill(met2_phi, weight);
    H1(dirPrefix+fhData2.metCollection+"_sumEt")->Fill(met2_sumEt, weight);
  }

  H2(dirPrefix+fhData1.metCollection+"_pt__vs__"+fhData2.metCollection+"_pt")->Fill(met1_pt, met2_pt, weight);
  H2(dirPrefix+fhData1.metCollection+"_phi__vs__"+fhData2.metCollection+"_phi")->Fill(met1_phi, met2_phi, weight);
  H2(dirPrefix+fhData1.metCollection+"_sumEt__vs__"+fhData2.metCollection+"_sumEt")->Fill(met1_sumEt, met2_sumEt, weight);
}

void JMETriggerAnalysisDriverPhase2::bookHistograms_METMHT(const std::string& dir){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_pt(161);
  for(uint idx=0; idx<binEdges_pt.size(); ++idx){ binEdges_pt.at(idx) = idx * 5.; }

  std::vector<float> binEdges_pt_2(37);
  for(uint idx=0; idx<binEdges_pt_2.size(); ++idx){ binEdges_pt_2.at(idx) = 80. + idx * 5.; }

  addTH2D(dirPrefix+"genMETTrue_pt__vs__l1tPFPuppiMET_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT20_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT30_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT40_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT50_pt", binEdges_pt, binEdges_pt);
  addTH3D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT20_pt", binEdges_pt, binEdges_pt_2, binEdges_pt_2);
  addTH3D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT30_pt", binEdges_pt, binEdges_pt_2, binEdges_pt_2);
  addTH3D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT40_pt", binEdges_pt, binEdges_pt_2, binEdges_pt_2);
  addTH3D(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT50_pt", binEdges_pt, binEdges_pt_2, binEdges_pt_2);
  addTH2D(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT20_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT30_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT40_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT50_pt", binEdges_pt, binEdges_pt);
}

void JMETriggerAnalysisDriverPhase2::fillHistograms_METMHT(const std::string& dir, float const weight){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  // MET
  auto const genMETTrue_pt = getMET("genMETTrue_pt");
  auto const l1tPFPuppiMET_pt = getMET("l1tPFPuppiMET_pt");
  auto const hltPFPuppiMETTypeOne_pt = getMET("hltPFPuppiMETTypeOne_pt");

  // MHT
  auto const hltPFPuppiMHT20_pt = getMHT(20., 5.0);
  auto const hltPFPuppiMHT30_pt = getMHT(30., 5.0);
  auto const hltPFPuppiMHT40_pt = getMHT(40., 5.0);
  auto const hltPFPuppiMHT50_pt = getMHT(50., 5.0);

  // filling of histograms
  H2(dirPrefix+"genMETTrue_pt__vs__l1tPFPuppiMET_pt")->Fill(genMETTrue_pt, l1tPFPuppiMET_pt, weight);
  H2(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt")->Fill(genMETTrue_pt, hltPFPuppiMETTypeOne_pt, weight);
  H2(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT20_pt")->Fill(genMETTrue_pt, hltPFPuppiMHT20_pt, weight);
  H2(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT30_pt")->Fill(genMETTrue_pt, hltPFPuppiMHT30_pt, weight);
  H2(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT40_pt")->Fill(genMETTrue_pt, hltPFPuppiMHT40_pt, weight);
  H2(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMHT50_pt")->Fill(genMETTrue_pt, hltPFPuppiMHT50_pt, weight);
  H3(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT20_pt")->Fill(genMETTrue_pt, hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT20_pt, weight);
  H3(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT30_pt")->Fill(genMETTrue_pt, hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT30_pt, weight);
  H3(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT40_pt")->Fill(genMETTrue_pt, hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT40_pt, weight);
  H3(dirPrefix+"genMETTrue_pt__vs__hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT50_pt")->Fill(genMETTrue_pt, hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT50_pt, weight);
  H2(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT20_pt")->Fill(hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT20_pt, weight);
  H2(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT30_pt")->Fill(hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT30_pt, weight);
  H2(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT40_pt")->Fill(hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT40_pt, weight);
  H2(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT50_pt")->Fill(hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT50_pt, weight);
}

bool JMETriggerAnalysisDriverPhase2::l1tSingleJetSeed(std::string const& key) const {

  auto const* v_pt = vector_ptr<float>("l1tSlwPFPuppiJetsCorrected_pt");
  auto const* v_eta = vector_ptr<float>("l1tSlwPFPuppiJetsCorrected_eta");

  if(not (v_pt and v_eta)){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriverPhase2::l1tSingleJetSeed(\"" << key << "\") -- "
        << "branches not available (histograms will not be filled): "
        << "l1tSlwPFPuppiJetsCorrected_{pt,eta}";
    throw std::runtime_error(oss.str());
  }

  int jetIndex(-1);
  float max_pt(-1.);
  for(uint idx=0; idx<v_pt->size(); ++idx){
    if(std::abs(v_eta->at(idx)) >= 5.) continue;
    if(v_pt->at(idx) > max_pt){
      max_pt = v_pt->at(idx);
      jetIndex = idx;
    }
  }

  if(jetIndex < 0) return false;

  auto const pt = v_pt->at(jetIndex);
  auto const eta = v_eta->at(jetIndex);

  float offlinePt(0.f);
  if(std::abs(eta) < 1.5) offlinePt = 1.40627 * pt + 11.1254;
  else if(std::abs(eta) < 2.4) offlinePt = 1.4152 * pt + 24.8375;
  else offlinePt = 1.33052 * pt + 42.4039;

  if(key == "L1T_SinglePFPuppiJet200off2") return offlinePt > 200.;
  else if(key == "L1T_SinglePFPuppiJet230off2") return offlinePt > 230.;
  else if(key == "L1T_SinglePFPuppiJet280off2") return offlinePt > 280.;
  else if(key == "L1T_SinglePFPuppiJet320off2") return offlinePt > 320.;
  else if(key == "L1T_SinglePFPuppiJet350off2") return offlinePt > 350.;
  else if(key == "L1T_SinglePFPuppiJet380off2") return offlinePt > 380.;
  else if(key == "L1T_SinglePFPuppiJet400off2") return offlinePt > 400.;
  else if(key == "L1T_SinglePFPuppiJet420off2") return offlinePt > 420.;
  else
    throw std::runtime_error("JMETriggerAnalysisDriverPhase2::l1tSingleJetSeed(\""+key+"\") -- invalid key");

  return false;
}

bool JMETriggerAnalysisDriverPhase2::l1tHTSeed(std::string const& key) const {

  auto const* v_pt = vector_ptr<float>("l1tSlwPFPuppiJetsCorrected_pt");
  auto const* v_eta = vector_ptr<float>("l1tSlwPFPuppiJetsCorrected_eta");

  if(not (v_pt and v_eta)){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriverPhase2::l1tHTSeed(\"" << key << "\") -- "
        << "branches not available (histograms will not be filled): "
        << "l1tSlwPFPuppiJetsCorrected_{pt,eta}";
    throw std::runtime_error(oss.str());
  }

  float l1tHT(0.);
  for(uint idx=0; idx<v_pt->size(); ++idx){
    if(v_pt->at(idx) > 30. and std::abs(v_eta->at(idx)) < 2.4)
      l1tHT += v_pt->at(idx);
  }

  auto const offlineHT = l1tHT * 1.0961 + 50.0182;

  if(key == "L1T_PFPuppiHT450off2") return offlineHT > 450.;
  else if(key == "L1T_PFPuppiHT500off2") return offlineHT > 500.;
  else if(key == "L1T_PFPuppiHT550off2") return offlineHT > 550.;
  else if(key == "L1T_PFPuppiHT600off2") return offlineHT > 600.;
  else if(key == "L1T_PFPuppiHT650off2") return offlineHT > 650.;
  else if(key == "L1T_PFPuppiHT700off2") return offlineHT > 700.;
  else if(key == "L1T_PFPuppiHT750off2") return offlineHT > 750.;
  else if(key == "L1T_PFPuppiHT800off2") return offlineHT > 800.;
  else
    throw std::runtime_error("JMETriggerAnalysisDriverPhase2::l1tHTSeed(\""+key+"\") -- invalid key");

  return false;
}

bool JMETriggerAnalysisDriverPhase2::l1tMETSeed(std::string const& key) const {

  auto const offlineMET = getMET("l1tPFPuppiMET_pt") * 1.39739 + 54.2859;

  if(key == "L1T_PFPuppiMET200off2") return offlineMET > 200.;
  else if(key == "L1T_PFPuppiMET220off2") return offlineMET > 220.;
  else if(key == "L1T_PFPuppiMET250off2") return offlineMET > 250.;
  else
    throw std::runtime_error("JMETriggerAnalysisDriverPhase2::l1tMETSeed(\""+key+"\") -- invalid key");

  return false;
}

float JMETriggerAnalysisDriverPhase2::getMET(std::string const& branchName) const {
  auto const& v_pt = this->vector<float>(branchName);

  if(v_pt.size() != 1){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriverPhase2::fillHistograms(\"" << branchName << "\") -- "
        << "MET branches have invalid size (" << v_pt.size() << " != 1)";
    throw std::runtime_error(oss.str());
  }

  return v_pt.at(0);
}

float JMETriggerAnalysisDriverPhase2::getMHT(float const jetPtMin, float const jetAbsEtaMax) const {
  auto const& v_pt = vector<float>("hltAK4PFPuppiJetsCorrected_pt");
  auto const& v_eta = vector<float>("hltAK4PFPuppiJetsCorrected_eta");
  auto const& v_phi = vector<float>("hltAK4PFPuppiJetsCorrected_phi");
  auto const& v_mass = vector<float>("hltAK4PFPuppiJetsCorrected_mass");
/*
  auto const& v_GEN_pt = vector<float>("ak4GenJetsNoNu_pt");
  auto const& v_GEN_eta = vector<float>("ak4GenJetsNoNu_eta");
  auto const& v_GEN_phi = vector<float>("ak4GenJetsNoNu_phi");
*/
  float MHT_x(0.f), MHT_y(0.f);
  for(size_t jetIdx=0; jetIdx<v_pt.size(); ++jetIdx){
    if(std::abs(v_eta.at(jetIdx)) >= jetAbsEtaMax) continue;
/*
    bool isMatchedToGEN = false;
    for(size_t genJetIdx=0; genJetIdx<v_GEN_pt.size(); ++genJetIdx){
      if(v_GEN_pt.at(genJetIdx) <= 20.) continue;

      auto const dR2 = utils::deltaR2(v_eta.at(jetIdx), v_phi.at(jetIdx), v_GEN_eta.at(genJetIdx), v_GEN_phi.at(genJetIdx));
      if(dR2 < 0.01){
        isMatchedToGEN = true;
        break;
      }
    }
    if(not isMatchedToGEN) continue;
*/
    ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>> const p4polar(v_pt.at(jetIdx), v_eta.at(jetIdx), v_phi.at(jetIdx), v_mass.at(jetIdx));

    auto const jetPtMin_new = jetPtMin; //!! (std::abs(p4polar.Eta()) < 2.95 or std::abs(p4polar.Eta()) > 3.05) ? jetPtMin : std::max(60.f, jetPtMin);

    if(p4polar.Pt() > jetPtMin_new){
      MHT_x -= p4polar.Px();
      MHT_y -= p4polar.Py();
    }

//!!    if(p4polar.Et() > jetPtMin){
//!!      MHT_x -= p4polar.Et() * std::cos(v_phi.at(jetIdx));
//!!      MHT_y -= p4polar.Et() * std::sin(v_phi.at(jetIdx));
//!!    }
  }

  return sqrt(MHT_x*MHT_x + MHT_y*MHT_y);
}
