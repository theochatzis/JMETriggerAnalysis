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

//  _____       _                        _            ______      __     
// /  __ \     | |                      (_)           |  _  \    / _|    
// | /  \/ __ _| |_ ___  __ _  ___  _ __ _  ___  ___  | | | |___| |_ ___ 
// | |    / _` | __/ _ \/ _` |/ _ \| '__| |/ _ \/ __| | | | / _ \  _/ __|
// | \__/\ (_| | ||  __/ (_| | (_) | |  | |  __/\__ \ | |/ /  __/ | \__ \
//  \____/\__,_|\__\___|\__, |\___/|_|  |_|\___||___/ |___/ \___|_| |___/
//                       __/ |                                           
//                      |___/           

bool JMETriggerAnalysisDriverRun3::jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta, const float jetPhi, const float jetEta) const {

  bool ret(false);
  if(categLabel == "_EtaIncl"){ ret = (jetAbsEta < 5.0); }
  else if(categLabel == "_Eta2p5"){ ret = (jetAbsEta < 2.5); }
  else if(categLabel == "_HB"){ ret = (jetAbsEta < 1.3); } 
  else if (categLabel == "_HBPt0" ) {  //------------- pt regions (here only HB Minus is used for BPix check)
    ret = (jetAbsEta < 1.3) and (jetPt < 60.) and (jetEta < 0.);
  } else if (categLabel == "_HBPt1" ) {
    ret = (jetAbsEta < 1.3) and (60. <= jetPt) and (jetPt <= 80) and (jetEta < 0.);
  } else if (categLabel == "_HBPt2" ) {
    ret = (jetAbsEta < 1.3) and (80. <= jetPt) and (jetPt <= 130) and (jetEta < 0.);
  } else if (categLabel == "_HBPt3" ) {
    ret = (jetAbsEta < 1.3) and (130 <= jetPt) and (jetEta < 0.);
  } 
  else if(categLabel == "_HE"){ ret = (1.3 <= jetAbsEta) and (jetAbsEta < 3.0); }
  else if (categLabel == "_HEPt0" ) {  //------------- pt regions (here only HE Minus is used for FPix check)
    ret = (jetAbsEta > 1.3) and (jetPt < 60.) and ((jetEta < -1.5) and (jetEta<-3.0));
  } else if (categLabel == "_HEPt1" ) {
    ret = (jetAbsEta > 1.3) and (60. <= jetPt) and (jetPt <= 80) and ((jetEta < -1.5) and (jetEta<-3.0));
  } else if (categLabel == "_HEPt2" ) {
    ret = (jetAbsEta > 1.3) and (80. <= jetPt) and (jetPt <= 130) and ((jetEta < -1.5) and (jetEta<-3.0));
  } else if (categLabel == "_HEPt3" ) {
    ret = (jetAbsEta > 1.3) and (130 <= jetPt) and ((jetEta < -1.5) and (jetEta<-3.0));
  } 

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
  
    else if(categLabel == "_HF1"){ ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0); }
  else if (categLabel == "_HF1Pt0" ) {  //------------- pt regions
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (jetPt < 60.);
  } else if (categLabel == "_HF1Pt1" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HF1Pt2" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HF1Pt3" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 4.0) and (130 <= jetPt);
  } 

    else if(categLabel == "_HF2"){ ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0); }
  else if (categLabel == "_HF2Pt0" ) {  //------------- pt regions
    ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (jetPt < 60.);
  } else if (categLabel == "_HF2Pt1" ) {
    ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt <= 80);
  } else if (categLabel == "_HF2Pt2" ) {
    ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (80. <= jetPt) and (jetPt <= 130);
  } else if (categLabel == "_HF2Pt3" ) {
    ret = (4.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (130 <= jetPt);
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

  else if(categLabel == "_FPix"){ ret = (jetEta < -1.5) and (jetEta>-3.5) and (jetPhi<3.15) and (jetPhi>2.3);}
  else if(categLabel == "_FPixVeto"){ ret = !((jetEta < -1.5) and (jetEta>-3.5) and (jetPhi<3.15) and (jetPhi>2.3)) and jetAbsEta>1.5 and jetAbsEta<3.0;}
  return ret;
}

void JMETriggerAnalysisDriverRun3::init(){

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});
  addTH1D("weight", 100, -5, 5);
