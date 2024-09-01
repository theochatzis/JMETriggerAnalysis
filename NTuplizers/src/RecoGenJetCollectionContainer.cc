#include <JMETriggerAnalysis/NTuplizers/interface/RecoGenJetCollectionContainer.h>
#include <DataFormats/Candidate/interface/Candidate.h>
RecoGenJetCollectionContainer::RecoGenJetCollectionContainer(const std::string& name,
                                                             const std::string& inputTagLabel,
                                                             const edm::EDGetToken& token,
                                                             const std::string& strCut,
                                                             const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoGenJetCollectionContainer::clear() {
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();

  numberOfDaughters_.clear();

  chargedHadronEnergyFraction_.clear();
  neutralHadronEnergyFraction_.clear();
  electronEnergyFraction_.clear();
  photonEnergyFraction_.clear();
  muonEnergyFraction_.clear();

  chargedHadronMultiplicity_.clear();
  neutralHadronMultiplicity_.clear();
  electronMultiplicity_.clear();
  photonMultiplicity_.clear();
  muonMultiplicity_.clear();

  CandidateVz_.clear();
  CandidatePdgId_.clear();
  CandidateMass_.clear();
}

void RecoGenJetCollectionContainer::reserve(const size_t vec_size) {
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  numberOfDaughters_.reserve(vec_size);
  ;

  chargedHadronEnergyFraction_.reserve(vec_size);
  neutralHadronEnergyFraction_.reserve(vec_size);
  electronEnergyFraction_.reserve(vec_size);
  photonEnergyFraction_.reserve(vec_size);
  muonEnergyFraction_.reserve(vec_size);

  chargedHadronMultiplicity_.reserve(vec_size);
  neutralHadronMultiplicity_.reserve(vec_size);
  electronMultiplicity_.reserve(vec_size);
  photonMultiplicity_.reserve(vec_size);
  muonMultiplicity_.reserve(vec_size);
}

void RecoGenJetCollectionContainer::emplace_back(const reco::GenJet& obj) {
  bool isBJet = false;
  
  // get info for candidates of jet
  for(unsigned int iCandidate=0; iCandidate < obj.numberOfDaughters(); iCandidate++){
    // jet daughters are reco::GenParticle so use dynamic cast to change to "daughter class" reco::Candidate
    // reco::Candidate objects
    const reco::Candidate *JetCand = dynamic_cast<const reco::Candidate*>(obj.daughter(iCandidate)); 
    
    if(abs(JetCand->pdgId())>=0){
      isBJet = true;
      CandidateVz_.emplace_back(JetCand->vz());
      CandidatePdgId_.emplace_back(JetCand->pdgId());
      if (fabs(JetCand->pdgId()) == 11 || fabs(JetCand->pdgId()) == 13){
        CandidateMass_.emplace_back(JetCand->pt()/obj.pt());
      }
    }
  } // loop over jet daughter particles

  if (isBJet){
    pt_.emplace_back(obj.pt());
    eta_.emplace_back(obj.eta());
    phi_.emplace_back(obj.phi());
    mass_.emplace_back(obj.mass());

    numberOfDaughters_.emplace_back(obj.numberOfDaughters());

    chargedHadronEnergyFraction_.emplace_back(obj.energy() ? (obj.chargedHadronEnergy() / obj.energy()) : -99.);
    neutralHadronEnergyFraction_.emplace_back(obj.energy() ? (obj.neutralHadronEnergy() / obj.energy()) : -99.);
    electronEnergyFraction_.emplace_back(obj.energy() ? (obj.chargedEmEnergy() / obj.energy()) : -99.);
    photonEnergyFraction_.emplace_back(obj.energy() ? (obj.neutralEmEnergy() / obj.energy()) : -99.);
    muonEnergyFraction_.emplace_back(obj.energy() ? (obj.muonEnergy() / obj.energy()) : -99.);

    chargedHadronMultiplicity_.emplace_back(obj.chargedHadronMultiplicity());
    neutralHadronMultiplicity_.emplace_back(obj.neutralHadronMultiplicity());
    electronMultiplicity_.emplace_back(obj.chargedEmMultiplicity());
    photonMultiplicity_.emplace_back(obj.neutralEmMultiplicity());
    muonMultiplicity_.emplace_back(obj.muonMultiplicity());
  }
}
