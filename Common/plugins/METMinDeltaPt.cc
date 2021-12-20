#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDFilter.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <DataFormats/METReco/interface/PFMET.h>
#include <DataFormats/PatCandidates/interface/MET.h>

class METMinDeltaPt : public edm::EDFilter {
public:
  explicit METMinDeltaPt(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetToken online_;
  edm::EDGetToken offline_;

  const std::string offlineCorrectionLevel_;

  const double minRelDiff_;
};

METMinDeltaPt::METMinDeltaPt(const edm::ParameterSet& iConfig)
    : online_(consumes<edm::View<reco::PFMET> >(iConfig.getParameter<edm::InputTag>("online"))),
      offline_(consumes<edm::View<pat::MET> >(iConfig.getParameter<edm::InputTag>("offline"))),
      offlineCorrectionLevel_(iConfig.getParameter<std::string>("offlineCorrectionLevel")),
      minRelDiff_(iConfig.getParameter<double>("minRelDiff")) {
  if (minRelDiff_ <= 0.) {
    throw cms::Exception("Input") << "invalid (non-positive) value for input parameter \"minRelDiff\": " << minRelDiff_;
  }
}

bool METMinDeltaPt::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // offline
  edm::Handle<edm::View<pat::MET> > offline_handle;
  iEvent.getByToken(offline_, offline_handle);

  if (not offline_handle.isValid()) {
    edm::LogWarning("Input") << "invalid handle for InputTag under \"offline\"";

    return false;
  }

  if (offline_handle->empty()) {
    edm::LogWarning("Input") << "empty vector of candidates in input collection under \"offline\"";

    return false;
  }

  pat::MET::METCorrectionLevel offlineCorrLevel;
  if (offlineCorrectionLevel_ == "Raw") {
    offlineCorrLevel = pat::MET::Raw;
  } else if (offlineCorrectionLevel_ == "Type1") {
    offlineCorrLevel = pat::MET::Type1;
  } else if (offlineCorrectionLevel_ == "Type1XY") {
    offlineCorrLevel = pat::MET::Type1XY;
  } else if (offlineCorrectionLevel_ == "TypeXY") {
    offlineCorrLevel = pat::MET::TypeXY;
  } else if (offlineCorrectionLevel_ == "RawCalo") {
    offlineCorrLevel = pat::MET::RawCalo;
  } else if (offlineCorrectionLevel_ == "RawChs") {
    offlineCorrLevel = pat::MET::RawChs;
  } else if (offlineCorrectionLevel_ == "RawTrk") {
    offlineCorrLevel = pat::MET::RawTrk;
  } else {
    throw cms::Exception("Input") << "invalid string for correction level of offline-MET: " << offlineCorrectionLevel_;
  }

  const auto offline_pt = offline_handle->at(0).shiftedPt(pat::MET::NoShift, offlineCorrLevel);

  if (offline_pt == 0.) {
    edm::LogWarning("Input") << "offline pT value is zero, returning False";

    return false;
  }

  // online
  edm::Handle<edm::View<reco::PFMET> > online_handle;
  iEvent.getByToken(online_, online_handle);

  if (not online_handle.isValid()) {
    edm::LogWarning("Input") << "invalid handle for InputTag under \"online\"";

    return false;
  }

  if (online_handle->empty()) {
    edm::LogWarning("Input") << "empty vector of candidates in input collection under \"online\"";

    return false;
  }

  const auto online_pt = online_handle->at(0).pt();

  // (online - offline)/offline
  LogDebug("Output") << "online-MET pT=" << online_pt << ", offline-MET pT=" << offline_pt << ", filter condition = ("
                     << std::abs(online_pt - offline_pt) << " > " << (minRelDiff_ * offline_pt) << ")";

  return (std::abs(online_pt - offline_pt) > (minRelDiff_ * offline_pt));
}

void METMinDeltaPt::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  desc.add<edm::InputTag>("online")->setComment("InputTag for online MET collection (type = reco::PFMET)");
  desc.add<edm::InputTag>("offline")->setComment("InputTag for offline MET collection (type = pat::MET)");
  desc.add<std::string>("offlineCorrectionLevel")
      ->setComment("String to select correction level of offline-MET (see enum pat::MET::METCorrectionLevel)");
  desc.add<double>("minRelDiff")
      ->setComment("Minimum relative difference between online-pT and offline-pT (relative to offline-pT)");

  descriptions.add("METMinDeltaPt", desc);
}

DEFINE_FWK_MODULE(METMinDeltaPt);