//  _____       _ _           _   _                 
// /  __ \     | | |         | | (_)                
// | /  \/ ___ | | | ___  ___| |_ _  ___  _ __  ___ 
// | |    / _ \| | |/ _ \/ __| __| |/ _ \| '_ \/ __|
// | \__/\ (_) | | |  __/ (__| |_| | (_) | | | \__ \
//  \____/\___/|_|_|\___|\___|\__|_|\___/|_| |_|___/
                                                 
  labelMap_jetAK4_.clear();
  labelMap_jetAK4_ = {
    {"ak4GenJetsNoNu"                ,{{"hltCaloCorr", "hltAK4CaloJetsCorrected"},{"hltPFCorr", "hltAK4PFJetsCorrected"},{"offlPFPuppiCorr", "offlineAK4PFPuppiJetsCorrected"}}},
    {"ak4GenJetsNoNu"                ,{{"hltCalo", "hltAK4CaloJets"},{"hltPF", "hltAK4PFJets"}}},
    {"hltAK4CaloJetsCorrected"              , {{"GEN", "ak4GenJetsNoNu"},{"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"hltAK4CaloJets"                       , {{"GEN", "ak4GenJetsNoNu"},{"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"hltAK4PFJetsCorrected"       , {{"GEN", "ak4GenJetsNoNu"},{"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"hltAK4PFJets"                , {{"GEN", "ak4GenJetsNoNu"},{"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"hltAK4PFPuppiJetsCorrected"       , {{"GEN", "ak4GenJetsNoNu"},{"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"hltAK4PFPuppiJets"                , {{"GEN", "ak4GenJetsNoNu"},{"Offline", "offlineAK4PFPuppiJetsCorrected"}}},
    {"offlineAK4PFPuppiJetsCorrected"                ,{{"hltCaloCorr", "hltAK4CaloJetsCorrected"},{"hltPFCorr", "hltAK4PFJetsCorrected"}, {"hltPFPuppiCorr", "hltAK4PFPuppiJetsCorrected"}}},
  };

  labelMap_jetAK8_.clear();
  labelMap_jetAK8_ = {
    {"ak8GenJetsNoNu"                ,{{"hltCaloCorr", "hltAK8CaloJetsCorrected"},{"hltPFCorr", "hltAK8PFJetsCorrected"},{"offlPFPuppiCorr", "offlineAK8PFPuppiJetsCorrected"}}},
    {"ak8GenJetsNoNu"                ,{{"hltCalo", "hltAK8CaloJets"},{"hltPF", "hltAK8PFJets"}}},
    {"hltAK8CaloJetsCorrected"              , {{"GEN", "ak8GenJetsNoNu"},{"Offline", "offlineAK8PFPuppiJetsCorrected"}}},
    {"hltAK8CaloJets"                       , {{"GEN", "ak8GenJetsNoNu"},{"Offline", "offlineAK8PFPuppiJetsCorrected"}}},
    {"hltAK8PFJetsCorrected"       , {{"GEN", "ak8GenJetsNoNu"},{"Offline", "offlineAK8PFPuppiJetsCorrected"}}},
    {"hltAK8PFJets"                , {{"GEN", "ak8GenJetsNoNu"},{"Offline", "offlineAK8PFPuppiJetsCorrected"}}},
    {"hltAK8PFPuppiJetsCorrected"       , {{"GEN", "ak8GenJetsNoNu"},{"Offline", "offlineAK8PFPuppiJetsCorrected"}}},
    {"hltAK8PFPuppiJets"                , {{"GEN", "ak8GenJetsNoNu"},{"Offline", "offlineAK8PFPuppiJetsCorrected"}}},
    {"offlineAK8PFPuppiJetsCorrected"                ,{{"hltCaloCorr", "hltAK8CaloJetsCorrected"},{"hltPFCorr", "hltAK8PFJetsCorrected"}, {"hltPFPuppiCorr","hltAK8PFPuppiJetsCorrected"}}},
  };

  labelMap_MET_.clear();
  labelMap_MET_ = {
    {"genMETCalo", {}},
    {"genMETTrue", {}},
    {"hltCaloMET"             , {{"GEN", "genMETTrue"},{"Offline","offlinePFPuppiMET_Type1"}}},
    {"hltPFMET"               , {{"GEN", "genMETTrue"},{"Offline","offlinePFPuppiMET_Type1"}}},
    {"hltPFMETTypeOne"        , {{"GEN", "genMETTrue"},{"Offline","offlinePFPuppiMET_Type1"}}},
    {"hltPFPuppiMET"          , {{"GEN", "genMETTrue"},{"Offline","offlinePFPuppiMET_Type1"}}},
    {"hltPFPuppiMETTypeOne"   , {{"GEN", "genMETTrue"},{"Offline","offlinePFPuppiMET_Type1"}}},
    {"offlinePFMET_Raw"       , {{"GEN", "genMETTrue"}}},
    {"offlinePFMET_Type1"     , {{"GEN", "genMETTrue"}}},
    {"offlinePFPuppiMET_Raw"  , {{"GEN", "genMETTrue"}}},
    {"offlinePFPuppiMET_Type1", {{"GEN", "genMETTrue"}}},
  };
  
  /*
  jetCategoryLabels_ = {
    "_EtaIncl",
    "_Eta2p5", // useful for HT to keep this always.
    "_HB",
    //"_HBPt0",
    //"_HBPt1",
    //"_HBPt2",
    //"_HBPt3",
    //"_HE",
    //"_HEPt0",
    //"_HEPt1",
    //"_HEPt2",
    //"_HEPt3",
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
    // "_HE21",
    // "_HE21Pt0",
    // "_HE21Pt1",
    // "_HE21Pt2",
    // "_HE21Pt3",
    // "_HE22",
    // "_HE22Pt0",
    // "_HE22Pt1",
    // "_HE22Pt2",
    // "_HE22Pt3",
    "_HF", // useful for Fwd jet triggers
    // "_HFPt0",
    // "_HFPt1",
    // "_HFPt2",
    // "_HFPt3",
    "_BPix",
    // "_BPix_plus4",
    // "_BPix_minus4",
    // "_BPix_plus8",
    // "_BPix_minus8",
    "_BPixVeto",
    "_FPix",
    "_FPixVeto"
  };

  runPeriods = {
    "2022",
    "2023",
    "2024",
    "2023_eraC_beforeHCALOffline",
    "2023_eraC_afterHCALOffline",
    "2023_eraD",
    "2024_beforeHLTJECs",
    "2024_HLTJECs",
    "2024_HCALRespCorrs1",
    "2024_HCALRespCorrs2",
    "2024_HCALRespCorrs3",
    "2024_beforeFPix",
    "2024_FPix"
  };

  lightVersion = true; // with this provides very minimal output for efficiencies calculations only. It will contain only offline quantities in the output directories with minimal info, needed for efficiencies.
  useOnlyTriggers = true; // this will skip the NoSelection category. In case of MC can be set to False to provide denominators for efficiencies/unbiased selections for performances.
  useOnlyRunPeriods = true; // this will use only run periods definitions for categories selection. For MC should be deactivated.

  // From here and on define different selection regions (based on triggers/ offline quantities etc)
  // booleans for single jet triggers categories (forward jets are included here)
  jettriggers = {
  "HLT_PFJet60_HLTPathAccept",
  "HLT_PFJet60_HLTDenominatorPathAccept",
  "HLT_PFJet140_HLTPathAccept",
  "HLT_PFJet140_HLTDenominatorPathAccept",
  "HLT_PFJet320_HLTPathAccept",
  "HLT_PFJet320_HLTDenominatorPathAccept",
  "HLT_PFJet500_HLTPathAccept",
  "HLT_PFJet500_HLTDenominatorPathAccept",
  // Fwd paths
  "HLT_PFJetFwd60_HLTPathAccept",
  "HLT_PFJetFwd60_HLTDenominatorPathAccept",
  "HLT_PFJetFwd140_HLTPathAccept",
  "HLT_PFJetFwd140_HLTDenominatorPathAccept",
  "HLT_PFJetFwd320_HLTPathAccept",
  "HLT_PFJetFwd320_HLTDenominatorPathAccept",
  "HLT_PFJetFwd400_HLTPathAccept",
  "HLT_PFJetFwd400_HLTDenominatorPathAccept",
  //"HLT_PFJet60"
  //"HLT_PFJet80",
  //"HLT_PFJet110",
  //"HLT_PFJet140",
  //"HLT_PFJet320",
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
  
  httriggers = {
  "HLT_PFHT370_HLTPathAccept",
  "HLT_PFHT370_HLTDenominatorPathAccept",
  "HLT_PFHT510_HLTPathAccept",
  "HLT_PFHT510_HLTDenominatorPathAccept",
  "HLT_PFHT780_HLTPathAccept",
  "HLT_PFHT780_HLTDenominatorPathAccept",
  "HLT_PFHT1050_HLTPathAccept",
  "HLT_PFHT1050_HLTDenominatorPathAccept",
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

  mettriggers = {
  // "HLT_PFMET120_PFMHT120_IDTight_HLTPathAccept",
  // "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_HLTPathAccept",
  // "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF_HLTPathAccept",
  // "HLT_IsoMu27_HLTPathAccept", # For MET triggers just IsoMu27 can be used as reference.
  };
  */
//  ______             _      _   _ _     _                                      
// | ___ \           | |    | | | (_)   | |                                     
// | |_/ / ___   ___ | | __ | |_| |_ ___| |_ ___   __ _ _ __ __ _ _ __ ___  ___ 
// | ___ \/ _ \ / _ \| |/ / |  _  | / __| __/ _ \ / _` | '__/ _` | '_ ` _ \/ __|
// | |_/ / (_) | (_) |   <  | | | | \__ \ || (_) | (_| | | | (_| | | | | | \__ \
// \____/ \___/ \___/|_|\_\ \_| |_/_|___/\__\___/ \__, |_|  \__,_|_| |_| |_|___/
//                                                 __/ |                        
//                                                |___/                         
  for(auto const& selLabel : jettriggers){
    for(auto const& jetLabel : labelMap_jetAK4_){

      isOffline = (jetLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;

      if (!useOnlyRunPeriods){
        bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second), lightVersion);
      }
      // book histos for different run periods
      for(auto const& runPeriodLabel : runPeriods){
        bookHistograms_Jets(selLabel+"_"+runPeriodLabel, jetLabel.first, utils::mapKeys(jetLabel.second), lightVersion);
      }
    } 
  }
  
  for(auto const& selLabel : httriggers){
    for(auto const& jetLabel : labelMap_jetAK4_){

      isOffline = (jetLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;

      if (!useOnlyRunPeriods){
        bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second), lightVersion);
      }
      // also book histos for different run periods
      for(auto const& runPeriodLabel : runPeriods){
        bookHistograms_Jets(selLabel+"_"+runPeriodLabel, jetLabel.first, utils::mapKeys(jetLabel.second), lightVersion);
      }
    }
    //bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFJetsCorrected", "offlineAK4PFCHSJetsCorrected");
    //bookHistograms_Jets_2DMaps(selLabel, "hltAK4PFPuppiJetsCorrected", "offlineAK4PFPuppiJetsCorrected");
  }

  for(auto const& selLabel : mettriggers){
    for(auto const& metLabel : labelMap_MET_){
      
      isOffline = (metLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;

      if (!useOnlyRunPeriods){
        bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second), lightVersion);
      }
      for(auto const& runPeriodLabel : runPeriods){
        bookHistograms_MET(selLabel+"_"+runPeriodLabel, metLabel.first, utils::mapKeys(metLabel.second), lightVersion);
      }
    }
    // bookHistograms_METMHT(selLabel);
  }
  
  if (useOnlyTriggers){
    return;
  }

  // ==== More generic selections
  // This part of code applies no selection from the input files. Get all the quantities we use.
  for(auto const& selLabel : {
    "NoSelection",
  }){
    // histograms: AK4 Jets
    for(auto const& jetLabel : labelMap_jetAK4_){
      isOffline = (jetLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second), lightVersion);
    }

    // histograms: AK8 Jets
    for(auto const& jetLabel : labelMap_jetAK8_){
      isOffline = (jetLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;
      bookHistograms_Jets(selLabel, jetLabel.first, utils::mapKeys(jetLabel.second), lightVersion);
    }
    
    
    // histograms: MET
    for(auto const& metLabel : labelMap_MET_){
      isOffline = (metLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;
      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second), lightVersion);
    }

    //bookHistograms_METMHT(selLabel);
  }
  
  // For MET studies can create PU intervals categories. 
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
      isOffline = (metLabel.first.find("offline")!=std::string::npos);
      if (lightVersion and !isOffline) continue;

      bookHistograms_MET(selLabel, metLabel.first, utils::mapKeys(metLabel.second));
    }
  }

}


