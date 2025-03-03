#include <JMETriggerAnalysis/NTuplizers/interface/PATMETCollectionContainer.h>

PATMETCollectionContainer::PATMETCollectionContainer(const std::string& name,
                                                     const std::string& inputTagLabel,
                                                     const edm::EDGetToken& token,
                                                     const std::string& strCut,
                                                     const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void PATMETCollectionContainer::clear() {
  Raw_pt_.clear();
  Raw_phi_.clear();
  Raw_sumEt_.clear();
  Type1_pt_.clear();
  Type1_phi_.clear();
  Type1_sumEt_.clear();
  Type1XY_pt_.clear();
  Type1XY_phi_.clear();
  Type1XY_sumEt_.clear();
  NeutralEMFraction_.clear();
  NeutralHadEtFraction_.clear();
  ChargedEMEtFraction_.clear();
  ChargedHadEtFraction_.clear();
  MuonEtFraction_.clear();
  Type6EtFraction_.clear();
  Type7EtFraction_.clear();
}

void PATMETCollectionContainer::reserve(const size_t vec_size) {
  Raw_pt_.reserve(vec_size);
  Raw_phi_.reserve(vec_size);
  Raw_sumEt_.reserve(vec_size);
  Type1_pt_.reserve(vec_size);
  Type1_phi_.reserve(vec_size);
  Type1_sumEt_.reserve(vec_size);
  Type1XY_pt_.reserve(vec_size);
  Type1XY_phi_.reserve(vec_size);
  Type1XY_sumEt_.reserve(vec_size);
  NeutralEMFraction_.reserve(vec_size);
  NeutralHadEtFraction_.reserve(vec_size);
  ChargedEMEtFraction_.reserve(vec_size);
  ChargedHadEtFraction_.reserve(vec_size);
  MuonEtFraction_.reserve(vec_size);
  Type6EtFraction_.reserve(vec_size);
  Type7EtFraction_.reserve(vec_size);
}

void PATMETCollectionContainer::emplace_back(const pat::MET& obj) {
  Raw_pt_.emplace_back(obj.shiftedPt(pat::MET::NoShift, pat::MET::Raw));
  Raw_phi_.emplace_back(obj.shiftedPhi(pat::MET::NoShift, pat::MET::Raw));
  Raw_sumEt_.emplace_back(obj.shiftedSumEt(pat::MET::NoShift, pat::MET::Raw));
  Type1_pt_.emplace_back(obj.shiftedPt(pat::MET::NoShift, pat::MET::Type1));
  Type1_phi_.emplace_back(obj.shiftedPhi(pat::MET::NoShift, pat::MET::Type1));
  Type1_sumEt_.emplace_back(obj.shiftedSumEt(pat::MET::NoShift, pat::MET::Type1));
  Type1XY_pt_.emplace_back(obj.shiftedPt(pat::MET::NoShift, pat::MET::Type1XY));
  Type1XY_phi_.emplace_back(obj.shiftedPhi(pat::MET::NoShift, pat::MET::Type1XY));
  Type1XY_sumEt_.emplace_back(obj.shiftedSumEt(pat::MET::NoShift, pat::MET::Type1XY));
  NeutralEMFraction_.emplace_back(obj.NeutralEMFraction());
  NeutralHadEtFraction_.emplace_back(obj.NeutralHadEtFraction());
  ChargedEMEtFraction_.emplace_back(obj.ChargedEMEtFraction());
  ChargedHadEtFraction_.emplace_back(obj.ChargedHadEtFraction());
  MuonEtFraction_.emplace_back(obj.MuonEtFraction());
  Type6EtFraction_.emplace_back(obj.Type6EtFraction());
  Type7EtFraction_.emplace_back(obj.Type7EtFraction());
}
