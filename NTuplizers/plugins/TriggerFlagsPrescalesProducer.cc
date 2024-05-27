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
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"

//#include <iostream>
//#define LogTrace(X) std::cout << std::endl

class TriggerFlagsPrescalesProducer : public edm::stream::EDProducer<> {
public:
  explicit TriggerFlagsPrescalesProducer(const edm::ParameterSet&);
  ~TriggerFlagsPrescalesProducer() override = default;
  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void beginRun(edm::Run const&, edm::EventSetup const&) override;
  void produce(edm::Event&, const edm::EventSetup&) override;

  const edm::InputTag triggerResultsInputTag_;
  const edm::InputTag triggerObjectsInputTag_;
  const std::string pathName_;
  const std::string denominatorPathName_;
  const bool ignorePathVersion_;
  const bool useEmulationFromDenominator_;
  const double emulatedThreshold_;

  HLTPrescaleProvider hltPrescaleProvider_;
  bool initFailed_;
  bool skipRun_;

  edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;
  edm::EDGetTokenT<edm::View<pat::TriggerObjectStandAlone>> triggerObjectsToken_;
  
  // function to calculate the prescale weight
  // it uses the numerator trigger and the denominator trigger
  double Prescale(const std::string num,
                  const std::string den,
                  edm::Event const& iEvent,
                  edm::EventSetup const& iSetup,
                  HLTPrescaleProvider* hltPrescale_);
    
};

