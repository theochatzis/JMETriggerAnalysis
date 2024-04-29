#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriverRun3.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <utility>
#include <cmath>
#include <Math/GenVector/LorentzVector.h>
#include <Math/GenVector/PtEtaPhiM4D.h>

JMETriggerAnalysisDriverRun3::JMETriggerAnalysisDriverRun3(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriverRun3(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriverRun3::JMETriggerAnalysisDriverRun3(const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriver(outputFilePath, outputFileMode) {}

bool JMETriggerAnalysisDriverRun3::jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta, const float jetPhi, const float jetEta) const {

  bool ret(false);
  if(categLabel == "_EtaIncl"){ ret = (jetAbsEta < 5.0); }
  else if(categLabel == "_Eta2p5"){ ret = (jetAbsEta < 2.5); }
  else if(categLabel == "_HB"){ ret = (jetAbsEta < 1.3); } 
  else if (categLabel == "_HBPt0" ) {  //------------- pt regions
    ret = (jetAbsEta < 1.3) and (jetPt < 60.) and (jetEta < 0.);
  } else if (categLabel == "_HBPt1" ) {
    ret = (jetAbsEta < 1.3) and (60. <= jetPt) and (jetPt <= 80) and (jetEta < 0.);
  } else if (categLabel == "_HBPt2" ) {
    ret = (jetAbsEta < 1.3) and (80. <= jetPt) and (jetPt <= 130) and (jetEta < 0.);
  } else if (categLabel == "_HBPt3" ) {
    ret = (jetAbsEta < 1.3) and (130 <= jetPt) and (jetEta < 0.);
  } 
  else if(categLabel == "_HE"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if(categLabel == "_HE1"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5); }
  else if (categLabel == "_HE1Pt0" ) {  //------------- pt regions
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (jetPt < 60.);
  } else if (categLabel == "_HE1Pt1" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HE1Pt2" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HE1Pt3" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (130 <= jetPt);
  } 
  else if(categLabel == "_HE2"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if (categLabel == "_HE2Pt0" ) {  //------------- pt regions
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (jetPt < 60.);
  } else if (categLabel == "_HE2Pt1" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HE2Pt2" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HE2Pt3" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (130 <= jetPt);
  } 
  else if(categLabel == "_HF"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if (categLabel == "_HFPt0" ) {  //------------- pt regions
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (jetPt < 60.);
  } else if (categLabel == "_HFPt1" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HFPt2" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HFPt3" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (130 <= jetPt);
  } 
  
  
  else if(categLabel == "_HE21"){ ret = (2.5 <= jetAbsEta) and (jetAbsEta < 2.7); }
  else if (categLabel == "_HE21Pt0" ) {  //------------- pt regions
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 2.7) and (jetPt < 60.);
  } else if (categLabel == "_HE21Pt1" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 2.7) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HE21Pt2" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 2.7) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HE21Pt3" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 2.7) and (130 <= jetPt);
  } 
  else if(categLabel == "_HE22"){ ret = (2.7 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if (categLabel == "_HE22Pt0" ) {  //------------- pt regions
    ret = (2.7 <= jetAbsEta) and (jetAbsEta < 3.0) and (jetPt < 60.);
  } else if (categLabel == "_HE22Pt1" ) {
    ret = (2.7 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HE22Pt2" ) {
    ret = (2.7 <= jetAbsEta) and (jetAbsEta < 3.0) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HE22Pt3" ) {
    ret = (2.7 <= jetAbsEta) and (jetAbsEta < 3.0) and (130 <= jetPt);
  } 
  else if(categLabel == "_BPix"){ ret = (jetEta < 0.) and (jetEta>-1.5) and (jetPhi<-0.8) and (jetPhi>-1.2);}
  else if(categLabel == "_BPixVeto"){ ret = !((jetEta < 0.) and (jetEta>-1.5) and (jetPhi<-0.8) and (jetPhi>-1.2)) and jetAbsEta<=1.5;}
  else if(categLabel == "_BPix_plus4"){ ret = (jetEta < 0.) and (jetEta>-1.5) and (jetPhi<-0.6) and (jetPhi>-0.8);}
  else if(categLabel == "_BPix_minus4"){ ret = (jetEta < 0.) and (jetEta>-1.5) and (jetPhi<-1.2) and (jetPhi>-1.4);}
  else if(categLabel == "_BPix_plus8"){ ret = (jetEta < 0.) and (jetEta>-1.5) and (jetPhi<-0.4) and (jetPhi>-0.8);}
  else if(categLabel == "_BPix_minus8"){ ret = (jetEta < 0.) and (jetEta>-1.5) and (jetPhi<-1.2) and (jetPhi>-1.6);}
  return ret;
}

void JMETriggerAnalysisDriverRun3::init(){

  jetCategoryLabels_ = {
    "_EtaIncl",
    //"_Eta2p5",
    "_HB",
    // "_HBPt0",
    // "_HBPt1",
    // "_HBPt2",
    // "_HBPt3",
    //"_HE",
    "_HE1",
    // "_HE1Pt0",
    // "_HE1Pt1",
    // "_HE1Pt2",
    // "_HE1Pt3",
    "_HE2",
    // "_HE2Pt0",
    // "_HE2Pt1",
    // "_HE2Pt2",
    // "_HE2Pt3",
    "_HE21",
    "_HE21Pt0",
    "_HE21Pt1",
    "_HE21Pt2",
    "_HE21Pt3",
    "_HE22",
    "_HE22Pt0",
    "_HE22Pt1",
    "_HE22Pt2",
    "_HE22Pt3",
    "_HF",
    // "_HFPt0",
    // "_HFPt1",
    // "_HFPt2",
    // "_HFPt3",
    // "_BPix",
    // "_BPix_plus4",
    // "_BPix_minus4",
    // "_BPix_plus8",
    // "_BPix_minus8",
    // "_BPixVeto",
  };

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});
  addTH1D("weight", 100, -5, 5);

  labelMap_jetAK4_.clear();
  labelMap_jetAK4_ = {
    {"ak4GenJetsNoNu"                ,{{"hltCaloCorr", "hltAK4CaloJetsCorrected"},{"hltPFCorr", "hltAK4PFJetsCorrected"}}},
    //{"ak4GenJetsNoNu"                ,{{"hltCalo", "hltAK4CaloJets"},{"hltPF", "hltAK4PFJets"}}},
    //        {"hltCaloCorr", "hltAK4CaloJetsCorrected"},
    //        //{"hltPFClusterCorr", "hltAK4PFClusterJetsCorrected"},
    //        {"hltPFCorr", "hltAK4PFJetsCorrected"},
    //        {"offlPFCorr", "offlineAK4PFCHSJetsCorrected"},
    //        //{"hltPFPuppiCorr", "hltAK4PFPuppiJetsCorrected"},
    //        {"offlPFPuppiCorr", "offlineAK4PFPuppiJetsCorrected"}}},
    {"hltAK4CaloJetsCorrected"              , {{"GEN", "ak4GenJetsNoNu"}}},
    //{"hltAK4CaloJets"     , {{"GEN", "ak4GenJetsNoNu"}}},
    //{"hltAK4PFClusterJets"         , {{"GEN", "ak4GenJetsNoNu"}}},
    //{"hltAK4PFClusterJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}}},
    //{"hltAK4PFJets"                , {{"GEN", "ak4GenJetsNoNu"}}},
    {"hltAK4PFJetsCorrected"                , {{"GEN", "ak4GenJetsNoNu"}}},
    //{"hltAK4PFJetsCorrected"       , {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    //{"hltAK4PFPuppiJets"           , {{"GEN", "ak4GenJetsNoNu"}}},
    //{"hltAK4PFPuppiJetsCorrected"  , {{"GEN", "ak4GenJetsNoNu"}, {"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    //{"offlineAK4PFCHSJetsCorrected"   , {{"GEN", "ak4GenJetsNoNu"}, {"HLT", "hltAK4PFJetsCorrected"}}},
    //{"offlineAK4PFPuppiJetsCorrected", {{"GEN", "ak4GenJetsNoNu"}, {"HLT", "hltAK4PFJetsCorrected"}}},
    // {"offlineAK4PFPuppiJets", {{"GEN", "ak4GenJetsNoNu"}}},
  };

  labelMap_jetAK8_.clear();
  labelMap_jetAK8_ = {
    {"ak8GenJetsNoNu"                ,{{"hltCaloCorr", "hltAK8CaloJetsCorrected"},{"hltPFCorr", "hltAK8PFJetsCorrected"}}},
    // {"ak8GenJetsNoNu",{
    //        {"hltCaloCorr", "hltAK8CaloJetsCorrected"},
    //        //{"hltPFClusterCorr", "hltAK8PFClusterJetsCorrected"},
    //        {"hltPFCorr", "hltAK8PFJetsCorrected"},
    //        {"offlPFCorr", "offlineAK8PFJetsCorrected"},
    //        //{"hltPFPuppiCorr", "hltAK8PFPuppiJetsCorrected"},
    //        {"offlPFPuppiCorr", "offlineAK8PFPuppiJetsCorrected"}}},
    //{"hltAK8CaloJets"              , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8CaloJetsCorrected"     , {{"GEN", "ak8GenJetsNoNu"}}},
    // {"hltAK8PFClusterJets"         , {{"GEN", "ak8GenJetsNoNu"}}},
    // {"hltAK8PFClusterJetsCorrected", {{"GEN", "ak8GenJetsNoNu"}}},
    // {"hltAK8PFJets"                , {{"GEN", "ak8GenJetsNoNu"}}},
    {"hltAK8PFJetsCorrected"       , {{"GEN", "ak8GenJetsNoNu"}}},
    //{"hltAK8PFPuppiJets"           , {{"GEN", "ak8GenJetsNoNu"}}},
    //{"hltAK8PFPuppiJetsCorrected"  , {{"GEN", "ak8GenJetsNoNu"}}},
  };

  labelMap_MET_.clear();
  labelMap_MET_ = {
    //{"genMETCalo", {}},
    //{"genMETTrue", {}},
    //{"hltCaloMET"             , {{"GEN", "genMETCalo"}}},
    //{"hltCaloMETTypeOne"      , {{"GEN", "genMETCalo"}}},
    //{"hltPFClusterMET"        , {{"GEN", "genMETCalo"}}},
    //{"hltPFClusterMETTypeOne" , {{"GEN", "genMETCalo"}}},
    //{"hltPFMET"               , {{"GEN", "genMETTrue"}}},
    //{"hltPFMETTypeOne"        , {{"GEN", "genMETTrue"}}},
    //{"hltPFPuppiMET"          , {{"GEN", "genMETTrue"}}},
    //{"hltPFPuppiMETTypeOne"   , {{"GEN", "genMETTrue"}}},
    //{"offlinePFPuppiMET", {}}
    //{"offlinePFMET_Raw"       , {{"GEN", "genMETTrue"}}},
    //{"offlinePFMET_Type1"     , {{"GEN", "genMETTrue"}}},
    //{"offlinePFPuppiMET_Raw"  , {{"GEN", "genMETTrue"}}},
    //{"offlinePFPuppiMET_Type1", {{"GEN", "genMETTrue"}}},
  };

  for(auto const& selLabel : {
    "NoSelection",
  }){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    //bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFCHSJetsCorrected");
    //bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");

    // histograms: AK8 Jets
    for(auto const& jetLabel : labelMap_jetAK8_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }

    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }

    //bookHistograms_METMHT(selLabel);
  }

  jettriggers = {
  // "HLT_PFJet60",
  // "HLT_PFJet80",
  // "HLT_PFJet110",
  // "HLT_PFJet140",
  // "HLT_PFJet320",
  // "HLT_PFJet500",
  // "HLT_PFJetFwd60",
  // "HLT_PFJetFwd80",
  // "HLT_PFJetFwd140",
  // "HLT_PFJetFwd320",
  // "HLT_PFJetFwd500",
  // "HLT_PFJet60",
  // //"HLT_PFJet110",
  // "HLT_PFJet140",
  // "HLT_PFJet320",
  // "HLT_PFJet500",
  };

  for(auto const& selLabel : jettriggers){
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    } 
  }

  httriggers = {
  // "HLT_PFHT180",
  // "HLT_PFHT250",
  // "HLT_PFHT350",
  // "HLT_PFHT510",
  // "HLT_PFHT780",
  // "HLT_PFHT890",
  // "HLT_PFHT1050",
  // //"HLT_PFHT180",
  // //"HLT_PFHT250",
  // //"HLT_PFHT350",
  // //"HLT_PFHT510",
  // "HLT_PFHT780",
  // "HLT_PFHT890",
  // "HLT_PFHT1050",
  };

  for(auto const& selLabel : httriggers){
    for(auto const& jetLabel : labelMap_jetAK4_){
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second));
    }
    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFCHSJetsCorrected");
    bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");
  }

  mettriggers = {
  // "HLT_PFMET120_PFMHT120_IDTight",
  // "HLT_PFMET140_PFMHT140_IDTight",
  // "HLT_PFMETTypeOne140_PFMHT140_IDTight",
  };

  for(auto const& selLabel : mettriggers){
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }
    bookHistograms_METMHT(selLabel);
  }

  puintervals = {
  // "PU0to20",
  // "PU20to40",
  // "PUgt40",
  // "PU0to20_HLT",
  // "PU20to40_HLT",
  // "PUgt40_HLT",
  //"PU0to20_HLT_TypeOne",
  //"PU20to40_HLT_TypeOne",
  //"PUgt40_HLT_TypeOne",
  };

  for(auto const& selLabel : puintervals){
    for(auto const& metLabel : labelMap_MET_){
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }
  }

}

