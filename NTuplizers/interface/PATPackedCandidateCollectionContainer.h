#ifndef JMETriggerAnalysis_PATPackedCandidateCollectionContainer_h
#define JMETriggerAnalysis_PATPackedCandidateCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/PackedCandidate.h>

class PATPackedCandidateCollectionContainer : public VRecoCandidateCollectionContainer<pat::PackedCandidate> {
public:
  explicit PATPackedCandidateCollectionContainer(const std::string&,
                                                 const std::string&,
                                                 const edm::EDGetToken&,
                                                 const std::string& strCut = "",
                                                 const bool orderByHighestPt = false);
  ~PATPackedCandidateCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const pat::PackedCandidate&) override;

  std::vector<int>& vec_pdgId() { return pdgId_; }
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }
  std::vector<float>& vec_vx() { return vx_; }
  std::vector<float>& vec_vy() { return vy_; }
  std::vector<float>& vec_vz() { return vz_; }
  std::vector<int>& vec_fromPV() { return fromPV_; }
  std::vector<float>& vec_time() { return time_; }
  std::vector<float>& vec_timeError() { return timeError_; }

protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
  std::vector<int> fromPV_;
  std::vector<float> time_;
  std::vector<float> timeError_;
};

#endif
