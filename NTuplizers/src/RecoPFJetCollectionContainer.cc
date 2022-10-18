#include <JMETriggerAnalysis/NTuplizers/interface/RecoPFJetCollectionContainer.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

RecoPFJetCollectionContainer::RecoPFJetCollectionContainer(const std::string& name,
                                                           const std::string& inputTagLabel,
                                                           const edm::EDGetToken& token,
                                                           const std::string& strCut,
                                                           const bool orderByHighestPt)
    : VRecoCandidateCollectionContainer(name, inputTagLabel, token, strCut, orderByHighestPt) {}

void RecoPFJetCollectionContainer::clear() {
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
  CandidateVx_.clear();
  CandidateVy_.clear();
  CandidateVz_.clear();


  CandidateBelongsToJet_.clear();

  JetIndex_ = 0;
  //associationIndex = -10;
}

void RecoPFJetCollectionContainer::reserve(const size_t vec_size) {
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

void RecoPFJetCollectionContainer::emplace_back(const reco::PFJet& obj) {
  energy_.emplace_back(obj.energy());
  pt_.emplace_back(obj.pt());
  eta_.emplace_back(obj.eta());
  phi_.emplace_back(obj.phi());
  mass_.emplace_back(obj.mass());

  const auto totFrac = obj.chargedHadronEnergyFraction() + obj.neutralHadronEnergyFraction() +
                       obj.photonEnergyFraction() + obj.electronEnergyFraction() + obj.muonEnergyFraction() +
                       +obj.HFEMEnergyFraction();

  const auto jesc = totFrac ? (1. / totFrac) : 1.;

  jesc_.emplace_back(jesc);
  jetArea_.emplace_back(obj.jetArea());
  numberOfDaughters_.emplace_back(obj.numberOfDaughters());

  chargedHadronEnergyFraction_.emplace_back(obj.chargedHadronEnergyFraction() * jesc);
  neutralHadronEnergyFraction_.emplace_back(obj.neutralHadronEnergyFraction() * jesc);
  electronEnergyFraction_.emplace_back(obj.electronEnergyFraction() * jesc);
  photonEnergyFraction_.emplace_back(obj.photonEnergyFraction() * jesc);
  muonEnergyFraction_.emplace_back(obj.muonEnergyFraction() * jesc);

  chargedHadronMultiplicity_.emplace_back(obj.chargedHadronMultiplicity());
  neutralHadronMultiplicity_.emplace_back(obj.neutralHadronMultiplicity());
  electronMultiplicity_.emplace_back(obj.electronMultiplicity());
  photonMultiplicity_.emplace_back(obj.photonMultiplicity());
  muonMultiplicity_.emplace_back(obj.muonMultiplicity());


  // get info for candidates of jet
  for(unsigned int iCandidate=0; iCandidate < obj.numberOfDaughters(); iCandidate++){
    // jet daughters are reco::Candidate so use dynamic cast to change to "mother class" reco::PFCandidate
    // reco::PFCandidate objects have the time(),timeError() attributes
    const reco::PFCandidate *JetCand = dynamic_cast<const reco::PFCandidate*>(obj.daughter(iCandidate)); 
    CandidateEnergy_.emplace_back((JetCand->p4()).energy());
    CandidatePt_.emplace_back((JetCand->p4()).pt());
    CandidateEta_.emplace_back((JetCand->p4()).eta());
    CandidatePhi_.emplace_back((JetCand->p4()).phi());
    CandidateCharge_.emplace_back(JetCand->charge());
    CandidateTime_.emplace_back(JetCand->time());
    CandidateTimeError_.emplace_back(JetCand->timeError());
    CandidateVx_.emplace_back(JetCand->vx());
    CandidateVy_.emplace_back(JetCand->vy());
    CandidateVz_.emplace_back(JetCand->vz());
    CandidateBelongsToJet_.emplace_back(JetIndex_);

    // for each candidate find if its track was used in association or not 
    // using exactly the way it is done in Puppi
    // -> this is like the fromPV in packedPFCandidates
    // but with 2 categories 
    // 1) particles which were assigned to LV/PU with association
    // 2) particles which were unassociated
    // for neutrals the value is -10 (default)
    //associationIndex_ = -10
    //const reco::TrackRef aTrackRef = JetCand->trackRef();
    
    //if (std::abs(JetCand->charge()) > 0) {
    //  associationIndex_ = (closestVtx != nullptr) ? 1 : 0.;
    //}
  } // loop over jet daughter particles
  
  JetIndex_+=1;
}