void JMETriggerAnalysisDriverRun3::analyze(){

  // for data to use also the IsoMu27 (works only with muon dataset)
  // all events analyzed must fullfill the iso muon requirement
  if(hasTTreeReaderValue("HLT_IsoMu27") && !value<bool>("HLT_IsoMu27")){
    return;
  }

  H1("eventsProcessed")->Fill(0.5);

  float wgt = 1.f;
  H1("weight")->Fill(wgt);

  // AK4 Jets
  const float minAK4JetPt(30.);
  const float minAK4JetPtRef(20.);
  const float maxAK4JetDeltaRmatchRef(0.2);

  // Single-Jet
  for(auto const& jetLabel : labelMap_jetAK4_){

    //auto const isGENJets = (jetLabel.first.find("GenJets") != std::string::npos);

    //auto const jetPt1 = isGENJets ? minAK4JetPtRef : minAK4JetPt;
    //auto const jetPt2 = isGENJets ? minAK4JetPtRef * 0.75 : minAK4JetPtRef;
    auto const jetPt1 = minAK4JetPt;
    auto const jetPt2 = minAK4JetPtRef;
    
    fillHistoDataJets fhDataAK4Jets;
    fhDataAK4Jets.jetCollection = jetLabel.first;
    fhDataAK4Jets.jetPtMin = jetPt1;
    fhDataAK4Jets.jetAbsEtaMax = 5.0;
    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK4Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK4JetDeltaRmatchRef));
    }

    fillHistograms_Jets("NoSelection", fhDataAK4Jets, wgt);

    for(auto const& selLabel : jettriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : hltJetTrigger(selLabel);
      if(not hltTrig){
        continue;
      }
      auto fhDataAK4JetsNew = fhDataAK4Jets;
      for(auto& match : fhDataAK4JetsNew.matches){
        if(match.label == "HLT" && selLabel == "HLT_PFJet140") match.jetPtMin = 140.;
        else if(match.label == "HLT" && selLabel == "HLT_PFJet320") match.jetPtMin = 320.;
        else if(match.label == "HLT" && selLabel == "HLT_PFJet500") match.jetPtMin = 500.;
        else if(match.label == "HLT" && selLabel == "HLT_PFJet60") match.jetPtMin = 60.;
      }

      fillHistograms_Jets(selLabel, fhDataAK4JetsNew, wgt);
    }

    //if(isGENJets) continue;

    for(auto const& selLabel : httriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : hltHTTrigger(selLabel);
      if(not hltTrig){
        continue;
      }

      fillHistograms_Jets(selLabel, fhDataAK4Jets, wgt);
    }
  }

  // HT
  for(std::string const& jetType : {"PF", "PFPuppi"}){

    fillHistoDataJets fhDataHLTAK4Jets;
    fhDataHLTAK4Jets.jetCollection = "hltAK4"+jetType+"JetsCorrected";
    fhDataHLTAK4Jets.jetPtMin = minAK4JetPt;
    fhDataHLTAK4Jets.jetAbsEtaMax = 5.0;

    fillHistoDataJets fhDataOffAK4Jets;
    if(jetType == "PF") fhDataOffAK4Jets.jetCollection = "offlineAK4PFCHSJetsCorrected";
    else if(jetType == "PFPuppi") fhDataOffAK4Jets.jetCollection = "offlineAK4PFPuppiJetsCorrected";
    //fhDataOffAK4Jets.jetCollection = "offlineAK4"+jetType+"JetsCorrected";
    fhDataOffAK4Jets.jetPtMin = minAK4JetPt;
    fhDataOffAK4Jets.jetAbsEtaMax = 5.0;

    //fillHistograms_Jets_2DMaps("NoSelection", fhDataHLTAK4Jets, fhDataOffAK4Jets, wgt);

    fillHistoDataMET fhDataHLTHT;
    fhDataHLTHT.metCollection = "hlt"+jetType+"HT";

    for(auto const& selLabel : httriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : hltHTTrigger(selLabel);
      if(not hltTrig){
        continue;
      }

      fillHistograms_Jets_2DMaps(selLabel, fhDataHLTAK4Jets, fhDataOffAK4Jets, wgt);

    }
  }

  // AK8 Jets
  const float minAK8JetPt(30.);
  const float minAK8JetPtRef(20.);
  const float maxAK8JetDeltaRmatchRef(0.4);

  for(auto const& jetLabel : labelMap_jetAK8_){

    //auto const isGENJets = (jetLabel.first.find("GenJets") != std::string::npos);

    // auto const jetPt1 = isGENJets ? minAK8JetPtRef : minAK8JetPt;
    // auto const jetPt2 = isGENJets ? minAK8JetPtRef * 0.75 : minAK8JetPtRef;
    
    auto const jetPt1 = minAK8JetPt;
    auto const jetPt2 = minAK8JetPtRef;

    fillHistoDataJets fhDataAK8Jets;
    fhDataAK8Jets.jetCollection = jetLabel.first;
    fhDataAK8Jets.jetPtMin = jetPt1;
    fhDataAK8Jets.jetAbsEtaMax = 5.0;

    for(auto const& jetLabelRefs : jetLabel.second){
      fhDataAK8Jets.matches.emplace_back(fillHistoDataJets::Match(jetLabelRefs.first, jetLabelRefs.second, jetPt2, maxAK8JetDeltaRmatchRef));
    }

    fillHistograms_Jets("NoSelection", fhDataAK8Jets, wgt);
  }

  // MET
  for(auto const& metLabel : labelMap_MET_){

    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel.first;
    for(auto const& metRefs : metLabel.second){
      fhDataMET.matches.emplace_back(fillHistoDataMET::Match(metRefs.first, metRefs.second));
    }

    fillHistograms_MET("NoSelection", fhDataMET, wgt);

    for(auto const& selLabel : mettriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : hltMETTrigger(selLabel);
      if(hltTrig){
        fillHistograms_MET(selLabel, fhDataMET, wgt);
      }
    }

    for(auto const& selLabel : puintervals){
      auto const puInt = hasTTreeReaderValue("pileupInfo_BX0_numPUInteractions") ? pileupintervals(selLabel) : false;
      if(puInt){
        fillHistograms_MET(selLabel, fhDataMET, wgt);
      }
    }
  }

  // MET+MHT
  //fillHistograms_METMHT("NoSelection", wgt);

  for(auto const& selLabel : mettriggers){
    auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : hltMETTrigger(selLabel);
    if(hltTrig){
      fillHistograms_METMHT(selLabel, wgt);
    }
  }
}

