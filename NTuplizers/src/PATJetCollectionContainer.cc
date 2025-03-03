#include <JMETriggerAnalysis/NTuplizers/interface/PATJetCollectionContainer.h>

PATJetCollectionContainer::PATJetCollectionContainer(const std::string& name,
                                                     const std::string& inputTagLabel,
                                                     const edm::EDGetToken& token,
                                                     const std::string& strCut,
                                                     const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void PATJetCollectionContainer::clear() {
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();

  jesc_.clear();
  jetArea_.clear();
  numberOfDaughters_.clear();
  jetID_.clear();

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

void PATJetCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  jesc_.reserve(vec_size);
  jetArea_.reserve(vec_size);
  numberOfDaughters_.reserve(vec_size);
  jetID_.reserve(vec_size);

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

void PATJetCollectionContainer::emplace_back(const pat::Jet& obj) {
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  jesc_.emplace_back(obj.jecFactor(0) ? (1. / obj.jecFactor(0)) : 1.);
  jetArea_.emplace_back(obj.jetArea());
  numberOfDaughters_.emplace_back(obj.numberOfDaughters());
  
  uint jid(0);
  if(obj.hasUserInt("PFJetIDTightLepVeto") && (obj.userInt("PFJetIDTightLepVeto") > 0)){ jid = 3; }
  else if(obj.hasUserInt("PFJetIDTight") && (obj.userInt("PFJetIDTight") > 0)){ jid = 2; }
  else if(obj.hasUserInt("PFJetIDLoose") && (obj.userInt("PFJetIDLoose") > 0)){ jid = 1; }
  jetID_.emplace_back(jid);

  chargedHadronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.chargedHadronEnergyFraction() : -99.);
  neutralHadronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.neutralHadronEnergyFraction() : -99.);
  electronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.electronEnergyFraction() : -99.);
  photonEnergyFraction_.emplace_back(obj.isPFJet() ? obj.photonEnergyFraction() : -99.);
  muonEnergyFraction_.emplace_back(obj.isPFJet() ? obj.muonEnergyFraction() : -99.);

  chargedHadronMultiplicity_.emplace_back(obj.isPFJet() ? obj.chargedHadronMultiplicity() : -1);
  neutralHadronMultiplicity_.emplace_back(obj.isPFJet() ? obj.neutralHadronMultiplicity() : -1);
  electronMultiplicity_.emplace_back(obj.isPFJet() ? obj.electronMultiplicity() : -1);
  photonMultiplicity_.emplace_back(obj.isPFJet() ? obj.photonMultiplicity() : -1);
  muonMultiplicity_.emplace_back(obj.isPFJet() ? obj.muonMultiplicity() : -1);
}
