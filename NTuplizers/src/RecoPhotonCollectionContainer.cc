#include <JMETriggerAnalysis/NTuplizers/interface/RecoPhotonCollectionContainer.h>

RecoPhotonCollectionContainer::RecoPhotonCollectionContainer(const std::string& name,
                                                           const std::string& inputTagLabel,
                                                           const edm::EDGetToken& token,
                                                           const std::string& strCut,
                                                           const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPhotonCollectionContainer::clear() {
  pt_.clear();
  eta_.clear();
  phi_.clear();
  m_.clear();

  r9_.clear();
  sigmaIetaIeta_.clear();
  hOverE_.clear();
}

void RecoPhotonCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  m_.reserve(vec_size);

  r9_.reserve(vec_size);
  sigmaIetaIeta_.reserve(vec_size);
  hOverE_.reserve(vec_size);
}

void RecoPhotonCollectionContainer::emplace_back(const reco::Photon& obj) {
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  m_.emplace_back(obj.mass());

  r9_.emplace_back(obj.r9());
  sigmaIetaIeta_.emplace_back(obj.sigmaIetaIeta());
  hOverE_.emplace_back(obj.hcalOverEcal());
}