bool JMETriggerAnalysisDriverRun3::hltJetTrigger(std::string const& key) const {
  if(key == "HLT_PFJet140") return value<bool>("HLT_PFJet140");
  else if(key == "HLT_PFJet320") return value<bool>("HLT_PFJet320");
  else if(key == "HLT_PFJet500") return value<bool>("HLT_PFJet500");
  else if(key == "HLT_PFJet60") return value<bool>("HLT_PFJet60");
  else
    throw std::runtime_error("JMETriggerAnalysisDriverRun3::hltJetTrigger(\""+key+"\") -- invalid key");

  return false;
}

bool JMETriggerAnalysisDriverRun3::hltHTTrigger(std::string const& key) const {
  if(key == "HLT_PFHT780") return value<bool>("HLT_PFHT780");
  else if(key == "HLT_PFHT890") return value<bool>("HLT_PFHT890");
  else if(key == "HLT_PFHT1050") return value<bool>("HLT_PFHT1050");
  else
    throw std::runtime_error("JMETriggerAnalysisDriverRun3::hltHTTrigger(\""+key+"\") -- invalid key");

  return false;
}

bool JMETriggerAnalysisDriverRun3::hltMETTrigger(std::string const& key) const {
  if(key == "HLT_PFMET120_PFMHT120_IDTight") return value<bool>("HLT_PFMET120_PFMHT120_IDTight");
  else if(key == "HLT_PFMET140_PFMHT140_IDTight") return value<bool>("HLT_PFMET140_PFMHT140_IDTight");
  else if(key == "HLT_PFMETTypeOne140_PFMHT140_IDTight") return value<bool>("HLT_PFMETTypeOne140_PFMHT140_IDTight");
  else
    throw std::runtime_error("JMETriggerAnalysisDriverRun3::hltMETTrigger(\""+key+"\") -- invalid key");

  return false;
}

