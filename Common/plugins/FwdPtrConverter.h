#ifndef JMETriggerAnalysis_FwdPtrConverter_h
#define JMETriggerAnalysis_FwdPtrConverter_h

#include <vector>
#include <memory>
#include <utility>

#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/stream/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <FWCore/ParameterSet/interface/ParameterSetDescription.h>
#include <FWCore/ParameterSet/interface/ConfigurationDescriptions.h>
#include <DataFormats/Common/interface/FwdPtr.h>
#include <HLTrigger/HLTcore/interface/defaultModuleLabel.h>

template <class T>
class FwdPtrConverter : public edm::stream::EDProducer<> {
public:
  explicit FwdPtrConverter(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::EDGetTokenT<edm::View<edm::FwdPtr<T>>> src_token_;
  const edm::EDPutTokenT<std::vector<T>> out_token_;
};

template <class T>
FwdPtrConverter<T>::FwdPtrConverter(const edm::ParameterSet& iConfig)
    : src_token_{consumes<edm::View<edm::FwdPtr<T>>>(iConfig.getParameter<edm::InputTag>("src"))},
      out_token_{produces<std::vector<T>>()} {}

template <class T>
void FwdPtrConverter<T>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto const& coll(iEvent.get(src_token_));

  std::vector<T> output;
  output.reserve(coll.size());

  for (auto const& fwdptr : coll) {
    output.emplace_back(*fwdptr);
  }

  iEvent.emplace(out_token_, std::move(output));
}

template <class T>
void FwdPtrConverter<T>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("pfNoPileUp"))
      ->setComment("edm::InputTag of input collection (type: edm::View<edm::FwdPtr<T>>)");
  descriptions.add(defaultModuleLabel<FwdPtrConverter<T>>(), desc);
}

#endif