TriggerFlagsPrescalesProducer::TriggerFlagsPrescalesProducer(const edm::ParameterSet& iConfig)
    : triggerResultsInputTag_(iConfig.getParameter<edm::InputTag>("triggerResults")),
      triggerObjectsInputTag_(iConfig.getParameter<edm::InputTag>("triggerObjects")),
      pathName_(iConfig.getParameter<std::string>("pathName")),
      denominatorPathName_(iConfig.getParameter<std::string>("denominatorPathName")),
      ignorePathVersion_(iConfig.getParameter<bool>("ignorePathVersion")),
      useEmulationFromDenominator_(iConfig.getParameter<bool>("useEmulationFromDenominator")),
      emulatedThreshold_(iConfig.getParameter<double>("emulatedThreshold")),
      hltPrescaleProvider_(iConfig, consumesCollector(), *this),
      initFailed_(false),
      skipRun_(false) {
  if (pathName_.empty()) {
    edm::LogError("Input") << "Value of plugin argument \"pathName\" is an empty string";
    initFailed_ = true;
    return;
  }
  if (denominatorPathName_.empty()) {
    edm::LogError("Input") << "Value of plugin argument \"denominatorPathName\" is an empty string";
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
  

  if(useEmulationFromDenominator_ && triggerResultsInputTag_.process().empty()){
    edm::LogError("Input") << "Process name not specified in InputTag argument \"TriggerObjects\". Needed when \"useEmulationFromDenominator\" is used.";
    initFailed_ = true;
    return;
  } else {
    triggerObjectsToken_ = consumes<edm::View<pat::TriggerObjectStandAlone>>(triggerObjectsInputTag_);
  }
    
  if(useEmulationFromDenominator_ && emulatedThreshold_ < 0.){
    edm::LogError("Input") << "Invalid plugin argument \"emulatedThreshold\".";
    initFailed_ = true;
    return;
  }

  produces<bool>("L1TSeedAccept");
  produces<bool>("L1TSeedPrescaledOrMasked");
  produces<bool>("HLTPathPrescaled");
  produces<bool>("HLTPathAccept");
  produces<bool>("HLTDenPathAccept");
  produces<bool>("L1TSeedInitialDecision");
  produces<bool>("L1TSeedFinalDecision");
  produces<double>("HLTPathPrescaleWeight");
}

void TriggerFlagsPrescalesProducer::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {
  if (initFailed_) {
    return;
  }

  LogTrace("")
      << "[TriggerFlagsPrescalesProducer] "
      << "----------------------------------------------------------------------------------------------------";
  LogTrace("") << "[TriggerFlagsPrescalesProducer::beginRun] Run = " << iRun.id();

  // reset data members holding information from the previous run
  skipRun_ = false;

  bool hltChanged(true);
  if (hltPrescaleProvider_.init(iRun, iSetup, triggerResultsInputTag_.process(), hltChanged)) {
    LogTrace("") << "[TriggerFlagsPrescalesProducer::beginRun] HLTPrescaleProvider initialized [processName() = \""
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

void TriggerFlagsPrescalesProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (skipRun_ or initFailed_) {
    return;
  }

  LogTrace("") << "[TriggerFlagsPrescalesProducer::produce] --------------------------------------------------------";
  LogTrace("") << "[TriggerFlagsPrescalesProducer::produce] Run = " << iEvent.id().run()
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

  LogTrace("") << "[TriggerFlagsPrescalesProducer::produce] L1T Menu: " << l1GlobalUtils.gtTriggerMenuName()
               << " (version = " << l1GlobalUtils.gtTriggerMenuVersion()
               << ", type = " << hltPrescaleProvider_.hltConfigProvider().l1tType() << ")";
  LogTrace("") << "[TriggerFlagsPrescalesProducer::produce] HLT Menu: " << hltPrescaleProvider_.hltConfigProvider().tableName()
               << " (PS Column = " << psColumn << ")";

  size_t numMatches(0);
  std::string originalMatch("");

  bool l1tSeedPrescaledOrMasked(false);
  bool l1tSeedInitialDecision(false);
  bool l1tSeedFinalDecision(false);
  bool l1tSeedAccept(false);
  bool hltPathPrescaled(false);
  bool hltPathAccept(false);
  bool hltDenPathAccept(false);
  double hltPathPrescaleWeight(1.0);
  
  // std::cout << "------------" << std::endl;
  // std::cout << "pathName: " << pathName_ << std::endl;
  
  /*
  hltPathPrescaleWeight = Prescale(iPathName, denominatorPathName_, iEvent, iSetup, &hltPrescaleProvider_);
  std::cout << hltPathPrescaleWeight << std::endl;
  */
  
  std::string denPathName("");
  
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
    
    // find the denominator name in trigger names
    for (auto const& iDenPathName : triggerNames) {
      if (ignorePathVersion_) {
        auto const iDenPathNameUnv(iDenPathName.substr(0, iDenPathName.rfind("_v")));
        if (iDenPathNameUnv == denominatorPathName_) {
          denPathName = iDenPathName;
        }
      } else {
        if (iDenPathName == denominatorPathName_) {
          denPathName = iDenPathName;
        }
      }
    }
    // std::cout << "-------------------" << iPathName << std::endl;
    // std::cout << "iPathName: " << iPathName << std::endl;
    // std::cout << "denPathName: " << denPathName << std::endl;

    ++numMatches;

    if (numMatches > 1) {
      edm::LogError("Logic") << "Attempting to overwrite output products -> new match for path name \"" << pathName_
                             << "\" will be ignored: " << iPathName << " (original match was \"" << originalMatch
                             << "\")";
      continue;
    } else {
      originalMatch = iPathName;
    }
    //std::cout << iPathName << std::endl;
    //std::cout << denPathName << std::endl;
    // calculate the prescale weight 
    hltPathPrescaleWeight = Prescale(iPathName, denPathName, iEvent, iSetup, &hltPrescaleProvider_);
    //std::cout << hltPathPrescaleWeight << std::endl;

    const uint iPathIndex(hltPrescaleProvider_.hltConfigProvider().triggerIndex(iPathName));
    
    if (iPathIndex >= triggerResults->size()) {
      edm::LogError("Logic") << "Index associated to path \"" << iPathName << "\" (" << iPathIndex
                             << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
                             << ") -> path will be ignored";
      continue;
    }

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
                 << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                 << "\") = " << iPathIndex;

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       moduleLabels";

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

      LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]         " << moduleLabel;
    }

    if (hltPathLastModuleIndex < 0) {
      throw cms::Exception("InputError") << "failed to find last module executed in the HLT-Path: " << iPathName;
    } else if (hltL1TSeedModuleIndex < 0) {
      throw cms::Exception("InputError") << "failed to find L1T-Seed module of HLT-Path: " << iPathName;
    } else if (hltPrescaleModuleIndex < 0) {
      throw cms::Exception("InputError") << "failed to find HLT-Prescale module of HLT-Path: " << iPathName;
    }

    if(hltL1TSeedModuleIndex>=0){
      LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
                 << "hltL1TSeedModuleIndex = " << hltL1TSeedModuleIndex << " (\""
                 << moduleLabels.at(hltL1TSeedModuleIndex) << "\")";
    }

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
                 << "hltPrescaleModuleIndex = " << hltPrescaleModuleIndex << " (\""
                 << moduleLabels.at(hltPrescaleModuleIndex) << "\")";

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
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
    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       hltL1TSeeds";
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
        LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]        " << l1tSeedExpr;
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

          LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]           " << l1tSeedName
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

          LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]           " << l1tSeedName
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

          LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]           " << l1tSeedName
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

        LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedAcceptFromL1GlobalUtilInitial = " << l1tSeedAcceptFromL1GlobalUtilInitial;
        LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedAcceptFromL1GlobalUtilInterm = " << l1tSeedAcceptFromL1GlobalUtilInterm;
        LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedAcceptFromL1GlobalUtilFinal = " << l1tSeedAcceptFromL1GlobalUtilFinal;
        LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       " << l1tSeedExpr
                     << " l1tSeedPrescaledOrMasked = " << l1tSeedPrescaledOrMasked;
      }
    } else {
      edm::LogError("Input") << "Unsupported case: HLT-Path does not use a unique L1T-Seed expression"
                             << " (hltL1TSeeds.size() = " << hltL1TSeeds.size()
                             << ") -- L1T-related output products will be set to \"false\"";
    }

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
                 << "Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                 << "\") = " << iPathIndex << " l1tSeedAccept = " << l1tSeedAccept
                 << " l1tSeedPrescaledOrMasked = " << l1tSeedPrescaledOrMasked
                 << " hltPathPrescaled = " << hltPathPrescaled << " hltPathAccept = " << hltPathAccept;
  }

  if (numMatches < 1) {
    edm::LogWarning("Output") << "Zero matches found for path name \"" << pathName_
                              << "\" --> all output products will be \"false\"";
  }

  LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
               << "Path = \"" << originalMatch << ", l1tSeedAccept = " << l1tSeedAccept
               << ", l1tSeedPrescaledOrMasked = " << l1tSeedPrescaledOrMasked
               << ", hltPathPrescaled = " << hltPathPrescaled << ", hltPathAccept = " << hltPathAccept;
  
  // std::cout << "l1tSeedPrescaledOrMasked: " << l1tSeedPrescaledOrMasked << std::endl;
  // std::cout << "l1tSeedAccept: " << l1tSeedAccept << std::endl;
  // std::cout << "hltPathPrescaled: " << hltPathPrescaled << std::endl;
  // std::cout << "hltPathAccept: " << hltPathAccept << std::endl;
  



  // in the same way search for the denominator path and just check if it was accepted or not.
  // the final decision will be the denominator path*trigger path decision
  for (auto const& iPathName : triggerNames) {
    if (ignorePathVersion_) {
      auto const iPathNameUnv(iPathName.substr(0, iPathName.rfind("_v")));
      if (iPathNameUnv != denominatorPathName_) {
        continue;
      }
    } else {
      if (iPathName != denominatorPathName_) {
        continue;
      }
    }
  
    const uint iPathIndex(hltPrescaleProvider_.hltConfigProvider().triggerIndex(iPathName));

    if (iPathIndex >= triggerResults->size()) {
      edm::LogError("Logic") << "Index associated to denominator path \"" << iPathName << "\" (" << iPathIndex
                             << ") is inconsistent with triggerResults::size() (" << triggerResults->size()
                             << ") -> path will be ignored";
      continue;
    }

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       "
                 << "Denominator Path = \"" << iPathName << "\", HLTConfigProvider::triggerIndex(\"" << iPathName
                 << "\") = " << iPathIndex;

    LogTrace("") << "[TriggerFlagsPrescalesProducer::produce]       moduleLabels";

    auto const lastModuleExecutedInPath(
        hltPrescaleProvider_.hltConfigProvider().moduleLabel(iPathIndex, triggerResults->index(iPathIndex)));
    
    hltDenPathAccept = triggerResults->accept(iPathIndex);
    
    

    // in case the emulation method is used the trigger path decision is rewritten by the trigger object of the denominator path here
    if(useEmulationFromDenominator_){
      edm::Handle<edm::View<pat::TriggerObjectStandAlone>> triggerObjects;
      iEvent.getByToken(triggerObjectsToken_, triggerObjects);
      
      // Get the trigger names for the event
      const edm::TriggerNames& triggerNames = iEvent.triggerNames(*triggerResults);  

      // Loop over trigger objects and see which one is corresponding to the denominator path name
      //bool hasTriggerName = false;
      double trigObjPt(0.);

      for (const pat::TriggerObjectStandAlone& triggerObject : *triggerObjects) {
        pat::TriggerObjectStandAlone triggerObjectNonConst = triggerObject;
        // Unpack trigger path names and filters
        triggerObjectNonConst.unpackPathNames(triggerNames);  
        
        // if the object is found change the decision of the trigger path based on the emulated threshold
        // using the function hasPathName() with last filter to be accepted from the path:
        // bool hasPathName(const std::string &pathName,
        //              bool pathLastFilterAccepted = false,
        //              bool pathL3FilterAccepted = true)
        //if (triggerObjectNonConst.hasPathName(iPathName)){
        if (triggerObjectNonConst.hasPathName(iPathName, true, true)){
          triggerObjectNonConst.unpackFilterLabels(iEvent,*triggerResults);
          /*
          // -- usefull outputs for checks (do not remove)
          std::cout << "path name: " << iPathName << std::endl;
          std::cout << "pt: " << triggerObjectNonConst.pt() << std::endl;
          std::cout << "eta: " << triggerObjectNonConst.eta() << std::endl;
          std::cout << "phi: " << triggerObjectNonConst.phi() << std::endl;
          std::cout << "mass: " << triggerObjectNonConst.mass() << std::endl;
          std::cout << "pdgId: " << triggerObjectNonConst.pdgId() << std::endl;
          std::cout << "collection: " << triggerObjectNonConst.collection() << std::endl;
          */
          if((iPathName.find("PFJet") != std::string::npos) && triggerObjectNonConst.pdgId()==0){
            trigObjPt = triggerObjectNonConst.pt();
            break; 
          } else if((iPathName.find("PFHT") != std::string::npos) && triggerObjectNonConst.pdgId()==89){
            trigObjPt = triggerObjectNonConst.pt();
            break; 
          }
        }
      }
      
      // std::cout << trigObjPt << std::endl;
      hltPathAccept = (trigObjPt > emulatedThreshold_);
    }
  }
  

  // the trigger is considered accepted only if both the denominator trigger and the path are accepting the event
  hltPathAccept = hltPathAccept && hltDenPathAccept;
  
  // in case you use the emulator method use the L1 seed to be accepting the events as well
  if(useEmulationFromDenominator_){ 
    hltPathAccept = l1tSeedAccept && hltPathAccept;
    hltDenPathAccept = l1tSeedAccept && hltDenPathAccept;
  }

  auto out_l1tSeedAccept = std::make_unique<bool>(l1tSeedAccept);
  auto out_l1tSeedPrescaledOrMasked = std::make_unique<bool>(l1tSeedPrescaledOrMasked);
  auto out_l1tSeedInitialDecision = std::make_unique<bool>(l1tSeedInitialDecision);
  auto out_l1tSeedFinalDecision = std::make_unique<bool>(l1tSeedFinalDecision);
  auto out_hltPathPrescaled = std::make_unique<bool>(hltPathPrescaled);
  auto out_hltPathAccept = std::make_unique<bool>(hltPathAccept);
  auto out_hltDenPathAccept = std::make_unique<bool>(hltDenPathAccept);
  auto out_hltPathPrescaleWeight = std::make_unique<double>(hltPathPrescaleWeight);

  iEvent.put(std::move(out_l1tSeedAccept), "L1TSeedAccept");
  iEvent.put(std::move(out_l1tSeedPrescaledOrMasked), "L1TSeedPrescaledOrMasked");
  iEvent.put(std::move(out_hltPathPrescaled), "HLTPathPrescaled");
  iEvent.put(std::move(out_hltPathAccept), "HLTPathAccept");
  iEvent.put(std::move(out_hltDenPathAccept), "HLTDenPathAccept");
  iEvent.put(std::move(out_l1tSeedInitialDecision), "L1TSeedInitialDecision");
  iEvent.put(std::move(out_l1tSeedFinalDecision), "L1TSeedFinalDecision");
  iEvent.put(std::move(out_hltPathPrescaleWeight), "HLTPathPrescaleWeight");
}

