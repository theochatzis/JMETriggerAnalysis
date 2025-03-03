#ifndef JMETriggerAnalysis_PFCandidateHistogrammer_h
#define JMETriggerAnalysis_PFCandidateHistogrammer_h

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "HLTrigger/HLTcore/interface/defaultModuleLabel.h"

#include <memory>

#include <TH1D.h>

template <typename PFCandType>
class PFCandidateHistogrammer : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit PFCandidateHistogrammer(const edm::ParameterSet &);
  static void fillDescriptions(edm::ConfigurationDescriptions &);

private:
  void analyze(const edm::Event &, const edm::EventSetup &) override;

  const edm::InputTag pfCands_tag_;
  const edm::EDGetTokenT<std::vector<PFCandType>> pfCands_token_;

  const StringCutObjectSelector<PFCandType> stringCutSelector_;

  const reco::PFCandidate dummyPFCandToUseTranslatePdgId_;

  TH1D *h_pfcand_mult_ = nullptr;
  TH1D *h_pfcand_mult_X_ = nullptr;
  TH1D *h_pfcand_mult_h_ = nullptr;
  TH1D *h_pfcand_mult_e_ = nullptr;
  TH1D *h_pfcand_mult_mu_ = nullptr;
  TH1D *h_pfcand_mult_gamma_ = nullptr;
  TH1D *h_pfcand_mult_h0_ = nullptr;
  TH1D *h_pfcand_mult_hHF_ = nullptr;
  TH1D *h_pfcand_mult_egammaHF_ = nullptr;
  TH1D *h_pfcand_particleId_ = nullptr;
  TH1D *h_pfcand_pt_ = nullptr;
  TH1D *h_pfcand_pt_2_ = nullptr;
  TH1D *h_pfcand_eta_ = nullptr;
  TH1D *h_pfcand_phi_ = nullptr;
  TH1D *h_pfcand_mass_ = nullptr;
  TH1D *h_pfcand_vx_ = nullptr;
  TH1D *h_pfcand_vy_ = nullptr;
  TH1D *h_pfcand_vz_ = nullptr;
};

template <typename PFCandType>
PFCandidateHistogrammer<PFCandType>::PFCandidateHistogrammer(const edm::ParameterSet &iConfig)
    : pfCands_tag_(iConfig.getParameter<edm::InputTag>("src")),
      pfCands_token_(consumes<std::vector<PFCandType>>(pfCands_tag_)),
      stringCutSelector_(iConfig.getParameter<std::string>("cut")) {
  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  h_pfcand_mult_ = fs->make<TH1D>("pfcand_mult", "pfcand_mult", 240, 0, 12000);
  h_pfcand_mult_X_ = fs->make<TH1D>("pfcand_mult_X", "pfcand_mult_X", 240, 0, 240);
  h_pfcand_mult_h_ = fs->make<TH1D>("pfcand_mult_h", "pfcand_mult_h", 240, 0, 7200);
  h_pfcand_mult_e_ = fs->make<TH1D>("pfcand_mult_e", "pfcand_mult_e", 240, 0, 240);
  h_pfcand_mult_mu_ = fs->make<TH1D>("pfcand_mult_mu", "pfcand_mult_mu", 240, 0, 240);
  h_pfcand_mult_gamma_ = fs->make<TH1D>("pfcand_mult_gamma", "pfcand_mult_gamma", 240, 0, 7200);
  h_pfcand_mult_h0_ = fs->make<TH1D>("pfcand_mult_h0", "pfcand_mult_h0", 240, 0, 7200);
  h_pfcand_mult_hHF_ = fs->make<TH1D>("pfcand_mult_hHF", "pfcand_mult_hHF", 240, 0, 7200);
  h_pfcand_mult_egammaHF_ = fs->make<TH1D>("pfcand_mult_egammaHF", "pfcand_mult_egammaHF", 240, 0, 7200);

  h_pfcand_particleId_ = fs->make<TH1D>("pfcand_particleId", "pfcand_particleId", 8, 0, 8);
  h_pfcand_particleId_->GetXaxis()->SetLabelSize(0.06);
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(1, "X");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(2, "h");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(3, "e");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(4, "#mu");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(5, "#gamma");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(6, "h0");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(7, "h_HF");
  h_pfcand_particleId_->GetXaxis()->SetBinLabel(8, "eg_HF");

  h_pfcand_pt_ = fs->make<TH1D>("pfcand_pt", "pfcand_pt", 600, 0, 5.);
  h_pfcand_pt_2_ = fs->make<TH1D>("pfcand_pt_2", "pfcand_pt_2", 600, 0, 600);
  h_pfcand_eta_ = fs->make<TH1D>("pfcand_eta", "pfcand_eta", 600, -5., 5.);
  h_pfcand_phi_ = fs->make<TH1D>("pfcand_phi", "pfcand_phi", 600, -3., 3.);
  h_pfcand_mass_ = fs->make<TH1D>("pfcand_mass", "pfcand_mass", 240, 0, 240.);
  h_pfcand_vx_ = fs->make<TH1D>("pfcand_vx", "pfcand_vx", 240, -0.1, 0.1);
  h_pfcand_vy_ = fs->make<TH1D>("pfcand_vy", "pfcand_vy", 240, -0.1, 0.1);
  h_pfcand_vz_ = fs->make<TH1D>("pfcand_vz", "pfcand_vz", 240, -30, 30);
}

