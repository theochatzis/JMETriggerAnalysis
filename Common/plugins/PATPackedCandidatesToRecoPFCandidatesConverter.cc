#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>

#include <DataFormats/PatCandidates/interface/PackedCandidate.h>
#include <DataFormats/ParticleFlowCandidate/interface/PFCandidate.h>

#include <memory>
#include <utility>

class PATPackedCandidatesToRecoPFCandidatesConverter : public edm::EDProducer {
public:
  explicit PATPackedCandidatesToRecoPFCandidatesConverter(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetToken src_;
};

PATPackedCandidatesToRecoPFCandidatesConverter::PATPackedCandidatesToRecoPFCandidatesConverter(
    const edm::ParameterSet& iConfig) {
  src_ = consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("src"));

  produces<reco::PFCandidateCollection>();
}

void PATPackedCandidatesToRecoPFCandidatesConverter::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<pat::PackedCandidateCollection> packedCands_;
  iEvent.getByToken(src_, packedCands_);

  std::unique_ptr<reco::PFCandidateCollection> recoPFCands(new reco::PFCandidateCollection());

  reco::PFCandidate dummy;
  for (int iCand = 0; iCand < int(packedCands_->size()); ++iCand) {
    reco::PFCandidate intPFCand(packedCands_->at(iCand).charge(),
                                packedCands_->at(iCand).p4(),
                                dummy.translatePdgIdToType(packedCands_->at(iCand).pdgId()));
    recoPFCands->push_back(intPFCand);
  }

  iEvent.put(std::move(recoPFCands));

  return;
}

void PATPackedCandidatesToRecoPFCandidatesConverter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  desc.add<edm::InputTag>("src")->setComment("edm::InputTag of input pat::PackedCandidateCollection");

  descriptions.add("PATPackedCandidatesToRecoPFCandidatesConverter", desc);
}

DEFINE_FWK_MODULE(PATPackedCandidatesToRecoPFCandidatesConverter);
