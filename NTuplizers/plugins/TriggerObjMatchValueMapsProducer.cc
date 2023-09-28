#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include <sstream>
#include <algorithm>
//#include <iostream>
//#define LogTrace(X) std::cout << std::endl

class TriggerObjMatchValueMapsProducer : public edm::stream::EDProducer<> {
 public:
  explicit TriggerObjMatchValueMapsProducer(const edm::ParameterSet&);
  ~TriggerObjMatchValueMapsProducer() override = default;
  static void fillDescriptions(edm::ConfigurationDescriptions&);

 private:
  void beginRun(edm::Run const&, edm::EventSetup const&) override;
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag recoCandidatesInputTag_;
  const edm::InputTag triggerResultsInputTag_;
  const edm::InputTag triggerObjectsInputTag_;
  const std::string pathName_;
  const bool ignorePathVersion_;
  const double deltaR_;
  const bool verbose_;

  HLTConfigProvider hltConfigProvider_;
  bool initFailed_;
  bool skipRun_;
  bool skipTrigObjMatching_;

  std::string hltPath_;
  std::string hltFilterL1TSeed_;
  std::vector<std::string> hltFiltersWithTags_;

  edm::EDGetTokenT<edm::View<reco::Candidate>> recoCandidatesToken_;
  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
  edm::EDGetTokenT<edm::View<pat::TriggerObjectStandAlone>> triggerObjectsToken_;
};

TriggerObjMatchValueMapsProducer::TriggerObjMatchValueMapsProducer(const edm::ParameterSet& iConfig)
  : recoCandidatesInputTag_(iConfig.getParameter<edm::InputTag>("src")),
    triggerResultsInputTag_(iConfig.getParameter<edm::InputTag>("triggerResults")),
    triggerObjectsInputTag_(iConfig.getParameter<edm::InputTag>("triggerObjects")),
    pathName_(iConfig.getParameter<std::string>("pathName")),
    ignorePathVersion_(iConfig.getParameter<bool>("ignorePathVersion")),
    deltaR_(iConfig.getParameter<double>("deltaR")),
    verbose_(iConfig.getParameter<bool>("verbose")),
    initFailed_(false),
    skipRun_(false),
    skipTrigObjMatching_(false),
    hltPath_(""),
    hltFilterL1TSeed_("") {

  hltFiltersWithTags_.clear();

  if (pathName_.empty()) {
    edm::LogError("Input") << "Value of plugin argument \"pathName\" is an empty string (plugin will not produce outputs)";
    initFailed_ = true;
    return;
  }

  if (deltaR_ <= 0.) {
    edm::LogError("Input") << "Value of plugin argument \"deltaR\" (" << deltaR_
      << ") is null or negative (plugin will not produce outputs)";
    initFailed_ = true;
    return;
  }

  if (triggerResultsInputTag_.process().empty()) {
    edm::LogError("Input") << "Process name not specified in InputTag argument \"triggerResults\""
      << " (plugin will not produce outputs): \"" << triggerResultsInputTag_.encode() << "\"";
    initFailed_ = true;
    return;
  } else {
    recoCandidatesToken_ = consumes<edm::View<reco::Candidate>>(recoCandidatesInputTag_);
    triggerResultsToken_ = consumes<edm::TriggerResults>(triggerResultsInputTag_);
    triggerObjectsToken_ = consumes<edm::View<pat::TriggerObjectStandAlone>>(triggerObjectsInputTag_);
  }

  produces<edm::ValueMap<bool>>("trigObjMatchL1TSeed");
  produces<edm::ValueMap<bool>>("trigObjMatchHLTLastFilter");
  produces<edm::ValueMap<bool>>("trigObjMatchHLTAllFilters");
}

