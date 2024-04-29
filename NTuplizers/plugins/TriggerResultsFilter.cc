#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"

//#include <iostream>
//#define LogTrace(X) std::cout << std::endl

class TriggerResultsFilter : public edm::stream::EDFilter<> {
 public:
  explicit TriggerResultsFilter(const edm::ParameterSet&);
  ~TriggerResultsFilter() override = default;
  static void fillDescriptions(edm::ConfigurationDescriptions&);

 private:
  bool filter(edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag triggerResultsInputTag_;
  const std::vector<std::string> pathNames_;
  const bool useLogicalAND_;
  const bool ignoreIfMissing_;

  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
};

TriggerResultsFilter::TriggerResultsFilter(const edm::ParameterSet& iConfig)
  : triggerResultsInputTag_(iConfig.getParameter<edm::InputTag>("triggerResults")),
    pathNames_(iConfig.getParameter<std::vector<std::string>>("pathNames")),
    useLogicalAND_(iConfig.getParameter<bool>("useLogicalAND")),
    ignoreIfMissing_(iConfig.getParameter<bool>("ignoreIfMissing")) {


  if (pathNames_.empty()) {
    edm::LogWarning("Input") << "Value of plugin argument \"pathNames\" is an empty vector";
  }

  triggerResultsToken_ = consumes<edm::TriggerResults>(triggerResultsInputTag_);
}

bool TriggerResultsFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {

  LogTrace("") << "[TriggerResultsFilter::filter] --------------------------------------------------------";
  LogTrace("") << "[TriggerResultsFilter::filter] Run = " << iEvent.id().run() << ", LuminosityBlock = " << iEvent.id().luminosityBlock() << ", Event = " << iEvent.id().event();

  if(pathNames_.size() == 0){
    edm::LogWarning("Input") << "Vector of path names is empty (will return \"true\")";
    return true;
  }

  edm::Handle<edm::TriggerResults> triggerResults;
  iEvent.getByToken(triggerResultsToken_, triggerResults);

  if (not triggerResults.isValid()) {
    edm::LogWarning("Input") << "Invalid handle to edm::TriggerResults (InputTag: \""
      << triggerResultsInputTag_.encode() << "\") -> plugin will return \"false\"";
    return false;
  }

  auto const& triggerNames(iEvent.triggerNames(*triggerResults).triggerNames());

  if(triggerResults->size() != triggerNames.size()){
    edm::LogWarning("Input") << "Size of TriggerResults (" << triggerResults->size()
      << ") and TriggerNames (" << triggerNames.size() << ") differ --> plugin will return \"false\"";
    return false;
  }

  if(not ignoreIfMissing_){
    for(auto const& path_i : pathNames_){
      if(std::find(triggerNames.begin(), triggerNames.end(), path_i) == triggerNames.end()){
        throw cms::Exception("Input") << "Entry of plugin argument \"pathNames\" not available in \""
          << triggerResultsInputTag_.encode() << "\": \"" << path_i << "\"";
      }
    }
  }

  if(useLogicalAND_){
    for(unsigned int idx=0; idx<triggerResults->size(); ++idx){
      if(triggerResults->at(idx).accept() == false){
        auto const& triggerName(triggerNames.at(idx));
        if(std::find(pathNames_.begin(), pathNames_.end(), triggerName) != pathNames_.end()){
          LogTrace("") << "[TriggerResultsFilter::filter]  " << triggerName << " = 0";
          return false;
        }
//        else {
//          auto const triggerNameUnv(triggerName.substr(0, triggerName.rfind("_v")));
//          if(std::find(pathNames_.begin(), pathNames_.end(), triggerNameUnv) != pathNames_.end()){
//            LogTrace("") << "[TriggerResultsFilter::filter]  " << triggerNameUnv << " = 0";
//            return false;
//          }
//        }
      }
    }
  } else {
    for(unsigned int idx=0; idx<triggerResults->size(); ++idx){
      if(triggerResults->at(idx).accept() == true){
        auto const& triggerName(triggerNames.at(idx));
        if(std::find(pathNames_.begin(), pathNames_.end(), triggerName) != pathNames_.end()){
          LogTrace("") << "[TriggerResultsFilter::filter]  " << triggerName << " = 1";
          return true;
        }
//        else {
//          auto const triggerNameUnv(triggerName.substr(0, triggerName.rfind("_v")));
//          if(std::find(pathNames_.begin(), pathNames_.end(), triggerNameUnv) != pathNames_.end()){
//            LogTrace("") << "[TriggerResultsFilter::filter]  " << triggerNameUnv << " = 1";
//            return true;
//          }
//        }
      }
    }
  }
  
  return useLogicalAND_;
}

void TriggerResultsFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("TriggerResults", "", "HLT"));
  desc.add<std::vector<std::string>>("pathNames", {});
  desc.add<bool>("useLogicalAND", false);
  desc.add<bool>("ignoreIfMissing", false);
  descriptions.add("triggerResultsFilter", desc);
}

DEFINE_FWK_MODULE(TriggerResultsFilter);
