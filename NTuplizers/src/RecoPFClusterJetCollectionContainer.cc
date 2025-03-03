#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFClusterJetCollectionContainer.h>

RecoPFClusterJetCollectionContainer::RecoPFClusterJetCollectionContainer(const std::string& name,
                                                                         const std::string& inputTagLabel,
                                                                         const edm::EDGetToken& token,
                                                                         const std::string& strCut,
                                                                         const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPFClusterJetCollectionContainer::clear() {
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();

  numberOfDaughters_.clear();
}

void RecoPFClusterJetCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  numberOfDaughters_.reserve(vec_size);
}

void RecoPFClusterJetCollectionContainer::emplace_back(const reco::PFClusterJet& obj) {
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  numberOfDaughters_.emplace_back(obj.numberOfDaughters());
}