void TriggerObjMatchValueMapsProducer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {
  if (initFailed_) {
    return;
  }

  LogTrace("") << "[TriggerObjMatchValueMapsProducer] " << "----------------------------------------------------------------------------------------------------";
  LogTrace("") << "[TriggerObjMatchValueMapsProducer::beginRun] Run = " << iRun.id();

  // reset data members holding information from the previous run
  skipRun_ = false;
  skipTrigObjMatching_ = false;

  bool hltChanged(true);
  if (hltConfigProvider_.init(iRun, iSetup, triggerResultsInputTag_.process(), hltChanged)) {
    LogTrace("") << "[TriggerObjMatchValueMapsProducer::beginRun] HLTConfigProvider initialized [processName() = \""
                 << hltConfigProvider_.processName() << "\", tableName() = \"" << hltConfigProvider_.tableName()
                 << "\", size() = " << hltConfigProvider_.size() << "]";
  } else {
    edm::LogError("Input") << "Initialization of HLTConfigProvider failed for Run=" << iRun.id() << " (process=\""
                           << triggerResultsInputTag_.process() << "\") -> plugin will not produce outputs for this Run";
    skipRun_ = true;
    return;
  }

  hltPath_.clear();
  hltFilterL1TSeed_.clear();
  hltFiltersWithTags_.clear();

  size_t numMatches(0);

  auto const& triggerNames(hltConfigProvider_.triggerNames());
  for (auto const& iPathName : triggerNames) {

    if(ignorePathVersion_){
      auto const iPathNameUnv(iPathName.substr(0, iPathName.rfind("_v")));
      if(iPathNameUnv != pathName_){
        continue;
      }
    }
    else {
      if(iPathName != pathName_){
        continue;
      }
    }

    ++numMatches;

    if(numMatches > 1){
      edm::LogError("Logic") << "Attempting to overwrite output products -> new match for path name \""
        << pathName_ << "\" will be ignored: " << iPathName << " (original match was \"" << hltPath_ << "\")";
      continue;
    }
    else {
      hltPath_ = iPathName;
    }

    const uint iPathIndex(hltConfigProvider_.triggerIndex(iPathName));

    LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]       " << "Path = \"" << iPathName
      << "\", HLTConfigProvider::triggerIndex(\"" << iPathName << "\") = " << iPathIndex;

    LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]       hltFiltersWithTags";

    auto const& moduleLabels(hltConfigProvider_.moduleLabels(iPathIndex));

    int hltL1TSeedModuleIndex(-1);
    hltFilterL1TSeed_.clear();
    hltFiltersWithTags_.clear();
    hltFiltersWithTags_.reserve(moduleLabels.size());

    for(size_t idx=0; idx<moduleLabels.size(); ++idx){
      auto const& moduleLabel(moduleLabels.at(idx));

      auto const& moduleEDMType(hltConfigProvider_.moduleEDMType(moduleLabel));
      if(moduleEDMType != "EDFilter"){
        continue;
      }

      auto const& moduleType(hltConfigProvider_.moduleType(moduleLabel));
      if((moduleType == "HLTTriggerTypeFilter") or (moduleType == "HLTBool") or (moduleType == "HLTPrescaler")){
        continue;
      }

      if(not hltConfigProvider_.saveTags(moduleLabel)){
        continue;
      }

      if(moduleLabel.find("hltL1", 0) == 0){
        if(hltL1TSeedModuleIndex < 0){
          hltL1TSeedModuleIndex = idx;
        }
        else {
          throw cms::Exception("InputError") << "found more than one match for L1T-Seed module of HLT-Path"
            << " (1st match = \"" << moduleLabels.at(hltL1TSeedModuleIndex) << "\", 2nd match = \"" << moduleLabel << "\")"
            << ", HLT-Path = \"" << iPathName << "\"";
        }
      }

      LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]         " << moduleLabel;

      hltFiltersWithTags_.emplace_back(moduleLabel);
    }

    if(hltL1TSeedModuleIndex < 0){
      throw cms::Exception("Input") << "failed to find L1T-Seed module of HLT-Path: " << iPathName;
    }
    else if(hltFiltersWithTags_.empty()){
      throw cms::Exception("Input") << "zero filters associated to HLT-Path: " << iPathName;
    }

    hltFilterL1TSeed_ = moduleLabels.at(hltL1TSeedModuleIndex);

    LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]       "
      << "hltFilterL1TSeed = " << hltFilterL1TSeed_ << " (index = " << hltL1TSeedModuleIndex << ")";

    if(std::find(hltFiltersWithTags_.begin(), hltFiltersWithTags_.end(), hltFilterL1TSeed_) == hltFiltersWithTags_.end()){
      std::ostringstream oss;
      oss << "L1T-Seed (\"" << hltFilterL1TSeed_ << "\") does not belong to the list of filters-with-tags of the HLT-Path (\"" << iPathName << "\"): [ ";
      for(auto const& filt : hltFiltersWithTags_){ oss << filt << " "; }
      oss << "]";

      throw cms::Exception("Logic") << oss.str();
    }
  }

  if(numMatches < 1){
    edm::LogWarning("Output") << "Zero matches found for path name \""
      << pathName_ << "\" --> all output products will be \"false\"";
    skipTrigObjMatching_ = true;
  }
}

void TriggerObjMatchValueMapsProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (skipRun_ or initFailed_) {
    return;
  }

  LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce] --------------------------------------------------------";
  LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce] Run = " << iEvent.id().run() << ", LuminosityBlock = " << iEvent.id().luminosityBlock() << ", Event = " << iEvent.id().event();

  edm::Handle<edm::View<reco::Candidate>> recoCandidates;
  iEvent.getByToken(recoCandidatesToken_, recoCandidates);

  if (not recoCandidates.isValid()) {
    edm::LogWarning("Input") << "Invalid handle to edm::View<reco::Candidate> (InputTag: \""
      << recoCandidatesInputTag_.encode() << "\") -> plugin will not produce outputs for this event";
    return;
  }

  edm::Handle<edm::TriggerResults> triggerResults;
  iEvent.getByToken(triggerResultsToken_, triggerResults);

  if (not triggerResults.isValid()) {
    edm::LogWarning("Input") << "Invalid handle to edm::TriggerResults (InputTag: \""
      << triggerResultsInputTag_.encode() << "\") -> plugin will not produce outputs for this event";
    return;
  }

  edm::Handle<edm::View<pat::TriggerObjectStandAlone>> triggerObjects;
  iEvent.getByToken(triggerObjectsToken_, triggerObjects);

  if (not triggerObjects.isValid()) {
    edm::LogWarning("Input") << "Invalid handle to edm::View<pat::TriggerObjectStandAlone> (InputTag: \""
      << triggerObjectsInputTag_.encode() << "\") -> plugin will not produce outputs for this event";
    return;
  }

  LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce] HLT Menu: " << hltConfigProvider_.tableName();

  std::vector<bool> trigObjMatchL1TSeed_flags(recoCandidates->size(), false);
  std::vector<bool> trigObjMatchHLTLastFilter_flags(recoCandidates->size(), false);
  std::vector<bool> trigObjMatchHLTAllFilters_flags(recoCandidates->size(), false);

  if(not skipTrigObjMatching_){

    auto const iPathIndex(hltConfigProvider_.triggerIndex(hltPath_));
    if (iPathIndex >= triggerResults->size()) {
      edm::LogError("Logic") << "Index associated to path \"" << hltPath_ << "\" (" << iPathIndex
        << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
        << ") -> all outputs will be set to \"false\"";
    }
    else {
      LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]"
        << " Trigger Objects (InputTag = \"" << triggerObjectsInputTag_.encode()
        << "\"): size = " << triggerObjects->size();

      std::vector<pat::TriggerObjectStandAlone> triggerObjectsUnpacked;
      triggerObjectsUnpacked.reserve(triggerObjects->size());
      for(auto& trigObj : *triggerObjects){
        triggerObjectsUnpacked.emplace_back(trigObj);
        triggerObjectsUnpacked.back().unpackFilterLabels(iEvent, *triggerResults);
      }

      if(verbose_){

        for(size_t trigIdx=0; trigIdx<hltFiltersWithTags_.size(); ++trigIdx){

          auto const& hltFilter(hltFiltersWithTags_.at(trigIdx));
          LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]    " << hltFilter;

          for(auto const& trigObj : triggerObjectsUnpacked){

            if(trigObj.hasFilterLabel(hltFilter)){
              LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]      "
                << " energy = " << trigObj.energy() << " pt = " << trigObj.pt()
                << " eta = " << trigObj.eta() << " phi = " << trigObj.phi();
            }
          }
        }
      }

      auto const maxDeltaR2(deltaR_ * deltaR_);

      auto const& hltFilterHLTLastFilter(hltFiltersWithTags_.back());

      for(uint idx=0; idx<recoCandidates->size(); ++idx){
        auto const& recoCand(recoCandidates->at(idx));

        bool trigObjMatchL1TSeed_flag(false);
        bool trigObjMatchHLTLastFilter_flag(false);
        bool trigObjMatchHLTAllFilters_flag(true);

        for(size_t trigIdx=0; trigIdx<hltFiltersWithTags_.size(); ++trigIdx){
          auto const& hltFilter(hltFiltersWithTags_.at(trigIdx));

          bool hasMatch(false);
          for(auto const& trigObj : triggerObjectsUnpacked){
            if(not trigObj.hasFilterLabel(hltFilter)){
              continue;
            }

            auto const deltaR2(reco::deltaR2(recoCand.eta(), recoCand.phi(), trigObj.eta(), trigObj.phi()));

            if(deltaR2 >= maxDeltaR2){
              continue;
            }

            hasMatch = true;
            break;
          }

          if(hltFilter == hltFilterL1TSeed_){
            trigObjMatchL1TSeed_flag = hasMatch;
          }
          else {

            if(hltFilter == hltFilterHLTLastFilter){
              trigObjMatchHLTLastFilter_flag = hasMatch;
            }

            if(trigObjMatchHLTAllFilters_flag){
              trigObjMatchHLTAllFilters_flag &= hasMatch;
            }
          }
        }

        if(trigObjMatchHLTAllFilters_flag and (not trigObjMatchHLTLastFilter_flag)){

          throw cms::Exception("Logic") << "Candidate flagged as matched to a trigger-object"
            << " for all filters-with-tags of the HLT-Path (\"" << hltPath_ << "\")"
            << ", but not for the last such filter (\"" << hltFilterHLTLastFilter << "\")";
        }

        trigObjMatchL1TSeed_flags.at(idx) = trigObjMatchL1TSeed_flag;
        trigObjMatchHLTLastFilter_flags.at(idx) = trigObjMatchHLTLastFilter_flag;
        trigObjMatchHLTAllFilters_flags.at(idx) = trigObjMatchHLTAllFilters_flag;

        LogTrace("") << "[TriggerObjMatchValueMapsProducer::produce]    candidate:"
          << " pt = " << recoCand.pt() << ", eta = " << recoCand.eta() << ", phi = " << recoCand.phi()
          << ", trigObjMatchL1TSeed = " << trigObjMatchL1TSeed_flag
          << ", trigObjMatchHLTLastFilter = " << trigObjMatchHLTLastFilter_flag
          << ", trigObjMatchHLTAllFilters = " << trigObjMatchHLTAllFilters_flag;
      }
    }
  }

  // TrigObjMatch: L1TSeed
  auto trigObjMatchL1TSeed_vMap = std::make_unique<edm::ValueMap<bool>>();
  edm::ValueMap<bool>::Filler trigObjMatchL1TSeed_vMapFiller(*trigObjMatchL1TSeed_vMap);
  trigObjMatchL1TSeed_vMapFiller.insert(recoCandidates, trigObjMatchL1TSeed_flags.begin(), trigObjMatchL1TSeed_flags.end());
  trigObjMatchL1TSeed_vMapFiller.fill();
  iEvent.put(std::move(trigObjMatchL1TSeed_vMap), "trigObjMatchL1TSeed");

  // TrigObjMatch: HLTLastFilter
  auto trigObjMatchHLTLastFilter_vMap = std::make_unique<edm::ValueMap<bool>>();
  edm::ValueMap<bool>::Filler trigObjMatchHLTLastFilter_vMapFiller(*trigObjMatchHLTLastFilter_vMap);
  trigObjMatchHLTLastFilter_vMapFiller.insert(recoCandidates, trigObjMatchHLTLastFilter_flags.begin(), trigObjMatchHLTLastFilter_flags.end());
  trigObjMatchHLTLastFilter_vMapFiller.fill();
  iEvent.put(std::move(trigObjMatchHLTLastFilter_vMap), "trigObjMatchHLTLastFilter");

  // TrigObjMatch: HLTAllFilters
  auto trigObjMatchHLTAllFilters_vMap = std::make_unique<edm::ValueMap<bool>>();
  edm::ValueMap<bool>::Filler trigObjMatchHLTAllFilters_vMapFiller(*trigObjMatchHLTAllFilters_vMap);
  trigObjMatchHLTAllFilters_vMapFiller.insert(recoCandidates, trigObjMatchHLTAllFilters_flags.begin(), trigObjMatchHLTAllFilters_flags.end());
  trigObjMatchHLTAllFilters_vMapFiller.fill();
  iEvent.put(std::move(trigObjMatchHLTAllFilters_vMap), "trigObjMatchHLTAllFilters");
}

void TriggerObjMatchValueMapsProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("fooCandidates"));
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("TriggerResults", "", "HLT"));
  desc.add<edm::InputTag>("triggerObjects", edm::InputTag("slimmedPatTrigger"));
  desc.add<std::string>("pathName", "");
  desc.add<bool>("ignorePathVersion", false);
  desc.add<double>("deltaR", 0.2);
  desc.add<bool>("verbose", false);
  descriptions.add("triggerObjMatchValueMapsProducer", desc);
}

DEFINE_FWK_MODULE(TriggerObjMatchValueMapsProducer);
