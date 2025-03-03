#ifndef JMETriggerAnalysis_PATMETCollectionContainer_h
#define JMETriggerAnalysis_PATMETCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/MET.h>

class PATMETCollectionContainer : public VRecoCandidateCollectionContainer<pat::MET> {
public:
  explicit PATMETCollectionContainer(const std::string&,
                                     const std::string&,
                                     const edm::EDGetToken&,
                                     const std::string& strCut = "",
                                     const bool orderByHighestPt = false);
  ~PATMETCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const pat::MET&) override;

  std::vector<float>& vec_Raw_pt() { return Raw_pt_; }
  std::vector<float>& vec_Raw_phi() { return Raw_phi_; }
  std::vector<float>& vec_Raw_sumEt() { return Raw_sumEt_; }
  std::vector<float>& vec_Type1_pt() { return Type1_pt_; }
  std::vector<float>& vec_Type1_phi() { return Type1_phi_; }
  std::vector<float>& vec_Type1_sumEt() { return Type1_sumEt_; }
  std::vector<float>& vec_Type1XY_pt() { return Type1XY_pt_; }
  std::vector<float>& vec_Type1XY_phi() { return Type1XY_phi_; }
  std::vector<float>& vec_Type1XY_sumEt() { return Type1XY_sumEt_; }
  std::vector<float>& vec_NeutralEMFraction() { return NeutralEMFraction_; }
  std::vector<float>& vec_NeutralHadEtFraction() { return NeutralHadEtFraction_; }
  std::vector<float>& vec_ChargedEMEtFraction() { return ChargedEMEtFraction_; }
  std::vector<float>& vec_ChargedHadEtFraction() { return ChargedHadEtFraction_; }
  std::vector<float>& vec_MuonEtFraction() { return MuonEtFraction_; }
  std::vector<float>& vec_Type6EtFraction() { return Type6EtFraction_; }
  std::vector<float>& vec_Type7EtFraction() { return Type7EtFraction_; }

protected:
  std::vector<float> Raw_pt_;
  std::vector<float> Raw_phi_;
  std::vector<float> Raw_sumEt_;
  std::vector<float> Type1_pt_;
  std::vector<float> Type1_phi_;
  std::vector<float> Type1_sumEt_;
  std::vector<float> Type1XY_pt_;
  std::vector<float> Type1XY_phi_;
  std::vector<float> Type1XY_sumEt_;
  std::vector<float> NeutralEMFraction_;
  std::vector<float> NeutralHadEtFraction_;
  std::vector<float> ChargedEMEtFraction_;
  std::vector<float> ChargedHadEtFraction_;
  std::vector<float> MuonEtFraction_;
  std::vector<float> Type6EtFraction_;
  std::vector<float> Type7EtFraction_;
};

#endif
