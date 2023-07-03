#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/ParticleFlowReco/interface/PFSimParticle.h"
#include "DataFormats/ParticleFlowReco/interface/PFSimParticleFwd.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlockElementTrack.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

#include <cassert>

#include <TFile.h>
#include <TTree.h>

class PFHadCalibNTuple : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit PFHadCalibNTuple(edm::ParameterSet const&);
  ~PFHadCalibNTuple() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  // name of module
  std::string const moduleLabel_;

  // name of TTree
  std::string const ttreeName_;

  // input EDM collections
  edm::EDGetTokenT<reco::GenParticleCollection> const genPartsToken_;
  edm::EDGetTokenT<reco::PFSimParticleCollection> const pfSimPartsToken_;
  edm::EDGetTokenT<reco::PFCandidateCollection> const recoPFCandsToken_;

  // status code of selected GEN particles
  int const genParticleStatus_;

  // PDG-ID of selected GEN particles
  int const genParticlePdgId_;

  // min-DeltaR of isolated GEN particles from other GEN particles
  double const genParticleIsoMinDeltaR_;

  // min pt for charged hadrons
  double const minPt_;

  // min track-p for charged hadrons
  double const minTrackP_;

  // min track-pT for charged hadrons
  double const minTrackPt_;

  // min ecal+hcal raw energy for charged hadrons
  double const minCaloEnergy_;

  // max ecal raw energy to define a MIP
  double const maxECalEnergy_;

  // min number of pixel and pixel+strip hits for charged hadrons
  std::vector<uint> const minPixelHits_;
  std::vector<uint> const minTrackerHits_;
  std::vector<double> const maxEtaForMinTrkHitsCuts_;

  // use PFBlockElements to count tracks associated to reco::PFCandidate
  bool const usePFBlockElements_;

  // Number of tracks after cuts
  std::vector<uint> globalCounter_;

  TTree* ttree_ = nullptr;

  std::vector<float> true_energy_;
  std::vector<float> true_eta_;
  std::vector<float> true_phi_;
  std::vector<float> true_dr_;
  std::vector<int> true_charge_;
  std::vector<float> pfc_ecal_;
  std::vector<float> pfc_hcal_;
  std::vector<float> pfc_eta_;
  std::vector<float> pfc_phi_;
  std::vector<int> pfc_charge_;
  std::vector<float> pfc_id_;
  std::vector<float> pfc_trackRef_p_;
  std::vector<float> pfc_trackRef_pt_;
  std::vector<float> pfc_trackRef_eta_;
  std::vector<float> pfc_trackRef_phi_;
  std::vector<uint> pfc_trackRef_nValidPixelHits_;
  std::vector<uint> pfc_trackRef_nValidTrackerHits_;

  void reset_variables();
};

