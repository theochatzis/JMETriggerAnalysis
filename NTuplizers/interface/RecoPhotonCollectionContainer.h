#ifndef JMETriggerAnalysis_RecoPhotonCollectionContainer_h
#define JMETriggerAnalysis_RecoPhotonCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/EgammaCandidates/interface/Photon.h>

class RecoPhotonCollectionContainer : public VRecoCandidateCollectionContainer<reco::Photon> {
public:
  explicit RecoPhotonCollectionContainer(const std::string&,
                                        const std::string&,
                                        const edm::EDGetToken&,
                                        const std::string& strCut = "",
                                        const bool orderByHighestPt = false);
  ~RecoPhotonCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::Photon&) override;

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_m() { return m_; }
  
  std::vector<float>& vec_r9() { return r9_; }
  std::vector<float>& vec_sigmaIetaIeta() { return sigmaIetaIeta_; }
  std::vector<float>& vec_hOverE() { return hOverE_; }

protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> m_;

  std::vector<float> r9_;
  std::vector<float> sigmaIetaIeta_;
  std::vector<float> hOverE_;

};

#endif
