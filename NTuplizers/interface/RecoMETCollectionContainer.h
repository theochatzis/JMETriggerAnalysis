#ifndef JMETriggerAnalysis_RecoMETCollectionContainer_h
#define JMETriggerAnalysis_RecoMETCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/METReco/interface/MET.h>

class RecoMETCollectionContainer : public VRecoCandidateCollectionContainer<reco::MET> {
public:
  explicit RecoMETCollectionContainer(const std::string&,
                                      const std::string&,
                                      const edm::EDGetToken&,
                                      const std::string& strCut = "",
                                      const bool orderByHighestPt = false);
  ~RecoMETCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::MET&) override;

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_sumEt() { return sumEt_; }

protected:
  std::vector<float> pt_;
  std::vector<float> phi_;
  std::vector<float> sumEt_;
};

#endif