bool JMETriggerAnalysisDriverRun3::pileupintervals(std::string const& key) const {
  if(key == "PU0to20") return (value<int>("pileupInfo_BX0_numPUInteractions") > 0 && value<int>("pileupInfo_BX0_numPUInteractions") <= 20);
  if(key == "PU20to40") return (value<int>("pileupInfo_BX0_numPUInteractions") > 20 && value<int>("pileupInfo_BX0_numPUInteractions") <= 40);
  if(key == "PUgt40") return (value<int>("pileupInfo_BX0_numPUInteractions") > 40);
  if(key == "PU0to20_HLT") return (value<int>("pileupInfo_BX0_numPUInteractions") > 0 && value<int>("pileupInfo_BX0_numPUInteractions") <= 20 && value<bool>("HLT_PFMET120_PFMHT120_IDTight"));
  if(key == "PU20to40_HLT") return (value<int>("pileupInfo_BX0_numPUInteractions") > 20 && value<int>("pileupInfo_BX0_numPUInteractions") <= 40 && value<bool>("HLT_PFMET120_PFMHT120_IDTight"));
  if(key == "PUgt40_HLT") return(value<int>("pileupInfo_BX0_numPUInteractions") > 40 && value<bool>("HLT_PFMET120_PFMHT120_IDTight"));
  //if(key == "PU0to20_HLT_TypeOne") return (value<int>("pileupInfo_BX0_numPUInteractions") > 0 && value<int>("pileupInfo_BX0_numPUInteractions") <= 20 && value<bool>("HLT_PFMETTypeOne120_PFMHT120_IDTight"));
  //if(key == "PU20to40_HLT_TypeOne") return (value<int>("pileupInfo_BX0_numPUInteractions") > 20 && value<int>("pileupInfo_BX0_numPUInteractions") <= 40 && value<bool>("HLT_PFMETTypeOne120_PFMHT120_IDTight"));
  //if(key == "PUgt40_HLT_TypeOne") return(value<int>("pileupInfo_BX0_numPUInteractions") > 40 && value<bool>("HLT_PFMETTypeOne120_PFMHT120_IDTight"));
  else
    throw std::runtime_error("JMETriggerAnalysisDriverRun3::hltMETTrigger(\""+key+"\") -- invalid key");

  return false;
}

