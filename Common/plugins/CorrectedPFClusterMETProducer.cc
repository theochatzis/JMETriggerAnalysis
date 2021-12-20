#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/METReco/interface/PFClusterMET.h"
#include "DataFormats/METReco/interface/CorrMETData.h"
#include "JetMETCorrections/Type1MET/interface/AddCorrectionsToGenericMET.h"

#include <vector>

class CorrectedPFClusterMETProducer : public edm::stream::EDProducer<> {
public:
  explicit CorrectedPFClusterMETProducer(const edm::ParameterSet& cfg)
      : corrector(), token_(consumes<METCollection>(cfg.getParameter<edm::InputTag>("src"))) {
    std::vector<edm::InputTag> corrInputTags = cfg.getParameter<std::vector<edm::InputTag> >("srcCorrections");
    std::vector<edm::EDGetTokenT<CorrMETData> > corrTokens;
    for (std::vector<edm::InputTag>::const_iterator inputTag = corrInputTags.begin(); inputTag != corrInputTags.end();
         ++inputTag) {
      corrTokens.push_back(consumes<CorrMETData>(*inputTag));
    }

    corrector.setCorTokens(corrTokens);

    produces<METCollection>("");
  }

  ~CorrectedPFClusterMETProducer() override {}

private:
  AddCorrectionsToGenericMET corrector;

  typedef std::vector<reco::PFClusterMET> METCollection;

  edm::EDGetTokenT<METCollection> token_;

  void produce(edm::Event& evt, const edm::EventSetup& es) override {
    edm::Handle<METCollection> srcMETCollection;
    evt.getByToken(token_, srcMETCollection);

    const reco::PFClusterMET& srcMET = (*srcMETCollection)[0];

    auto corrMET = corrector.getCorrectedMET(srcMET, evt);

    reco::PFClusterMET outMET(corrMET.sumEt(), corrMET.p4(), corrMET.vertex());

    std::unique_ptr<METCollection> product(new METCollection);
    product->push_back(outMET);
    evt.put(std::move(product));
  }
};

DEFINE_FWK_MODULE(CorrectedPFClusterMETProducer);
