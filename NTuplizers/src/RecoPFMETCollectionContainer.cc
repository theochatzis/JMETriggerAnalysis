#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h>

RecoPFMETCollectionContainer::RecoPFMETCollectionContainer(const std::string& name,
                                                           const std::string& inputTagLabel,
                                                           const edm::EDGetToken& token,
                                                           const std::string& strCut,
                                                           const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPFMETCollectionContainer::clear() {
  pt_.clear();
  phi_.clear();
  sumEt_.clear();
  NeutralEMFraction_.clear();
  NeutralHadEtFraction_.clear();
  ChargedEMEtFraction_.clear();
  ChargedHadEtFraction_.clear();
  MuonEtFraction_.clear();
  Type6EtFraction_.clear();
  Type7EtFraction_.clear();
}

void RecoPFMETCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  phi_.reserve(vec_size);
  sumEt_.reserve(vec_size);
  NeutralEMFraction_.reserve(vec_size);
  NeutralHadEtFraction_.reserve(vec_size);
  ChargedEMEtFraction_.reserve(vec_size);
  ChargedHadEtFraction_.reserve(vec_size);
  MuonEtFraction_.reserve(vec_size);
  Type6EtFraction_.reserve(vec_size);
  Type7EtFraction_.reserve(vec_size);
}

void RecoPFMETCollectionContainer::emplace_back(const reco::PFMET& obj) {
  pt_.emplace_back(obj.pt());
  phi_.emplace_back(obj.phi());
  sumEt_.emplace_back(obj.sumEt());
  NeutralEMFraction_.emplace_back(obj.NeutralEMFraction());
  NeutralHadEtFraction_.emplace_back(obj.NeutralHadEtFraction());
  ChargedEMEtFraction_.emplace_back(obj.ChargedEMEtFraction());
  ChargedHadEtFraction_.emplace_back(obj.ChargedHadEtFraction());
  MuonEtFraction_.emplace_back(obj.MuonEtFraction());
  Type6EtFraction_.emplace_back(obj.Type6EtFraction());
  Type7EtFraction_.emplace_back(obj.Type7EtFraction());
}
