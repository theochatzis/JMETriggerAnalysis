#include <JMETriggerAnalysis/NTuplizers/interface/PATJetCollectionContainer.h>
#include <DataFormats/PatCandidates/interface/PackedCandidate.h>
#include <DataFormats/TrackReco/interface/Track.h>

PATJetCollectionContainer::PATJetCollectionContainer(const std::string& name,
                                                     const std::string& inputTagLabel,
                                                     const edm::EDGetToken& token,
                                                     const std::string& strCut,
                                                     const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void PATJetCollectionContainer::clear() {
  energy_.clear();
  pt_.clear();
  eta_.clear();
  phi_.clear();
  mass_.clear();

  jesc_.clear();
  jetArea_.clear();
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

  CandidateEnergy_.clear();
  CandidatePt_.clear();
  CandidateEta_.clear();
  CandidatePhi_.clear();
  CandidateCharge_.clear();
  CandidateTime_.clear();
  CandidateTimeError_.clear();
  CandidateDtime_.clear();
  CandidateDz_.clear();
  CandidateVx_.clear();
  CandidateVy_.clear();
  CandidateVz_.clear();
  CandidatePuppiWeight_.clear();
  CandidatePuppiWeightNoLep_.clear();

  CandidateBelongsToJet_.clear();

  JetIndex_ = 0;
}

void PATJetCollectionContainer::reserve(const size_t vec_size) {
  energy_.reserve(vec_size);
  pt_.reserve(vec_size);
  eta_.reserve(vec_size);
  phi_.reserve(vec_size);
  mass_.reserve(vec_size);

  jesc_.reserve(vec_size);
  jetArea_.reserve(vec_size);
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

void PATJetCollectionContainer::emplace_back(const pat::Jet& obj) {
  energy_.emplace_back(obj.energy());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  jesc_.emplace_back(obj.jecFactor(0) ? (1. / obj.jecFactor(0)) : 1.);
  jetArea_.emplace_back(obj.jetArea());
  numberOfDaughters_.emplace_back(obj.numberOfDaughters());

  chargedHadronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.chargedHadronEnergyFraction() : -99.);
  neutralHadronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.neutralHadronEnergyFraction() : -99.);
  electronEnergyFraction_.emplace_back(obj.isPFJet() ? obj.electronEnergyFraction() : -99.);
  photonEnergyFraction_.emplace_back(obj.isPFJet() ? obj.photonEnergyFraction() : -99.);
  muonEnergyFraction_.emplace_back(obj.isPFJet() ? obj.muonEnergyFraction() : -99.);

  chargedHadronMultiplicity_.emplace_back(obj.isPFJet() ? obj.chargedHadronMultiplicity() : -1);
  neutralHadronMultiplicity_.emplace_back(obj.isPFJet() ? obj.neutralHadronMultiplicity() : -1);
  electronMultiplicity_.emplace_back(obj.isPFJet() ? obj.electronMultiplicity() : -1);
  photonMultiplicity_.emplace_back(obj.isPFJet() ? obj.photonMultiplicity() : -1);
  muonMultiplicity_.emplace_back(obj.isPFJet() ? obj.muonMultiplicity() : -1);
  
  // get info for candidates of jet
  for(unsigned int iCandidate=0; iCandidate < obj.numberOfDaughters(); iCandidate++){
    // jet daughters are reco::Candidate so use dynamic cast to change to "daughter class" pat::PackedCandidate
    // pat::PackedCandidate objects have the time(),timeError() attributes
    const pat::PackedCandidate *JetCand = dynamic_cast<const pat::PackedCandidate*>(obj.daughter(iCandidate)); 
    CandidateEnergy_.emplace_back((JetCand->p4()).energy());
    CandidatePt_.emplace_back((JetCand->p4()).pt());
    CandidateEta_.emplace_back((JetCand->p4()).eta());
    CandidatePhi_.emplace_back((JetCand->p4()).phi());
    CandidateCharge_.emplace_back(JetCand->charge());
    CandidateTime_.emplace_back(JetCand->time());
    CandidateTimeError_.emplace_back(JetCand->timeError());
    CandidateDtime_.emplace_back(JetCand->dtime());
    CandidateDz_.emplace_back(JetCand->dz());
    CandidateVx_.emplace_back(JetCand->vx());
    CandidateVy_.emplace_back(JetCand->vy());
    CandidateVz_.emplace_back(JetCand->vz());
    CandidatePuppiWeight_.emplace_back(JetCand->puppiWeight());
    CandidatePuppiWeightNoLep_.emplace_back(JetCand->puppiWeightNoLep());
    CandidateBelongsToJet_.emplace_back(JetIndex_);
  } // loop over jet daughter particles
  
  // easy alternative from track
  // get track of particle
  //auto candidateTrk = (obj.daughter(iCandidate))->bestTrack();
  //if(candidateTrk){// if particle has track only
  //  std::cout << candidateTrk->t0()<< std::endl; // time value
  //  std::cout << candidateTrk->covt0t0()<< std::endl; // time error
  //}
  
  JetIndex_+=1;

}