void JMETriggerAnalysisDriverRun3::bookHistograms_Jets_2DMaps(const std::string& dir, const std::string& jetType1, const std::string& jetType2){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_HT(221);
  for(uint idx=0; idx<binEdges_HT.size(); ++idx){ binEdges_HT.at(idx) = idx * 10.; }

  addTH2D(dirPrefix+jetType1+"_HT__vs__"+jetType2+"_HT", binEdges_HT, binEdges_HT);
}

void JMETriggerAnalysisDriverRun3::bookHistograms_MET_2DMaps(const std::string& dir, const std::string& metType1, const std::string& metType2, bool const book1D){

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

void JMETriggerAnalysisDriverRun3::bookHistograms_METMHT(const std::string& dir){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_pt(161);
  for(uint idx=0; idx<binEdges_pt.size(); ++idx){ binEdges_pt.at(idx) = idx * 5.; }

  std::vector<float> binEdges_pt_2(37);
  for(uint idx=0; idx<binEdges_pt_2.size(); ++idx){ binEdges_pt_2.at(idx) = 80. + idx * 5.; }

  //addTH2D(dirPrefix+"hltPFMET_pt__vs__hltPFMHT_pt", binEdges_pt, binEdges_pt);
  //addTH2D(dirPrefix+"hltPFMETTypeOne_pt__vs__hltPFMHT_pt", binEdges_pt, binEdges_pt);
  //addTH2D(dirPrefix+"hltPFPuppiMET_pt__vs__hltPFPuppiMHT_pt", binEdges_pt, binEdges_pt);
  //addTH2D(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT_pt", binEdges_pt, binEdges_pt);
}

void JMETriggerAnalysisDriverRun3::fillHistograms_Jets_2DMaps(const std::string& dir, const fillHistoDataJets& fhData1, const fillHistoDataJets& fhData2, float const weight){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt1(this->vector_ptr<float>(fhData1.jetCollection+"_pt"));
  auto const* v_eta1(this->vector_ptr<float>(fhData1.jetCollection+"_eta"));

  if(not (v_pt1 and v_eta1)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverRun3::fillHistograms_Jets_2DMaps(\"" << dir << "\", const fillHistoDataJets&, const fillHistoDataJets&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData1.jetCollection+"_pt/eta" << std::endl;
    }
    return;
  }

  auto const* v_pt2(this->vector_ptr<float>(fhData2.jetCollection+"_pt"));
  auto const* v_eta2(this->vector_ptr<float>(fhData2.jetCollection+"_eta"));

  if(not (v_pt2 and v_eta2)){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverRun3::fillHistograms_Jets_2DMaps(\"" << dir << "\", const fillHistoDataJets&, const fillHistoDataJets&) -- "
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

void JMETriggerAnalysisDriverRun3::fillHistograms_MET_2DMaps(const std::string& dir, const fillHistoDataMET& fhData1, const fillHistoDataMET& fhData2, bool const fill1D, float const weight){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  auto const* v_pt1(this->vector_ptr<float>(fhData1.metCollection+"_pt"));
  if(not v_pt1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverRun3::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData1.metCollection+"_pt" << std::endl;
    }
    return;
  }
  else if(v_pt1->size() != 1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverRun3::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData1.metCollection+"_pt" << std::endl;
    }
    return;
  }

  auto const* v_pt2(this->vector_ptr<float>(fhData2.metCollection+"_pt"));
  if(not v_pt2){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverRun3::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): "
                << fhData2.metCollection+"_pt" << std::endl;
    }
    return;
  }
  else if(v_pt2->size() != 1){
    if(verbosity_ >= 0){
      std::cout << "JMETriggerAnalysisDriverRun3::fillHistograms_MET_2DMaps(\"" << dir << "\", const fillHistoDataMET&, const fillHistoDataMET&) -- "
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

void JMETriggerAnalysisDriverRun3::fillHistograms_METMHT(const std::string& dir, float const weight){
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  //auto const hltPFMET_pt = getMET("hltPFMET_pt");
  //auto const hltPFMETTypeOne_pt = getMET("hltPFMETTypeOne_pt");
  //auto const hltPFPuppiMET_pt = getMET("hltPFPuppiMET_pt");
  //auto const hltPFPuppiMETTypeOne_pt = getMET("hltPFPuppiMETTypeOne_pt");

  //auto const hltPFMHT_pt = getPFMHT(30., 5.0);
  //auto const hltPFPuppiMHT_pt = getPuppiMHT(30., 5.0);

  //H2(dirPrefix+"hltPFMET_pt__vs__hltPFMHT_pt")->Fill(hltPFMET_pt, hltPFMHT_pt, weight);
  //H2(dirPrefix+"hltPFMETTypeOne_pt__vs__hltPFMHT_pt")->Fill(hltPFMETTypeOne_pt, hltPFMHT_pt, weight);
  //H2(dirPrefix+"hltPFPuppiMET_pt__vs__hltPFPuppiMHT_pt")->Fill(hltPFPuppiMET_pt, hltPFPuppiMHT_pt, weight);
  //H2(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT_pt")->Fill(hltPFPuppiMETTypeOne_pt, hltPFPuppiMHT_pt, weight);
}

float JMETriggerAnalysisDriverRun3::getMET(std::string const& branchName) const {
  auto const& v_pt = this->vector<float>(branchName);

  if(v_pt.size() != 1){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriverPhase2::fillHistograms(\"" << branchName << "\") -- "
        << "MET branches have invalid size (" << v_pt.size() << " != 1)";
    throw std::runtime_error(oss.str());
  }

  return v_pt.at(0);
}

float JMETriggerAnalysisDriverRun3::getPFMHT(float const jetPtMin, float const jetAbsEtaMax) const {
  auto const& v_pt = vector<float>("hltAK4PFJetsCorrected_pt");
  auto const& v_eta = vector<float>("hltAK4PFJetsCorrected_eta");
  auto const& v_phi = vector<float>("hltAK4PFJetsCorrected_phi");
  auto const& v_mass = vector<float>("hltAK4PFJetsCorrected_mass");

  float MHT_x(0.f), MHT_y(0.f);
  for(size_t jetIdx=0; jetIdx<v_pt.size(); ++jetIdx){
    if(std::abs(v_eta.at(jetIdx)) >= jetAbsEtaMax) continue;
    ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>> const p4polar(v_pt.at(jetIdx), v_eta.at(jetIdx), v_phi.at(jetIdx), v_mass.at(jetIdx));

    auto const jetPtMin_new = jetPtMin; //!! (std::abs(p4polar.Eta()) < 2.95 or std::abs(p4polar.Eta()) > 3.05) ? jetPtMin : std::max(60.f, jetPtMin);

    if(p4polar.Pt() > jetPtMin_new){
      MHT_x -= p4polar.Px();
      MHT_y -= p4polar.Py();
    }
  }

  return sqrt(MHT_x*MHT_x + MHT_y*MHT_y);
}


float JMETriggerAnalysisDriverRun3::getPuppiMHT(float const jetPtMin, float const jetAbsEtaMax) const {
  auto const& v_pt = vector<float>("hltAK4PFPuppiJetsCorrected_pt");
  auto const& v_eta = vector<float>("hltAK4PFPuppiJetsCorrected_eta");
  auto const& v_phi = vector<float>("hltAK4PFPuppiJetsCorrected_phi");
  auto const& v_mass = vector<float>("hltAK4PFPuppiJetsCorrected_mass");

  float MHT_x(0.f), MHT_y(0.f);
  for(size_t jetIdx=0; jetIdx<v_pt.size(); ++jetIdx){
    if(std::abs(v_eta.at(jetIdx)) >= jetAbsEtaMax) continue;
    ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>> const p4polar(v_pt.at(jetIdx), v_eta.at(jetIdx), v_phi.at(jetIdx), v_mass.at(jetIdx));

    auto const jetPtMin_new = jetPtMin; //!! (std::abs(p4polar.Eta()) < 2.95 or std::abs(p4polar.Eta()) > 3.05) ? jetPtMin : std::max(60.f, jetPtMin);

    if(p4polar.Pt() > jetPtMin_new){
      MHT_x -= p4polar.Px();
      MHT_y -= p4polar.Py();
    }
  }

  return sqrt(MHT_x*MHT_x + MHT_y*MHT_y);
}
