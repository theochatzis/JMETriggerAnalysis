#ifndef JMETriggerAnalysis_PATPackedGenParticleCollectionContainer_h
#define JMETriggerAnalysis_PATPackedGenParticleCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/PackedGenParticle.h>

class PATPackedGenParticleCollectionContainer : public VRecoCandidateCollectionContainer<pat::PackedGenParticle> {
public:
  explicit PATPackedGenParticleCollectionContainer(const std::string&,
                                                 const std::string&,
                                                 const edm::EDGetToken&,
                                                 const std::string& strCut = "",
                                                 const bool orderByHighestPt = false);
  ~PATPackedGenParticleCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const pat::PackedGenParticle&) override;

  std::vector<int>& vec_pdgId() { return pdgId_; }
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }
  std::vector<float>& vec_vx() { return vx_; }
  std::vector<float>& vec_vy() { return vy_; }
  std::vector<float>& vec_vz() { return vz_; }

protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
};

#endif
