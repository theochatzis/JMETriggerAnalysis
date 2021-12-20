#include <JMETriggerAnalysis/NTuplizers/interface/RecoMETCollectionContainer.h>

RecoMETCollectionContainer::RecoMETCollectionContainer(const std::string& name,
                                                       const std::string& inputTagLabel,
                                                       const edm::EDGetToken& token,
                                                       const std::string& strCut,
                                                       const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoMETCollectionContainer::clear() {
  pt_.clear();
  phi_.clear();
  sumEt_.clear();
}

void RecoMETCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  phi_.reserve(vec_size);
  sumEt_.reserve(vec_size);
}

void RecoMETCollectionContainer::emplace_back(const reco::MET& obj) {
  pt_.emplace_back(obj.pt());
  phi_.emplace_back(obj.phi());
  sumEt_.emplace_back(obj.sumEt());
}
