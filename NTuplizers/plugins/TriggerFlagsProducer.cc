#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/L1TGlobal/interface/GlobalLogicParser.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"

//#include <iostream>
//#define LogTrace(X) std::cout << std::endl

class TriggerFlagsProducer : public edm::stream::EDProducer<> {
public:
  explicit TriggerFlagsProducer(const edm::ParameterSet&);
  ~TriggerFlagsProducer() override = default;
  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void beginRun(edm::Run const&, edm::EventSetup const&) override;
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag triggerResultsInputTag_;
  const std::string pathName_;
  const bool ignorePathVersion_;

  HLTPrescaleProvider hltPrescaleProvider_;
  bool initFailed_;
  bool skipRun_;

  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
};

TriggerFlagsProducer::TriggerFlagsProducer(const edm::ParameterSet& iConfig)
    : triggerResultsInputTag_(iConfig.getParameter<edm::InputTag>("triggerResults")),
      pathName_(iConfig.getParameter<std::string>("pathName")),
      ignorePathVersion_(iConfig.getParameter<bool>("ignorePathVersion")),
      hltPrescaleProvider_(iConfig, consumesCollector(), *this),
      initFailed_(false),
      skipRun_(false) {
  if (pathName_.empty()) {
    edm::LogError("Input") << "Value of plugin argument \"pathName\" is an empty string";
    initFailed_ = true;
    return;
  }

  if (triggerResultsInputTag_.process().empty()) {
    edm::LogError("Input") << "Process name not specified in InputTag argument \"triggerResults\""
                           << " (plugin will not produce outputs): \"" << triggerResultsInputTag_.encode() << "\"";
    initFailed_ = true;
    return;
  } else {
    triggerResultsToken_ = consumes<edm::TriggerResults>(triggerResultsInputTag_);
  }

  produces<bool>("L1TSeedAccept");
  produces<bool>("L1TSeedPrescaledOrMasked");
  produces<bool>("HLTPathPrescaled");
  produces<bool>("HLTPathAccept");
  produces<bool>("L1TSeedInitialDecision");
  produces<bool>("L1TSeedFinalDecision");
}

void TriggerFlagsProducer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {
  if (initFailed_) {
    return;
  }

  LogTrace("")
      << "[TriggerFlagsProducer] "
      << "----------------------------------------------------------------------------------------------------";
  LogTrace("") << "[TriggerFlagsProducer::beginRun] Run = " << iRun.id();

  // reset data members holding information from the previous run
  skipRun_ = false;

  bool hltChanged(true);
  if (hltPrescaleProvider_.init(iRun, iSetup, triggerResultsInputTag_.process(), hltChanged)) {
    LogTrace("") << "[TriggerFlagsProducer::beginRun] HLTPrescaleProvider initialized [processName() = \""
                 << hltPrescaleProvider_.hltConfigProvider().processName() << "\", tableName() = \""
                 << hltPrescaleProvider_.hltConfigProvider().tableName()
                 << "\", size() = " << hltPrescaleProvider_.hltConfigProvider().size() << "]";
  } else {
    edm::LogError("Input") << "Initialization of HLTPrescaleProvider failed for Run=" << iRun.id() << " (process=\""
                           << triggerResultsInputTag_.process()
                           << "\") -> plugin will not produce outputs for this Run";
    skipRun_ = true;
    return;
  }
}

void TriggerFlagsProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (skipRun_ or initFailed_) {
    return;
  }

  LogTrace("") << "[TriggerFlagsProducer::produce] --------------------------------------------------------";
  LogTrace("") << "[TriggerFlagsProducer::produce] Run = " << iEvent.id().run()
               << ", LuminosityBlock = " << iEvent.id().luminosityBlock() << ", Event = " << iEvent.id().event();

  edm::Handle<edm::TriggerResults> triggerResults;
  iEvent.getByToken(triggerResultsToken_, triggerResults);

  if (not triggerResults.isValid()) {
    edm::LogWarning("Input") << "Invalid handle to edm::TriggerResults (InputTag: \"triggerResults\")"
                             << " -> plugin will not produce outputs for this event";
    return;
  }

  // loads L1T information
  auto const psColumn(hltPrescaleProvider_.prescaleSet(iEvent, iSetup));

  auto const& l1GlobalUtils(hltPrescaleProvider_.l1tGlobalUtil());

  LogTrace("") << "[TriggerFlagsProducer::produce] L1T Menu: " << l1GlobalUtils.gtTriggerMenuName()
               << " (version = " << l1GlobalUtils.gtTriggerMenuVersion()
               << ", type = " << hltPrescaleProvider_.hltConfigProvider().l1tType() << ")";
  LogTrace("") << "[TriggerFlagsProducer::produce] HLT Menu: " << hltPrescaleProvider_.hltConfigProvider().tableName()
               << " (PS Column = " << psColumn << ")";

  size_t numMatches(0);
  std::string originalMatch("");

  bool l1tSeedPrescaledOrMasked(false);
  bool l1tSeedInitialDecision(false);
  bool l1tSeedFinalDecision(false);
  bool l1tSeedAccept(false);
  bool hltPathPrescaled(false);
  bool hltPathAccept(false);
  
  // std::cout << "------------" << std::endl;
  // std::cout << "pathName: " << pathName_ << std::endl;

  auto const& triggerNames(hltPrescaleProvider_.hltConfigProvider().triggerNames());
  for (auto const& iPathName : triggerNames) {
    if (ignorePathVersion_) {
      auto const iPathNameUnv(iPathName.substr(0, iPathName.rfind("_v")));
      if (iPathNameUnv != pathName_) {
        continue;
      }
    } else {
      if (iPathName != pathName_) {
        continue;
      }
    }
    
    // std::cout << "iPathName: " << iPathName << std::endl;

    ++numMatches;

    if (numMatches > 1) {
      edm::LogError("Logic") << "Attempting to overwrite output products -> new match for path name \"" << pathName_
                             << "\" will be ignored: " << iPathName << " (original match was \"" << originalMatch
                             << "\")";
      continue;
    } else {
      originalMatch = iPathName;
    }

    const uint iPathIndex(hltPrescaleProvider_.hltConfigProvider().triggerIndex(iPathName));
    if (iPathIndex >= triggerResults->size()) {
      edm::LogError("Logic") << "Index associated to path \"" << iPathName << "\" (" << iPathIndex
                             << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
                             << ") -> path will be ignored";
      continue;
    }

    LogTrace("") << "[TriggerFlagsProducer::produce]       "
                 << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                 << "\") = " << iPathIndex;

    LogTrace("") << "[TriggerFlagsProducer::produce]       moduleLabels";

    int hltL1TSeedModuleIndex(-1), hltPrescaleModuleIndex(-1), hltPathLastModuleIndex(-1);

    auto const lastModuleExecutedInPath(
        hltPrescaleProvider_.hltConfigProvider().moduleLabel(iPathIndex, triggerResults->index(iPathIndex)));
    
    // std::cout << "lastModuleExecutedInPath: " << lastModuleExecutedInPath << std::endl;

    auto const& moduleLabels(hltPrescaleProvider_.hltConfigProvider().moduleLabels(iPathIndex));
    for (size_t idx = 0; idx < moduleLabels.size(); ++idx) {
      auto const& moduleLabel(moduleLabels.at(idx));  
      
      if (moduleLabel == lastModuleExecutedInPath) {
        hltPathLastModuleIndex = idx;
      }

      if ((hltPrescaleProvider_.hltConfigProvider().moduleEDMType(moduleLabel) != "EDFilter") or
          (moduleLabel == "hltTriggerType") or (moduleLabel == "hltBoolEnd")) {
        continue;
      }

      if (moduleLabel.find("hltL1s", 0) == 0) {
        if ((hltL1TSeedModuleIndex < 0) and (hltPrescaleModuleIndex < 0)) {
          hltL1TSeedModuleIndex = idx;
        } else if (hltL1TSeedModuleIndex >= 0) {
          throw cms::Exception("InputError") << "found more than one match for L1T-Seed module of HLT-Path"
                                             << " (1st match = \"" << moduleLabels.at(hltL1TSeedModuleIndex)
                                             << "\", 2nd match = \"" << moduleLabel << "\")"
                                             << ", HLT-Path = \"" << iPathName << "\"";
        } else {
          throw cms::Exception("InputError")
              << "found L1T-Seed module of HLT-Path after its HLT-Prescale module"
              << " (L1T-Seed module = \"" << moduleLabel
              << ", HLT-Prescale module = " << moduleLabels.at(hltPrescaleModuleIndex) << "\")"
              << ", HLT-Path = \"" << iPathName << "\"";
        }
      }

      if (moduleLabel.find("hltPre", 0) == 0) {
        if ((hltL1TSeedModuleIndex >= 0) and (hltPrescaleModuleIndex < 0)) {
          // std::cout << "prescale moduleLabel: " << moduleLabel << std::endl;
          hltPrescaleModuleIndex = idx;
        } else if (hltPrescaleModuleIndex >= 0) {
          throw cms::Exception("InputError") << "found more than one match for HLT-Prescale module of HLT-Path"
                                             << " (1st match = \"" << moduleLabels.at(hltPrescaleModuleIndex)
                                             << "\", 2nd match = \"" << moduleLabel << "\")"
                                             << ", HLT-Path = \"" << iPathName << "\"";
        } else {
          throw cms::Exception("InputError")
              << "found HLT-Prescale module of HLT-Path before its L1T-Seed module"
              << " (HLT-Prescale module = \"" << moduleLabel << "\"), HLT-Path = \"" << iPathName << "\"";
        }
      }

      LogTrace("") << "[TriggerFlagsProducer::produce]         " << moduleLabel;
    }

    if (hltPathLastModuleIndex < 0) {
      throw cms::Exception("InputError") << "failed to find last module executed in the HLT-Path: " << iPathName;
    } else if (hltL1TSeedModuleIndex < 0) {
      throw cms::Exception("InputError") << "failed to find L1T-Seed module of HLT-Path: " << iPathName;
    } else if (hltPrescaleModuleIndex < 0) {
      throw cms::Exception("InputError") << "failed to find HLT-Prescale module of HLT-Path: " << iPathName;
    }

    if(hltL1TSeedModuleIndex>=0){
      LogTrace("") << "[TriggerFlagsProducer::produce]       "
                 << "hltL1TSeedModuleIndex = " << hltL1TSeedModuleIndex << " (\""
                 << moduleLabels.at(hltL1TSeedModuleIndex) << "\")";
    }

    LogTrace("") << "[TriggerFlagsProducer::produce]       "
                 << "hltPrescaleModuleIndex = " << hltPrescaleModuleIndex << " (\""
                 << moduleLabels.at(hltPrescaleModuleIndex) << "\")";

    LogTrace("") << "[TriggerFlagsProducer::produce]       "
                 << "hltPathLastModuleIndex = " << hltPathLastModuleIndex << " (\""
                 << moduleLabels.at(hltPathLastModuleIndex) << "\")";
    if(hltL1TSeedModuleIndex<0){
      l1tSeedAccept = false;
    }else{
      l1tSeedAccept = (hltL1TSeedModuleIndex == hltPathLastModuleIndex)
                        ? triggerResults->accept(iPathIndex)
                        : (hltL1TSeedModuleIndex < hltPathLastModuleIndex);
    }
    
    // std::cout << "hltPrescaleModuleIndex: " << hltPrescaleModuleIndex << std::endl;
    // std::cout << "hltPathLastModuleIndex: " << hltPathLastModuleIndex << std::endl;
    hltPathPrescaled =
        (hltPrescaleModuleIndex == hltPathLastModuleIndex) ? (not triggerResults->accept(iPathIndex)) : false;
    hltPathAccept = triggerResults->accept(iPathIndex);

    LogTrace("") << "[TriggerFlagsProducer::produce]       hltL1TSeeds";
    auto const& hltL1TSeeds(hltPrescaleProvider_.hltConfigProvider().hltL1TSeeds(iPathIndex));

    if (hltL1TSeeds.empty()) {
      edm::LogWarning("Input") << "No L1T-Seed expression associated to the HLT-Path \"" << iPathName << "\""
                               << " (hltL1TSeeds.size() = " << hltL1TSeeds.size()
                               << ") -- L1T-related flags will be set to \"false\"";
    } else if (hltL1TSeeds.size() == 1) {
      auto l1tSeedExpr(hltL1TSeeds.at(0));
      if (l1tSeedExpr.empty()) {
        throw cms::Exception("Input") << "value of L1T-Seed expression is empty";
      } else if (l1tSeedExpr == "L1GlobalDecision") {
        throw cms::Exception("Input") << "Unsupported case: HLT-Path \"" << iPathName
                                      << "\" seeded at L1T by \"L1GlobalDecision\"";
      } else {
        LogTrace("") << "[TriggerFlagsProducer::produce]        " << l1tSeedExpr;
        // logical expression of L1T seed [ref: HLTL1Seed plugin]
        //  - three instances (initial, interm, final)
        //  - note: use GlobalLogicParser ctor with (non-const) std::string& - add/remove spaces if needed
        bool l1tSeedAcceptFromL1GlobalUtilInitial(false), l1tSeedAcceptFromL1GlobalUtilInterm(false),
            l1tSeedAcceptFromL1GlobalUtilFinal(false);

        // GlobalLogicParser - Initial
        //std::cout << l1tSeedExpr << std::endl;
        auto l1AlgoLogicParserInitial = GlobalLogicParser(l1tSeedExpr);
        auto& l1AlgoLogicParserInitial_opTokenVector = l1AlgoLogicParserInitial.operandTokenVector();
        for (auto& token_i : l1AlgoLogicParserInitial_opTokenVector) {
          auto const& l1tSeedName(token_i.tokenName);

          bool decInitial(false);
          auto const decInitialIsValid(l1GlobalUtils.getInitialDecisionByName(l1tSeedName, decInitial));

          if (decInitialIsValid) {
            token_i.tokenResult = decInitial;
          } else {
            edm::LogWarning("Input")
                << "call to HLTPrescaleProvider::l1GlobalUtils().getInitialDecisionByName(\"" << l1tSeedName
                << "\", bool&) did not succeed -> result of L1T-Seed set to \"false\" (HLT-Path = \"" << iPathName
                << "\")";

            token_i.tokenResult = false;
          }

          LogTrace("") << "[TriggerFlagsProducer::produce]           " << l1tSeedName
                       << " getInitialDecisionByName = " << decInitial << " (valid = " << decInitialIsValid << ")";
        }
        l1tSeedAcceptFromL1GlobalUtilInitial = l1AlgoLogicParserInitial.expressionResult();

        // GlobalLogicParser - Interm
        auto l1AlgoLogicParserInterm = GlobalLogicParser(l1tSeedExpr);
        auto& l1AlgoLogicParserInterm_opTokenVector = l1AlgoLogicParserInterm.operandTokenVector();
        for (auto& token_i : l1AlgoLogicParserInterm_opTokenVector) {
          auto const& l1tSeedName(token_i.tokenName);

          bool decInterm(false);
          auto const decIntermIsValid(l1GlobalUtils.getIntermDecisionByName(l1tSeedName, decInterm));

          if (decIntermIsValid) {
            token_i.tokenResult = decInterm;
          } else {
            edm::LogWarning("Input")
                << "call to HLTPrescaleProvider::l1GlobalUtils().getIntermDecisionByName(\"" << l1tSeedName
                << "\", bool&) did not succeed -> result of L1T-Seed set to \"false\" (HLT-Path = \"" << iPathName
                << "\")";

            token_i.tokenResult = false;
          }

          LogTrace("") << "[TriggerFlagsProducer::produce]           " << l1tSeedName
                       << " getIntermDecisionByName = " << decInterm << " (valid = " << decIntermIsValid << ")";
        }
        l1tSeedAcceptFromL1GlobalUtilInterm = l1AlgoLogicParserInterm.expressionResult();

        // GlobalLogicParser - Final
        auto l1AlgoLogicParserFinal = GlobalLogicParser(l1tSeedExpr);
        auto& l1AlgoLogicParserFinal_opTokenVector = l1AlgoLogicParserFinal.operandTokenVector();
        for (auto& token_i : l1AlgoLogicParserFinal_opTokenVector) {
          auto const& l1tSeedName(token_i.tokenName);

          bool decFinal(false);
          auto const decFinalIsValid(l1GlobalUtils.getFinalDecisionByName(l1tSeedName, decFinal));

          if (decFinalIsValid) {
            token_i.tokenResult = decFinal;
          } else {
            edm::LogWarning("Input")
                << "call to HLTPrescaleProvider::l1GlobalUtils().getFinalDecisionByName(\"" << l1tSeedName
                << "\", bool&) did not succeed -> result of L1T-Seed set to \"false\" (HLT-Path = \"" << iPathName
                << "\")";

            token_i.tokenResult = false;
          }

          LogTrace("") << "[TriggerFlagsProducer::produce]           " << l1tSeedName
                       << " getFinalDecisionByName = " << decFinal << " (valid = " << decFinalIsValid << ")";
        }
        l1tSeedAcceptFromL1GlobalUtilFinal = l1AlgoLogicParserFinal.expressionResult();
        
        // consistency check between HLT-Path and L1GlobalUtil
        if (hltL1TSeedModuleIndex <= hltPathLastModuleIndex) {
          if (l1tSeedAccept != l1tSeedAcceptFromL1GlobalUtilFinal) {
            if(hltL1TSeedModuleIndex>=0){
              throw cms::Exception("Input") << "Return value of L1T-Seed module of HLT-Path (" << l1tSeedAccept
                                          << ") differs from value returned by the HLTPrescaleProvider::l1tGlobalUtil ("
                                          << l1tSeedAcceptFromL1GlobalUtilFinal << "): " << iPathName;
            }
          }
        }

        // l1tSeedPrescaledOrMasked
        //std::cout << iPathName << std::endl;
        // std::cout << l1tSeedAcceptFromL1GlobalUtilInitial << std::endl;
        // std::cout << l1tSeedAcceptFromL1GlobalUtilInterm << std::endl;
        // std::cout << l1tSeedAcceptFromL1GlobalUtilFinal << std::endl;
        // modify this to get the prescale:
        l1tSeedPrescaledOrMasked = (l1tSeedAcceptFromL1GlobalUtilInitial != l1tSeedAcceptFromL1GlobalUtilFinal);
        l1tSeedInitialDecision = l1tSeedAcceptFromL1GlobalUtilInitial;
        l1tSeedFinalDecision = l1tSeedAcceptFromL1GlobalUtilFinal;

        LogTrace("") << "[TriggerFlagsProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedAcceptFromL1GlobalUtilInitial = " << l1tSeedAcceptFromL1GlobalUtilInitial;
        LogTrace("") << "[TriggerFlagsProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedAcceptFromL1GlobalUtilInterm = " << l1tSeedAcceptFromL1GlobalUtilInterm;
        LogTrace("") << "[TriggerFlagsProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedAcceptFromL1GlobalUtilFinal = " << l1tSeedAcceptFromL1GlobalUtilFinal;
        LogTrace("") << "[TriggerFlagsProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedPrescaledOrMasked = " << l1tSeedPrescaledOrMasked;
      }
    } else {
      edm::LogError("Input") << "Unsupported case: HLT-Path does not use a unique L1T-Seed expression"
                             << " (hltL1TSeeds.size() = " << hltL1TSeeds.size()
                             << ") -- L1T-related output products will be set to \"false\"";
    }

    LogTrace("") << "[TriggerFlagsProducer::produce]       "
                 << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                 << "\") = " << iPathIndex << " l1tSeedAccept = " << l1tSeedAccept
                 << " l1tSeedPrescaledOrMasked = " << l1tSeedPrescaledOrMasked
                 << " hltPathPrescaled = " << hltPathPrescaled << " hltPathAccept = " << hltPathAccept;
  }

  if (numMatches < 1) {
    edm::LogWarning("Output") << "Zero matches found for path name \"" << pathName_
                              << "\" --> all output products will be \"false\"";
  }

  LogTrace("") << "[TriggerFlagsProducer::produce]       "
               << "Path = \"" << originalMatch << ", l1tSeedAccept = " << l1tSeedAccept
               << ", l1tSeedPrescaledOrMasked = " << l1tSeedPrescaledOrMasked
               << ", hltPathPrescaled = " << hltPathPrescaled << ", hltPathAccept = " << hltPathAccept;
  
  // std::cout << "l1tSeedPrescaledOrMasked: " << l1tSeedPrescaledOrMasked << std::endl;
  // std::cout << "l1tSeedAccept: " << l1tSeedAccept << std::endl;
  // std::cout << "hltPathPrescaled: " << hltPathPrescaled << std::endl;
  // std::cout << "hltPathAccept: " << hltPathAccept << std::endl;

  auto out_l1tSeedAccept = std::make_unique<bool>(l1tSeedAccept);
  auto out_l1tSeedPrescaledOrMasked = std::make_unique<bool>(l1tSeedPrescaledOrMasked);
  auto out_l1tSeedInitialDecision = std::make_unique<bool>(l1tSeedInitialDecision);
  auto out_l1tSeedFinalDecision = std::make_unique<bool>(l1tSeedFinalDecision);
  auto out_hltPathPrescaled = std::make_unique<bool>(hltPathPrescaled);
  auto out_hltPathAccept = std::make_unique<bool>(hltPathAccept);

  iEvent.put(std::move(out_l1tSeedAccept), "L1TSeedAccept");
  iEvent.put(std::move(out_l1tSeedPrescaledOrMasked), "L1TSeedPrescaledOrMasked");
  iEvent.put(std::move(out_hltPathPrescaled), "HLTPathPrescaled");
  iEvent.put(std::move(out_hltPathAccept), "HLTPathAccept");
  iEvent.put(std::move(out_l1tSeedInitialDecision), "L1TSeedInitialDecision");
  iEvent.put(std::move(out_l1tSeedFinalDecision), "L1TSeedFinalDecision");
}

void TriggerFlagsProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("TriggerResults", "", "HLT"));
  desc.add<std::string>("pathName", "");
  desc.add<bool>("ignorePathVersion", false);
  desc.add<uint>("stageL1Trigger", 2);
  descriptions.add("triggerFlagsProducer", desc);
}

DEFINE_FWK_MODULE(TriggerFlagsProducer);
