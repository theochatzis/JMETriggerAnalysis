#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h>

RecoPFCandidateCollectionContainer::RecoPFCandidateCollectionContainer(const std::string& name,
                                                                       const std::string& inputTagLabel,
                                                                       const edm::EDGetToken& token,
                                                                       const std::string& strCut,
                                                                       const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPFCandidateCollectionContainer::clear() {
  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  rawEcalEnergy_.clear();
  rawHcalEnergy_.clear();
  ecalEnergyToRaw_.clear();
  hcalEnergyToRaw_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
  time_.clear();
  timeError_.clear();
}

void RecoPFCandidateCollectionContainer::reserve(const size_t vec_size) {
  pdgId_.reserve(vec_size);
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  rawEcalEnergy_.reserve(vec_size);
  rawHcalEnergy_.reserve(vec_size);
  ecalEnergyToRaw_.reserve(vec_size);
  hcalEnergyToRaw_.reserve(vec_size);
  vx_.reserve(vec_size);
  vy_.reserve(vec_size);
  vz_.reserve(vec_size);
  time_.reserve(vec_size);
  timeError_.reserve(vec_size);
}

void RecoPFCandidateCollectionContainer::emplace_back(const reco::PFCandidate& obj) {
  pdgId_.emplace_back(obj.pdgId());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());
  rawEcalEnergy_.emplace_back(obj.rawEcalEnergy());
  rawHcalEnergy_.emplace_back(obj.rawHcalEnergy());
  
  float ecalResponse = -1;
  if (obj.rawEcalEnergy()>0.){
    ecalResponse = obj.ecalEnergy()/obj.rawEcalEnergy();
  }

  float hcalResponse = -1;
  if (obj.rawHcalEnergy()>0.){
    hcalResponse = obj.hcalEnergy()/obj.rawHcalEnergy();
  }

  ecalEnergyToRaw_.emplace_back(ecalResponse); 
  hcalEnergyToRaw_.emplace_back(hcalResponse);
  
  vx_.emplace_back(obj.vx());
  vy_.emplace_back(obj.vy());
  vz_.emplace_back(obj.vz());
  time_.emplace_back(obj.time());
  timeError_.emplace_back(obj.timeError());
}
