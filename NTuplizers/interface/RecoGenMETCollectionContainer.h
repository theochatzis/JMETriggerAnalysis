#ifndef JMETriggerAnalysis_RecoGenMETCollectionContainer_h
#define JMETriggerAnalysis_RecoGenMETCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/METReco/interface/GenMET.h>

class RecoGenMETCollectionContainer : public VRecoCandidateCollectionContainer<reco::GenMET> {
public:
  explicit RecoGenMETCollectionContainer(const std::string&,
                                         const std::string&,
                                         const edm::EDGetToken&,
                                         const std::string& strCut = "",
                                         const bool orderByHighestPt = false);
  ~RecoGenMETCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::GenMET&) override;

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_sumEt() { return sumEt_; }
  std::vector<float>& vec_NeutralEMEtFraction() { return NeutralEMEtFraction_; }
  std::vector<float>& vec_NeutralHadEtFraction() { return NeutralHadEtFraction_; }
  std::vector<float>& vec_ChargedEMEtFraction() { return ChargedEMEtFraction_; }
  std::vector<float>& vec_ChargedHadEtFraction() { return ChargedHadEtFraction_; }
  std::vector<float>& vec_MuonEtFraction() { return MuonEtFraction_; }
  std::vector<float>& vec_InvisibleEtFraction() { return InvisibleEtFraction_; }

protected:
  std::vector<float> pt_;
  std::vector<float> phi_;
  std::vector<float> sumEt_;
  std::vector<float> NeutralEMEtFraction_;
  std::vector<float> NeutralHadEtFraction_;
  std::vector<float> ChargedEMEtFraction_;
  std::vector<float> ChargedHadEtFraction_;
  std::vector<float> MuonEtFraction_;
  std::vector<float> InvisibleEtFraction_;
};

#endif
