#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriver.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <cmath>

JMETriggerAnalysisDriver::JMETriggerAnalysisDriver(const std::string& tfile,
                                                   const std::string& ttree,
                                                   const std::string& outputFilePath,
                                                   const std::string& outputFileMode)
    : JMETriggerAnalysisDriver(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriver::JMETriggerAnalysisDriver(const std::string& outputFilePath, const std::string& outputFileMode)
    : AnalysisDriverBase(outputFilePath, outputFileMode) {}

bool JMETriggerAnalysisDriver::jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta, const float jetPhi, const float jetEta) const {
  bool ret(false);
  
  // modification start
  // booleans that show if jet is AK4 or AK8
  // bool isAK4 = (jetCollection.find("AK4")!=std::string::npos) or (jetCollection.find("ak4")!=std::string::npos);
  // bool isAK8 = (jetCollection.find("AK8")!=std::string::npos) or (jetCollection.find("ak8")!=std::string::npos);
  
  if (categLabel == "_EtaIncl") {
    ret = (jetAbsEta < 5.0);
  } else if (categLabel == "_EtaInclPt0" ) {  //------------- AK4 pt regions
    ret = (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_EtaInclPt1" ) {
    ret = (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 80.);
  } else if (categLabel == "_EtaInclPt2" ) {
    ret = (jetAbsEta < 5.0) and (80. <= jetPt) and (jetPt < 100.);
  } else if (categLabel == "_EtaInclPt3" ) {
    ret = (jetAbsEta < 5.0) and (100. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_EtaInclPt4" ) {
    ret = (jetAbsEta < 5.0) and (200. <= jetPt);
  } else if (categLabel == "_EtaInclPt0" ) {  //------------- AK8 pt regions
    ret = (jetAbsEta < 5.0) and (90. <= jetPt) and (jetPt < 150.);
  } else if (categLabel == "_EtaInclPt1" ) {
    ret = (jetAbsEta < 5.0) and (150. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_EtaInclPt2" ) {
    ret = (jetAbsEta < 5.0) and (200. <= jetPt) and (jetPt < 250.);
  } else if (categLabel == "_EtaInclPt3" ) {
    ret = (jetAbsEta < 5.0) and (250. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_EtaInclPt4" ) {
    ret = (jetAbsEta < 5.0) and (400. <= jetPt);
  } 

  else if (categLabel == "_HB") {
    ret = (jetAbsEta < 1.3);
  } else if (categLabel == "_HBPt0" ) {  //------------- AK4 pt regions
    ret = (jetAbsEta < 1.3) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HBPt1" ) {
    ret = (jetAbsEta < 1.3) and (60. <= jetPt) and (jetPt < 80.);
  } else if (categLabel == "_HBPt2" ) {
    ret = (jetAbsEta < 1.3) and (80. <= jetPt) and (jetPt < 100.);
  } else if (categLabel == "_HBPt3" ) {
    ret = (jetAbsEta < 1.3) and (100. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HBPt4" ) {
    ret = (jetAbsEta < 1.3) and (200. <= jetPt);
  } else if (categLabel == "_HBPt0" ) {  //------------- AK8 pt regions
    ret = (jetAbsEta < 1.3) and (90. <= jetPt) and (jetPt < 150.);
  } else if (categLabel == "_HBPt1" ) {
    ret = (jetAbsEta < 1.3) and (150. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HBPt2" ) {
    ret = (jetAbsEta < 1.3) and (200. <= jetPt) and (jetPt < 250.);
  } else if (categLabel == "_HBPt3" ) {
    ret = (jetAbsEta < 1.3) and (250. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HBPt4" ) {
    ret = (jetAbsEta < 1.3) and (400. <= jetPt);
  }

  else if (categLabel == "_HE1") {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5);
  } else if (categLabel == "_HE1Pt0" ) {  //------------- AK4 pt regions
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HE1Pt1" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (60. <= jetPt) and (jetPt < 80.);
  } else if (categLabel == "_HE1Pt2" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (80. <= jetPt) and (jetPt < 100.);
  } else if (categLabel == "_HE1Pt3" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (100. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HE1Pt4" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (200. <= jetPt);
  } else if (categLabel == "_HE1Pt0" ) {  //------------- AK8 pt regions
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (90. <= jetPt) and (jetPt < 150.);
  } else if (categLabel == "_HE1Pt1" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (150. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HE1Pt2" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (200. <= jetPt) and (jetPt < 250.);
  } else if (categLabel == "_HE1Pt3" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (250. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HE1Pt4" ) {
    ret = (1.3 <= jetAbsEta) and (jetAbsEta < 2.5) and (400. <= jetPt);
  } 

  else if (categLabel == "_HE2") {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0);
  } else if (categLabel == "_HE2Pt0" ) {  //------------- AK4 pt regions
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HE2Pt1" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (60. <= jetPt) and (jetPt < 80.);
  } else if (categLabel == "_HE2Pt2" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (80. <= jetPt) and (jetPt < 100.);
  } else if (categLabel == "_HE2Pt3" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (100. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HE2Pt4" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (200. <= jetPt);
  } else if (categLabel == "_HE2Pt0" ) {  //------------- AK8 pt regions
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (90. <= jetPt) and (jetPt < 150.);
  } else if (categLabel == "_HE2Pt1" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (150. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HE2Pt2" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (200. <= jetPt) and (jetPt < 250.);
  } else if (categLabel == "_HE2Pt3" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (250. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HE2Pt4" ) {
    ret = (2.5 <= jetAbsEta) and (jetAbsEta < 3.0) and (400. <= jetPt);
  } 

  else if (categLabel == "_HF") {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0);
  } else if (categLabel == "_HFPt0" ) {  //------------- AK4 pt regions
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (30. <= jetPt) and (jetPt < 60.);
  } else if (categLabel == "_HFPt1" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (60. <= jetPt) and (jetPt < 80.);
  } else if (categLabel == "_HFPt2" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (80. <= jetPt) and (jetPt < 100.);
  } else if (categLabel == "_HFPt3" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (100. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HFPt4" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (200. <= jetPt);
  } else if (categLabel == "_HFPt0" ) {  //------------- AK8 pt regions
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (90. <= jetPt) and (jetPt < 150.);
  } else if (categLabel == "_HFPt1" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (150. <= jetPt) and (jetPt < 200.);
  } else if (categLabel == "_HFPt2" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (200. <= jetPt) and (jetPt < 250.);
  } else if (categLabel == "_HFPt3" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (250. <= jetPt) and (jetPt < 400.);
  } else if (categLabel == "_HFPt4" ) {
    ret = (3.0 <= jetAbsEta) and (jetAbsEta < 5.0) and (400. <= jetPt);
  } 
  // modification end
  
  return ret;
}

void JMETriggerAnalysisDriver::init() {
  jetCategoryLabels_ = {
      "_EtaIncl",
      "_EtaInclPt0",
      "_EtaInclPt1",
      "_EtaInclPt2",
      "_EtaInclPt3",
      "_EtaInclPt4",

      "_HB",
      "_HBPt0",
      "_HBPt1",
      "_HBPt2",
      "_HBPt3",
      "_HBPt4",

      "_HE1",
      "_HE1Pt0",
      "_HE1Pt1",
      "_HE1Pt2",
      "_HE1Pt3",
      "_HE1Pt4",

      "_HE2",
      "_HE2Pt0",
      "_HE2Pt1",
      "_HE2Pt2",
      "_HE2Pt3",
      "_HE2Pt4",

      "_HF",
      "_HFPt0",
      "_HFPt1",
      "_HFPt2",
      "_HFPt3",
      "_HFPt4", 
      
  };

  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});

  for (auto const& selLabel : {"NoSelection"}) {
    // histograms: AK4 Jets
    bookHistograms_Jets(selLabel,
                        "ak4GenJetsNoNu",
                        {
                            "Calo",
                            "CaloCorr",
                            "PFCluster",
                            "PF",
                            "PFCorr",
                            "PFCHSv1",
                            "PFCHSv1Corr",
                            "PFCHSv2",
                            "PFCHSv2Corr",
                            "PuppiV1",
                            "PuppiV1Corr",
                            "PuppiV3",
                            "PuppiV3Corr",
                            "OfflineCorr",
                        });
    bookHistograms_Jets(selLabel, "hltAK4CaloJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4CaloJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PFClusterJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSv1Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSv1JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSv2Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PFCHSv2JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiV1Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiV1JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiV3Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK4PuppiV3JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "offlineAK4PFCHSJetsCorrected", {"GEN"});
    bookHistograms_Jets(selLabel, "offlineAK4PuppiJetsCorrected", {"GEN"});

    // histograms: AK8 Jets
    bookHistograms_Jets(selLabel,
                        "ak8GenJetsNoNu",
                        {
                            "Calo",
                            "CaloCorr",
                            "PFCluster",
                            "PF",
                            "PFCorr",
                            "PFCHSv1",
                            "PFCHSv1Corr",
                            "PFCHSv2",
                            "PFCHSv2Corr",
                            "PuppiV1",
                            "PuppiV1Corr",
                            "PuppiV3",
                            "PuppiV3Corr",
                            "OfflineCorr",
                        });
    bookHistograms_Jets(selLabel, "hltAK8CaloJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8CaloJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PFClusterJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFJetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSv1Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSv1JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSv2Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PFCHSv2JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiV1Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiV1JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiV3Jets", {"GEN"});
    bookHistograms_Jets(selLabel, "hltAK8PuppiV3JetsCorrected", {"GEN", "Offline"});
    bookHistograms_Jets(selLabel, "offlineAK8PuppiJetsCorrected", {"GEN"});

    // histograms: MET
    bookHistograms_MET(selLabel, "genMETCalo");
    bookHistograms_MET(selLabel, "genMETTrue");

    bookHistograms_MET(selLabel, "hltCaloMET", {"GEN"});
    bookHistograms_MET(selLabel, "hltPFClusterMET", {"GEN"});

    bookHistograms_MET(selLabel, "hltPFMET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPFMETNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPFSoftKillerMET", {"GEN"});
    bookHistograms_MET(selLabel, "hltPFCHSv1MET", {"GEN"});
    bookHistograms_MET(selLabel, "hltPFCHSv2MET", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiV1MET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiV1METNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiV2MET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiV2METNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiV3MET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiV3METNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "hltPuppiV4MET", {"GEN", "Offline"});
    bookHistograms_MET(selLabel, "hltPuppiV4METNoMu", {"GEN"});

    bookHistograms_MET(selLabel, "offlinePFMET_Raw", {"GEN"});
    bookHistograms_MET(selLabel, "offlinePFMET_Type1", {"GEN"});
    bookHistograms_MET(selLabel, "offlinePuppiMET_Raw", {"GEN"});
    bookHistograms_MET(selLabel, "offlinePuppiMET_Type1", {"GEN"});
  }
}

void JMETriggerAnalysisDriver::analyze() {
  H1("eventsProcessed")->Fill(0.5, 1.);

  //// AK4 Jets
  const float minAK4JetPt(30.);
  const float minAK4JetPt_GEN(20.);
  const float minAK4JetPt_Offline(20.);
  const float maxAK4JetDeltaRmatch_GEN(0.2);
  const float maxAK4JetDeltaRmatch_Offline(0.2);

  // GEN
  fillHistoDataJets fhDataAK4GEN;
  fhDataAK4GEN.jetCollection = "ak4GenJetsNoNu";
  fhDataAK4GEN.jetPtMin = minAK4JetPt_GEN;
  fhDataAK4GEN.jetAbsEtaMax = 5.0;
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("Calo", "hltAK4CaloJets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("CaloCorr", "hltAK4CaloJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCluster", "hltAK4PFClusterJets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PF", "hltAK4PFJets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCorr", "hltAK4PFJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv1", "hltAK4PFCHSv1Jets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv1Corr", "hltAK4PFCHSv1JetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv2", "hltAK4PFCHSv2Jets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv2Corr", "hltAK4PFCHSv2JetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV1", "hltAK4PuppiV1Jets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV1Corr", "hltAK4PuppiV1JetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV3", "hltAK4PuppiV3Jets", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV3Corr", "hltAK4PuppiV3JetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fhDataAK4GEN.matches.emplace_back(
      fillHistoDataJets::Match("OfflineCorr", "offlineAK4PuppiJetsCorrected", minAK4JetPt, maxAK4JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK4GEN);

  for (std::string const& jetLabel : {
           "hltAK4CaloJets",
           "hltAK4CaloJetsCorrected",
           "hltAK4PFClusterJets",
           "hltAK4PFJets",
           "hltAK4PFJetsCorrected",
           "hltAK4PFCHSv1Jets",
           "hltAK4PFCHSv1JetsCorrected",
           "hltAK4PFCHSv2Jets",
           "hltAK4PFCHSv2JetsCorrected",
           "hltAK4PuppiV1Jets",
           "hltAK4PuppiV1JetsCorrected",
           "hltAK4PuppiV3Jets",
           "hltAK4PuppiV3JetsCorrected",
           "offlineAK4PFCHSJetsCorrected",
           "offlineAK4PuppiJetsCorrected",
       }) {
    fillHistoDataJets fhDataAK4Jets;
    fhDataAK4Jets.jetCollection = jetLabel;
    fhDataAK4Jets.jetPtMin = minAK4JetPt;
    fhDataAK4Jets.jetAbsEtaMax = 5.0;
    fhDataAK4Jets.matches.emplace_back(
        fillHistoDataJets::Match("GEN", "ak4GenJetsNoNu", minAK4JetPt_GEN, maxAK4JetDeltaRmatch_GEN));

    if (utils::stringStartsWith(jetLabel, "hlt") and utils::stringEndsWith(jetLabel, "Corrected")) {
      fhDataAK4Jets.matches.emplace_back(fillHistoDataJets::Match(
          "Offline", "offlineAK4PuppiJetsCorrected", minAK4JetPt_Offline, maxAK4JetDeltaRmatch_Offline));
    }

    fillHistograms_Jets("NoSelection", fhDataAK4Jets);
  }

  //// AK8 Jets
  const float minAK8JetPt(90.);
  const float minAK8JetPt_GEN(60.);
  const float minAK8JetPt_Offline(60.);
  const float maxAK8JetDeltaRmatch_GEN(0.2);
  const float maxAK8JetDeltaRmatch_Offline(0.2);

  // AK8 GEN
  fillHistoDataJets fhDataAK8GEN;
  fhDataAK8GEN.jetCollection = "ak8GenJetsNoNu";
  fhDataAK8GEN.jetPtMin = minAK8JetPt_GEN;
  fhDataAK8GEN.jetAbsEtaMax = 5.0;
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("Calo", "hltAK8CaloJets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("CaloCorr", "hltAK8CaloJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCluster", "hltAK8PFClusterJets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PF", "hltAK8PFJets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCorr", "hltAK8PFJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv1", "hltAK8PFCHSv1Jets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv1Corr", "hltAK8PFCHSv1JetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv2", "hltAK8PFCHSv2Jets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PFCHSv2Corr", "hltAK8PFCHSv2JetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV1", "hltAK8PuppiV1Jets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV1Corr", "hltAK8PuppiV1JetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV3", "hltAK8PuppiV3Jets", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("PuppiV3Corr", "hltAK8PuppiV3JetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fhDataAK8GEN.matches.emplace_back(
      fillHistoDataJets::Match("OfflineCorr", "offlineAK8PuppiJetsCorrected", minAK8JetPt, maxAK8JetDeltaRmatch_GEN));
  fillHistograms_Jets("NoSelection", fhDataAK8GEN);

  for (std::string const& jetLabel : {
           "hltAK8CaloJets",
           "hltAK8CaloJetsCorrected",
           "hltAK8PFClusterJets",
           "hltAK8PFJets",
           "hltAK8PFJetsCorrected",
           "hltAK8PFCHSv1Jets",
           "hltAK8PFCHSv1JetsCorrected",
           "hltAK8PFCHSv2Jets",
           "hltAK8PFCHSv2JetsCorrected",
           "hltAK8PuppiV1Jets",
           "hltAK8PuppiV1JetsCorrected",
           "hltAK8PuppiV3Jets",
           "hltAK8PuppiV3JetsCorrected",
           "offlineAK8PuppiJetsCorrected",
       }) {
    fillHistoDataJets fhDataAK8Jets;
    fhDataAK8Jets.jetCollection = jetLabel;
    fhDataAK8Jets.jetPtMin = minAK8JetPt;
    fhDataAK8Jets.jetAbsEtaMax = 5.0;
    fhDataAK8Jets.matches.emplace_back(
        fillHistoDataJets::Match("GEN", "ak8GenJetsNoNu", minAK8JetPt_GEN, maxAK8JetDeltaRmatch_GEN));

    if (utils::stringStartsWith(jetLabel, "hlt") and utils::stringEndsWith(jetLabel, "Corrected")) {
      fhDataAK8Jets.matches.emplace_back(fillHistoDataJets::Match(
          "Offline", "offlineAK8PuppiJetsCorrected", minAK8JetPt_Offline, maxAK8JetDeltaRmatch_Offline));
    }

    fillHistograms_Jets("NoSelection", fhDataAK8Jets);
  }

  //// MET

  // GEN Calo
  fillHistoDataMET fhDataGENMETCalo;
  fhDataGENMETCalo.metCollection = "genMETCalo";
  fillHistograms_MET("NoSelection", fhDataGENMETCalo);

  // GEN True
  fillHistoDataMET fhDataGENMETTrue;
  fhDataGENMETTrue.metCollection = "genMETTrue";
  fillHistograms_MET("NoSelection", fhDataGENMETTrue);

  // wrt GEN MET Calo
  for (std::string const& metLabel : {
           "hltCaloMET",
           "hltPFClusterMET",
           "hltPFMETNoMu",
           "hltPuppiV1METNoMu",
           "hltPuppiV2METNoMu",
           "hltPuppiV3METNoMu",
           "hltPuppiV4METNoMu",
       }) {
    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel;
    fhDataMET.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETCalo"));
    fillHistograms_MET("NoSelection", fhDataMET);
  }

  // wrt GEN MET
  for (std::string const& metLabel : {
           "hltPFSoftKillerMET",
           "hltPFCHSv1MET",
           "hltPFCHSv2MET",
           "offlinePFMET_Raw",
           "offlinePFMET_Type1",
           "offlinePuppiMET_Raw",
           "offlinePuppiMET_Type1",
       }) {
    fillHistoDataMET fhDataMET;
    fhDataMET.metCollection = metLabel;
    fhDataMET.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
    fillHistograms_MET("NoSelection", fhDataMET);
  }

  // HLT PF
  for (std::string const& pfLabel : {
           "hltPFMET",
       }) {
    fillHistoDataMET fhDataMETPF;
    fhDataMETPF.metCollection = pfLabel;
    fhDataMETPF.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
    fhDataMETPF.matches.emplace_back(fillHistoDataMET::Match("Offline", "offlinePFMET_Raw"));
    fillHistograms_MET("NoSelection", fhDataMETPF);
  }

  // HLT Puppi
  for (std::string const& puppiLabel : {
           "hltPuppiV1MET",
           "hltPuppiV2MET",
           "hltPuppiV3MET",
           "hltPuppiV4MET",
       }) {
    fillHistoDataMET fhDataMETPuppi;
    fhDataMETPuppi.metCollection = puppiLabel;
    fhDataMETPuppi.matches.emplace_back(fillHistoDataMET::Match("GEN", "genMETTrue"));
    fhDataMETPuppi.matches.emplace_back(fillHistoDataMET::Match("Offline", "offlinePuppiMET_Raw"));
    fillHistograms_MET("NoSelection", fhDataMETPuppi);
  }
}

void JMETriggerAnalysisDriver::bookHistograms_Jets(const std::string& dir,
                                                   const std::string& jetType,
                                                   const std::vector<std::string>& matchLabels) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }
  
  // modification start
  // defining the bins for the simulated number of PU
  /*
  const std::vector<float> binEdges_simNPU({0,  10, 15, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38,  40,  42,
                                           44, 46, 48, 50, 52, 54, 56, 58, 60, 65, 70, 80, 100, 120, 140}); 
  */
  //const std::vector<float> binEdges_simNPU({0,  10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 100, 120, 140});
  const std::vector<float> binEdges_simNPU({0, 10, 20, 30, 40, 50, 60, 70, 80});
  // modification end
  
  std::vector<float> binEdges_njets(16);
  for (uint idx = 0; idx < binEdges_njets.size(); ++idx) {
    binEdges_njets.at(idx) = idx;
  }
  
  // modification start
  std::vector<float> binEdges_njets_ratio(101);
  for (uint idx = 0; idx < binEdges_njets_ratio.size(); ++idx) {
    binEdges_njets_ratio.at(idx) = idx*0.01;
  }
  // modification end
  
  std::vector<float> binEdges_HT(221);
  for (uint idx = 0; idx < binEdges_HT.size(); ++idx) {
    binEdges_HT.at(idx) = idx * 10.;
  }

  std::vector<float> binEdges_MHT(221);
  for (uint idx = 0; idx < binEdges_MHT.size(); ++idx) {
    binEdges_MHT.at(idx) = idx * 10.;
  }

  // std::vector<float> binEdges_pt(16);
  // for (uint idx = 0; idx < binEdges_pt.size(); ++idx) {
  //   binEdges_pt.at(idx) = 20. * idx;
  // }
  //std::vector<float> binEdges_pt({0, 30, 50, 70, 100, 150, 200, 300});
  std::vector<float> binEdges_pt({0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,//{0,10,20,30,40,50,60,70,80,90,100,
                                  125,150,175,200,
                                  250,300,350,400,450,500});//,
                                  //550,600,650,700,
                                  //800,900,1000});

  std::vector<float> binEdges_eta(101);
  for (uint idx = 0; idx < binEdges_eta.size(); ++idx) {
    binEdges_eta.at(idx) = -5.0 + 0.1 * idx;
  }

  std::vector<float> binEdges_phi(41);
  for (uint idx = 0; idx < binEdges_phi.size(); ++idx) {
    binEdges_phi.at(idx) = M_PI * (0.05 * idx - 1.);
  }

  std::vector<float> const binEdges_mass(
      {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 400, 500, 600});

  std::vector<float> binEdges_numberOfDaughters(121);
  for (uint idx = 0; idx < binEdges_numberOfDaughters.size(); ++idx) {
    binEdges_numberOfDaughters.at(idx) = 2. * idx;
  }

  std::vector<float> binEdges_energyFrac(21);
  for (uint idx = 0; idx < binEdges_energyFrac.size(); ++idx) {
    binEdges_energyFrac.at(idx) = 0.05 * idx;
  }

  std::vector<float> binEdges_dauMult1(61);
  for (uint idx = 0; idx < binEdges_dauMult1.size(); ++idx) {
    binEdges_dauMult1.at(idx) = idx;
  }

  std::vector<float> binEdges_dauMult2(13);
  for (uint idx = 0; idx < binEdges_dauMult2.size(); ++idx) {
    binEdges_dauMult2.at(idx) = idx;
  }

  std::vector<float> binEdges_dRmatch(26);
  for (uint idx = 0; idx < binEdges_dRmatch.size(); ++idx) {
    binEdges_dRmatch.at(idx) = 0.2 * idx;
  }

  std::vector<float> binEdges_minDeltaR(61);
  for (uint idx = 0; idx < binEdges_minDeltaR.size(); ++idx) {
    binEdges_minDeltaR.at(idx) = 0.05 * idx;
  }

  std::vector<float> binEdges_response(101);
  for (uint idx = 0; idx < binEdges_response.size(); ++idx) {
    binEdges_response.at(idx) = 0.05 * idx;
  }

  for (auto const& catLabel : jetCategoryLabels_) {
    addTH1D(dirPrefix + jetType + catLabel + "_njets", binEdges_njets);
    addTH1D(dirPrefix + jetType + catLabel + "_HT", binEdges_HT);
    addTH1D(dirPrefix + jetType + catLabel + "_MHT", binEdges_MHT);
    // modification start
    addTH1D(dirPrefix + jetType + catLabel + "_simNPU", binEdges_simNPU);
    addTH2D(dirPrefix + jetType + catLabel + "_simNPU__vs__pt0", binEdges_simNPU, binEdges_pt); // for efficiencies vs NPU
    addTH2D(dirPrefix + jetType + catLabel + "_simNPU__vs__HT", binEdges_simNPU, binEdges_HT); // for efficiencies vs NPU
    // modification end
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
      addTH2D(dirPrefix + jetType + catLabel + "_pt__vs__" + matchLabel + "_pt", binEdges_pt, binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_pt__vs__" + matchLabel + "_eta", binEdges_pt, binEdges_eta);
      addTH2D(
          dirPrefix + jetType + catLabel + "_pt__vs__" + matchLabel + "_minDeltaR", binEdges_pt, binEdges_minDeltaR);
      addTH2D(dirPrefix + jetType + catLabel + "_pt0__vs__" + matchLabel + "_pt", binEdges_pt, binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_pt0__vs__" + matchLabel + "_eta", binEdges_pt, binEdges_eta);
      addTH2D(
          dirPrefix + jetType + catLabel + "_pt0__vs__" + matchLabel + "_minDeltaR", binEdges_pt, binEdges_minDeltaR);
      addTH2D(
          dirPrefix + jetType + catLabel + "_eta__vs__" + matchLabel + "_minDeltaR", binEdges_eta, binEdges_minDeltaR);

      addTH2D(dirPrefix + jetType + catLabel + "_HT__vs__" + matchLabel + "_HT", binEdges_HT, binEdges_HT);
      addTH2D(dirPrefix + jetType + catLabel + "_MHT__vs__" + matchLabel + "_MHT", binEdges_MHT, binEdges_MHT);

      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_njets", binEdges_njets);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_HT", binEdges_HT);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_MHT", binEdges_MHT);
      // modification start
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_simNPU", binEdges_simNPU);
      // modification
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt0", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_eta", binEdges_eta);
      addTH1D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_phi", binEdges_phi);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
      // modification start
      //addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_njets__vs__simNPU", binEdges_njets, binEdges_simNPU);
      //addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_njets_over_tot" + "__vs__simNPU", binEdges_njets_ratio, binEdges_simNPU);
      // modification end 
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
      
      // modification start
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
             matchLabel + "_simNPU",
                  binEdges_response,
                  binEdges_simNPU);
      // modification end
      
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
                  matchLabel + "_pt",
              binEdges_response,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_leadCandPt_over" + matchLabel + "__vs__" +
                  matchLabel + "_pt",
              binEdges_response,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_leadCandPt_over" + matchLabel + "__vs__" +
                  matchLabel + "_simNPU",
                  binEdges_response,
                  binEdges_simNPU);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__pt",
              binEdges_response,
              binEdges_pt);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__phi",
              binEdges_response,
              binEdges_phi);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
                  matchLabel + "_eta",
              binEdges_response,
              binEdges_eta);
      addTH2D(dirPrefix + jetType + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel + "__vs__" +
                  matchLabel + "_phi",
              binEdges_response,
              binEdges_phi);

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
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_HT", binEdges_HT);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_MHT", binEdges_MHT);
      // modification start
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_simNPU", binEdges_simNPU);
      // modification
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_pt", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_pt0", binEdges_pt);
      addTH1D(dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_eta", binEdges_eta);
      addTH2D(
          dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_eta__vs__pt", binEdges_eta, binEdges_pt);
      // modification start
      addTH2D(
          dirPrefix + jetType + catLabel + "_NotMatchedTo" + matchLabel + "_njets__vs__simNPU", binEdges_njets, binEdges_simNPU);
      // modification end 
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

void JMETriggerAnalysisDriver::bookHistograms_MET(const std::string& dir,
                                                  const std::string& metType,
                                                  const std::vector<std::string>& matchLabels) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }
  
  // modification start
  std::vector<float> binEdges_pt(81);
  for (uint idx = 0; idx < binEdges_pt.size(); ++idx) {
    binEdges_pt.at(idx) = idx * 5.;
  }
  // modification end

  std::vector<float> binEdges_phi(41);
  for (uint idx = 0; idx < binEdges_phi.size(); ++idx) {
    binEdges_phi.at(idx) = M_PI * (0.05 * idx - 1.);
  }

  std::vector<float> binEdges_sumEt(121);
  for (uint idx = 0; idx < binEdges_sumEt.size(); ++idx) {
    binEdges_sumEt.at(idx) = idx * 50.;
  }

  //const std::vector<float> binEdges_simNPU({0,  10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 100, 120, 140});
  const std::vector<float> binEdges_simNPU({20, 30, 40, 50, 60, 70});
  
  const std::vector<float> binEdges_offlineNPV({0,  10, 15, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38,  40,  42,
                                                44, 46, 48, 50, 52, 54, 56, 58, 60, 65, 70, 80, 100, 120, 140});

  addTH1D(dirPrefix + metType + "_pt", binEdges_pt);
  addTH1D(dirPrefix + metType + "_phi", binEdges_phi);
  addTH1D(dirPrefix + metType + "_sumEt", binEdges_sumEt);
  addTH2D(dirPrefix + metType + "_simNPU__vs__pt", binEdges_simNPU, binEdges_pt); // for efficiencies vs NPU

  if (matchLabels.empty()) {
    return;
  }

  std::vector<float> binEdges_response(101);
  for (uint idx = 0; idx < binEdges_response.size(); ++idx) {
    binEdges_response.at(idx) = 0.05 * idx;
  }

  std::vector<float> binEdges_deltaPhi(21);
  for (uint idx = 0; idx < binEdges_deltaPhi.size(); ++idx) {
    binEdges_deltaPhi.at(idx) = M_PI * 0.05 * idx;
  }

  std::vector<float> binEdges_deltaPt(61);
  for (uint idx = 0; idx < binEdges_deltaPt.size(); ++idx) {
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
    addTH2D(dirPrefix + metType + "_pt_over" + matchLabel + "__vs__simNPU", binEdges_response, binEdges_simNPU);
    addTH2D(dirPrefix + metType + "_pt_over" + matchLabel + "__vs__offlineNPV", binEdges_response, binEdges_offlineNPV);

    addTH2D(
        dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_deltaPhi, binEdges_pt);
    addTH2D(dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPhi,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPhi,
            binEdges_sumEt);
    addTH2D(dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__simNPU", binEdges_deltaPhi, binEdges_simNPU);
    addTH2D(
        dirPrefix + metType + "_deltaPhi" + matchLabel + "__vs__offlineNPV", binEdges_deltaPhi, binEdges_offlineNPV);

    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_pt",
            binEdges_response,
            binEdges_pt);
    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_response,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_response,
            binEdges_sumEt);
    addTH2D(dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__simNPU", binEdges_response, binEdges_simNPU);
    addTH2D(
        dirPrefix + metType + "_sumEt_over" + matchLabel + "__vs__offlineNPV", binEdges_response, binEdges_offlineNPV);

    addTH2D(
        dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPt,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPt,
            binEdges_sumEt);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__simNPU", binEdges_deltaPt, binEdges_simNPU);
    addTH2D(
        dirPrefix + metType + "_pt_paraTo" + matchLabel + "__vs__offlineNPV", binEdges_deltaPt, binEdges_offlineNPV);

    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel + "_pt",
            binEdges_deltaPt,
            binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPt,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPt,
            binEdges_sumEt);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__simNPU",
            binEdges_deltaPt,
            binEdges_simNPU);
    addTH2D(dirPrefix + metType + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__offlineNPV",
            binEdges_deltaPt,
            binEdges_offlineNPV);

    addTH2D(
        dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_pt", binEdges_deltaPt, binEdges_pt);
    addTH2D(dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_phi",
            binEdges_deltaPt,
            binEdges_phi);
    addTH2D(dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_sumEt",
            binEdges_deltaPt,
            binEdges_sumEt);
    addTH2D(dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__simNPU", binEdges_deltaPt, binEdges_simNPU);
    addTH2D(
        dirPrefix + metType + "_pt_perpTo" + matchLabel + "__vs__offlineNPV", binEdges_deltaPt, binEdges_offlineNPV);
  }
}

void JMETriggerAnalysisDriver::fillHistograms_Jets(const std::string& dir,
                                                   const fillHistoDataJets& fhData,
                                                   float const weight) {
  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') {
    dirPrefix.pop_back();
  }
  if (not dirPrefix.empty()) {
    dirPrefix += "/";
  }
  // modification start
  // adding the simulated number of PU in the variables
  auto const simNPU = this->value<int>("pileupInfo_BX0_numPUInteractions"); 
  // modification end  
  auto const* v_pt(this->vector_ptr<float>(fhData.jetCollection + "_pt"));
  auto const* v_eta(this->vector_ptr<float>(fhData.jetCollection + "_eta"));
  auto const* v_phi(this->vector_ptr<float>(fhData.jetCollection + "_phi"));
  auto const* v_mass(this->vector_ptr<float>(fhData.jetCollection + "_mass"));
  auto const* v_leadCandPt(this->vector_ptr<float>(fhData.jetCollection + "_leadCandPt"));
  
  
  auto const* v_numberOfDaughters(this->vector_ptr<uint>(fhData.jetCollection + "_numberOfDaughters"));
  
  auto const* v_chargedHadronMultiplicity(this->vector_ptr<int>(fhData.jetCollection + "_chargedHadronMultiplicity"));
  auto const* v_neutralHadronMultiplicity(this->vector_ptr<int>(fhData.jetCollection + "_neutralHadronMultiplicity"));
  auto const* v_electronMultiplicity(this->vector_ptr<int>(fhData.jetCollection + "_electronMultiplicity"));
  auto const* v_photonMultiplicity(this->vector_ptr<int>(fhData.jetCollection + "_photonMultiplicity"));
  auto const* v_muonMultiplicity(this->vector_ptr<int>(fhData.jetCollection + "_muonMultiplicity"));

  auto const* v_chargedHadronEnergyFraction(
      this->vector_ptr<float>(fhData.jetCollection + "_chargedHadronEnergyFraction"));
  auto const* v_neutralHadronEnergyFraction(
      this->vector_ptr<float>(fhData.jetCollection + "_neutralHadronEnergyFraction"));
  auto const* v_electronEnergyFraction(this->vector_ptr<float>(fhData.jetCollection + "_electronEnergyFraction"));
  auto const* v_photonEnergyFraction(this->vector_ptr<float>(fhData.jetCollection + "_photonEnergyFraction"));
  auto const* v_muonEnergyFraction(this->vector_ptr<float>(fhData.jetCollection + "_muonEnergyFraction"));
  
  
  if (not(v_pt and v_eta and v_phi and v_mass)) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriver::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
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
      if (v_pt->at(idx) <= fhData.jetPtMin or std::abs(v_eta->at(idx)) >= fhData.jetAbsEtaMax) {
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

    float sumPt(0.), sumPx(0.), sumPy(0.);

    for (auto const jetIdx : jetIndices) {
      if(v_pt->at(jetIdx) > 30){ // add only contributions with above 30GeV for HT
        sumPt += v_pt->at(jetIdx);
      }
      if(v_pt->at(jetIdx) > 15){ // add only contributions with above 30GeV for MHT
        sumPx += v_pt->at(jetIdx) * std::cos(v_phi->at(jetIdx));
        sumPy += v_pt->at(jetIdx) * std::sin(v_phi->at(jetIdx));
      }
      
      // modification start
      H1(dirPrefix + fhData.jetCollection + catLabel + "_simNPU")->Fill(simNPU, weight);
      // modification end 
      H1(dirPrefix + fhData.jetCollection + catLabel + "_pt")->Fill(v_pt->at(jetIdx), weight);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_eta")->Fill(v_eta->at(jetIdx), weight);
      H2(dirPrefix + fhData.jetCollection + catLabel + "_eta__vs__pt")
          ->Fill(v_eta->at(jetIdx), v_pt->at(jetIdx), weight);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_phi")->Fill(v_phi->at(jetIdx), weight);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_mass")->Fill(v_mass->at(jetIdx), weight);
      
      if (v_numberOfDaughters) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_numberOfDaughters")
            ->Fill(v_numberOfDaughters->at(jetIdx), weight);
      }
      if (v_chargedHadronMultiplicity) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_chargedHadronMultiplicity")
            ->Fill(v_chargedHadronMultiplicity->at(jetIdx), weight);
      }
      if (v_neutralHadronMultiplicity) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_neutralHadronMultiplicity")
            ->Fill(v_neutralHadronMultiplicity->at(jetIdx), weight);
      }
      if (v_electronMultiplicity) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_electronMultiplicity")
            ->Fill(v_electronMultiplicity->at(jetIdx), weight);
      }
      if (v_photonMultiplicity) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_photonMultiplicity")
            ->Fill(v_photonMultiplicity->at(jetIdx), weight);
      }
      if (v_muonMultiplicity) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_muonMultiplicity")
            ->Fill(v_muonMultiplicity->at(jetIdx), weight);
      }
      if (v_chargedHadronEnergyFraction) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_chargedHadronEnergyFraction")
            ->Fill(v_chargedHadronEnergyFraction->at(jetIdx), weight);
      }
      if (v_neutralHadronEnergyFraction) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_neutralHadronEnergyFraction")
            ->Fill(v_neutralHadronEnergyFraction->at(jetIdx), weight);
      }
      if (v_electronEnergyFraction) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_electronEnergyFraction")
            ->Fill(v_electronEnergyFraction->at(jetIdx), weight);
      }
      if (v_photonEnergyFraction) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_photonEnergyFraction")
            ->Fill(v_photonEnergyFraction->at(jetIdx), weight);
      }
      if (v_muonEnergyFraction) {
        H1(dirPrefix + fhData.jetCollection + catLabel + "_muonEnergyFraction")
            ->Fill(v_muonEnergyFraction->at(jetIdx), weight);
      }
      
    }

    H1(dirPrefix + fhData.jetCollection + catLabel + "_njets")->Fill(0.01 + jetIndices.size(), weight);

    H1(dirPrefix + fhData.jetCollection + catLabel + "_HT")->Fill(sumPt, weight);
    H1(dirPrefix + fhData.jetCollection + catLabel + "_MHT")->Fill(sqrt(sumPx * sumPx + sumPy * sumPy), weight);
    
    H2(dirPrefix + fhData.jetCollection + catLabel + "_simNPU__vs__HT")
          ->Fill(simNPU, sumPt, weight);
    if (indexMaxPtJet >= 0) {
      H1(dirPrefix + fhData.jetCollection + catLabel + "_pt0")->Fill(v_pt->at(indexMaxPtJet), weight);
      H2(dirPrefix + fhData.jetCollection + catLabel + "_simNPU__vs__pt0")
          ->Fill(simNPU, v_pt->at(indexMaxPtJet), weight);
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
    auto const* v_match_leadCandPt(this->vector_ptr<float>(matchJetColl + "_leadCandPt"));

    if (not(v_match_pt and v_match_eta and v_match_phi and v_match_mass)) {
      if (verbosity_ >= 0) {
        std::cout << "JMETriggerAnalysisDriver::fillHistograms_Jets(\"" << dir << "\", const fillHistoDataJets&) -- "
                  << "branches not available (histograms will not be filled): " << matchJetColl + "_pt/eta/phi/mass"
                  << std::endl;
      }
      continue;
    }

    std::map<size_t, size_t> mapMatchIndeces;
    std::vector<float> vecMatchMinDeltaR2(v_pt->size(), -1.f);
    for (size_t idx = 0; idx < v_pt->size(); ++idx) {
      if (v_pt->at(idx) <= fhData.jetPtMin or std::abs(v_eta->at(idx)) >= fhData.jetAbsEtaMax) {
        continue;
      }

      int indexBestMatch = -1;
      auto const dR2thr = matchJetDeltaRMin * matchJetDeltaRMin;
      auto& dR2min = vecMatchMinDeltaR2.at(idx);
      for (size_t idxMatch = 0; idxMatch < v_match_pt->size(); ++idxMatch) {
        if (v_match_pt->at(idxMatch) <= matchJetPtMin) {
          continue;
        }

        auto const dR2 =
            utils::deltaR2(v_eta->at(idx), v_phi->at(idx), v_match_eta->at(idxMatch), v_match_phi->at(idxMatch));
        if (dR2min < 0 or dR2 < dR2min) {
          dR2min = dR2;
          if (dR2 < dR2thr)
            indexBestMatch = idxMatch;
        }
      }

      if (indexBestMatch >= 0) {
        mapMatchIndeces.insert(std::make_pair(idx, indexBestMatch));
      }
    }

    //    if(verbose_ > 0){
    //
    //
    //      for(size_t idx=0; idx<v_pt->size(); ++idx){
    //        if(v_pt->at(idx) <= fhData.jetPtMin){ continue; }
    //
    //        for(auto const& catLabel : jetCategoryLabels_){
    //
    //          if(jetBelongsToCategory(catLabel, v_pt->at(idx), std::abs(v_eta->at(idx))))
    //        }
    //
    //
    //      }
    //
    //
    //    }

    for (auto const& catLabel : jetCategoryLabels_) {
      std::vector<size_t> jetIndices;
      jetIndices.reserve(v_pt->size());
      for (size_t idx = 0; idx < v_pt->size(); ++idx) {
        if (v_pt->at(idx) <= fhData.jetPtMin or std::abs(v_eta->at(idx)) >= fhData.jetAbsEtaMax) {
          continue;
        }

        if (jetBelongsToCategory(catLabel, v_pt->at(idx), std::abs(v_eta->at(idx)), v_phi->at(idx), v_eta->at(idx))) {
          jetIndices.emplace_back(idx);
        }
      }

      // indeces of match-jets with same selection as target jets
      std::vector<size_t> jetMatchRefIndices;
      jetMatchRefIndices.reserve(v_match_pt->size());
      for (size_t idx = 0; idx < v_match_pt->size(); ++idx) {
        if (v_match_pt->at(idx) <= fhData.jetPtMin or std::abs(v_match_eta->at(idx)) >= fhData.jetAbsEtaMax) {
          continue;
        }

        if (jetBelongsToCategory(catLabel, v_match_pt->at(idx), std::abs(v_match_eta->at(idx)), v_match_phi->at(idx), v_match_eta->at(idx))) {
          jetMatchRefIndices.emplace_back(idx);
        }
      }

      float sumPt(0.), sumPx(0.), sumPy(0.);
      for (auto const jetIdx : jetIndices) {
        auto const jetPt(v_pt->at(jetIdx));
        auto const jetPhi(v_phi->at(jetIdx));

        sumPt += jetPt;
        sumPx += jetPt * std::cos(jetPhi);
        sumPy += jetPt * std::sin(jetPhi);
      }

      float sumMatchRefPt(0.), sumMatchRefPx(0.), sumMatchRefPy(0.);
      for (auto const jetMatchRefIdx : jetMatchRefIndices) {
        auto const jetMatchRefPt(v_match_pt->at(jetMatchRefIdx));
        auto const jetMatchRefPhi(v_match_phi->at(jetMatchRefIdx));

        sumMatchRefPt += jetMatchRefPt;
        sumMatchRefPx += jetMatchRefPt * std::cos(jetMatchRefPhi);
        sumMatchRefPy += jetMatchRefPt * std::sin(jetMatchRefPhi);
      }

      H2(dirPrefix + fhData.jetCollection + catLabel + "_HT__vs__" + matchLabel + "_HT")
          ->Fill(sumPt, sumMatchRefPt, weight);
      H2(dirPrefix + fhData.jetCollection + catLabel + "_MHT__vs__" + matchLabel + "_MHT")
          ->Fill(sqrt(sumPx * sumPx + sumPy * sumPy),
                 sqrt(sumMatchRefPx * sumMatchRefPx + sumMatchRefPy * sumMatchRefPy),
                 weight);

      size_t nJetsMatched(0), nJetsNotMatched(0);
      float sumPtMatched(0.), sumPtNotMatched(0.);
      float sumPxMatched(0.), sumPxNotMatched(0.);
      float sumPyMatched(0.), sumPyNotMatched(0.);
      int indexMaxPtJetWithMatch(-1), indexMaxPtJetWithNoMatch(-1);
      float maxPtJetPtWithMatch(-1.), maxPtJetPtWithNoMatch(-1.);

      int indexCounter(-1);
      for (auto const jetIdx : jetIndices) {
        ++indexCounter;

        auto const jetPt(v_pt->at(jetIdx));
        auto const jetEta(v_eta->at(jetIdx));
        auto const jetPhi(v_phi->at(jetIdx));
        auto const jetMass(v_mass->at(jetIdx));

        auto const hasMatch(mapMatchIndeces.find(jetIdx) != mapMatchIndeces.end());

        auto const minDeltaR = vecMatchMinDeltaR2.at(jetIdx) < 0.f ? -1.f : sqrt(vecMatchMinDeltaR2.at(jetIdx));

        if (hasMatch) {
          ++nJetsMatched;

          sumPtMatched += jetPt;
          sumPxMatched += jetPt * std::cos(jetPhi);
          sumPyMatched += jetPt * std::sin(jetPhi);

          if ((nJetsMatched == 1) or (jetPt > maxPtJetPtWithMatch)) {
            maxPtJetPtWithMatch = jetPt;
            indexMaxPtJetWithMatch = jetIdx;
          }
          // modification start
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_simNPU")->Fill(simNPU, weight);
          // modification
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt")->Fill(jetPt, weight);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_eta")->Fill(jetEta, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__pt")
              ->Fill(jetEta, jetPt, weight);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_phi")->Fill(jetPhi, weight);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass")->Fill(jetMass, weight);
          
          
          if (v_numberOfDaughters) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_numberOfDaughters")
                ->Fill(v_numberOfDaughters->at(jetIdx), weight);
          }
          if (v_chargedHadronMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_chargedHadronMultiplicity")
                ->Fill(v_chargedHadronMultiplicity->at(jetIdx), weight);
          }
          if (v_neutralHadronMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_neutralHadronMultiplicity")
                ->Fill(v_neutralHadronMultiplicity->at(jetIdx), weight);
          }
          if (v_electronMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_electronMultiplicity")
                ->Fill(v_electronMultiplicity->at(jetIdx), weight);
          }
          if (v_photonMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_photonMultiplicity")
                ->Fill(v_photonMultiplicity->at(jetIdx), weight);
          }
          if (v_muonMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_muonMultiplicity")
                ->Fill(v_muonMultiplicity->at(jetIdx), weight);
          }
          if (v_chargedHadronEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_chargedHadronEnergyFraction")
                ->Fill(v_chargedHadronEnergyFraction->at(jetIdx), weight);
          }
          if (v_neutralHadronEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_neutralHadronEnergyFraction")
                ->Fill(v_neutralHadronEnergyFraction->at(jetIdx), weight);
          }
          if (v_electronEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_electronEnergyFraction")
                ->Fill(v_electronEnergyFraction->at(jetIdx), weight);
          }
          if (v_photonEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_photonEnergyFraction")
                ->Fill(v_photonEnergyFraction->at(jetIdx), weight);
          }
          if (v_muonEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_muonEnergyFraction")
                ->Fill(v_muonEnergyFraction->at(jetIdx), weight);
          }
          
          
          auto const jetMatchIdx(mapMatchIndeces.at(jetIdx));

          auto const jetMatchPt(v_match_pt->at(jetMatchIdx));
          auto const jetMatchEta(v_match_eta->at(jetMatchIdx));
          auto const jetMatchPhi(v_match_phi->at(jetMatchIdx));
          auto const jetMatchMass(v_match_mass->at(jetMatchIdx));

          H2(dirPrefix + fhData.jetCollection + catLabel + "_pt__vs__" + matchLabel + "_pt")
              ->Fill(jetPt, jetMatchPt, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_pt__vs__" + matchLabel + "_eta")
              ->Fill(jetPt, jetMatchEta, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_pt__vs__" + matchLabel + "_minDeltaR")
              ->Fill(jetPt, minDeltaR, weight);

          if (indexCounter == 0) {
            H2(dirPrefix + fhData.jetCollection + catLabel + "_pt0__vs__" + matchLabel + "_pt")
                ->Fill(jetPt, jetMatchPt, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_pt0__vs__" + matchLabel + "_eta")
                ->Fill(jetPt, jetMatchEta, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_pt0__vs__" + matchLabel + "_minDeltaR")
                ->Fill(jetPt, minDeltaR, weight);
          }

          H2(dirPrefix + fhData.jetCollection + catLabel + "_eta__vs__" + matchLabel + "_minDeltaR")
              ->Fill(jetEta, minDeltaR, weight);

          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt__vs__" + matchLabel + "_pt")
              ->Fill(jetPt, jetMatchPt, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_eta__vs__" + matchLabel +
             "_eta")
              ->Fill(jetEta, jetMatchEta, weight);

          auto const dR2match(utils::deltaR2(jetEta, jetPhi, jetMatchEta, jetMatchPhi));
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_dRmatch")
              ->Fill(sqrt(dR2match), weight);

          if (jetMatchPt != 0.) {
            auto const jetPtRatio(jetPt / jetMatchPt);
            
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel)
                ->Fill(jetPtRatio, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__" + matchLabel + "_pt")
                ->Fill(jetPtRatio, jetMatchPt, weight);
            if (v_leadCandPt && v_match_leadCandPt){
              H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_leadCandPt_over" + matchLabel +
                 "__vs__" + matchLabel + "_pt")
                  ->Fill(v_leadCandPt->at(jetIdx)/v_match_leadCandPt->at(jetMatchIdx), jetMatchPt, weight);
              
              H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_leadCandPt_over" + matchLabel +
                 "__vs__" + matchLabel + "_simNPU")
                  ->Fill(v_leadCandPt->at(jetIdx)/v_match_leadCandPt->at(jetMatchIdx), simNPU, weight);
              
            }
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__pt")
                ->Fill(jetPtRatio, jetPt, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__phi")
                ->Fill(jetPtRatio, jetPhi, weight);
            // modification start
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__" + matchLabel + "_simNPU")
                ->Fill(jetPtRatio, simNPU, weight);
            // modification end
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__" + matchLabel + "_eta")
                ->Fill(jetPtRatio, jetMatchEta, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt_over" + matchLabel +
               "__vs__" + matchLabel + "_phi")
                ->Fill(jetPtRatio, jetMatchPhi, weight);
          }

          if (jetMatchMass != 0.) {
            auto const jetMassRatio(jetMass / jetMatchMass);
            H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel)
                ->Fill(jetMassRatio, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel +
               "__vs__" + matchLabel + "_pt")
                ->Fill(jetMassRatio, jetMatchPt, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel +
               "__vs__" + matchLabel + "_eta")
                ->Fill(jetMassRatio, jetMatchEta, weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_mass_over" + matchLabel +
               "__vs__" + matchLabel + "_mass")
                ->Fill(jetMassRatio, jetMatchMass, weight);
          }
        } else {
          ++nJetsNotMatched;

          sumPtNotMatched += jetPt;
          sumPxNotMatched += jetPt * std::cos(jetPhi);
          sumPyNotMatched += jetPt * std::sin(jetPhi);

          if ((nJetsNotMatched == 1) or (jetPt > maxPtJetPtWithNoMatch)) {
            maxPtJetPtWithNoMatch = jetPt;
            indexMaxPtJetWithNoMatch = jetIdx;
          }

          H2(dirPrefix + fhData.jetCollection + catLabel + "_pt__vs__" + matchLabel + "_pt")->Fill(jetPt, -1., weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_pt__vs__" + matchLabel + "_eta")->Fill(jetPt, -99., weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_pt__vs__" + matchLabel + "_minDeltaR")
              ->Fill(jetPt, minDeltaR, weight);

          if (indexCounter == 0) {
            H2(dirPrefix + fhData.jetCollection + catLabel + "_pt0__vs__" + matchLabel + "_pt")
                ->Fill(jetPt, -1., weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_pt0__vs__" + matchLabel + "_eta")
                ->Fill(jetPt, -99., weight);
            H2(dirPrefix + fhData.jetCollection + catLabel + "_pt0__vs__" + matchLabel + "_minDeltaR")
                ->Fill(jetPt, minDeltaR, weight);
          }

          H2(dirPrefix + fhData.jetCollection + catLabel + "_eta__vs__" + matchLabel + "_minDeltaR")
              ->Fill(jetEta, minDeltaR, weight);
          // modification start
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_simNPU")->Fill(simNPU, weight);
          // modification
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_pt")->Fill(jetPt, weight);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_eta")->Fill(jetEta, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_eta__vs__pt")
              ->Fill(jetEta, jetPt, weight);
              
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_phi")->Fill(jetPhi, weight);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_mass")
              ->Fill(jetMass, weight);
              
          
          if (v_numberOfDaughters) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_numberOfDaughters")
                ->Fill(v_numberOfDaughters->at(jetIdx), weight);
          }
          if (v_chargedHadronMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel +
               "_chargedHadronMultiplicity")
                ->Fill(v_chargedHadronMultiplicity->at(jetIdx), weight);
          }
          if (v_neutralHadronMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel +
               "_neutralHadronMultiplicity")
                ->Fill(v_neutralHadronMultiplicity->at(jetIdx), weight);
          }
          if (v_electronMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_electronMultiplicity")
                ->Fill(v_electronMultiplicity->at(jetIdx), weight);
          }
          if (v_photonMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_photonMultiplicity")
                ->Fill(v_photonMultiplicity->at(jetIdx), weight);
          }
          if (v_muonMultiplicity) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_muonMultiplicity")
                ->Fill(v_muonMultiplicity->at(jetIdx), weight);
          }
          if (v_chargedHadronEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel +
               "_chargedHadronEnergyFraction")
                ->Fill(v_chargedHadronEnergyFraction->at(jetIdx), weight);
          }
          if (v_neutralHadronEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel +
               "_neutralHadronEnergyFraction")
                ->Fill(v_neutralHadronEnergyFraction->at(jetIdx), weight);
          }
          if (v_electronEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_electronEnergyFraction")
                ->Fill(v_electronEnergyFraction->at(jetIdx), weight);
          }
          if (v_photonEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_photonEnergyFraction")
                ->Fill(v_photonEnergyFraction->at(jetIdx), weight);
          }
          if (v_muonEnergyFraction) {
            H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_muonEnergyFraction")
                ->Fill(v_muonEnergyFraction->at(jetIdx), weight);
          }
          
        }
      }

      H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_njets")
          ->Fill(0.01 + nJetsMatched, weight);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_njets")
          ->Fill(0.01 + nJetsNotMatched, weight);
      // modification start
      //if((nJetsMatched+nJetsNotMatched)!=0){
      //  H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_njets_over_tot" +"__vs__simNPU")
      //        ->Fill( (nJetsMatched*1.0)/((nJetsMatched+nJetsNotMatched)*1.0), simNPU, weight);
      //}
      if((nJetsMatched+nJetsNotMatched)!=0){
        H2(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_njets__vs__simNPU")
              ->Fill(0.01 + nJetsNotMatched, simNPU, weight);
      }
      // modification end
      H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_HT")->Fill(sumPtMatched, weight);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_HT")
          ->Fill(sumPtNotMatched, weight);

      H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_MHT")
          ->Fill(sqrt(sumPxMatched * sumPxMatched + sumPyMatched * sumPyMatched), weight);
      H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_MHT")
          ->Fill(sqrt(sumPxNotMatched * sumPxNotMatched + sumPyNotMatched * sumPyNotMatched), weight);

      if (indexMaxPtJetWithMatch >= 0) {
        auto const maxPtJetPt(v_pt->at(indexMaxPtJetWithMatch));
        auto const maxPtJetMatchPt(v_match_pt->at(mapMatchIndeces.at(indexMaxPtJetWithMatch)));
        auto const maxPtJetMatchEta(v_match_eta->at(mapMatchIndeces.at(indexMaxPtJetWithMatch)));
        H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0")->Fill(maxPtJetPt, weight);
        H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0__vs__" + matchLabel + "_pt")
            ->Fill(maxPtJetPt, maxPtJetMatchPt, weight);
        H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0__vs__" + matchLabel + "_eta")
            ->Fill(maxPtJetPt, maxPtJetMatchEta, weight);
        if (maxPtJetMatchPt != 0.) {
          auto const maxPtJetPtRatio(maxPtJetPt / maxPtJetMatchPt);
          H1(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel)
              ->Fill(maxPtJetPtRatio, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel +
             "__vs__" + matchLabel + "_pt")
              ->Fill(maxPtJetPtRatio, maxPtJetMatchPt, weight);
          H2(dirPrefix + fhData.jetCollection + catLabel + "_MatchedTo" + matchLabel + "_pt0_over" + matchLabel +
             "__vs__" + matchLabel + "_eta")
              ->Fill(maxPtJetPtRatio, maxPtJetMatchEta, weight);
        }
      }

      if (indexMaxPtJetWithNoMatch >= 0) {
        auto const maxPtJetPt(v_pt->at(indexMaxPtJetWithNoMatch));
        H1(dirPrefix + fhData.jetCollection + catLabel + "_NotMatchedTo" + matchLabel + "_pt0")
            ->Fill(maxPtJetPt, weight);
      }
    }
  }
}

