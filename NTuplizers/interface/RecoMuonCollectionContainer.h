#ifndef JMETriggerAnalysis_RecoMuonCollectionContainer_h
#define JMETriggerAnalysis_RecoMuonCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/MuonReco/interface/Muon.h>

#include <vector>

class RecoMuonCollectionContainer : public VRecoCandidateCollectionContainer<reco::Muon> {
public:
  explicit RecoMuonCollectionContainer(const std::string&,
                                      const std::string&,
                                      const edm::EDGetToken&,
                                      const std::string& strCut = "",
                                      const bool orderByHighestPt = false);
  ~RecoMuonCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::Muon&) override;

  std::vector<int>& vec_pdgId() { return pdgId_; }
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }
  std::vector<float>& vec_vx() { return vx_; }
  std::vector<float>& vec_vy() { return vy_; }
  std::vector<float>& vec_vz() { return vz_; }
  std::vector<bool>& vec_isTightID() { return isTightID_; }
  std::vector<float>& vec_pfIso() { return pfIso_; }
  std::vector<float>& vec_trkIso() { return trkIso_; }


protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
   std::vector<bool> isTightID_;
  std::vector<float> pfIso_;
  std::vector<float> trkIso_;
};

#endif