template <typename PFCandType>
void PFCandidateHistogrammer<PFCandType>::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
  auto const &pfCands_handle(iEvent.getHandle(pfCands_token_));

  if (pfCands_handle.isValid()) {
    uint pfcand_mult(0), pfcand_mult_X(0), pfcand_mult_h(0), pfcand_mult_e(0), pfcand_mult_mu(0), pfcand_mult_gamma(0),
        pfcand_mult_h0(0), pfcand_mult_hHF(0), pfcand_mult_egammaHF(0);

    for (auto const &pfc : *pfCands_handle) {
      if (not stringCutSelector_(pfc)) {
        continue;
      }

      ++pfcand_mult;

      auto const pid(dummyPFCandToUseTranslatePdgId_.translatePdgIdToType(pfc.pdgId()));

      if (pid == reco::PFCandidate::X) {
        ++pfcand_mult_X;
      }  // undefined
      else if (pid == reco::PFCandidate::h) {
        ++pfcand_mult_h;
      }  // charged hadron
      else if (pid == reco::PFCandidate::e) {
        ++pfcand_mult_e;
      }  // electron
      else if (pid == reco::PFCandidate::mu) {
        ++pfcand_mult_mu;
      }  // muon
      else if (pid == reco::PFCandidate::gamma) {
        ++pfcand_mult_gamma;
      }  // photon
      else if (pid == reco::PFCandidate::h0) {
        ++pfcand_mult_h0;
      }  // neutral hadron
      else if (pid == reco::PFCandidate::h_HF) {
        ++pfcand_mult_hHF;
      }  // HF tower identified as a hadron
      else if (pid == reco::PFCandidate::egamma_HF) {
        ++pfcand_mult_egammaHF;
      }  // HF tower identified as an EM particle

      h_pfcand_particleId_->Fill(pid + 0.5);
      h_pfcand_pt_->Fill(pfc.pt());
      h_pfcand_pt_2_->Fill(pfc.pt());
      h_pfcand_eta_->Fill(pfc.eta());
      h_pfcand_phi_->Fill(pfc.phi());
      h_pfcand_mass_->Fill(pfc.mass());
      h_pfcand_vx_->Fill(pfc.vx());
      h_pfcand_vy_->Fill(pfc.vy());
      h_pfcand_vz_->Fill(pfc.vz());
    }

    h_pfcand_mult_->Fill(pfcand_mult);
    h_pfcand_mult_X_->Fill(pfcand_mult_X);
    h_pfcand_mult_h_->Fill(pfcand_mult_h);
    h_pfcand_mult_e_->Fill(pfcand_mult_e);
    h_pfcand_mult_mu_->Fill(pfcand_mult_mu);
    h_pfcand_mult_gamma_->Fill(pfcand_mult_gamma);
    h_pfcand_mult_h0_->Fill(pfcand_mult_h0);
    h_pfcand_mult_hHF_->Fill(pfcand_mult_hHF);
    h_pfcand_mult_egammaHF_->Fill(pfcand_mult_egammaHF);
  } else {
    edm::LogWarning("Input") << "invalid handle to input collection : " << pfCands_tag_.encode();
  }
}

template <typename PFCandType>
void PFCandidateHistogrammer<PFCandType>::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("particleFlow"))
      ->setComment("edm::InputTag of PF candidates collection");
  desc.add<std::string>("cut", "")->setComment("string selector for PF candidates collection");
  descriptions.add(defaultModuleLabel<PFCandidateHistogrammer<PFCandType>>(), desc);
}

#endif
