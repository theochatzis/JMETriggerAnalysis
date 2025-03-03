#include <JMETriggerAnalysis/NTuplizers/interface/L1TPFCandidateCollectionContainer.h>

L1TPFCandidateCollectionContainer::L1TPFCandidateCollectionContainer(const std::string& name,
                                                                     const std::string& inputTagLabel,
                                                                     const edm::EDGetToken& token,
                                                                     const std::string& strCut,
                                                                     const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void L1TPFCandidateCollectionContainer::clear() {
  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
  puppiWeight_.clear();
}

void L1TPFCandidateCollectionContainer::reserve(const size_t vec_size) {
  pdgId_.reserve(vec_size);
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  vx_.reserve(vec_size);
  vy_.reserve(vec_size);
  vz_.reserve(vec_size);
  puppiWeight_.reserve(vec_size);
}

void L1TPFCandidateCollectionContainer::emplace_back(const l1t::PFCandidate& obj) {
  pdgId_.emplace_back(obj.pdgId());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());
  vx_.emplace_back(obj.vx());
  vy_.emplace_back(obj.vy());
  vz_.emplace_back(obj.vz());
  puppiWeight_.emplace_back(obj.vz());
}
