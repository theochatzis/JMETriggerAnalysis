#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriverPhase2MET.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>
#include <Math/GenVector/LorentzVector.h>
#include <Math/GenVector/PtEtaPhiM4D.h>
#include <utility>
#include <cmath>

JMETriggerAnalysisDriverPhase2MET::JMETriggerAnalysisDriverPhase2MET(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriverPhase2MET(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

JMETriggerAnalysisDriverPhase2MET::JMETriggerAnalysisDriverPhase2MET(const std::string& outputFilePath, const std::string& outputFileMode)
  : JMETriggerAnalysisDriver(outputFilePath, outputFileMode) {}

void JMETriggerAnalysisDriverPhase2MET::init(){
  // histogram: events counter
  addTH1D("eventsProcessed", {0, 1});
  addTH1D("weight", 100, -5, 5);

  for(auto const& selLabel : {
    "NoSelection",
    "L1T_PFPuppiMET200off",
    "L1T_PFPuppiMET200off2",
    "L1T_PFPuppiMET220off2",
    "L1T_PFPuppiMET250off2",
  }){
    bookHistograms(selLabel);
  }
}

void JMETriggerAnalysisDriverPhase2MET::analyze(){
  H1("eventsProcessed")->Fill(0.5);

  float wgt(1.f);
//  std::string const tfileName = theFile_->GetName();
//  auto const tfileBasename = tfileName.substr(tfileName.find_last_of("/\\") + 1);
//  if(utils::stringContains(tfileBasename, "MinBias") or (utils::stringContains(tfileBasename, "QCD") and not utils::stringContains(tfileBasename, "Flat"))){
//    if(utils::stringContains(tfileBasename, "PU200"))
//      wgt = value<double>("qcdWeightPU200");
//    else if(utils::stringContains(tfileBasename, "PU140"))
//      wgt = value<double>("qcdWeightPU140");
//    else
//      throw std::runtime_error("failed to determine weight choice from TFile basename: "+tfileName);
//  }
  H1("weight")->Fill(wgt);

  // MET
  fillHistograms("NoSelection", wgt);

  auto const L1T_PFPuppiMET200off = value<bool>("L1T_PFPuppiMET200off");
  auto const L1T_PFPuppiMET200off2 = l1tMETSeed("L1T_PFPuppiMET200off2");
  auto const L1T_PFPuppiMET220off2 = l1tMETSeed("L1T_PFPuppiMET220off2");
  auto const L1T_PFPuppiMET250off2 = l1tMETSeed("L1T_PFPuppiMET250off2");

  if(L1T_PFPuppiMET200off) fillHistograms("L1T_PFPuppiMET200off", wgt);
  if(L1T_PFPuppiMET200off2) fillHistograms("L1T_PFPuppiMET200off2", wgt);
  if(L1T_PFPuppiMET220off2) fillHistograms("L1T_PFPuppiMET220off2", wgt);
  if(L1T_PFPuppiMET250off2) fillHistograms("L1T_PFPuppiMET250off2", wgt);
}

void JMETriggerAnalysisDriverPhase2MET::bookHistograms(const std::string& dir){

  auto dirPrefix(dir);
  while (dirPrefix.back() == '/') { dirPrefix.pop_back(); }
  if(not dirPrefix.empty()){ dirPrefix += "/"; }

  std::vector<float> binEdges_pt(161);
  for(uint idx=0; idx<binEdges_pt.size(); ++idx){ binEdges_pt.at(idx) = idx * 5.; }

  std::vector<float> binEdges_pt_2(15);
  for(uint idx=0; idx<binEdges_pt_2.size(); ++idx){ binEdges_pt_2.at(idx) = 100. + idx * 5.; }

  addTH1D(dirPrefix+"genMETTrue_pt", binEdges_pt);
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

void JMETriggerAnalysisDriverPhase2MET::fillHistograms(const std::string& dir, float const weight){

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
  H1(dirPrefix+"genMETTrue_pt")->Fill(genMETTrue_pt, weight);
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

bool JMETriggerAnalysisDriverPhase2MET::l1tMETSeed(std::string const& key) const {

  auto const offlineMET = getMET("l1tPFPuppiMET_pt") * 1.39739 + 54.2859;

  if(key == "L1T_PFPuppiMET200off2") return offlineMET > 200.;
  else if(key == "L1T_PFPuppiMET220off2") return offlineMET > 220.;
  else if(key == "L1T_PFPuppiMET250off2") return offlineMET > 250.;
  else
    throw std::runtime_error("JMETriggerAnalysisDriverPhase2MET::l1tMETSeed(\""+key+"\") -- invalid key");

  return false;
}

float JMETriggerAnalysisDriverPhase2MET::getMET(std::string const& branchName) const {
  auto const& v_pt = this->vector<float>(branchName);

  if(v_pt.size() != 1){
    std::ostringstream oss;
    oss << "JMETriggerAnalysisDriverPhase2MET::fillHistograms(\"" << branchName << "\") -- "
        << "MET branches have invalid size (" << v_pt.size() << " != 1)";
    throw std::runtime_error(oss.str());
  }

  return v_pt.at(0);
}

float JMETriggerAnalysisDriverPhase2MET::getMHT(float const jetPtMin, float const jetAbsEtaMax) const {
  auto const& v_pt = vector<float>("hltAK4PFPuppiJetsCorrected_pt");
  auto const& v_eta = vector<float>("hltAK4PFPuppiJetsCorrected_eta");
  auto const& v_phi = vector<float>("hltAK4PFPuppiJetsCorrected_phi");
  auto const& v_mass = vector<float>("hltAK4PFPuppiJetsCorrected_mass");

  float MHT_x(0.f), MHT_y(0.f);
  for(size_t jetIdx=0; jetIdx<v_pt.size(); ++jetIdx){
    if(std::abs(v_eta.at(jetIdx)) >= jetAbsEtaMax) continue;

    ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>> const p4polar
      (v_pt.at(jetIdx), v_eta.at(jetIdx), v_phi.at(jetIdx), v_mass.at(jetIdx));

    if(v_pt.at(jetIdx) > jetPtMin){
      MHT_x += p4polar.Px();
      MHT_y += p4polar.Py();
    }
  }

  return sqrt(MHT_x*MHT_x + MHT_y*MHT_y);
}
