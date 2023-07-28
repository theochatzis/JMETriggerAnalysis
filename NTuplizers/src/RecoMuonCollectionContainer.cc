#include <JMETriggerAnalysis/NTuplizers/interface/RecoMuonCollectionContainer.h>

RecoMuonCollectionContainer::RecoMuonCollectionContainer(const std::string& name,
                                                       const std::string& inputTagLabel,
                                                       const edm::EDGetToken& token,
                                                       const std::string& strCut,
                                                       const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoMuonCollectionContainer::clear() {
  pdgId_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();
  vx_.clear();
  vy_.clear();
  vz_.clear();
  isTightID_.clear();
  pfIso_.clear();
  trkIso_.clear();
}

void RecoMuonCollectionContainer::reserve(const size_t vec_size) {
  pdgId_.reserve(vec_size);
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);
  vx_.reserve(vec_size);
  vy_.reserve(vec_size);
  vz_.reserve(vec_size);
  isTightID_.reserve(vec_size);
  pfIso_.reserve(vec_size);
  trkIso_.reserve(vec_size);
}

void RecoMuonCollectionContainer::emplace_back(const reco::Muon& obj) {
  pdgId_.emplace_back(obj.pdgId());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());
  vx_.emplace_back(obj.vx());
  vy_.emplace_back(obj.vy());
  vz_.emplace_back(obj.vz());
  // note: this ID doesn't contain the dxy, dz from Primary Vertex. Needs to be added.
  isTightID_.emplace_back(
  obj.isGlobalMuon() 
  && obj.isPFMuon() 
  && obj.globalTrack()->normalizedChi2() < 10. 
  && obj.globalTrack()->hitPattern().numberOfValidMuonHits() > 0 
  && obj.numberOfMatchedStations() > 1 
  && obj.innerTrack()->hitPattern().numberOfValidPixelHits() > 0
  && obj.innerTrack()->hitPattern().trackerLayersWithMeasurement() > 5
  );
  // pf isolation: works for offline muons cause at HLT is not so meaningful as the isolation is not done with PF.
  // cuts: tight: 0.15, very tight: 0.10 , super tight 0.05 -> a tight requirement is the "usual"
  pfIso_.emplace_back((obj.pfIsolationR04().sumChargedHadronPt + std::max(0., obj.pfIsolationR04().sumNeutralHadronEt + obj.pfIsolationR04().sumPhotonEt - 0.5*obj.pfIsolationR04().sumPUPt))/obj.pt());
  // track isolation: isolation using only the PV tracks (closer to HLT logic)
  // cuts: loose: 0.10 , tight: 0.05
  trkIso_.emplace_back(obj.isolationR03().sumPt/obj.pt()); 
}
