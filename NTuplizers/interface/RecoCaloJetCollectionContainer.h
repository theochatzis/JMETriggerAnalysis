#ifndef JMETriggerAnalysis_RecoCaloJetCollectionContainer_h
#define JMETriggerAnalysis_RecoCaloJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/JetReco/interface/CaloJet.h>

class RecoCaloJetCollectionContainer : public VRecoCandidateCollectionContainer<reco::CaloJet> {
public:
  explicit RecoCaloJetCollectionContainer(const std::string&,
                                          const std::string&,
                                          const edm::EDGetToken&,
                                          const std::string& strCut = "",
                                          const bool orderByHighestPt = false);
  ~RecoCaloJetCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::CaloJet&) override;

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }

  std::vector<uint>& vec_numberOfDaughters() { return numberOfDaughters_; }

protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;

  std::vector<uint> numberOfDaughters_;
};

#endif
