#ifndef JMETriggerAnalysis_PATJetCollectionContainer_h
#define JMETriggerAnalysis_PATJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/Jet.h>

class PATJetCollectionContainer : public VRecoCandidateCollectionContainer<pat::Jet> {
public:
  explicit PATJetCollectionContainer(const std::string&,
                                     const std::string&,
                                     const edm::EDGetToken&,
                                     const std::string& strCut = "",
                                     const bool orderByHighestPt = false);
  ~PATJetCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const pat::Jet&) override;
  
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }

  std::vector<float>& vec_jesc() { return jesc_; }
  std::vector<float>& vec_jetArea() { return jetArea_; }
  std::vector<uint>& vec_numberOfDaughters() { return numberOfDaughters_; }

  std::vector<float>& vec_chargedHadronEnergyFraction() { return chargedHadronEnergyFraction_; }
  std::vector<float>& vec_neutralHadronEnergyFraction() { return neutralHadronEnergyFraction_; }
  std::vector<float>& vec_electronEnergyFraction() { return electronEnergyFraction_; }
  std::vector<float>& vec_photonEnergyFraction() { return photonEnergyFraction_; }
  std::vector<float>& vec_muonEnergyFraction() { return muonEnergyFraction_; }

  std::vector<int>& vec_chargedHadronMultiplicity() { return chargedHadronMultiplicity_; }
  std::vector<int>& vec_neutralHadronMultiplicity() { return neutralHadronMultiplicity_; }
  std::vector<int>& vec_electronMultiplicity() { return electronMultiplicity_; }
  std::vector<int>& vec_photonMultiplicity() { return photonMultiplicity_; }
  std::vector<int>& vec_muonMultiplicity() { return muonMultiplicity_; }
  
  std::vector<float>& vec_CandidateEnergy() { return CandidateEnergy_; }
  std::vector<float>& vec_CandidatePt() { return CandidatePt_; }
  std::vector<float>& vec_CandidateEta() { return CandidateEta_; }
  std::vector<float>& vec_CandidatePhi() { return CandidatePhi_; }
  std::vector<float>& vec_CandidateTime() { return CandidateTime_; }
  std::vector<float>& vec_CandidateTimeError() { return CandidateTimeError_; }
  std::vector<float>& vec_CandidateVx() { return CandidateVx_; }
  std::vector<float>& vec_CandidateVy() { return CandidateVy_; }
  std::vector<float>& vec_CandidateVz() { return CandidateVz_; }
  std::vector<float>& vec_CandidatePuppiWeight() {return CandidatePuppiWeight_; } // full puppi weight
  std::vector<float>& vec_CandidatePuppiWeightNoLep() {return CandidatePuppiWeightNoLep_; } // puppi weight without leptons
  
  std::vector<int>& vec_CandidateBelongsToJet() { return CandidateBelongsToJet_; }

protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;

  std::vector<float> jesc_;
  std::vector<float> jetArea_;
  std::vector<uint> numberOfDaughters_;

  std::vector<float> chargedHadronEnergyFraction_;
  std::vector<float> neutralHadronEnergyFraction_;
  std::vector<float> electronEnergyFraction_;
  std::vector<float> photonEnergyFraction_;
  std::vector<float> muonEnergyFraction_;

  std::vector<int> chargedHadronMultiplicity_;
  std::vector<int> neutralHadronMultiplicity_;
  std::vector<int> electronMultiplicity_;
  std::vector<int> photonMultiplicity_;
  std::vector<int> muonMultiplicity_;
  
  std::vector<float> CandidateEnergy_;
  std::vector<float> CandidatePt_;
  std::vector<float> CandidateEta_;
  std::vector<float> CandidatePhi_;
  std::vector<float> CandidateTime_;
  std::vector<float> CandidateTimeError_;
  std::vector<float> CandidateVx_;
  std::vector<float> CandidateVy_;
  std::vector<float> CandidateVz_;
  std::vector<float> CandidatePuppiWeight_;
  std::vector<float> CandidatePuppiWeightNoLep_;

  std::vector<int> CandidateBelongsToJet_;

  int JetIndex_;

};

#endif
