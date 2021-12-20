#include <JMETriggerAnalysis/NTuplizers/interface/RecoGenMETCollectionContainer.h>

RecoGenMETCollectionContainer::RecoGenMETCollectionContainer(const std::string& name,
                                                             const std::string& inputTagLabel,
                                                             const edm::EDGetToken& token,
                                                             const std::string& strCut,
                                                             const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoGenMETCollectionContainer::clear() {
  pt_.clear();
  phi_.clear();
  sumEt_.clear();
  NeutralEMEtFraction_.clear();
  NeutralHadEtFraction_.clear();
  ChargedEMEtFraction_.clear();
  ChargedHadEtFraction_.clear();
  MuonEtFraction_.clear();
  InvisibleEtFraction_.clear();
}

void RecoGenMETCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  phi_.reserve(vec_size);
  sumEt_.reserve(vec_size);
  NeutralEMEtFraction_.reserve(vec_size);
  NeutralHadEtFraction_.reserve(vec_size);
  ChargedEMEtFraction_.reserve(vec_size);
  ChargedHadEtFraction_.reserve(vec_size);
  MuonEtFraction_.reserve(vec_size);
  InvisibleEtFraction_.reserve(vec_size);
}

void RecoGenMETCollectionContainer::emplace_back(const reco::GenMET& obj) {
  pt_.emplace_back(obj.pt());
  phi_.emplace_back(obj.phi());
  sumEt_.emplace_back(obj.sumEt());
  NeutralEMEtFraction_.emplace_back(obj.NeutralEMEtFraction());
  NeutralHadEtFraction_.emplace_back(obj.NeutralHadEtFraction());
  ChargedEMEtFraction_.emplace_back(obj.ChargedEMEtFraction());
  ChargedHadEtFraction_.emplace_back(obj.ChargedHadEtFraction());
  MuonEtFraction_.emplace_back(obj.MuonEtFraction());
  InvisibleEtFraction_.emplace_back(obj.InvisibleEtFraction());
}
