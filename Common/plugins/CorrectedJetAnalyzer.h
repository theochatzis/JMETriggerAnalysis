#ifndef JMETriggerAnalysis_Common_CorrectedJetAnalyzer_h
#define JMETriggerAnalysis_Common_CorrectedJetAnalyzer_h

#include <string>
#include <vector>

#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Utilities/interface/transform.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/RefToBase.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "JetMETCorrections/JetCorrector/interface/JetCorrector.h"

template <class T>
class CorrectedJetAnalyzer : public edm::one::EDAnalyzer<> {
public:
  explicit CorrectedJetAnalyzer(edm::ParameterSet const& fParameters);
  void analyze(edm::Event const&, edm::EventSetup const&) override;

protected:
  edm::InputTag const srcInputTag_;
  edm::EDGetTokenT<edm::View<T>> const srcToken_;
  std::vector<edm::EDGetTokenT<reco::JetCorrector>> const jetCorrectorTokens_;
  std::vector<edm::FileInPath> const textFilesInPath_;
  bool const useRho_;
  edm::EDGetTokenT<double> const rhoToken_;
  bool const verbose_;

  std::vector<std::unique_ptr<FactorizedJetCorrector>> factorizedJetCorrectors_;
};

template <class T>
CorrectedJetAnalyzer<T>::CorrectedJetAnalyzer(edm::ParameterSet const& iConfig)
    : srcInputTag_(iConfig.getParameter<edm::InputTag>("src")),
      srcToken_(consumes<edm::View<T>>(srcInputTag_)),
      jetCorrectorTokens_(
          edm::vector_transform(iConfig.getParameter<std::vector<edm::InputTag>>("correctors"),
                                [this](edm::InputTag const& foo) { return consumes<reco::JetCorrector>(foo); })),
      textFilesInPath_(edm::vector_transform(iConfig.getParameter<std::vector<std::string>>("textFiles"),
                                             [this](std::string const& foo) { return edm::FileInPath(foo); })),
      useRho_(iConfig.getParameter<bool>("useRho")),
      rhoToken_(useRho_ ? consumes<double>(iConfig.getParameter<edm::InputTag>("rho")) : edm::EDGetTokenT<double>()),
      verbose_(iConfig.getParameter<bool>("verbose")) {
  factorizedJetCorrectors_.clear();
  factorizedJetCorrectors_.reserve(textFilesInPath_.size());
  for (auto const& foo : textFilesInPath_) {
    std::vector<JetCorrectorParameters> jetCorrectorParameters({foo.fullPath()});
    factorizedJetCorrectors_.emplace_back(new FactorizedJetCorrector(jetCorrectorParameters));
  }
}

template <class T>
void CorrectedJetAnalyzer<T>::analyze(edm::Event const& iEvent, edm::EventSetup const&) {
  std::vector<reco::JetCorrector const*> correctors(jetCorrectorTokens_.size(), nullptr);
  for (uint idx = 0; idx < jetCorrectorTokens_.size(); ++idx) {
    auto const handle = iEvent.getHandle(jetCorrectorTokens_.at(idx));
    correctors[idx] = handle.product();
  }

  double const rho = useRho_ ? iEvent.get(rhoToken_) : 0.;

  auto const jets = iEvent.getHandle(srcToken_);

  for (uint idx = 0; idx < jets->size(); ++idx) {
    const T* referenceJet = &(jets->at(idx));
    edm::RefToBase<reco::Jet> jetRef(edm::Ref<edm::View<T>>(jets, idx));
    T correctedJet = jets->at(idx);  // copy original jet
    if (verbose_) {
      edm::LogPrint("") << "[" << srcInputTag_.encode() << "] Jet #" << idx;
      edm::LogPrint("") << "  - Original: pt=" << referenceJet->pt() << " eta=" << referenceJet->eta();
    }

    // globaltag/database
    for (uint corr_idx = 0; corr_idx < jetCorrectorTokens_.size(); ++corr_idx) {
      if (correctors[corr_idx]->vectorialCorrection()) {
        // Vectorial correction
        reco::JetCorrector::LorentzVector corrected;
        auto const scale = correctors[corr_idx]->correction(*referenceJet, jetRef, corrected);
        correctedJet.setP4(corrected);

        if (verbose_)
          edm::LogPrint("") << "  - [GT] After Correction #" << corr_idx + 1 << ": pt=" << correctedJet.pt()
                            << " eta=" << correctedJet.eta() << " JESC=" << scale;
      } else {
        // Scalar correction
        auto const scale = correctors[corr_idx]->refRequired() ? correctors[corr_idx]->correction(*referenceJet, jetRef)
                                                               : correctors[corr_idx]->correction(*referenceJet);
        correctedJet.scaleEnergy(scale);

        if (verbose_)
          edm::LogPrint("") << "  - [GT] After Correction #" << corr_idx + 1 << ": pt=" << correctedJet.pt()
                            << " eta=" << correctedJet.eta() << " JESC=" << scale;
      }

      referenceJet = &correctedJet;
    }

    // .txt files
    referenceJet = &(jets->at(idx));
    correctedJet = jets->at(idx);  // copy original jet

    for (uint corr_idx = 0; corr_idx < factorizedJetCorrectors_.size(); ++corr_idx) {
      auto& factorizedJetCorrector = factorizedJetCorrectors_.at(corr_idx);

      factorizedJetCorrector->setJetEta(referenceJet->eta());
      factorizedJetCorrector->setJetPt(referenceJet->pt());
      factorizedJetCorrector->setJetA(referenceJet->jetArea());
      factorizedJetCorrector->setRho(rho);

      auto const scale = factorizedJetCorrector->getCorrection();
      // Scalar correction
      correctedJet.scaleEnergy(scale);

      if (verbose_)
        edm::LogPrint("") << "  - [TXT] After Correction #" << corr_idx + 1 << ": pt=" << correctedJet.pt()
                          << " eta=" << correctedJet.eta() << " JESC=" << scale;

      referenceJet = &correctedJet;
    }
  }
}

#endif
