#ifndef JMETriggerAnalysis_L1TPFJetCollectionContainer_h
#define JMETriggerAnalysis_L1TPFJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/L1TParticleFlow/interface/PFJet.h>

class L1TPFJetCollectionContainer : public VRecoCandidateCollectionContainer<l1t::PFJet> {
public:
  explicit L1TPFJetCollectionContainer(const std::string&,
                                       const std::string&,
                                       const edm::EDGetToken&,
                                       const std::string& strCut = "",
                                       const bool orderByHighestPt = false);
  ~L1TPFJetCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const l1t::PFJet&) override;

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }

  std::vector<float>& vec_jesc() { return jesc_; }
  std::vector<uint>& vec_numberOfDaughters() { return numberOfDaughters_; }

protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;

  std::vector<float> jesc_;
  std::vector<uint> numberOfDaughters_;
};

#endif
