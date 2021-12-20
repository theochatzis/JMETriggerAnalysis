#include <JMETriggerAnalysis/NTuplizers/interface/L1TPFJetCollectionContainer.h>

L1TPFJetCollectionContainer::L1TPFJetCollectionContainer(const std::string& name,
                                                         const std::string& inputTagLabel,
                                                         const edm::EDGetToken& token,
                                                         const std::string& strCut,
                                                         const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void L1TPFJetCollectionContainer::clear() {
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();

  jesc_.clear();
  numberOfDaughters_.clear();
}

void L1TPFJetCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  jesc_.reserve(vec_size);
  numberOfDaughters_.reserve(vec_size);
  ;
}

void L1TPFJetCollectionContainer::emplace_back(const l1t::PFJet& obj) {
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  auto const jesc(obj.rawPt() ? (obj.pt() / obj.rawPt()) : 1.);

  jesc_.emplace_back(jesc);
  numberOfDaughters_.emplace_back(obj.numberOfDaughters());
}