PFHadCalibNTuple::PFHadCalibNTuple(const edm::ParameterSet& iConfig)
    : moduleLabel_(iConfig.getParameter<std::string>("@module_label")),
      ttreeName_(iConfig.getParameter<std::string>("TTreeName")),
      genPartsToken_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("genParticles"))),
      pfSimPartsToken_(consumes<reco::PFSimParticleCollection>(iConfig.getParameter<edm::InputTag>("pfSimParticles"))),
      recoPFCandsToken_(consumes<reco::PFCandidateCollection>(iConfig.getParameter<edm::InputTag>("recoPFCandidates"))),
      genParticleStatus_(iConfig.getParameter<int>("genParticleStatus")),
      genParticlePdgId_(iConfig.getParameter<int>("genParticlePdgId")),
      genParticleIsoMinDeltaR_(iConfig.getParameter<double>("genParticleIsoMinDeltaR")),
      minPt_(iConfig.getParameter<double>("minPt")),
      minTrackP_(iConfig.getParameter<double>("minTrackP")),
      minTrackPt_(iConfig.getParameter<double>("minTrackPt")),
      minCaloEnergy_(iConfig.getParameter<double>("minCaloEnergy")),
      maxECalEnergy_(iConfig.getParameter<double>("maxECalEnergy")),
      minPixelHits_(iConfig.getParameter<std::vector<uint>>("minPixelHits")),
      minTrackerHits_(iConfig.getParameter<std::vector<uint>>("minTrackerHits")),
      maxEtaForMinTrkHitsCuts_(iConfig.getParameter<std::vector<double>>("maxEtaForMinTrkHitsCuts")),
      usePFBlockElements_(iConfig.getParameter<bool>("usePFBlockElements")) {
  assert(minPixelHits_.size() == minTrackerHits_.size());
  assert(minPixelHits_.size() == maxEtaForMinTrkHitsCuts_.size());
  for (uint idx = 0; 1 + idx < maxEtaForMinTrkHitsCuts_.size(); ++idx) {
    assert(maxEtaForMinTrkHitsCuts_[idx] < maxEtaForMinTrkHitsCuts_[idx + 1]);
  }

  globalCounter_ = std::vector<uint>(13, 0);

  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fs->make<TTree>(ttreeName_.c_str(), ttreeName_.c_str());

  if (not ttree_) {
    throw edm::Exception(edm::errors::Configuration, "failed to create TTree via TFileService::make<TTree>");
  }

  ttree_->Branch("true_energy", &true_energy_);
  ttree_->Branch("true_eta", &true_eta_);
  ttree_->Branch("true_phi", &true_phi_);
  ttree_->Branch("true_dr", &true_dr_);
  ttree_->Branch("true_charge", &true_charge_);
  ttree_->Branch("pfc_ecal", &pfc_ecal_);
  ttree_->Branch("pfc_hcal", &pfc_hcal_);
  ttree_->Branch("pfc_eta", &pfc_eta_);
  ttree_->Branch("pfc_phi", &pfc_phi_);
  ttree_->Branch("pfc_charge", &pfc_charge_);
  ttree_->Branch("pfc_id", &pfc_id_);
  ttree_->Branch("pfc_trackRef_p", &pfc_trackRef_p_);
  ttree_->Branch("pfc_trackRef_pt", &pfc_trackRef_pt_);
  ttree_->Branch("pfc_trackRef_eta", &pfc_trackRef_eta_);
  ttree_->Branch("pfc_trackRef_phi", &pfc_trackRef_phi_);
  ttree_->Branch("pfc_trackRef_nValidPixelHits", &pfc_trackRef_nValidPixelHits_);
  ttree_->Branch("pfc_trackRef_nValidTrackerHits", &pfc_trackRef_nValidTrackerHits_);
}

PFHadCalibNTuple::~PFHadCalibNTuple() {
  edm::LogPrint("") << "----------------------------------------------------------";
  edm::LogPrint("") << moduleLabel_;
  edm::LogPrint("") << "----------------------------------------------------------";
  edm::LogPrint("") << "Total number of events: " << globalCounter_[0];
  edm::LogPrint("") << "Number of GEN isolated pions: " << globalCounter_[1];
  edm::LogPrint("") << "Number of pfSIM particles within dR = 0.01 of an isolated GEN pion: " << globalCounter_[2];
  edm::LogPrint("") << "Number of pfSIM particles with valid extrapolation point to ECAL surface: "
                    << globalCounter_[3];
  edm::LogPrint("") << "Number of PF candidates: " << globalCounter_[4];
  edm::LogPrint("") << "Number of PF Charged Hadrons: " << globalCounter_[5];
  edm::LogPrint("") << " - with pt > " << minPt_ << " GeV: " << globalCounter_[6];
  edm::LogPrint("") << " - with E_ECAL+E_HCAL > " << minCaloEnergy_ << " GeV: " << globalCounter_[7];
  if (usePFBlockElements_)
    edm::LogPrint("") << " - with only 1 track in the block: " << globalCounter_[8];
  edm::LogPrint("") << " - with track-p > " << minTrackP_ << " GeV and track-pT > " << minTrackPt_
                    << " GeV: " << globalCounter_[9];
  edm::LogPrint("") << " - with min nb of pixel hits: " << globalCounter_[10];
  edm::LogPrint("") << " - with min nb of pixel+strip hits: " << globalCounter_[11];
  edm::LogPrint("") << " - with E_ECAL < " << maxECalEnergy_ << " GeV: " << globalCounter_[12];
}