double TriggerFlagsPrescalesProducer::Prescale(const std::string hltpath1,
                            const std::string hltpath,
                            edm::Event const& iEvent,
                            edm::EventSetup const& iSetup,
                            HLTPrescaleProvider* hltPrescale_) {
  //std::cout << "entering prescale function" << std::endl;
  double Prescale_num = 1;
  double L1P = 1, HLTP = 1;
  bool flag = true;
  std::vector<bool> theSame_den;
  std::vector<bool> theSame_num;
  // object holding L1T (double) and HLT (uint) prescales
  auto const prescales_den = hltPrescale_->prescaleValuesInDetail<double>(iEvent, iSetup, hltpath);
  auto const prescales_num = hltPrescale_->prescaleValuesInDetail<double>(iEvent, iSetup, hltpath1);

  // retrieving HLT prescale
  auto PrescaleHLT_den = prescales_den.second;
  auto PrescaleHLT_num = prescales_num.second;

  if (PrescaleHLT_den > 0 && PrescaleHLT_num > 0)
    HLTP = PrescaleHLT_num / std::min(PrescaleHLT_num, PrescaleHLT_den);
  
  //retrieving L1 prescale
  //Checking if we have the same l1 seeds in den and num
  //taking into account that they can be written in different order in num and den
  //and some of them can be also switched off

  //check if for each den l1 there is the same l1 seed in num
  if (not prescales_den.first.empty()) {
    for (size_t iSeed = 0; iSeed < prescales_den.first.size(); ++iSeed) {
      auto l1_den = prescales_den.first.at(iSeed).first;
      auto l1_denp = prescales_den.first.at(iSeed).second;
      if (l1_denp < 1)
        continue;
      flag = false;
      for (size_t iSeed1 = 0; iSeed1 < prescales_num.first.size(); ++iSeed1) {
        auto l1_num = prescales_num.first.at(iSeed1).first;
        auto l1_nump = prescales_num.first.at(iSeed1).second;
        if (l1_num == l1_den && l1_nump >= 1)  //the same seed
        {
          flag = true;
          break;
        }
      }
      theSame_den.push_back(flag);
    }
  }


  //check if for each num l1 there is the same l1 seed in den
  if (not prescales_num.first.empty()) {
    for (size_t iSeed = 0; iSeed < prescales_num.first.size(); ++iSeed) {
      auto l1_num = prescales_num.first.at(iSeed).first;
      auto l1_nump = prescales_num.first.at(iSeed).second;
      if (l1_nump < 1)
        continue;
      flag = false;
      for (size_t iSeed1 = 0; iSeed1 < prescales_den.first.size(); ++iSeed1) {
        auto l1_den = prescales_den.first.at(iSeed1).first;
        auto l1_denp = prescales_den.first.at(iSeed1).second;
        if (l1_den == l1_num && l1_denp >= 1)  //the same seed
        {
          flag = true;
          break;
        }
      }
      theSame_num.push_back(flag);
    }
  }
  
  flag = true;

  if (theSame_num.size() == theSame_den.size()) {
    for (size_t i = 0; i < theSame_num.size(); ++i) {
      if ((!theSame_num.at(i)) || (!theSame_den.at(i))) {
        flag = false;
        break;
      }
    }
  }
  
  
  if (flag && (theSame_num.size() == theSame_den.size())) {
    L1P = 1;  //den and num have the same set of l1 seeds
  } else {
    if (not prescales_num.first.empty()) {
      Prescale_num = 1;
      for (size_t iSeed = 0; iSeed < prescales_num.first.size(); ++iSeed) {
        auto l1 = prescales_num.first.at(iSeed).second;
        if (l1 < 1)
          continue;
        if (l1 == 1) {
          Prescale_num = 1;
          break;
        } else
          Prescale_num *= 1 - (1.0 / (l1));
      }
      if (Prescale_num != 1)
        Prescale_num = 1.0 / (1 - Prescale_num);
    }
    L1P = Prescale_num;
  }

  

  return L1P * HLTP;
}



void TriggerFlagsPrescalesProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("triggerResults", edm::InputTag("TriggerResults", "", "HLT"));
  desc.add<edm::InputTag>("triggerObjects",edm::InputTag("slimmedPatTrigger"));
  desc.add<std::string>("pathName", "");
  desc.add<std::string>("denominatorPathName","");
  desc.add<bool>("ignorePathVersion", false);
  desc.add<bool>("useEmulationFromDenominator", false);
  desc.add<double>("emulatedThreshold",-1.);
  desc.add<uint>("stageL1Trigger", 2);
  descriptions.add("TriggerFlagsPrescalesProducer", desc);
}

DEFINE_FWK_MODULE(TriggerFlagsPrescalesProducer);
