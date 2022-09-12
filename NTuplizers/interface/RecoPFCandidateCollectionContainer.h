#ifndef JMETriggerAnalysis_RecoPFCandidateCollectionContainer_h
#define JMETriggerAnalysis_RecoPFCandidateCollectionContainer_h

#include <JMETriggerAnalysis/NTuplizers/interface/VRecoCandidateCollectionContainer.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

class RecoPFCandidateCollectionContainer : public VRecoCandidateCollectionContainer<reco::PFCandidate> {
public:
  explicit RecoPFCandidateCollectionContainer(const std::string&,
                                              const std::string&,
                                              const edm::EDGetToken&,
                                              const std::string& strCut = "",
                                              const bool orderByHighestPt = false);
  ~RecoPFCandidateCollectionContainer() override {}

  void clear() override;
  void reserve(const size_t) override;
  void emplace_back(const reco::PFCandidate&) override;

  std::vector<int>& vec_pdgId() { return pdgId_; }
  std::vector<float>& vec_pt() { return pt_; }
  std::vector<float>& vec_eta() { return eta_; }
  std::vector<float>& vec_phi() { return phi_; }
  std::vector<float>& vec_mass() { return mass_; }
  std::vector<float>& vec_rawEcalEnergy() { return rawEcalEnergy_; }
  std::vector<float>& vec_rawHcalEnergy() { return rawHcalEnergy_; }
  std::vector<float>& vec_ecalEnergyToRaw() { return ecalEnergyToRaw_; }
  std::vector<float>& vec_hcalEnergyToRaw() { return hcalEnergyToRaw_; }
  std::vector<float>& vec_vx() { return vx_; }
  std::vector<float>& vec_vy() { return vy_; }
  std::vector<float>& vec_vz() { return vz_; }
  std::vector<float>& vec_time() { return time_; }
  std::vector<float>& vec_timeError() { return timeError_; }

protected:
  std::vector<int> pdgId_;
  std::vector<float> pt_;
  std::vector<float> eta_;
  std::vector<float> phi_;
  std::vector<float> mass_;
  std::vector<float> rawEcalEnergy_;
  std::vector<float> rawHcalEnergy_;
  std::vector<float> ecalEnergyToRaw_;
  std::vector<float> hcalEnergyToRaw_;
  std::vector<float> vx_;
  std::vector<float> vy_;
  std::vector<float> vz_;
  std::vector<float> time_;
  std::vector<float> timeError_;
};

#endif
