#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h>

RecoPFCandidateCollectionContainer::RecoPFCandidateCollectionContainer(const std::string& name,
                                                                       const std::string& inputTagLabel,
                                                                       const edm::EDGetToken& token,
                                                                       const std::string& strCut,
                                                                       const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPFCandidateCollectionContainer::clear() {
  charge_.clear();
  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  energy_.clear();
  rawEcalEnergy_.clear();
  rawHcalEnergy_.clear();
  ecalEnergy_.clear();
  hcalEnergy_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
}

void RecoPFCandidateCollectionContainer::reserve(const size_t vec_size) {
  charge_.reserve(vec_size);
  pdgId_.reserve(vec_size);
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  energy_.clear();
  rawEcalEnergy_.reserve(vec_size);
  rawHcalEnergy_.reserve(vec_size);
  ecalEnergy_.reserve(vec_size);
  hcalEnergy_.reserve(vec_size);
  vx_.reserve(vec_size);
  vy_.reserve(vec_size);
  vz_.reserve(vec_size);
}

void RecoPFCandidateCollectionContainer::emplace_back(const reco::PFCandidate& obj) {
  charge_.emplace_back(obj.charge());
  pdgId_.emplace_back(obj.pdgId());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());
  energy_.emplace_back(obj.energy());
  rawEcalEnergy_.emplace_back(obj.rawEcalEnergy());
  rawHcalEnergy_.emplace_back(obj.rawHcalEnergy());
  ecalEnergy_.emplace_back(obj.ecalEnergy());
  hcalEnergy_.emplace_back(obj.hcalEnergy());
  vx_.emplace_back(obj.vx());
  vy_.emplace_back(obj.vy());
  vz_.emplace_back(obj.vz());
}
