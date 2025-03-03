#ifndef JMETriggerAnalysis_RecoGenJetCollectionContainer_h
#define JMETriggerAnalysis_RecoGenJetCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/JetReco/interface/GenJet.h>

class RecoGenJetCollectionContainer : public VRecoCandidateCollectionContainer<reco::GenJet> {
public:
  explicit RecoGenJetCollectionContainer(const std::string&,
                                         const std::string&,
                                         const edm::EDGetToken&,
                                         const std::string& strCut = "",
                                         const bool orderByHighestPt = false);
  ~RecoGenJetCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::GenJet&) override;

  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }

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

protected:
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;

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
};

#endif