void PFHadCalibNTuple::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& genParts = iEvent.get(genPartsToken_);
  auto const& pfSimParts = iEvent.get(pfSimPartsToken_);
  auto const& recoPFCands = iEvent.get(recoPFCandsToken_);

  reset_variables();

  ++globalCounter_[0];

  LogTrace("") << "----------------------------------------------------------";

  for (uint genpIdx_i = 0; genpIdx_i < genParts.size(); ++genpIdx_i) {
    auto const& genp_i = genParts.at(genpIdx_i);

    LogTrace("") << " genParticle[" << genpIdx_i << "]:"
                 << " pt=" << genp_i.pt() << " eta=" << genp_i.eta() << " phi=" << genp_i.phi()
                 << " pdgId=" << genp_i.pdgId() << " status=" << genp_i.status();

    // GEN and true(simPF) particle selection
    if (genp_i.status() == genParticleStatus_ and genp_i.pdgId() == genParticlePdgId_) {
      auto mindR = 999999.f;
      for (uint genpIdx_j = 0; genpIdx_j != genpIdx_i and genpIdx_j < genParts.size(); ++genpIdx_j) {
        auto const& genp_j = genParts.at(genpIdx_j);
        if (genp_j.status() == genParticleStatus_) {
          auto const dR = reco::deltaR(genp_i.eta(), genp_i.phi(), genp_j.eta(), genp_j.phi());
          if (dR < mindR)
            mindR = dR;
        }
      }

      // Isolated GEN particle
      if (mindR > genParticleIsoMinDeltaR_) {
        ++globalCounter_[1];

        for (auto const& ptc : pfSimParts) {
          // only consider negatively charged particles
          if (ptc.charge() >= 0)
            continue;

          // require true particle within deltaR = 0.01 of the gen particle
          auto const& gen = ptc.trajectoryPoint(reco::PFTrajectoryPoint::ClosestApproach);
          auto const dR = reco::deltaR(genp_i.eta(), genp_i.phi(), gen.momentum().Eta(), gen.momentum().Phi());
          if (dR > 0.01)
            continue;
          ++globalCounter_[2];

          auto const& tpatecal = ptc.extrapolatedPoint(reco::PFTrajectoryPoint::ECALEntrance);
          if (not tpatecal.isValid())
            continue;

          auto const eta = tpatecal.positionREP().Eta();
          auto const phi = tpatecal.positionREP().Phi();
          auto const trueE = std::sqrt(tpatecal.momentum().Vect().Mag2());
          auto const true_dr = reco::deltaR(gen.momentum().Eta(), gen.momentum().Phi(), eta, phi);

          ++globalCounter_[3];

          true_energy_.emplace_back(trueE);
          true_eta_.emplace_back(eta);
          true_phi_.emplace_back(phi);
          true_dr_.emplace_back(true_dr);
          true_charge_.emplace_back(ptc.charge());
        }
      }
    }
  }

  LogTrace("") << "----------------------------------------------------------";

  // Reco pion(pi-) selection
  for (auto const& pfc : recoPFCands) {
    ++globalCounter_[4];

    if (pfc.particleId() != 1)
      continue;
    ++globalCounter_[5];

    auto const ecalRaw = pfc.rawEcalEnergy();
    auto const hcalRaw = pfc.rawHcalEnergy();
    if ((ecalRaw + hcalRaw) < minCaloEnergy_)
      continue;
    ++globalCounter_[7];

    auto nTracks = 0u;
    auto const& theElements = pfc.elementsInBlocks();
    if (theElements.empty()) {
      if (not usePFBlockElements_)
        nTracks = 1;  //!! hack for pfTICL (ref: https://github.com/cms-sw/cmssw/pull/32202)
    } else {
      auto const& elements = theElements[0].first->elements();
      for (unsigned iEle = 0; iEle < elements.size(); ++iEle) {
        if (elements[iEle].type() == reco::PFBlockElement::TRACK) {
          ++nTracks;
        }
      }
    }

    auto trackRef = pfc.trackRef();

    auto const track_p = trackRef->p();
    auto const track_pt = trackRef->pt();
    auto const track_eta = trackRef->eta();
    auto const track_phi = trackRef->phi();

    auto const& hp = trackRef->hitPattern();
    uint const track_nValidPixelHits = hp.numberOfValidPixelHits();
    uint const track_nValidTrackerHits = trackRef->numberOfValidHits();

    LogTrace("") << "----------------------------------------------------------";
    LogTrace("") << moduleLabel_ << " trackRef:";
    LogTrace("") << "     pt=" << trackRef->pt();
    LogTrace("") << "     eta=" << trackRef->eta();
    LogTrace("") << "     phi=" << trackRef->phi();
    LogTrace("") << "     algo=" << trackRef->algo();
    LogTrace("") << "     numberOfValidStripTOBHits=" << hp.numberOfValidStripTOBHits();
    LogTrace("") << "     numberOfValidStripTECHits=" << hp.numberOfValidStripTECHits();
    LogTrace("") << "     numberOfValidStripTIBHits=" << hp.numberOfValidStripTIBHits();
    LogTrace("") << "     numberOfValidStripTIDHits=" << hp.numberOfValidStripTIDHits();
    LogTrace("") << "     numberOfValidPixelBarrelHits=" << hp.numberOfValidPixelBarrelHits();
    LogTrace("") << "     numberOfValidPixelEndcapHits=" << hp.numberOfValidPixelEndcapHits();
    LogTrace("") << "     numberOfValidPixelHits=" << hp.numberOfValidPixelHits();
    LogTrace("") << "     numberOfValidStripHits=" << hp.numberOfValidStripHits();
    LogTrace("") << "     numberOfValidHits=" << trackRef->numberOfValidHits();
    LogTrace("") << "     numberOfLostHits=" << trackRef->numberOfLostHits();
    LogTrace("") << "----------------------------------------------------------";

    if (pfc.pt() < minPt_)
      continue;
    ++globalCounter_[6];
    if (nTracks != 1)
      continue;
    ++globalCounter_[8];
    if (track_p < minTrackP_ or track_pt < minTrackPt_)
      continue;
    ++globalCounter_[9];


    auto hasMinPixelHits = false;
    auto hasMinTrackerHits = false;
    for (uint ieta = 0; ieta < maxEtaForMinTrkHitsCuts_.size(); ++ieta) {
      auto const etaMin = ieta ? maxEtaForMinTrkHitsCuts_[ieta - 1] : 0.;
      auto const etaMax = maxEtaForMinTrkHitsCuts_[ieta];

      if (std::abs(track_eta) >= etaMin and std::abs(track_eta) < etaMax) {
        hasMinPixelHits = track_nValidPixelHits >= minPixelHits_[ieta];
        hasMinTrackerHits = track_nValidTrackerHits >= minTrackerHits_[ieta];
        break;
      }
    }

    if (not hasMinPixelHits)
      continue;
    ++globalCounter_[10];

    if (not hasMinTrackerHits)
      continue;
    ++globalCounter_[11];

    if (ecalRaw > maxECalEnergy_)
      continue;
    ++globalCounter_[12];

    pfc_ecal_.emplace_back(ecalRaw);
    pfc_hcal_.emplace_back(hcalRaw);
    pfc_eta_.emplace_back(pfc.eta());
    pfc_phi_.emplace_back(pfc.phi());
    pfc_charge_.emplace_back(pfc.charge());
    pfc_id_.emplace_back(pfc.particleId());
    pfc_trackRef_p_.emplace_back(track_p);
    pfc_trackRef_pt_.emplace_back(track_pt);
    pfc_trackRef_eta_.emplace_back(track_eta);
    pfc_trackRef_phi_.emplace_back(track_phi);
    pfc_trackRef_nValidPixelHits_.emplace_back(track_nValidPixelHits);
    pfc_trackRef_nValidTrackerHits_.emplace_back(track_nValidTrackerHits);
  }

  ttree_->Fill();
}

void PFHadCalibNTuple::reset_variables() {
  true_energy_.clear();
  true_eta_.clear();
  true_phi_.clear();
  true_dr_.clear();
  true_charge_.clear();
  pfc_ecal_.clear();
  pfc_hcal_.clear();
  pfc_eta_.clear();
  pfc_phi_.clear();
  pfc_charge_.clear();
  pfc_id_.clear();
  pfc_trackRef_p_.clear();
  pfc_trackRef_pt_.clear();
  pfc_trackRef_eta_.clear();
  pfc_trackRef_phi_.clear();
  pfc_trackRef_nValidPixelHits_.clear();
  pfc_trackRef_nValidTrackerHits_.clear();
}

void PFHadCalibNTuple::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

DEFINE_FWK_MODULE(PFHadCalibNTuple);
