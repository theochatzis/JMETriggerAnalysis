#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "CommonTools/TriggerUtils/interface/GenericTriggerEventFlag.h"

#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESWatcher.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Utilities/interface/ESGetToken.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "CondFormats/HLTObjects/interface/AlCaRecoTriggerBits.h"
#include "CondFormats/DataRecord/interface/AlCaRecoTriggerBitsRcd.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerEvmReadoutRecord.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "DataFormats/OnlineMetaData/interface/DCSRecord.h"
#include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

//#include <iostream>

class TriggerGenericFlagsProducer : public edm::stream::EDProducer<> {
public:
  explicit TriggerGenericFlagsProducer(const edm::ParameterSet&);
  ~TriggerGenericFlagsProducer() throw() override;
  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  //void beginRun(edm::Run const&, edm::EventSetup const&) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  
  std::unique_ptr<GenericTriggerEventFlag> genTriggerEventFlag_;

  const edm::InputTag triggerResultsInputTag_;

  //bool hltPathsAreValid_;
};

TriggerGenericFlagsProducer::TriggerGenericFlagsProducer(const edm::ParameterSet& iConfig)
    : genTriggerEventFlag_(new GenericTriggerEventFlag(
          iConfig.getParameter<edm::ParameterSet>("genericTriggerEventPSet"), consumesCollector(), *this))
      //hltPathsAreValid_(false){
   {
  produces<bool>("HLTPathIsOn");
  produces<bool>("HLTPathAccept");
}

TriggerGenericFlagsProducer::~TriggerGenericFlagsProducer() throw() {
  if (genTriggerEventFlag_) {
    genTriggerEventFlag_.reset();
  }
}
// void TriggerGenericFlagsProducer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {
//   if (genTriggerEventFlag_) {
//     genTriggerEventFlag_.reset();
//   }
// }

void TriggerGenericFlagsProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  
  bool hltPathIsOn(false);
  bool hltPathAccept(false);
  
  hltPathIsOn = ( genTriggerEventFlag_ && 
                        genTriggerEventFlag_->on()); 
                        // && genTriggerEventFlag_->allHLTPathsAreValid() );
  hltPathAccept = genTriggerEventFlag_->accept(iEvent, iSetup); 
  
  std::cout << hltPathIsOn << std::endl;
  std::cout << hltPathAccept << std::endl;
  
  auto out_hltPathIsOn = std::make_unique<bool>(hltPathIsOn);
  auto out_hltPathAccept = std::make_unique<bool>(hltPathAccept);

  iEvent.put(std::move(out_hltPathIsOn), "HLTPathIsOn");
  iEvent.put(std::move(out_hltPathAccept), "HLTPathAccept");
}

void TriggerGenericFlagsProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  edm::ParameterSetDescription genericTriggerEventPSet;
  GenericTriggerEventFlag::fillPSetDescription(genericTriggerEventPSet);
  desc.add<edm::ParameterSetDescription>("genericTriggerEventPSet", genericTriggerEventPSet);
  descriptions.add("TriggerGenericFlagsProducer", desc);
}

DEFINE_FWK_MODULE(TriggerGenericFlagsProducer);