// ______ _ _ _   _   _ _     _                                      
// |  ___(_) | | | | | (_)   | |                                     
// | |_   _| | | | |_| |_ ___| |_ ___   __ _ _ __ __ _ _ __ ___  ___ 
// |  _| | | | | |  _  | / __| __/ _ \ / _` | '__/ _` | '_ ` _ \/ __|
// | |   | | | | | | | | \__ \ || (_) | (_| | | | (_| | | | | | \__ \
// \_|   |_|_|_| \_| |_/_|___/\__\___/ \__, |_|  \__,_|_| |_| |_|___/
//                                      __/ |                        
//                                     |___/                         

void JMETriggerAnalysisDriverRun3::analyze(){

  // for data to use also the IsoMu27 (works only with muon dataset)
  // all events analyzed must fullfill the iso muon requirement
  // if(hasTTreeReaderValue("HLT_IsoMu27") && !value<bool>("HLT_IsoMu27")){
  //   return;
  // }

  H1("eventsProcessed")->Fill(0.5);

  float wgt = 1.f;
  H1("weight")->Fill(wgt);

  // AK4 Jets
  const float minAK4JetPt(30.);
  const float minAK4JetPtRef(20.);
  const float maxAK4JetDeltaRmatchRef(0.2);

  // Single-Jet
  for(auto const& jetLabel : labelMap_jetAK4_){
    
    isOffline = (jetLabel.first.find("offline")!=std::string::npos);
    if (lightVersion and !isOffline) continue;

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
    if (!useOnlyTriggers){
      fillHistograms_Jets("NoSelection", fhDataAK4Jets, wgt, lightVersion);
    }
    

    for(auto const& selLabel : jettriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : false; // hltJetTrigger(selLabel);
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
      if (!useOnlyRunPeriods){
        fillHistograms_Jets(selLabel, fhDataAK4JetsNew, wgt, lightVersion);
      }
      // fill different run periods
      for(auto const& runPeriodLabel : runPeriods){
        auto const runPer = hasTTreeReaderValue("run") ? runPeriod(runPeriodLabel) : false;
        if(runPer){
          fillHistograms_Jets(selLabel+"_"+runPeriodLabel, fhDataAK4JetsNew, wgt, lightVersion);
        }
      }
      
    }

    //if(isGENJets) continue;

    for(auto const& selLabel : httriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : false; // hltHTTrigger(selLabel);
      if(not hltTrig){
        continue;
      }
      if (!useOnlyRunPeriods){
        fillHistograms_Jets(selLabel, fhDataAK4Jets, wgt, lightVersion);
      }
      // fill different run periods
      for(auto const& runPeriodLabel : runPeriods){
        auto const runPer = hasTTreeReaderValue("run") ? runPeriod(runPeriodLabel) : false;
        if(runPer){
          fillHistograms_Jets(selLabel+"_"+runPeriodLabel, fhDataAK4Jets, wgt, lightVersion);
        }
      }
    }
  }


  // AK8 Jets
  const float minAK8JetPt(30.);
  const float minAK8JetPtRef(20.);
  const float maxAK8JetDeltaRmatchRef(0.4);

  for(auto const& jetLabel : labelMap_jetAK8_){
    isOffline = (jetLabel.first.find("offline")!=std::string::npos);
    if (lightVersion and !isOffline) continue;

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
    if (!useOnlyTriggers){
      fillHistograms_Jets("NoSelection", fhDataAK8Jets, wgt);
    }
  }

  // MET
  for(auto const& metLabel : labelMap_MET_){
    isOffline = (metLabel.first.find("offline")!=std::string::npos);
    if (lightVersion and !isOffline) continue;

    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel.first;
    for(auto const& metRefs : metLabel.second){
      fhDataMET.matches.emplace_back(fillHistoDataMET::Match(metRefs.first, metRefs.second));
    }
    if (!useOnlyTriggers){
      fillHistograms_MET("NoSelection", fhDataMET, wgt);
    }
    for(auto const& selLabel : mettriggers){
      auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : false;//hltMETTrigger(selLabel);
      if(hltTrig){
        if (!useOnlyRunPeriods){
          fillHistograms_MET(selLabel, fhDataMET, wgt, lightVersion);
        }
        // fill different run periods
        for(auto const& runPeriodLabel : runPeriods){
          auto const runPer = hasTTreeReaderValue("run") ? runPeriod(runPeriodLabel) : false;
          if(runPer){
            fillHistograms_MET(selLabel+"_"+runPeriodLabel, fhDataMET, wgt, lightVersion);
          }
        }
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
  /*
  fillHistograms_METMHT("NoSelection", wgt);
  
  for(auto const& selLabel : mettriggers){
    auto const hltTrig = hasTTreeReaderValue(selLabel) ? value<bool>(selLabel) : false; //hltMETTrigger(selLabel);
    if(hltTrig){
      fillHistograms_METMHT(selLabel, wgt);
    }
  }
  */
}

/*
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
*/

//  _   _      _                     
// | | | |    | |                    
// | |_| | ___| |_ __   ___ _ __ ___ 
// |  _  |/ _ \ | '_ \ / _ \ '__/ __|
// | | | |  __/ | |_) |  __/ |  \__ \
// \_| |_/\___|_| .__/ \___|_|  |___/
//              | |                  
//              |_|                  

bool JMETriggerAnalysisDriverRun3::runPeriod(std::string const& key) const {
  // 2023 periods (basic milestones for jets/MET performance)
  int runNumber_ = value<unsigned int>("run");
  if ( key == "2022") return ( runNumber_ > 355794 and runNumber_ < 362760 ); // Eras C -> G
  else if ( key == "2023") return ( runNumber_ > 367080 and runNumber_ < 372415 );
  else if ( key == "2024") return ( runNumber_ > 379412 and runNumber_ < 387121	); // from Era C -> I
  else if ( key == "2022_eraCDE" ) return ( runNumber_ > 355794 and runNumber_ < 360332 ); // 2022 era C->E 
  else if ( key == "2022_eraFG" ) return ( runNumber_ > 360332 and runNumber_ < 362760 ); // 2022 era F , HCAL scale got updated
  else if (key == "2023_eraC_beforeHCALOffline") return (runNumber_ > 367080 and runNumber_ < 367765); // era C change of HCAL resp corrs in offline only
  else if (key == "2023_eraC_afterHCALOffline") return (runNumber_ >= 367765 and runNumber_ < 369802); // era C after HCAL resp corrs update in offline (this is right before era D)
  else if (key == "2023_eraD") return (runNumber_ >= 369864 and runNumber_ < 372415); // the BPix run was 369334 so this contains BPix.
  // 2024 periods 
  // if(key == "beforeHCAL") return (runNumber_ < 382287 );
  // if(key == "afterHCAL_offline") return (runNumber_ > 382287 && runNumber_ < 383219);
  // if(key == "afterHCAL") return (runNumber_ > 383219); 
  // if(key == "afterFPix") return (runNumber_ > 382798);
  else if ( key == "2024_beforeHLTJECs") return ( runNumber_ > 379412 and runNumber_ < 380266); // start of Era C as baseline
  else if ( key == "2024_HLTJECs" ) return (runNumber_ > 380266 and runNumber_ < 380637); // new HLT jecs (its right when Era D started)
  else if ( key == "2024_HCALRespCorrs1") return ( runNumber_ > 380637 and runNumber_ < 383219 ); // HF resp corrs update
  else if ( key == "2024_HCALRespCorrs2" ) return ( runNumber_ > 383219 and runNumber_ < 386401 ); // Generic HCAL resp corrs
  else if ( key == "2024_HCALRespCorrs3" ) return ( runNumber_ > 386401 and runNumber_ < 387121 ); // This was again for HF to fix the over-correction in Era I (up to end or era I)
  else if ( key == "2024_beforeFPix" ) return (runNumber_ > 380637 and runNumber_ < 382798 ); // after last HCAL resp corrs update before FPix
  else if ( key == "2024_FPix" ) return (runNumber_ > 382798 and runNumber_ < 383219 ); // in FPix period
  // --- for 2025
  else if ( key == "2024I" ) return ( runNumber_ >  386409 and runNumber_ < 387121); // used as reference in 2025
  else if ( key == "2025C" ) return ( runNumber_ > 392159	and runNumber_ < 393609); 
  else if ( key == "2025D" ) return ( runNumber_ > 394286 and runNumber_ < 395967);
  else if ( key == "2025E" ) return ( runNumber_ > 395967 and runNumber_ < 396598);
  else if ( key == "2025F" ) return ( runNumber_ > 396598 );
  else if ( key == "2025CV1" ) return ( runNumber_ > 392159	and runNumber_ < 393108); 
  else if ( key == "2025CV2" ) return ( runNumber_ > 393111	and runNumber_ < 393609 ); // In CV2 create a drop in responses in HF 
  else if ( key == "2025D_beforeIBCoff" ) return ( runNumber_ > 394286 and runNumber_ < 394790); // big MET rate drop, small rate drop in Fwd  // Prompt JECs update start of Era D: 394431
  else if ( key == "2025D_afterIBCoff") return ( runNumber_ > 394790 and runNumber_ < 395967 ); 
  else
    throw std::runtime_error("JMETriggerAnalysisDriverRun3::runPeriod(\""+key+"\") -- invalid key");
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
    throw std::runtime_error("JMETriggerAnalysisDriverRun3::pileupintervals(\""+key+"\") -- invalid key");

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

  addTH2D(dirPrefix+"hltPFMET_pt__vs__hltPFMHT_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"hltPFMETTypeOne_pt__vs__hltPFMHT_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"hltPFPuppiMET_pt__vs__hltPFPuppiMHT_pt", binEdges_pt, binEdges_pt);
  addTH2D(dirPrefix+"hltPFPuppiMETTypeOne_pt__vs__hltPFPuppiMHT_pt", binEdges_pt, binEdges_pt);
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
//  _____      _   _             ______                _   _                 
// /  ___|    | | | |            |  ___|              | | (_)                
// \ `--.  ___| |_| |_ ___ _ __  | |_ _   _ _ __   ___| |_ _  ___  _ __  ___ 
//  `--. \/ _ \ __| __/ _ \ '__| |  _| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
// /\__/ /  __/ |_| ||  __/ |    | | | |_| | | | | (__| |_| | (_) | | | \__ \
// \____/ \___|\__|\__\___|_|    \_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

// --- setter implementations (callable from Python for communication with the outside world) ---
void JMETriggerAnalysisDriverRun3::setJetCategoryLabels(const std::vector<std::string>& labels){
  jetCategoryLabels_ = labels;
}

void JMETriggerAnalysisDriverRun3::setRunPeriods(const std::vector<std::string>& periods){
  runPeriods = periods;
}

void JMETriggerAnalysisDriverRun3::setLightVersion(bool v){
  lightVersion = v;
}

void JMETriggerAnalysisDriverRun3::setUseOnlyTriggers(bool v){
  useOnlyTriggers = v;
}

void JMETriggerAnalysisDriverRun3::setUseOnlyRunPeriods(bool v){
  useOnlyRunPeriods = v;
}

void JMETriggerAnalysisDriverRun3::setJetTriggers(const std::vector<std::string>& triggers){
  jettriggers = triggers;
}

void JMETriggerAnalysisDriverRun3::setHTTriggers(const std::vector<std::string>& triggers){
  httriggers = triggers;
}

void JMETriggerAnalysisDriverRun3::setMETTriggers(const std::vector<std::string>& triggers){
  mettriggers = triggers;
}