void JMETriggerAnalysisDriver::fillHistograms_MET(const std::string& dir,
                                                  const fillHistoDataMET& fhData,
                                                  float const weight) {
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

  auto const simNPU = this->value<int>("pileupInfo_BX0_numPUInteractions");

  uint offlineNPV(0);
  auto const* v_offlinePV_z(this->vector_ptr<float>("offlinePrimaryVertices_z"));
  if (v_offlinePV_z) {
    offlineNPV = v_offlinePV_z->size();
  }

  if (not(v_pt and v_phi and v_sumEt)) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                << "branches not available (histograms will not be filled): " << fhData.metCollection + "_pt/phi/sumEt"
                << std::endl;
    }
    return;
  }

  if (not((v_pt->size() == 1) and (v_phi->size() == 1) and (v_sumEt->size() == 1))) {
    if (verbosity_ >= 0) {
      std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                << "MET branches have invalid size (histograms will not be filled): "
                << fhData.metCollection + "_pt/phi/sumEt" << std::endl;
    }
    return;
  }

  auto const metPt(v_pt->at(0));
  auto const metPhi(v_phi->at(0));
  auto const metSumEt(v_sumEt->at(0));

  H1(dirPrefix + fhData.metCollection + "_pt")->Fill(metPt, weight);
  H1(dirPrefix + fhData.metCollection + "_phi")->Fill(metPhi, weight);
  H1(dirPrefix + fhData.metCollection + "_sumEt")->Fill(metSumEt, weight);
  H2(dirPrefix + fhData.metCollection + "_simNPU__vs__pt")->Fill(simNPU, metPt); // for efficiencies vs NPU

  for (auto const& fhDataMatch : fhData.matches) {
    auto const matchLabel(fhDataMatch.label);
    auto const matchMetColl(fhDataMatch.metCollection);

    auto const* v_match_pt(this->vector_ptr<float>(matchMetColl + "_pt"));
    auto const* v_match_phi(this->vector_ptr<float>(matchMetColl + "_phi"));
    auto const* v_match_sumEt(this->vector_ptr<float>(matchMetColl + "_sumEt"));

    if (not(v_match_pt and v_match_phi and v_match_sumEt)) {
      if (verbosity_ >= 0) {
        std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
                  << "branches not available (histograms will not be filled): " << matchMetColl + "_pt/phi/sumEt"
                  << std::endl;
      }
      continue;
    }

    if (not((v_match_pt->size() == 1) and (v_match_phi->size() == 1) and (v_match_sumEt->size() == 1))) {
      if (verbosity_ >= 0) {
        std::cout << "JMETriggerAnalysisDriver::fillHistograms_MET(\"" << dir << "\", const fillHistoDataMET&) -- "
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
      H2(dirPrefix + fhData.metCollection + "_pt__vs__" + matchLabel + "_pt")->Fill(metPt, metMatchPt, weight);
      H1(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel)->Fill(metPtRatio, weight);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_pt")
          ->Fill(metPtRatio, metMatchPt, weight);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_phi")
          ->Fill(metPtRatio, metMatchPhi, weight);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt")
          ->Fill(metPtRatio, metMatchSumEt, weight);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__simNPU")->Fill(metPtRatio, simNPU, weight);
      H2(dirPrefix + fhData.metCollection + "_pt_over" + matchLabel + "__vs__offlineNPV")
          ->Fill(metPtRatio, offlineNPV, weight);
    }

    if (metMatchSumEt != 0.) {
      auto const metSumEtRatio(metSumEt / metMatchSumEt);
      H2(dirPrefix + fhData.metCollection + "_sumEt__vs__" + matchLabel + "_sumEt")
          ->Fill(metSumEt, metMatchSumEt, weight);
      H1(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel)->Fill(metSumEtRatio, weight);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_pt")
          ->Fill(metSumEtRatio, metMatchPt, weight);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_phi")
          ->Fill(metSumEtRatio, metMatchPhi, weight);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__" + matchLabel + "_sumEt")
          ->Fill(metSumEtRatio, metMatchSumEt, weight);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__simNPU")
          ->Fill(metSumEtRatio, simNPU, weight);
      H2(dirPrefix + fhData.metCollection + "_sumEt_over" + matchLabel + "__vs__offlineNPV")
          ->Fill(metSumEtRatio, offlineNPV, weight);
    }

    auto const metDeltaPhiMatch(utils::deltaPhi(metPhi, metMatchPhi));
    H2(dirPrefix + fhData.metCollection + "_phi__vs__" + matchLabel + "_phi")->Fill(metPhi, metMatchPhi, weight);
    H1(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel)->Fill(metDeltaPhiMatch, weight);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_pt")
        ->Fill(metDeltaPhiMatch, metMatchPt, weight);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_phi")
        ->Fill(metDeltaPhiMatch, metMatchPhi, weight);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__" + matchLabel + "_sumEt")
        ->Fill(metDeltaPhiMatch, metMatchSumEt, weight);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__simNPU")
        ->Fill(metDeltaPhiMatch, simNPU, weight);
    H2(dirPrefix + fhData.metCollection + "_deltaPhi" + matchLabel + "__vs__offlineNPV")
        ->Fill(metDeltaPhiMatch, offlineNPV, weight);

    auto const metParaToMatch(metPt *
                              (std::cos(metPhi) * std::cos(metMatchPhi) + std::sin(metPhi) * std::sin(metMatchPhi)));
    H1(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel)->Fill(metParaToMatch, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_pt")
        ->Fill(metParaToMatch, metMatchPt, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_phi")
        ->Fill(metParaToMatch, metMatchPhi, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__" + matchLabel + "_sumEt")
        ->Fill(metParaToMatch, metMatchSumEt, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__simNPU")
        ->Fill(metParaToMatch, simNPU, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "__vs__offlineNPV")
        ->Fill(metParaToMatch, offlineNPV, weight);

    auto const metParaToMatchMinusMatch(metParaToMatch - metMatchPt);
    H1(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel)
        ->Fill(metParaToMatchMinusMatch, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel +
       "_pt")
        ->Fill(metParaToMatchMinusMatch, metMatchPt, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel +
       "_phi")
        ->Fill(metParaToMatchMinusMatch, metMatchPhi, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__" + matchLabel +
       "_sumEt")
        ->Fill(metParaToMatchMinusMatch, metMatchSumEt, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__simNPU")
        ->Fill(metParaToMatchMinusMatch, simNPU, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_paraTo" + matchLabel + "Minus" + matchLabel + "__vs__offlineNPV")
        ->Fill(metParaToMatchMinusMatch, offlineNPV, weight);

    auto const metPerpToMatch(metPt *
                              (std::cos(metPhi) * std::sin(metMatchPhi) - std::sin(metPhi) * std::cos(metMatchPhi)));
    H1(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel)->Fill(metPerpToMatch, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_pt")
        ->Fill(metPerpToMatch, metMatchPt, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_phi")
        ->Fill(metPerpToMatch, metMatchPhi, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__" + matchLabel + "_sumEt")
        ->Fill(metPerpToMatch, metMatchSumEt, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__simNPU")
        ->Fill(metPerpToMatch, simNPU, weight);
    H2(dirPrefix + fhData.metCollection + "_pt_perpTo" + matchLabel + "__vs__offlineNPV")
        ->Fill(metPerpToMatch, offlineNPV, weight);
  }
}
