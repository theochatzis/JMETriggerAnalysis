#include <JMETriggerAnalysis/NTuplizers/interface/PATElectronCollectionContainer.h>

PATElectronCollectionContainer::PATElectronCollectionContainer(const std::string& name,
                                                               const std::string& inputTagLabel,
                                                               const edm::EDGetToken& token,
                                                               const std::string& strCut,
                                                               const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void PATElectronCollectionContainer::clear() {
  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
  dxyPV_.clear();
  dzPV_.clear();
  id_.clear();
  pfIso_.clear();
  etaSC_.clear();
}

void PATElectronCollectionContainer::reserve(const size_t vec_size) {
  pdgId_.reserve(vec_size);
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  vx_.reserve(vec_size);
  vy_.reserve(vec_size);
  vz_.reserve(vec_size);
  dxyPV_.reserve(vec_size);
  dzPV_.reserve(vec_size);
  id_.reserve(vec_size);
  pfIso_.reserve(vec_size);
  etaSC_.reserve(vec_size);
}

void PATElectronCollectionContainer::emplace_back(const pat::Electron& obj) {
  pdgId_.emplace_back(obj.pdgId());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());
  vx_.emplace_back(obj.vx());
  vy_.emplace_back(obj.vy());
  vz_.emplace_back(obj.vz());

  dxyPV_.emplace_back(obj.hasUserFloat("dxyPV") ? obj.userFloat("dxyPV") : -9999.);
  dzPV_.emplace_back(obj.hasUserFloat("dzPV") ? obj.userFloat("dzPV") : -9999.);

  uint obj_id(0);
  if (obj.hasUserInt("IDCutBasedVeto") && (obj.userInt("IDCutBasedVeto") > 0)) {
    obj_id |= (1u << 0);
  }
  if (obj.hasUserInt("IDCutBasedLoose") && (obj.userInt("IDCutBasedLoose") > 0)) {
    obj_id |= (1u << 1);
  }
  if (obj.hasUserInt("IDCutBasedMedium") && (obj.userInt("IDCutBasedMedium") > 0)) {
    obj_id |= (1u << 2);
  }
  if (obj.hasUserInt("IDCutBasedTight") && (obj.userInt("IDCutBasedTight") > 0)) {
    obj_id |= (1u << 3);
  }
  if (obj.hasUserInt("IDMVAIsoWP80") && (obj.userInt("IDMVAIsoWP80") > 0)) {
    obj_id |= (1u << 4);
  }
  if (obj.hasUserInt("IDMVAIsoWP90") && (obj.userInt("IDMVAIsoWP90") > 0)) {
    obj_id |= (1u << 5);
  }
  id_.emplace_back(obj_id);

  pfIso_.emplace_back(obj.hasUserFloat("pfIso") ? obj.userFloat("pfIso") : -9999.);

  etaSC_.emplace_back(obj.superCluster()->eta());
}
