#ifndef JMETriggerAnalysis_L1TPFCandidateCollectionContainer_h
#define JMETriggerAnalysis_L1TPFCandidateCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/L1TParticleFlow/interface/PFCandidate.h>

class L1TPFCandidateCollectionContainer : public VRecoCandidateCollectionContainer<l1t::PFCandidate> {
public:
  explicit L1TPFCandidateCollectionContainer(const std::string&,
                                             const std::string&,
                                             const edm::EDGetToken&,
                                             const std::string& strCut = "",
                                             const bool orderByHighestPt = false);
  ~L1TPFCandidateCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const l1t::PFCandidate&) override;

  std::vector<int>& vec_pdgId() { return pdgId_; }
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }
  std::vector<float>& vec_vx() { return vx_; }
  std::vector<float>& vec_vy() { return vy_; }
  std::vector<float>& vec_vz() { return vz_; }
  std::vector<float>& vec_puppiWeight() { return puppiWeight_; }

protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
  std::vector<float> puppiWeight_;
};

#endif
