#include <JMETriggerAnalysis/NTuplizers/interface/RecoGenJetCollectionContainer.h>

RecoGenJetCollectionContainer::RecoGenJetCollectionContainer(const std::string& name,
                                                             const std::string& inputTagLabel,
                                                             const edm::EDGetToken& token,
                                                             const std::string& strCut,
                                                             const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoGenJetCollectionContainer::clear() {
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();

  numberOfDaughters_.clear();

  chargedHadronEnergyFraction_.clear();
  neutralHadronEnergyFraction_.clear();
  electronEnergyFraction_.clear();
  photonEnergyFraction_.clear();
  muonEnergyFraction_.clear();

  chargedHadronMultiplicity_.clear();
  neutralHadronMultiplicity_.clear();
  electronMultiplicity_.clear();
  photonMultiplicity_.clear();
  muonMultiplicity_.clear();
}

void RecoGenJetCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  numberOfDaughters_.reserve(vec_size);
  ;

  chargedHadronEnergyFraction_.reserve(vec_size);
  neutralHadronEnergyFraction_.reserve(vec_size);
  electronEnergyFraction_.reserve(vec_size);
  photonEnergyFraction_.reserve(vec_size);
  muonEnergyFraction_.reserve(vec_size);

  chargedHadronMultiplicity_.reserve(vec_size);
  neutralHadronMultiplicity_.reserve(vec_size);
  electronMultiplicity_.reserve(vec_size);
  photonMultiplicity_.reserve(vec_size);
  muonMultiplicity_.reserve(vec_size);
}

void RecoGenJetCollectionContainer::emplace_back(const reco::GenJet& obj) {
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  numberOfDaughters_.emplace_back(obj.numberOfDaughters());

  chargedHadronEnergyFraction_.emplace_back(obj.energy() ? (obj.chargedHadronEnergy() / obj.energy()) : -99.);
  neutralHadronEnergyFraction_.emplace_back(obj.energy() ? (obj.neutralHadronEnergy() / obj.energy()) : -99.);
  electronEnergyFraction_.emplace_back(obj.energy() ? (obj.chargedEmEnergy() / obj.energy()) : -99.);
  photonEnergyFraction_.emplace_back(obj.energy() ? (obj.neutralEmEnergy() / obj.energy()) : -99.);
  muonEnergyFraction_.emplace_back(obj.energy() ? (obj.muonEnergy() / obj.energy()) : -99.);

  chargedHadronMultiplicity_.emplace_back(obj.chargedHadronMultiplicity());
  neutralHadronMultiplicity_.emplace_back(obj.neutralHadronMultiplicity());
  electronMultiplicity_.emplace_back(obj.chargedEmMultiplicity());
  photonMultiplicity_.emplace_back(obj.neutralEmMultiplicity());
  muonMultiplicity_.emplace_back(obj.muonMultiplicity());
}
