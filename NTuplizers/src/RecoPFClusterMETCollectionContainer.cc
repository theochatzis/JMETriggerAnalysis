#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFClusterMETCollectionContainer.h>

RecoPFClusterMETCollectionContainer::RecoPFClusterMETCollectionContainer(const std::string& name,
                                                                         const std::string& inputTagLabel,
                                                                         const edm::EDGetToken& token,
                                                                         const std::string& strCut,
                                                                         const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPFClusterMETCollectionContainer::clear() {
  pt_.clear();
  phi_.clear();
  sumEt_.clear();
}

void RecoPFClusterMETCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  phi_.reserve(vec_size);
  sumEt_.reserve(vec_size);
}

void RecoPFClusterMETCollectionContainer::emplace_back(const reco::PFClusterMET& obj) {
  pt_.emplace_back(obj.pt());
  phi_.emplace_back(obj.phi());
  sumEt_.emplace_back(obj.sumEt());
}
