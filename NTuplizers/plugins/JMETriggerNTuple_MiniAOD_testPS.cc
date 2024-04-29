#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "JMETriggerAnalysis/NTuplizers/interface/TriggerResultsContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/ValueContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoVertexCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/L1TPFCandidateCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFCandidateCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATPackedCandidateCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoGenJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/L1TPFJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoCaloJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFClusterJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATJetCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoGenMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoCaloMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFClusterMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/RecoPFMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATMETCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATMuonCollectionContainer.h"
#include "JMETriggerAnalysis/NTuplizers/interface/PATElectronCollectionContainer.h"


#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "CommonTools/TriggerUtils/interface/GenericTriggerEventFlag.h"

#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESWatcher.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "FWCore/Utilities/interface/ESGetToken.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "CondFormats/L1TObjects/interface/L1GtTriggerMenu.h"
#include "CondFormats/DataRecord/interface/L1GtTriggerMenuRcd.h"
#include "CondFormats/HLTObjects/interface/AlCaRecoTriggerBits.h"
#include "CondFormats/DataRecord/interface/AlCaRecoTriggerBitsRcd.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerEvmReadoutRecord.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "DataFormats/OnlineMetaData/interface/DCSRecord.h"
#include "L1Trigger/GlobalTriggerAnalyzer/interface/L1GtUtils.h"
#include "L1Trigger/L1TGlobal/interface/L1TGlobalUtil.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include <string>
#include <vector>
#include <memory>
#include <algorithm>
#include <unordered_map>

#include <Compression.h>
#include <TTree.h>

class JMETriggerNTuple_MiniAOD_testPS : public edm::one::EDAnalyzer<edm::one::SharedResources> {
public:
  explicit JMETriggerNTuple_MiniAOD_testPS(const edm::ParameterSet&);
  static void fillDescriptions(edm::ConfigurationDescriptions&);

protected:
  void analyze(const edm::Event&, const edm::EventSetup&) override;

  template <typename... Args>
  void addBranch(const std::string&, Args...);

  bool passesTriggerResults_OR(const edm::TriggerResults&, const edm::Event&, const std::vector<std::string>&);
  bool passesTriggerResults_AND(const edm::TriggerResults&, const edm::Event&, const std::vector<std::string>&);

  std::string const TTreeName_;

  bool const consumeHepMCProduct_;
  bool const consumeGenEventInfoProduct_;
  bool const consumePileupSummaryInfo_;
  
  std::vector<std::string> const TriggerResultsFilterOR_;
  std::vector<std::string> const TriggerResultsFilterAND_;

  std::vector<std::string> const outputBranchesToBeDropped_;
  // std::vector<uint> const SelectionRun_;
  // std::vector<uint> const SelectionLumi_;
  // std::vector<uint> const SelectionEvent_;

  std::unordered_map<std::string, std::string> stringCutObjectSelectors_map_;

  edm::EDGetTokenT<edm::HepMCProduct> hepMCProductToken_;
  edm::EDGetTokenT<GenEventInfoProduct> genEventInfoProductToken_;
  edm::EDGetTokenT<edm::View<PileupSummaryInfo>> pileupInfoToken_;

  std::unique_ptr<TriggerResultsContainer> triggerResultsContainer_ptr_;
  std::vector<ValueContainer<bool>> v_boolContainer_;
  std::vector<ValueContainer<int>> v_intContainer_;
  std::vector<ValueContainer<float>> v_floatContainer_;
  std::vector<ValueContainer<double>> v_doubleContainer_;
  std::vector<ValueContainer<std::vector<bool>>> v_vboolContainer_;
  std::vector<ValueContainer<std::vector<int>>> v_vintContainer_;
  std::vector<ValueContainer<std::vector<float>>> v_vfloatContainer_;
  std::vector<ValueContainer<std::vector<double>>> v_vdoubleContainer_;
  std::vector<RecoVertexCollectionContainer> v_recoVertexCollectionContainer_;
  std::vector<L1TPFCandidateCollectionContainer> v_l1tPFCandidateCollectionContainer_;
  std::vector<RecoPFCandidateCollectionContainer> v_recoPFCandidateCollectionContainer_;
  std::vector<PATPackedCandidateCollectionContainer> v_patPackedCandidateCollectionContainer_;
  std::vector<RecoGenJetCollectionContainer> v_recoGenJetCollectionContainer_;
  std::vector<L1TPFJetCollectionContainer> v_l1tPFJetCollectionContainer_;
  std::vector<RecoCaloJetCollectionContainer> v_recoCaloJetCollectionContainer_;
  std::vector<RecoPFJetCollectionContainer> v_recoPFJetCollectionContainer_;
  std::vector<RecoPFClusterJetCollectionContainer> v_recoPFClusterJetCollectionContainer_;
  std::vector<PATJetCollectionContainer> v_patJetCollectionContainer_;
  std::vector<RecoGenMETCollectionContainer> v_recoGenMETCollectionContainer_;
  std::vector<RecoMETCollectionContainer> v_recoMETCollectionContainer_;
  std::vector<RecoCaloMETCollectionContainer> v_recoCaloMETCollectionContainer_;
  std::vector<RecoPFClusterMETCollectionContainer> v_recoPFClusterMETCollectionContainer_;
  std::vector<RecoPFMETCollectionContainer> v_recoPFMETCollectionContainer_;
  std::vector<PATMETCollectionContainer> v_patMETCollectionContainer_;
  std::vector<PATMuonCollectionContainer> v_patMuonCollectionContainer_;
  std::vector<PATElectronCollectionContainer> v_patElectronCollectionContainer_;

  TTree* ttree_ = nullptr;
  
  bool createSkim_;
  bool createTriggerQuantities_;

  edm::EDGetTokenT<pat::JetCollection> jetsToken;
  edm::EDGetTokenT<pat::MuonCollection> muonsToken;
  edm::EDGetTokenT<pat::METCollection> metToken;

  edm::Handle<pat::JetCollection> jets;
  edm::Handle<pat::MuonCollection> muons;
  edm::Handle<pat::METCollection> met;
  
  // function that checks for JetID 
  bool  isGoodJet(const pat::Jet &jet);

  // quantities for branches in case createTriggerQuantities_ is used
  double leadingJetPt_ = 0.;
  double met_ = 0.;
  double ht_ = 0.;

  unsigned int run_ = 0;
  unsigned int luminosityBlock_ = 0;
  unsigned long long event_ = 0;

  float hepMCGenEvent_scale_ = -1.f;
  float genEventInfo_qScale_ = -1.f;

  int pileupInfo_BX0_numPUInteractions_ = -1;
  float pileupInfo_BX0_numTrueInteractions_ = -1.f;
  float pileupInfo_BX0_max_pT_hats_ = -1.f;
  uint pileupInfo_BX0_n_pThat000to020_ = 0;
  uint pileupInfo_BX0_n_pThat020to030_ = 0;
  uint pileupInfo_BX0_n_pThat030to050_ = 0;
  uint pileupInfo_BX0_n_pThat050to080_ = 0;
  uint pileupInfo_BX0_n_pThat080to120_ = 0;
  uint pileupInfo_BX0_n_pThat120to170_ = 0;
  uint pileupInfo_BX0_n_pThat170to300_ = 0;
  uint pileupInfo_BX0_n_pThat300to470_ = 0;
  uint pileupInfo_BX0_n_pThat470to600_ = 0;
  uint pileupInfo_BX0_n_pThat600toInf_ = 0;

  class FillCollectionConditionsMap {
  public:
    explicit FillCollectionConditionsMap();

    void clear();
    int init(const edm::ParameterSet&);

    struct condition {
      condition(const std::string& a_path, const bool a_accept = false) : path(a_path), accept(a_accept) {}

      const std::string path;
      bool accept;
    };

    bool has(const std::string&) const;
    const condition& at(const std::string&) const;
    bool accept(const std::string&) const;
    int update(const edm::TriggerResults&, const edm::Event&);

  protected:
    std::map<std::string, condition> condMap_;
  };

  FillCollectionConditionsMap fillCollectionConditionMap_;

  template <typename VAL_TYPE>
  int initValueContainers(std::vector<ValueContainer<VAL_TYPE>>&,
                          const std::string&,
                          const edm::ParameterSet&,
                          const VAL_TYPE);

  template <typename VAL_TYPE>
  void fillValueContainers(std::vector<ValueContainer<VAL_TYPE>>&,
                           const FillCollectionConditionsMap&,
                           const edm::Event&);

  template <typename COLL_CONTAINER_TYPE, typename OBJ_TYPE>
  int initCollectionContainer(const edm::ParameterSet&,
                              std::vector<COLL_CONTAINER_TYPE>&,
                              std::string const&,
                              std::string const&,
                              std::unordered_map<std::string, std::string> const&);

  template <typename COLL_CONTAINER_TYPE, typename OBJ_TYPE>
  void fillCollectionContainer(edm::Event const& iEvent,
                               std::vector<COLL_CONTAINER_TYPE>& v_collectionContainer,
                               FillCollectionConditionsMap const&);
};

JMETriggerNTuple_MiniAOD_testPS::JMETriggerNTuple_MiniAOD_testPS(const edm::ParameterSet& iConfig)
    : TTreeName_(iConfig.getParameter<std::string>("TTreeName")),
      consumeHepMCProduct_(iConfig.exists("HepMCProduct")),
      consumeGenEventInfoProduct_(iConfig.exists("GenEventInfoProduct")),
      consumePileupSummaryInfo_(iConfig.exists("PileupSummaryInfo")),
      TriggerResultsFilterOR_(iConfig.getParameter<std::vector<std::string>>("TriggerResultsFilterOR")),
      TriggerResultsFilterAND_(iConfig.getParameter<std::vector<std::string>>("TriggerResultsFilterAND")),
      outputBranchesToBeDropped_(iConfig.getParameter<std::vector<std::string>>("outputBranchesToBeDropped")) {
      // SelectionRun_(iConfig.getParameter<std::vector<uint>>("SelectionRun")),
      // SelectionLumi_(iConfig.getParameter<std::vector<uint>>("SelectionLumi")),
      // SelectionEvent_(iConfig.getParameter<std::vector<uint>>("SelectionEvent")) {
  const auto& TriggerResultsInputTag = iConfig.getParameter<edm::InputTag>("TriggerResults");
  const auto& TriggerResultsCollections = iConfig.getParameter<std::vector<std::string>>("TriggerResultsCollections");

  triggerResultsContainer_ptr_.reset(
      new TriggerResultsContainer(TriggerResultsCollections,
                                  TriggerResultsInputTag.label(),
                                  this->consumes<edm::TriggerResults>(TriggerResultsInputTag)));

  // fillCollectionConditions
  fillCollectionConditionMap_.clear();

  if (iConfig.exists("fillCollectionConditions")) {
    fillCollectionConditionMap_.init(iConfig.getParameter<edm::ParameterSet>("fillCollectionConditions"));
  }

  // make skim
  createSkim_= iConfig.getUntrackedParameter<bool>("createSkim",false);
  createTriggerQuantities_ = iConfig.getUntrackedParameter<bool>("createTriggerQuantities",false);
  jetsToken             = consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jets"));
  muonsToken            = consumes<pat::MuonCollection>(iConfig.getParameter<edm::InputTag>("muons"));
  metToken              = consumes<pat::METCollection>(iConfig.getParameter<edm::InputTag>("met"));
  
  // stringCutObjectSelectors
  stringCutObjectSelectors_map_.clear();

  if (iConfig.exists("stringCutObjectSelectors")) {
    const edm::ParameterSet& pset_stringCutObjectSelectors =
        iConfig.getParameter<edm::ParameterSet>("stringCutObjectSelectors");

    const auto& stringCutObjectSelectors_labels = pset_stringCutObjectSelectors.getParameterNamesForType<std::string>();

    for (const auto& label : stringCutObjectSelectors_labels) {
      stringCutObjectSelectors_map_[label] = pset_stringCutObjectSelectors.getParameter<std::string>(label);
    }
  }

  if (consumeHepMCProduct_) {
    hepMCProductToken_ = this->consumes<edm::HepMCProduct>(iConfig.getParameter<edm::InputTag>("HepMCProduct"));
  }

  if (consumeGenEventInfoProduct_) {
    genEventInfoProductToken_ =
        this->consumes<GenEventInfoProduct>(iConfig.getParameter<edm::InputTag>("GenEventInfoProduct"));
  }

  if (consumePileupSummaryInfo_) {
    pileupInfoToken_ =
        this->consumes<edm::View<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("PileupSummaryInfo"));
  }

  // bools
  this->initValueContainers(v_boolContainer_, "bools", iConfig, false);

  // ints
  this->initValueContainers(v_intContainer_, "ints", iConfig, -999);

  // floats
  this->initValueContainers(v_floatContainer_, "floats", iConfig, -999.f);

  // doubles
  this->initValueContainers(v_doubleContainer_, "doubles", iConfig, -999.);

  // vbools
  this->initValueContainers(v_vboolContainer_, "vbools", iConfig, std::vector<bool>());

  // vints
  this->initValueContainers(v_vintContainer_, "vints", iConfig, std::vector<int>());

  // vfloats
  this->initValueContainers(v_vfloatContainer_, "vfloats", iConfig, std::vector<float>());

  // vdoubles
  this->initValueContainers(v_vdoubleContainer_, "vdoubles", iConfig, std::vector<double>());

  // reco::VertexCollection
  initCollectionContainer<RecoVertexCollectionContainer, reco::Vertex>(iConfig,
                                                                       v_recoVertexCollectionContainer_,
                                                                       "recoVertexCollections",
                                                                       "reco::VertexCollection",
                                                                       stringCutObjectSelectors_map_);

  // l1t::PFCandidateCollection
  initCollectionContainer<L1TPFCandidateCollectionContainer, l1t::PFCandidate>(iConfig,
                                                                               v_l1tPFCandidateCollectionContainer_,
                                                                               "l1tPFCandidateCollections",
                                                                               "l1t::PFCandidateCollection",
                                                                               stringCutObjectSelectors_map_);
  for (auto& cc_i : v_l1tPFCandidateCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // reco::PFCandidateCollection
  initCollectionContainer<RecoPFCandidateCollectionContainer, reco::PFCandidate>(iConfig,
                                                                                 v_recoPFCandidateCollectionContainer_,
                                                                                 "recoPFCandidateCollections",
                                                                                 "reco::PFCandidateCollection",
                                                                                 stringCutObjectSelectors_map_);
  for (auto& cc_i : v_recoPFCandidateCollectionContainer_) {
    cc_i.orderByHighestPt(false);
  }

  // pat::PackedCandidateCollection
  initCollectionContainer<PATPackedCandidateCollectionContainer, pat::PackedCandidate>(
      iConfig,
      v_patPackedCandidateCollectionContainer_,
      "patPackedCandidateCollections",
      "pat::PackedCandidateCollection",
      stringCutObjectSelectors_map_);
  for (auto& cc_i : v_patPackedCandidateCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // reco::GenJetCollection
  initCollectionContainer<RecoGenJetCollectionContainer, reco::GenJet>(iConfig,
                                                                       v_recoGenJetCollectionContainer_,
                                                                       "recoGenJetCollections",
                                                                       "reco::GenJetCollection",
                                                                       stringCutObjectSelectors_map_);
  for (auto& cc_i : v_recoGenJetCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // l1t::PFJetCollection
  initCollectionContainer<L1TPFJetCollectionContainer, l1t::PFJet>(iConfig,
                                                                   v_l1tPFJetCollectionContainer_,
                                                                   "l1tPFJetCollections",
                                                                   "l1t::PFJetCollection",
                                                                   stringCutObjectSelectors_map_);
  for (auto& cc_i : v_l1tPFJetCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // reco::CaloJetCollection
  initCollectionContainer<RecoCaloJetCollectionContainer, reco::CaloJet>(iConfig,
                                                                         v_recoCaloJetCollectionContainer_,
                                                                         "recoCaloJetCollections",
                                                                         "reco::CaloJetCollection",
                                                                         stringCutObjectSelectors_map_);
  for (auto& cc_i : v_recoCaloJetCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // reco::PFClusterJetCollection
  initCollectionContainer<RecoPFClusterJetCollectionContainer, reco::PFClusterJet>(
      iConfig,
      v_recoPFClusterJetCollectionContainer_,
      "recoPFClusterJetCollections",
      "reco::PFClusterJetCollection",
      stringCutObjectSelectors_map_);
  for (auto& cc_i : v_recoPFClusterJetCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // reco::PFJetCollection
  initCollectionContainer<RecoPFJetCollectionContainer, reco::PFJet>(iConfig,
                                                                     v_recoPFJetCollectionContainer_,
                                                                     "recoPFJetCollections",
                                                                     "reco::PFJetCollection",
                                                                     stringCutObjectSelectors_map_);
  for (auto& cc_i : v_recoPFJetCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // pat::JetCollection
  initCollectionContainer<PATJetCollectionContainer, pat::Jet>(
      iConfig, v_patJetCollectionContainer_, "patJetCollections", "pat::JetCollection", stringCutObjectSelectors_map_);
  for (auto& cc_i : v_patJetCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // reco::GenMETCollection
  initCollectionContainer<RecoGenMETCollectionContainer, reco::GenMET>(iConfig,
                                                                       v_recoGenMETCollectionContainer_,
                                                                       "recoGenMETCollections",
                                                                       "reco::GenMETCollection",
                                                                       stringCutObjectSelectors_map_);

  // reco::METCollection
  initCollectionContainer<RecoMETCollectionContainer, reco::MET>(iConfig,
                                                                 v_recoMETCollectionContainer_,
                                                                 "recoMETCollections",
                                                                 "reco::METCollection",
                                                                 stringCutObjectSelectors_map_);

  // reco::CaloMETCollection
  initCollectionContainer<RecoCaloMETCollectionContainer, reco::CaloMET>(iConfig,
                                                                         v_recoCaloMETCollectionContainer_,
                                                                         "recoCaloMETCollections",
                                                                         "reco::CaloMETCollection",
                                                                         stringCutObjectSelectors_map_);

  // reco::PFClusterMETCollection
  initCollectionContainer<RecoPFClusterMETCollectionContainer, reco::PFClusterMET>(
      iConfig,
      v_recoPFClusterMETCollectionContainer_,
      "recoPFClusterMETCollections",
      "reco::PFClusterMETCollection",
      stringCutObjectSelectors_map_);

  // reco::PFMETCollection
  initCollectionContainer<RecoPFMETCollectionContainer, reco::PFMET>(iConfig,
                                                                     v_recoPFMETCollectionContainer_,
                                                                     "recoPFMETCollections",
                                                                     "reco::PFMETCollection",
                                                                     stringCutObjectSelectors_map_);

  // pat::METCollection
  initCollectionContainer<PATMETCollectionContainer, pat::MET>(
      iConfig, v_patMETCollectionContainer_, "patMETCollections", "pat::METCollection", stringCutObjectSelectors_map_);

  // pat::MuonCollection
  initCollectionContainer<PATMuonCollectionContainer, pat::Muon>(iConfig,
                                                                 v_patMuonCollectionContainer_,
                                                                 "patMuonCollections",
                                                                 "pat::MuonCollection",
                                                                 stringCutObjectSelectors_map_);
  for (auto& cc_i : v_patMuonCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // pat::ElectronCollection
  initCollectionContainer<PATElectronCollectionContainer, pat::Electron>(iConfig,
                                                                         v_patElectronCollectionContainer_,
                                                                         "patElectronCollections",
                                                                         "pat::ElectronCollection",
                                                                         stringCutObjectSelectors_map_);
  for (auto& cc_i : v_patElectronCollectionContainer_) {
    cc_i.orderByHighestPt(true);
  }

  // output TTree
  usesResource(TFileService::kSharedResource);

  edm::Service<TFileService> fs;

  if (not fs) {
    throw edm::Exception(edm::errors::Configuration, "TFileService is not registered in cfg file");
  }

  ttree_ = fs->make<TTree>(TTreeName_.c_str(), TTreeName_.c_str());

  if (not ttree_) {
    throw edm::Exception(edm::errors::Configuration, "failed to create TTree via TFileService::make<TTree>");
  }
  
  // add branches for trigger if option is activated
  if(createTriggerQuantities_){
    this->addBranch("leadingJet_pt", &leadingJetPt_);
    this->addBranch("met",&met_);
    this->addBranch("ht",&ht_);
  }

  this->addBranch("run", &run_);
  this->addBranch("luminosityBlock", &luminosityBlock_);
  this->addBranch("event", &event_);
  
  
  if(iConfig.exists("HepMCProduct")){
    this->addBranch("HepMCGenEvent_scale", &hepMCGenEvent_scale_);
    this->addBranch("GenEventInfo_qScale", &genEventInfo_qScale_);

    this->addBranch("pileupInfo_BX0_numPUInteractions", &pileupInfo_BX0_numPUInteractions_);
    this->addBranch("pileupInfo_BX0_numTrueInteractions", &pileupInfo_BX0_numTrueInteractions_);
    this->addBranch("pileupInfo_BX0_max_pT_hats", &pileupInfo_BX0_max_pT_hats_);

    this->addBranch("pileupInfo_BX0_n_pThat000to020", &pileupInfo_BX0_n_pThat000to020_);
    this->addBranch("pileupInfo_BX0_n_pThat020to030", &pileupInfo_BX0_n_pThat020to030_);
    this->addBranch("pileupInfo_BX0_n_pThat030to050", &pileupInfo_BX0_n_pThat030to050_);
    this->addBranch("pileupInfo_BX0_n_pThat050to080", &pileupInfo_BX0_n_pThat050to080_);
    this->addBranch("pileupInfo_BX0_n_pThat080to120", &pileupInfo_BX0_n_pThat080to120_);
    this->addBranch("pileupInfo_BX0_n_pThat120to170", &pileupInfo_BX0_n_pThat120to170_);
    this->addBranch("pileupInfo_BX0_n_pThat170to300", &pileupInfo_BX0_n_pThat170to300_);
    this->addBranch("pileupInfo_BX0_n_pThat300to470", &pileupInfo_BX0_n_pThat300to470_);
    this->addBranch("pileupInfo_BX0_n_pThat470to600", &pileupInfo_BX0_n_pThat470to600_);
    this->addBranch("pileupInfo_BX0_n_pThat600toInf", &pileupInfo_BX0_n_pThat600toInf_);
  }

  for (const auto& triggerEntry_i : triggerResultsContainer_ptr_->entries()) {
    this->addBranch(triggerEntry_i.name, const_cast<bool*>(&triggerEntry_i.accept));
  }

  for (const auto& triggerEntry_i : triggerResultsContainer_ptr_->entries()) {
    this->addBranch(triggerEntry_i.name + "_wasrun", const_cast<bool*>(&triggerEntry_i.wasrun));
  }

  for (auto& boolContainer_i : v_boolContainer_) {
    this->addBranch(boolContainer_i.name(), &boolContainer_i.value());
  }

  for (auto& intContainer_i : v_intContainer_) {
    this->addBranch(intContainer_i.name(), &intContainer_i.value());
  }

  for (auto& floatContainer_i : v_floatContainer_) {
    this->addBranch(floatContainer_i.name(), &floatContainer_i.value());
  }

  for (auto& doubleContainer_i : v_doubleContainer_) {
    this->addBranch(doubleContainer_i.name(), &doubleContainer_i.value());
  }

  for (auto& vboolContainer_i : v_vboolContainer_) {
    this->addBranch(vboolContainer_i.name(), &vboolContainer_i.value());
  }

  for (auto& vintContainer_i : v_vintContainer_) {
    this->addBranch(vintContainer_i.name(), &vintContainer_i.value());
  }

  for (auto& vfloatContainer_i : v_vfloatContainer_) {
    this->addBranch(vfloatContainer_i.name(), &vfloatContainer_i.value());
  }

  for (auto& vdoubleContainer_i : v_vdoubleContainer_) {
    this->addBranch(vdoubleContainer_i.name(), &vdoubleContainer_i.value());
  }

  for (auto& recoVertexCollectionContainer_i : v_recoVertexCollectionContainer_) {
    this->addBranch(recoVertexCollectionContainer_i.name() + "_tracksSize",
                    &recoVertexCollectionContainer_i.vec_tracksSize());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_isFake", &recoVertexCollectionContainer_i.vec_isFake());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_chi2", &recoVertexCollectionContainer_i.vec_chi2());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_ndof", &recoVertexCollectionContainer_i.vec_ndof());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_x", &recoVertexCollectionContainer_i.vec_x());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_y", &recoVertexCollectionContainer_i.vec_y());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_z", &recoVertexCollectionContainer_i.vec_z());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_xError", &recoVertexCollectionContainer_i.vec_xError());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_yError", &recoVertexCollectionContainer_i.vec_yError());
    this->addBranch(recoVertexCollectionContainer_i.name() + "_zError", &recoVertexCollectionContainer_i.vec_zError());
  }

  for (auto& l1tPFCandidateCollectionContainer_i : v_l1tPFCandidateCollectionContainer_) {
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_pdgId",
                    &l1tPFCandidateCollectionContainer_i.vec_pdgId());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_pt", &l1tPFCandidateCollectionContainer_i.vec_pt());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_eta",
                    &l1tPFCandidateCollectionContainer_i.vec_eta());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_phi",
                    &l1tPFCandidateCollectionContainer_i.vec_phi());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_mass",
                    &l1tPFCandidateCollectionContainer_i.vec_mass());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_vx", &l1tPFCandidateCollectionContainer_i.vec_vx());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_vy", &l1tPFCandidateCollectionContainer_i.vec_vy());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_vz", &l1tPFCandidateCollectionContainer_i.vec_vz());
    this->addBranch(l1tPFCandidateCollectionContainer_i.name() + "_puppiWeight",
                    &l1tPFCandidateCollectionContainer_i.vec_puppiWeight());
  }

  for (auto& recoPFCandidateCollectionContainer_i : v_recoPFCandidateCollectionContainer_) {
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_pdgId",
                    &recoPFCandidateCollectionContainer_i.vec_pdgId());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_pt",
                    &recoPFCandidateCollectionContainer_i.vec_pt());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_eta",
                    &recoPFCandidateCollectionContainer_i.vec_eta());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_phi",
                    &recoPFCandidateCollectionContainer_i.vec_phi());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_mass",
                    &recoPFCandidateCollectionContainer_i.vec_mass());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_rawEcalEnergy",
                    &recoPFCandidateCollectionContainer_i.vec_rawEcalEnergy());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_rawHcalEnergy",
                    &recoPFCandidateCollectionContainer_i.vec_rawHcalEnergy());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_ecalEnergy",
                    &recoPFCandidateCollectionContainer_i.vec_ecalEnergy());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_hcalEnergy",
                    &recoPFCandidateCollectionContainer_i.vec_hcalEnergy());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_vx",
                    &recoPFCandidateCollectionContainer_i.vec_vx());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_vy",
                    &recoPFCandidateCollectionContainer_i.vec_vy());
    this->addBranch(recoPFCandidateCollectionContainer_i.name() + "_vz",
                    &recoPFCandidateCollectionContainer_i.vec_vz());
  }

  for (auto& patPackedCandidateCollectionContainer_i : v_patPackedCandidateCollectionContainer_) {
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_pdgId",
                    &patPackedCandidateCollectionContainer_i.vec_pdgId());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_pt",
                    &patPackedCandidateCollectionContainer_i.vec_pt());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_eta",
                    &patPackedCandidateCollectionContainer_i.vec_eta());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_phi",
                    &patPackedCandidateCollectionContainer_i.vec_phi());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_mass",
                    &patPackedCandidateCollectionContainer_i.vec_mass());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_vx",
                    &patPackedCandidateCollectionContainer_i.vec_vx());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_vy",
                    &patPackedCandidateCollectionContainer_i.vec_vy());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_vz",
                    &patPackedCandidateCollectionContainer_i.vec_vz());
    this->addBranch(patPackedCandidateCollectionContainer_i.name() + "_fromPV",
                    &patPackedCandidateCollectionContainer_i.vec_fromPV());
  }

  for (auto& recoGenJetCollectionContainer_i : v_recoGenJetCollectionContainer_) {
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_pt", &recoGenJetCollectionContainer_i.vec_pt());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_eta", &recoGenJetCollectionContainer_i.vec_eta());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_phi", &recoGenJetCollectionContainer_i.vec_phi());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_mass", &recoGenJetCollectionContainer_i.vec_mass());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_numberOfDaughters",
                    &recoGenJetCollectionContainer_i.vec_numberOfDaughters());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_chargedHadronEnergyFraction",
                    &recoGenJetCollectionContainer_i.vec_chargedHadronEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_neutralHadronEnergyFraction",
                    &recoGenJetCollectionContainer_i.vec_neutralHadronEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_electronEnergyFraction",
                    &recoGenJetCollectionContainer_i.vec_electronEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_photonEnergyFraction",
                    &recoGenJetCollectionContainer_i.vec_photonEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_muonEnergyFraction",
                    &recoGenJetCollectionContainer_i.vec_muonEnergyFraction());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_chargedHadronMultiplicity",
                    &recoGenJetCollectionContainer_i.vec_chargedHadronMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_neutralHadronMultiplicity",
                    &recoGenJetCollectionContainer_i.vec_neutralHadronMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_electronMultiplicity",
                    &recoGenJetCollectionContainer_i.vec_electronMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_photonMultiplicity",
                    &recoGenJetCollectionContainer_i.vec_photonMultiplicity());
    this->addBranch(recoGenJetCollectionContainer_i.name() + "_muonMultiplicity",
                    &recoGenJetCollectionContainer_i.vec_muonMultiplicity());
  }

  for (auto& l1tPFJetCollectionContainer_i : v_l1tPFJetCollectionContainer_) {
    this->addBranch(l1tPFJetCollectionContainer_i.name() + "_pt", &l1tPFJetCollectionContainer_i.vec_pt());
    this->addBranch(l1tPFJetCollectionContainer_i.name() + "_eta", &l1tPFJetCollectionContainer_i.vec_eta());
    this->addBranch(l1tPFJetCollectionContainer_i.name() + "_phi", &l1tPFJetCollectionContainer_i.vec_phi());
    this->addBranch(l1tPFJetCollectionContainer_i.name() + "_mass", &l1tPFJetCollectionContainer_i.vec_mass());
    this->addBranch(l1tPFJetCollectionContainer_i.name() + "_jesc", &l1tPFJetCollectionContainer_i.vec_jesc());
    this->addBranch(l1tPFJetCollectionContainer_i.name() + "_numberOfDaughters",
                    &l1tPFJetCollectionContainer_i.vec_numberOfDaughters());
  }

  for (auto& recoCaloJetCollectionContainer_i : v_recoCaloJetCollectionContainer_) {
    this->addBranch(recoCaloJetCollectionContainer_i.name() + "_pt", &recoCaloJetCollectionContainer_i.vec_pt());
    this->addBranch(recoCaloJetCollectionContainer_i.name() + "_eta", &recoCaloJetCollectionContainer_i.vec_eta());
    this->addBranch(recoCaloJetCollectionContainer_i.name() + "_phi", &recoCaloJetCollectionContainer_i.vec_phi());
    this->addBranch(recoCaloJetCollectionContainer_i.name() + "_mass", &recoCaloJetCollectionContainer_i.vec_mass());
    this->addBranch(recoCaloJetCollectionContainer_i.name() + "_numberOfDaughters",
                    &recoCaloJetCollectionContainer_i.vec_numberOfDaughters());
  }

  for (auto& recoPFClusterJetCollectionContainer_i : v_recoPFClusterJetCollectionContainer_) {
    this->addBranch(recoPFClusterJetCollectionContainer_i.name() + "_pt",
                    &recoPFClusterJetCollectionContainer_i.vec_pt());
    this->addBranch(recoPFClusterJetCollectionContainer_i.name() + "_eta",
                    &recoPFClusterJetCollectionContainer_i.vec_eta());
    this->addBranch(recoPFClusterJetCollectionContainer_i.name() + "_phi",
                    &recoPFClusterJetCollectionContainer_i.vec_phi());
    this->addBranch(recoPFClusterJetCollectionContainer_i.name() + "_mass",
                    &recoPFClusterJetCollectionContainer_i.vec_mass());
    this->addBranch(recoPFClusterJetCollectionContainer_i.name() + "_numberOfDaughters",
                    &recoPFClusterJetCollectionContainer_i.vec_numberOfDaughters());
  }

  for (auto& recoPFJetCollectionContainer_i : v_recoPFJetCollectionContainer_) {
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_pt", &recoPFJetCollectionContainer_i.vec_pt());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_eta", &recoPFJetCollectionContainer_i.vec_eta());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_phi", &recoPFJetCollectionContainer_i.vec_phi());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_mass", &recoPFJetCollectionContainer_i.vec_mass());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_jesc", &recoPFJetCollectionContainer_i.vec_jesc());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_jetArea", &recoPFJetCollectionContainer_i.vec_jetArea());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_numberOfDaughters",
                    &recoPFJetCollectionContainer_i.vec_numberOfDaughters());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_chargedHadronEnergyFraction",
                    &recoPFJetCollectionContainer_i.vec_chargedHadronEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_neutralHadronEnergyFraction",
                    &recoPFJetCollectionContainer_i.vec_neutralHadronEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_electronEnergyFraction",
                    &recoPFJetCollectionContainer_i.vec_electronEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_photonEnergyFraction",
                    &recoPFJetCollectionContainer_i.vec_photonEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_muonEnergyFraction",
                    &recoPFJetCollectionContainer_i.vec_muonEnergyFraction());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_chargedHadronMultiplicity",
                    &recoPFJetCollectionContainer_i.vec_chargedHadronMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_neutralHadronMultiplicity",
                    &recoPFJetCollectionContainer_i.vec_neutralHadronMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_electronMultiplicity",
                    &recoPFJetCollectionContainer_i.vec_electronMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_photonMultiplicity",
                    &recoPFJetCollectionContainer_i.vec_photonMultiplicity());
    this->addBranch(recoPFJetCollectionContainer_i.name() + "_muonMultiplicity",
                    &recoPFJetCollectionContainer_i.vec_muonMultiplicity());
  }

  for (auto& patJetCollectionContainer_i : v_patJetCollectionContainer_) {
    this->addBranch(patJetCollectionContainer_i.name() + "_multiplicity",
                    &patJetCollectionContainer_i.getCollectionSize());
    this->addBranch(patJetCollectionContainer_i.name() + "_pt", &patJetCollectionContainer_i.vec_pt());
    this->addBranch(patJetCollectionContainer_i.name() + "_eta", &patJetCollectionContainer_i.vec_eta());
    this->addBranch(patJetCollectionContainer_i.name() + "_phi", &patJetCollectionContainer_i.vec_phi());
    this->addBranch(patJetCollectionContainer_i.name() + "_mass", &patJetCollectionContainer_i.vec_mass());
    this->addBranch(patJetCollectionContainer_i.name() + "_jesc", &patJetCollectionContainer_i.vec_jesc());
    this->addBranch(patJetCollectionContainer_i.name() + "_jetArea", &patJetCollectionContainer_i.vec_jetArea());
    this->addBranch(patJetCollectionContainer_i.name() + "_numberOfDaughters", &patJetCollectionContainer_i.vec_numberOfDaughters());
    this->addBranch(patJetCollectionContainer_i.name() + "_jetID", &patJetCollectionContainer_i.vec_jetID());
    this->addBranch(patJetCollectionContainer_i.name() + "_chargedHadronEnergyFraction",
                    &patJetCollectionContainer_i.vec_chargedHadronEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name() + "_neutralHadronEnergyFraction",
                    &patJetCollectionContainer_i.vec_neutralHadronEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name() + "_electronEnergyFraction",
                    &patJetCollectionContainer_i.vec_electronEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name() + "_photonEnergyFraction",
                    &patJetCollectionContainer_i.vec_photonEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name() + "_muonEnergyFraction",
                    &patJetCollectionContainer_i.vec_muonEnergyFraction());
    this->addBranch(patJetCollectionContainer_i.name() + "_chargedHadronMultiplicity",
                    &patJetCollectionContainer_i.vec_chargedHadronMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name() + "_neutralHadronMultiplicity",
                    &patJetCollectionContainer_i.vec_neutralHadronMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name() + "_electronMultiplicity",
                    &patJetCollectionContainer_i.vec_electronMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name() + "_photonMultiplicity",
                    &patJetCollectionContainer_i.vec_photonMultiplicity());
    this->addBranch(patJetCollectionContainer_i.name() + "_muonMultiplicity",
                    &patJetCollectionContainer_i.vec_muonMultiplicity());
  }

  for (auto& recoGenMETCollectionContainer_i : v_recoGenMETCollectionContainer_) {
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_pt", &recoGenMETCollectionContainer_i.vec_pt());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_phi", &recoGenMETCollectionContainer_i.vec_phi());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_sumEt", &recoGenMETCollectionContainer_i.vec_sumEt());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_NeutralEMEtFraction",
                    &recoGenMETCollectionContainer_i.vec_NeutralEMEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_NeutralHadEtFraction",
                    &recoGenMETCollectionContainer_i.vec_NeutralHadEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_ChargedEMEtFraction",
                    &recoGenMETCollectionContainer_i.vec_ChargedEMEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_ChargedHadEtFraction",
                    &recoGenMETCollectionContainer_i.vec_ChargedHadEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_MuonEtFraction",
                    &recoGenMETCollectionContainer_i.vec_MuonEtFraction());
    this->addBranch(recoGenMETCollectionContainer_i.name() + "_InvisibleEtFraction",
                    &recoGenMETCollectionContainer_i.vec_InvisibleEtFraction());
  }

  for (auto& recoCaloMETCollectionContainer_i : v_recoCaloMETCollectionContainer_) {
    this->addBranch(recoCaloMETCollectionContainer_i.name() + "_pt", &recoCaloMETCollectionContainer_i.vec_pt());
    this->addBranch(recoCaloMETCollectionContainer_i.name() + "_phi", &recoCaloMETCollectionContainer_i.vec_phi());
    this->addBranch(recoCaloMETCollectionContainer_i.name() + "_sumEt", &recoCaloMETCollectionContainer_i.vec_sumEt());
  }

  for (auto& recoMETCollectionContainer_i : v_recoMETCollectionContainer_) {
    this->addBranch(recoMETCollectionContainer_i.name() + "_pt", &recoMETCollectionContainer_i.vec_pt());
    this->addBranch(recoMETCollectionContainer_i.name() + "_phi", &recoMETCollectionContainer_i.vec_phi());
    this->addBranch(recoMETCollectionContainer_i.name() + "_sumEt", &recoMETCollectionContainer_i.vec_sumEt());
  }

  for (auto& recoPFClusterMETCollectionContainer_i : v_recoPFClusterMETCollectionContainer_) {
    this->addBranch(recoPFClusterMETCollectionContainer_i.name() + "_pt",
                    &recoPFClusterMETCollectionContainer_i.vec_pt());
    this->addBranch(recoPFClusterMETCollectionContainer_i.name() + "_phi",
                    &recoPFClusterMETCollectionContainer_i.vec_phi());
    this->addBranch(recoPFClusterMETCollectionContainer_i.name() + "_sumEt",
                    &recoPFClusterMETCollectionContainer_i.vec_sumEt());
  }

  for (auto& recoPFMETCollectionContainer_i : v_recoPFMETCollectionContainer_) {
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_pt", &recoPFMETCollectionContainer_i.vec_pt());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_phi", &recoPFMETCollectionContainer_i.vec_phi());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_sumEt", &recoPFMETCollectionContainer_i.vec_sumEt());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_NeutralEMFraction",
                    &recoPFMETCollectionContainer_i.vec_NeutralEMFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_NeutralHadEtFraction",
                    &recoPFMETCollectionContainer_i.vec_NeutralHadEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_ChargedEMEtFraction",
                    &recoPFMETCollectionContainer_i.vec_ChargedEMEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_ChargedHadEtFraction",
                    &recoPFMETCollectionContainer_i.vec_ChargedHadEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_MuonEtFraction",
                    &recoPFMETCollectionContainer_i.vec_MuonEtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_Type6EtFraction",
                    &recoPFMETCollectionContainer_i.vec_Type6EtFraction());
    this->addBranch(recoPFMETCollectionContainer_i.name() + "_Type7EtFraction",
                    &recoPFMETCollectionContainer_i.vec_Type7EtFraction());
  }

  for (auto& patMETCollectionContainer_i : v_patMETCollectionContainer_) {
    this->addBranch(patMETCollectionContainer_i.name() + "_Raw_pt", &patMETCollectionContainer_i.vec_Raw_pt());
    this->addBranch(patMETCollectionContainer_i.name() + "_Raw_phi", &patMETCollectionContainer_i.vec_Raw_phi());
    this->addBranch(patMETCollectionContainer_i.name() + "_Raw_sumEt", &patMETCollectionContainer_i.vec_Raw_sumEt());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type1_pt", &patMETCollectionContainer_i.vec_Type1_pt());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type1_phi", &patMETCollectionContainer_i.vec_Type1_phi());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type1_sumEt",
                    &patMETCollectionContainer_i.vec_Type1_sumEt());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type1XY_pt", &patMETCollectionContainer_i.vec_Type1XY_pt());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type1XY_phi",
                    &patMETCollectionContainer_i.vec_Type1XY_phi());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type1XY_sumEt",
                    &patMETCollectionContainer_i.vec_Type1XY_sumEt());
    this->addBranch(patMETCollectionContainer_i.name() + "_NeutralEMFraction",
                    &patMETCollectionContainer_i.vec_NeutralEMFraction());
    this->addBranch(patMETCollectionContainer_i.name() + "_NeutralHadEtFraction",
                    &patMETCollectionContainer_i.vec_NeutralHadEtFraction());
    this->addBranch(patMETCollectionContainer_i.name() + "_ChargedEMEtFraction",
                    &patMETCollectionContainer_i.vec_ChargedEMEtFraction());
    this->addBranch(patMETCollectionContainer_i.name() + "_ChargedHadEtFraction",
                    &patMETCollectionContainer_i.vec_ChargedHadEtFraction());
    this->addBranch(patMETCollectionContainer_i.name() + "_MuonEtFraction",
                    &patMETCollectionContainer_i.vec_MuonEtFraction());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type6EtFraction",
                    &patMETCollectionContainer_i.vec_Type6EtFraction());
    this->addBranch(patMETCollectionContainer_i.name() + "_Type7EtFraction",
                    &patMETCollectionContainer_i.vec_Type7EtFraction());
  }

  for (auto& patMuonCollectionContainer_i : v_patMuonCollectionContainer_) {
    this->addBranch(patMuonCollectionContainer_i.name() + "_multiplicity",
                    &patMuonCollectionContainer_i.getCollectionSize());
    this->addBranch(patMuonCollectionContainer_i.name() + "_pdgId", &patMuonCollectionContainer_i.vec_pdgId());
    this->addBranch(patMuonCollectionContainer_i.name() + "_pt", &patMuonCollectionContainer_i.vec_pt());
    this->addBranch(patMuonCollectionContainer_i.name() + "_eta", &patMuonCollectionContainer_i.vec_eta());
    this->addBranch(patMuonCollectionContainer_i.name() + "_phi", &patMuonCollectionContainer_i.vec_phi());
    this->addBranch(patMuonCollectionContainer_i.name() + "_mass", &patMuonCollectionContainer_i.vec_mass());
    this->addBranch(patMuonCollectionContainer_i.name() + "_vx", &patMuonCollectionContainer_i.vec_vx());
    this->addBranch(patMuonCollectionContainer_i.name() + "_vy", &patMuonCollectionContainer_i.vec_vy());
    this->addBranch(patMuonCollectionContainer_i.name() + "_vz", &patMuonCollectionContainer_i.vec_vz());
    this->addBranch(patMuonCollectionContainer_i.name() + "_dxyPV", &patMuonCollectionContainer_i.vec_dxyPV());
    this->addBranch(patMuonCollectionContainer_i.name() + "_dzPV", &patMuonCollectionContainer_i.vec_dzPV());
    this->addBranch(patMuonCollectionContainer_i.name() + "_id", &patMuonCollectionContainer_i.vec_id());
    this->addBranch(patMuonCollectionContainer_i.name() + "_pfIso", &patMuonCollectionContainer_i.vec_pfIso());
  }

  for (auto& patElectronCollectionContainer_i : v_patElectronCollectionContainer_) {
    this->addBranch(patElectronCollectionContainer_i.name() + "_pdgId", &patElectronCollectionContainer_i.vec_pdgId());
    this->addBranch(patElectronCollectionContainer_i.name() + "_pt", &patElectronCollectionContainer_i.vec_pt());
    this->addBranch(patElectronCollectionContainer_i.name() + "_eta", &patElectronCollectionContainer_i.vec_eta());
    this->addBranch(patElectronCollectionContainer_i.name() + "_phi", &patElectronCollectionContainer_i.vec_phi());
    this->addBranch(patElectronCollectionContainer_i.name() + "_mass", &patElectronCollectionContainer_i.vec_mass());
    this->addBranch(patElectronCollectionContainer_i.name() + "_vx", &patElectronCollectionContainer_i.vec_vx());
    this->addBranch(patElectronCollectionContainer_i.name() + "_vy", &patElectronCollectionContainer_i.vec_vy());
    this->addBranch(patElectronCollectionContainer_i.name() + "_vz", &patElectronCollectionContainer_i.vec_vz());
    this->addBranch(patElectronCollectionContainer_i.name() + "_dxyPV", &patElectronCollectionContainer_i.vec_dxyPV());
    this->addBranch(patElectronCollectionContainer_i.name() + "_dzPV", &patElectronCollectionContainer_i.vec_dzPV());
    this->addBranch(patElectronCollectionContainer_i.name() + "_id", &patElectronCollectionContainer_i.vec_id());
    this->addBranch(patElectronCollectionContainer_i.name() + "_pfIso", &patElectronCollectionContainer_i.vec_pfIso());
    this->addBranch(patElectronCollectionContainer_i.name() + "_etaSC", &patElectronCollectionContainer_i.vec_etaSC());
  }

  // settings for output TFile and TTree
  fs->file().SetCompressionAlgorithm(ROOT::ECompressionAlgorithm::kLZ4);
  fs->file().SetCompressionLevel(4);

  for (int idx = 0; idx < ttree_->GetListOfBranches()->GetEntries(); ++idx) {
    TBranch* br = dynamic_cast<TBranch*>(ttree_->GetListOfBranches()->At(idx));
    if (br) {
      br->SetBasketSize(1024 * 1024);
    }
  }

  if (ttree_->GetListOfBranches()->GetEntries() > 0) {
    ttree_->SetAutoFlush(-1024 * 1024 * ttree_->GetListOfBranches()->GetEntries());
  }
}

bool JMETriggerNTuple_MiniAOD_testPS::isGoodJet(const pat::Jet &jet){
  float chf = jet.chargedHadronEnergyFraction();
  float nhf = jet.neutralHadronEnergyFraction();
  float phf = jet.photonEnergyFraction();
  float muf = jet.muonEnergyFraction();
  float elf = jet.electronEnergyFraction();
  int chm   = jet.chargedHadronMultiplicity();
  int neutral_npr = jet.neutralMultiplicity();
  int charged_npr = jet.chargedMultiplicity();
  int npr = neutral_npr + charged_npr;
  float eta = fabs(jet.eta());
  // note: these are the 2022 BCDE jetID criteria
  bool idTightLepVeto = ((eta<=2.6 && nhf<0.90 && phf<0.90 && npr>1 && muf<0.80  && chf>0.01 && chm>0 && elf<0.80) || 
  ((eta>2.6 && eta<=2.7 ) && nhf<0.90 && phf<0.99 && muf<0.80 && elf<0.80) ||
  ((eta>2.7 && eta<=3.0 ) && nhf<0.9999) ||
  ((eta>3.0 && eta<=5.0 ) && phf<0.90 && neutral_npr>2) ||
  (eta>5.0)
  );
  // if you want the FG you can use the one bellow instead
  /*
  bool idTightLepVeto = ((eta<=2.6 && nhf<0.99 && phf<0.90 && npr>1 && muf<0.80  && chf>0.01 && chm>0 && elf<0.80) || 
  ((eta>2.6 && eta<=2.7 ) && nhf<0.90 && phf<0.99 && muf<0.80 && elf<0.80) ||
  ((eta>2.7 && eta<=3.0 ) && nhf<0.9999) ||
  ((eta>3.0 && eta<=5.0 ) && phf<0.90 && neutral_npr>2) ||
  (eta>5.0)
  );
  */
  return idTightLepVeto;
}

void JMETriggerNTuple_MiniAOD_testPS::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  run_ = iEvent.id().run();
  luminosityBlock_ = iEvent.id().luminosityBlock();
  event_ = iEvent.id().event();

  // use specific events to fill ////////////////////////////////////////////
  // bool foundEvent=false;
  // for(unsigned int i=0;i<SelectionRun_.size();i++){
  //   //std::cout << SelectionRun_[i] << std::endl;
  //   if(run_==SelectionRun_[i] && luminosityBlock_==SelectionLumi_[i] && event_==SelectionEvent_[i]){
  //     foundEvent=true;
  //   }
  // }

  // if(!foundEvent){
  //   return;
  // }
  ///////////////////////////////////////////////////////////////////////////
  
  // get objects 
  iEvent.getByToken(jetsToken,jets);
  iEvent.getByToken(muonsToken,muons);
  iEvent.getByToken(metToken,met);
  
  leadingJetPt_ = 0.;
  met_ = 0.;
  ht_ = 0.;

  // Assisting variables
  bool leadingJetIsGood=false; // this checks if the leading jet has tightID - if not event will be rejected.
  bool isLeptonMatched=false; // this checks if the leading jet is matched to the selected muon(s) (userMuons)
  float DRmax = 0.4; // maximum DR for matching

  // if create skim is used then return for events that don't pass the selections
  if(createSkim_){
    // muons selections
    // pt>30GeV , abs(eta) < 2.4, ID tight , pfIso < 0.15 are assumed to exist from the filter on the collection
    // so needs only to require one such muon
    if(!( muons->size()==1 )) return;
    
    // jets have looser requirements ((pt > 30.) && (abs(eta) < 5.0) so we can also calculate the ht quantity
    // note: ht triggers use abs(eta)<2.5 and pt>30GeV 
    // initially require a jet to exist
    if(!( jets->size()>0 )) return;
    
    // loop over jets to find leadingJet_pt and calculate ht
    for(pat::JetCollection::const_iterator ijet =jets->begin();ijet != jets->end(); ++ijet) {
      if(fabs(ijet->eta())<2.5){
        ht_ += ijet->pt();
      }

      if( ijet->pt()>leadingJetPt_ ){
        leadingJetPt_ = ijet->pt();
        // check if leading jet is matched to a Lepton
        for(pat::MuonCollection::const_iterator mu =muons->begin();mu != muons->end(); ++mu) if (deltaR(mu->eta(),mu->phi(),ijet->eta(),ijet->phi()) < DRmax) isLeptonMatched = true;
        // check if leading jet passes tightLepVeto ID
        leadingJetIsGood = (ijet->hasUserInt("PFJetIDTightLepVeto") && (ijet->userInt("PFJetIDTightLepVeto") > 0));
        //leadingJetIsGood = isGoodJet(*ijet); // the same but using the custom function not MiniAOD_testPS tools
        leadingJetIsGood = leadingJetIsGood && !isLeptonMatched;
      }
    } 
  }

  // leading jet is tight ID cut
  if (!leadingJetIsGood) return;
  
  // calculate MET
  met_ = (*met)[0].et();


  // MC: HepMCProduct
  hepMCGenEvent_scale_ = -1.f;
  if (consumeHepMCProduct_ and (not iEvent.isRealData())) {
    auto const& hepMCProduct = iEvent.get(hepMCProductToken_);
    auto const* hepMCGenEvent = hepMCProduct.GetEvent();

    if (hepMCGenEvent) {
      hepMCGenEvent_scale_ = hepMCGenEvent->event_scale();
    }
  }

  // MC: GenEventInfoProduct
  genEventInfo_qScale_ = -1.f;
  if (consumeGenEventInfoProduct_ and (not iEvent.isRealData())) {
    auto const& genEventInfo = iEvent.get(genEventInfoProductToken_);
    genEventInfo_qScale_ = genEventInfo.qScale();
  }

  // MC: PileupSummaryInfo (BX=0)
  pileupInfo_BX0_max_pT_hats_ = -1.f;

  pileupInfo_BX0_n_pThat000to020_ = 0;
  pileupInfo_BX0_n_pThat020to030_ = 0;
  pileupInfo_BX0_n_pThat030to050_ = 0;
  pileupInfo_BX0_n_pThat050to080_ = 0;
  pileupInfo_BX0_n_pThat080to120_ = 0;
  pileupInfo_BX0_n_pThat120to170_ = 0;
  pileupInfo_BX0_n_pThat170to300_ = 0;
  pileupInfo_BX0_n_pThat300to470_ = 0;
  pileupInfo_BX0_n_pThat470to600_ = 0;
  pileupInfo_BX0_n_pThat600toInf_ = 0;

  if (consumePileupSummaryInfo_ and (not iEvent.isRealData())) {
    auto const& pileupInfoView = iEvent.get(pileupInfoToken_);
    for (auto const& pileupInfo_i : pileupInfoView) {
      if (pileupInfo_i.getBunchCrossing() == 0) {
        pileupInfo_BX0_numTrueInteractions_ = pileupInfo_i.getTrueNumInteractions();
        pileupInfo_BX0_numPUInteractions_ = pileupInfo_i.getPU_NumInteractions();

        if (not pileupInfo_i.getPU_pT_hats().empty())
          pileupInfo_BX0_max_pT_hats_ =
              *std::max_element(pileupInfo_i.getPU_pT_hats().begin(), pileupInfo_i.getPU_pT_hats().end());

        for (uint idx = 0; idx <= pileupInfo_i.getPU_pT_hats().size(); ++idx) {
          auto const i_pThat = (idx == pileupInfo_i.getPU_pT_hats().size()) ? genEventInfo_qScale_
                                                                            : pileupInfo_i.getPU_pT_hats().at(idx);
          if (0. <= i_pThat and i_pThat < 20.)
            ++pileupInfo_BX0_n_pThat000to020_;
          else if (20. <= i_pThat and i_pThat < 30.)
            ++pileupInfo_BX0_n_pThat020to030_;
          else if (30. <= i_pThat and i_pThat < 50.)
            ++pileupInfo_BX0_n_pThat030to050_;
          else if (50. <= i_pThat and i_pThat < 80.)
            ++pileupInfo_BX0_n_pThat050to080_;
          else if (80. <= i_pThat and i_pThat < 120.)
            ++pileupInfo_BX0_n_pThat080to120_;
          else if (120. <= i_pThat and i_pThat < 170.)
            ++pileupInfo_BX0_n_pThat120to170_;
          else if (170. <= i_pThat and i_pThat < 300.)
            ++pileupInfo_BX0_n_pThat170to300_;
          else if (300. <= i_pThat and i_pThat < 470.)
            ++pileupInfo_BX0_n_pThat300to470_;
          else if (470. <= i_pThat and i_pThat < 600.)
            ++pileupInfo_BX0_n_pThat470to600_;
          else if (600. <= i_pThat)
            ++pileupInfo_BX0_n_pThat600toInf_;
        }
      }
    }
  }

  // fill TriggerResultsContainer
  edm::Handle<edm::TriggerResults> triggerResults_handle;
  iEvent.getByToken(triggerResultsContainer_ptr_->token(), triggerResults_handle);

  if (not triggerResults_handle.isValid()) {
    edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::analyze")
        << "invalid handle for input collection: \"" << triggerResultsContainer_ptr_->inputTagLabel()
        << "\" (NTuple branches for HLT paths)";

    triggerResultsContainer_ptr_->clear();
  } else {
    // exit method for events that do not pass the logical OR of the specified HLT paths (if any)
    if (!TriggerResultsFilterOR_.empty()) {
      if (not this->passesTriggerResults_OR(*triggerResults_handle, iEvent, TriggerResultsFilterOR_)) {
        return;
      }
    }

    // exit method for events that do not pass the logical AND of the specified HLT paths (if any)
    if (!TriggerResultsFilterAND_.empty()) {
      if (not this->passesTriggerResults_AND(*triggerResults_handle, iEvent, TriggerResultsFilterAND_)) {
        return;
      }
    }

    LogDebug("JMETriggerNTuple_MiniAOD_testPS::analyze") << "output collections will be saved to TTree";

    // fill TriggerResultsContainer
    triggerResultsContainer_ptr_->fill(*triggerResults_handle, iEvent);

    // update fill-collection conditions
    fillCollectionConditionMap_.update(*triggerResults_handle, iEvent);
  }

  // fill boolContainers
  this->fillValueContainers(v_boolContainer_, fillCollectionConditionMap_, iEvent);

  // fill intContainers
  this->fillValueContainers(v_intContainer_, fillCollectionConditionMap_, iEvent);

  // fill floatContainers
  this->fillValueContainers(v_floatContainer_, fillCollectionConditionMap_, iEvent);

  // fill doubleContainers
  this->fillValueContainers(v_doubleContainer_, fillCollectionConditionMap_, iEvent);

  // fill vboolContainers
  this->fillValueContainers(v_vboolContainer_, fillCollectionConditionMap_, iEvent);

  // fill vintContainers
  this->fillValueContainers(v_vintContainer_, fillCollectionConditionMap_, iEvent);

  // fill vfloatContainers
  this->fillValueContainers(v_vfloatContainer_, fillCollectionConditionMap_, iEvent);

  // fill vdoubleContainers
  this->fillValueContainers(v_vdoubleContainer_, fillCollectionConditionMap_, iEvent);

  // reco::Vertex
  this->fillCollectionContainer<RecoVertexCollectionContainer, reco::Vertex>(
      iEvent, v_recoVertexCollectionContainer_, fillCollectionConditionMap_);

  // l1t::PFCandidateCollection
  this->fillCollectionContainer<L1TPFCandidateCollectionContainer, l1t::PFCandidate>(
      iEvent, v_l1tPFCandidateCollectionContainer_, fillCollectionConditionMap_);

  // reco::PFCandidateCollection
  this->fillCollectionContainer<RecoPFCandidateCollectionContainer, reco::PFCandidate>(
      iEvent, v_recoPFCandidateCollectionContainer_, fillCollectionConditionMap_);

  // pat::PackedCandidateCollection
  this->fillCollectionContainer<PATPackedCandidateCollectionContainer, pat::PackedCandidate>(
      iEvent, v_patPackedCandidateCollectionContainer_, fillCollectionConditionMap_);

  // reco::GenJetCollection
  if (not iEvent.isRealData()) {
    this->fillCollectionContainer<RecoGenJetCollectionContainer, reco::GenJet>(
        iEvent, v_recoGenJetCollectionContainer_, fillCollectionConditionMap_);
  }

  // l1t::PFJetCollection
  this->fillCollectionContainer<L1TPFJetCollectionContainer, l1t::PFJet>(
      iEvent, v_l1tPFJetCollectionContainer_, fillCollectionConditionMap_);

  // reco::CaloJetCollection
  this->fillCollectionContainer<RecoCaloJetCollectionContainer, reco::CaloJet>(
      iEvent, v_recoCaloJetCollectionContainer_, fillCollectionConditionMap_);

  // reco::PFClusterJetCollection
  this->fillCollectionContainer<RecoPFClusterJetCollectionContainer, reco::PFClusterJet>(
      iEvent, v_recoPFClusterJetCollectionContainer_, fillCollectionConditionMap_);

  // reco::PFJetCollection
  this->fillCollectionContainer<RecoPFJetCollectionContainer, reco::PFJet>(
      iEvent, v_recoPFJetCollectionContainer_, fillCollectionConditionMap_);

  // pat::JetCollection
  this->fillCollectionContainer<PATJetCollectionContainer, pat::Jet>(
      iEvent, v_patJetCollectionContainer_, fillCollectionConditionMap_);

  // reco::GenMETCollection
  if (not iEvent.isRealData()) {
    this->fillCollectionContainer<RecoGenMETCollectionContainer, reco::GenMET>(
        iEvent, v_recoGenMETCollectionContainer_, fillCollectionConditionMap_);
  }

  // reco::METCollection
  this->fillCollectionContainer<RecoMETCollectionContainer, reco::MET>(
      iEvent, v_recoMETCollectionContainer_, fillCollectionConditionMap_);

  // reco::CaloMETCollection
  this->fillCollectionContainer<RecoCaloMETCollectionContainer, reco::CaloMET>(
      iEvent, v_recoCaloMETCollectionContainer_, fillCollectionConditionMap_);

  // reco::PFClusterMETCollection
  this->fillCollectionContainer<RecoPFClusterMETCollectionContainer, reco::PFClusterMET>(
      iEvent, v_recoPFClusterMETCollectionContainer_, fillCollectionConditionMap_);

  // reco::PFMETCollection
  this->fillCollectionContainer<RecoPFMETCollectionContainer, reco::PFMET>(
      iEvent, v_recoPFMETCollectionContainer_, fillCollectionConditionMap_);

  // pat::METCollection
  this->fillCollectionContainer<PATMETCollectionContainer, pat::MET>(
      iEvent, v_patMETCollectionContainer_, fillCollectionConditionMap_);

  // pat::MuonCollection
  this->fillCollectionContainer<PATMuonCollectionContainer, pat::Muon>(
      iEvent, v_patMuonCollectionContainer_, fillCollectionConditionMap_);

  // pat::ElectronCollection
  this->fillCollectionContainer<PATElectronCollectionContainer, pat::Electron>(
      iEvent, v_patElectronCollectionContainer_, fillCollectionConditionMap_);

  // fill TTree
  ttree_->Fill();
}

template <typename... Args>
void JMETriggerNTuple_MiniAOD_testPS::addBranch(const std::string& branch_name, Args... args) {
  if (ttree_) {
    if (std::find(outputBranchesToBeDropped_.begin(), outputBranchesToBeDropped_.end(), branch_name) ==
        outputBranchesToBeDropped_.end()) {
      if (ttree_->GetBranch(branch_name.c_str())) {
        throw cms::Exception("JMETriggerNTuple_MiniAOD_testPS::addBranch")
            << "output branch \"" << branch_name
            << "\" already exists (there was an attempt to create another TBranch with the same name)";
      } else {
        ttree_->Branch(branch_name.c_str(), args...);
      }
    } else {
      edm::LogInfo("JMETriggerNTuple_MiniAOD_testPS::addBranch")
          << "output branch \"" << branch_name
          << "\" will not be created (string appears in data member \"outputBranchesToBeDropped\")";
    }
  } else {
    edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::addBranch")
        << "pointer to TTree is null, output branch \"" << branch_name << "\" will not be created";
  }
}

bool JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_OR(const edm::TriggerResults& triggerResults,
                                               const edm::Event& iEvent,
                                               const std::vector<std::string>& paths) {
  if (paths.empty()) {
    edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_OR")
        << "input error: empty list of paths for event selection, will return True";
    return true;
  }

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if (triggerResults.size() != triggerNames.size()) {
    edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_OR")
        << "input error: size of TriggerResults (" << triggerResults.size() << ") and TriggerNames ("
        << triggerNames.size() << ") differ, exiting function";
    return false;
  }

  for (unsigned int idx = 0; idx < triggerResults.size(); ++idx) {
    if (triggerResults.at(idx).accept() == true) {
      const auto& triggerName = triggerNames.at(idx);

      if (std::find(paths.begin(), paths.end(), triggerName) != paths.end()) {
        LogDebug("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_OR") << "event accepted by path \"" << triggerName << "\"";
        return true;
      } else {
        const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

        if (std::find(paths.begin(), paths.end(), triggerName_unv) != paths.end()) {
          LogDebug("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_OR")
              << "event accepted by path \"" << triggerName_unv << "\"";
          return true;
        }
      }
    }
  }

  return false;
}

bool JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_AND(const edm::TriggerResults& triggerResults,
                                                const edm::Event& iEvent,
                                                const std::vector<std::string>& paths) {
  if (paths.empty()) {
    edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_AND")
        << "input error: empty list of paths for event selection, will return True";
    return true;
  }

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if (triggerResults.size() != triggerNames.size()) {
    edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_AND")
        << "input error: size of TriggerResults (" << triggerResults.size() << ") and TriggerNames ("
        << triggerNames.size() << ") differ, exiting function";

    return false;
  }

  for (unsigned int idx = 0; idx < triggerResults.size(); ++idx) {
    if (triggerResults.at(idx).accept() == false) {
      const auto& triggerName = triggerNames.at(idx);

      if (std::find(paths.begin(), paths.end(), triggerName) != paths.end()) {
        LogDebug("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_AND")
            << "event not accepted by path \"" << triggerName << "\"";
        return false;
      } else {
        const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

        if (std::find(paths.begin(), paths.end(), triggerName_unv) != paths.end()) {
          LogDebug("JMETriggerNTuple_MiniAOD_testPS::passesTriggerResults_AND")
              << "event not accepted by path \"" << triggerName_unv << "\"";
          return false;
        }
      }
    }
  }

  return true;
}

JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::FillCollectionConditionsMap() { this->clear(); }

int JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::init(const edm::ParameterSet& pset) {
  this->clear();

  const auto& pset_strings = pset.getParameterNamesForType<std::string>();

  for (const auto& name : pset_strings) {
    if (not this->has(name)) {
      condMap_.insert({name, condition(pset.getParameter<std::string>(name))});
    }
  }

  return 0;
}

void JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::clear() { condMap_.clear(); }

bool JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::has(const std::string& name) const {
  return (condMap_.find(name) != condMap_.end());
}

const JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::condition& JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::at(
    const std::string& name) const {
  if (not this->has(name)) {
    throw cms::Exception("LogicError") << "internal map has no entry associated to key \"" << name << "\"";
  }

  return condMap_.at(name);
}

bool JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::accept(const std::string& name) const {
  if (not this->has(name)) {
    throw cms::Exception("LogicError") << "internal map has no entry associated to key \"" << name << "\"";
  }

  return this->at(name).accept;
}

int JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap::update(const edm::TriggerResults& triggerResults,
                                                          const edm::Event& iEvent) {
  for (auto& map_entry : condMap_) {
    map_entry.second.accept = false;
  }

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if (triggerResults.size() != triggerNames.size()) {
    edm::LogWarning("InputError") << "size of TriggerResults (" << triggerResults.size() << ") and TriggerNames ("
                                  << triggerNames.size() << ") differ, exiting function";

    return 1;
  }

  for (unsigned int idx = 0; idx < triggerResults.size(); ++idx) {
    LogDebug("FillCollectionConditionsMap::update")
        << "path = " << triggerNames.at(idx) << ", accept = " << triggerResults.at(idx).accept();

    // since default value of condition::accept is false,
    // the value needs to be changed only for accepted paths
    if (triggerResults.at(idx).accept()) {
      const auto& triggerName = triggerNames.at(idx);
      const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

      for (auto& map_entry : condMap_) {
        // require match either full name or name without version
        if ((map_entry.second.path == triggerName_unv) || (map_entry.second.path == triggerName)) {
          map_entry.second.accept = triggerResults.at(idx).accept();

          LogDebug("FillCollectionConditionsMap::update")
              << "triggerResults entry \"" << triggerNames.at(idx) << "\" matches condition \"" << map_entry.second.path
              << "\" for collection \"" << map_entry.first << "\" (accept=" << map_entry.second.accept << ")";
        }
      }
    }
  }

  return 0;
}

template <typename VAL_TYPE>
int JMETriggerNTuple_MiniAOD_testPS::initValueContainers(std::vector<ValueContainer<VAL_TYPE>>& v_valContainers,
                                          const std::string& psetName,
                                          const edm::ParameterSet& iConfig,
                                          const VAL_TYPE defaultValue) {
  v_valContainers.clear();

  if (iConfig.exists(psetName)) {
    auto const& pset(iConfig.getParameter<edm::ParameterSet>(psetName));
    auto const& inputTagLabels(pset.getParameterNamesForType<edm::InputTag>());

    v_valContainers.reserve(inputTagLabels.size());

    for (auto const& label : inputTagLabels) {
      auto const& inputTag(pset.getParameter<edm::InputTag>(label));
      ValueContainer<VAL_TYPE> tmp(label, inputTag.label(), this->consumes<VAL_TYPE>(inputTag), defaultValue);
      v_valContainers.emplace_back(tmp);
    }

    return 0;
  }

  return 1;
}

template <typename VAL_TYPE>
void JMETriggerNTuple_MiniAOD_testPS::fillValueContainers(
    std::vector<ValueContainer<VAL_TYPE>>& v_valContainers,
    const JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap& fillCollectionConditionMap,
    const edm::Event& iEvent) {
  for (auto& valueContainer_i : v_valContainers) {
    valueContainer_i.setValue(valueContainer_i.defaultValue());

    if (fillCollectionConditionMap_.has(valueContainer_i.name()) and
        (not fillCollectionConditionMap_.accept(valueContainer_i.name()))) {
      continue;
    }

    auto const& i_handle(iEvent.getHandle(valueContainer_i.token()));

    if (not i_handle.isValid()) {
      edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::fillValueContainers")
          << "invalid handle for input collection: \"" << valueContainer_i.inputTagLabel() << "\" (NTuple branch: \""
          << valueContainer_i.name() << "\")";
    } else {
      valueContainer_i.setValue(*i_handle);
    }
  }
}

template <typename COLL_CONTAINER_TYPE, typename OBJ_TYPE>
int JMETriggerNTuple_MiniAOD_testPS::initCollectionContainer(
    const edm::ParameterSet& iConfig,
    std::vector<COLL_CONTAINER_TYPE>& v_collContainer,
    std::string const& collPSetName,
    std::string const& collTypeName,
    std::unordered_map<std::string, std::string> const& stringCutObjectSelectorsMap) {
  v_collContainer.clear();

  if (iConfig.exists(collPSetName)) {
    auto const& pset_collections(iConfig.getParameter<edm::ParameterSet>(collPSetName));

    auto const& inputTagLabels_collections(pset_collections.getParameterNamesForType<edm::InputTag>());
    v_collContainer.reserve(inputTagLabels_collections.size());

    for (auto const& label : inputTagLabels_collections) {
      auto const& inputTag(pset_collections.getParameter<edm::InputTag>(label));

      LogDebug("JMETriggerNTuple_MiniAOD_testPS::initCollectionContainer")
          << "adding " << collTypeName << " \"" << inputTag.label() << "\" (NTuple branches: \"" << label << "_*\")";

      v_collContainer.emplace_back(
          COLL_CONTAINER_TYPE(label, inputTag.label(), this->consumes<std::vector<OBJ_TYPE>>(inputTag)));

      if (stringCutObjectSelectorsMap.find(label) != stringCutObjectSelectorsMap.end()) {
        v_collContainer.back().setStringCutObjectSelector(stringCutObjectSelectorsMap.at(label));
      }
    }

    return 0;
  }

  return 1;
}

template <typename COLL_CONTAINER_TYPE, typename OBJ_TYPE>
void JMETriggerNTuple_MiniAOD_testPS::fillCollectionContainer(edm::Event const& iEvent,
                                               std::vector<COLL_CONTAINER_TYPE>& v_collectionContainer,
                                               JMETriggerNTuple_MiniAOD_testPS::FillCollectionConditionsMap const& fillConditionMap) {
  for (auto& collContainer_i : v_collectionContainer) {
    collContainer_i.clear();

    if (fillConditionMap.has(collContainer_i.name()) and (not fillConditionMap.accept(collContainer_i.name()))) {
      continue;
    }

    edm::Handle<std::vector<OBJ_TYPE>> i_handle;
    iEvent.getByToken(collContainer_i.token(), i_handle);

    if (i_handle.isValid()) {
      collContainer_i.fill(*i_handle);
    } else {
      edm::LogWarning("JMETriggerNTuple_MiniAOD_testPS::fillCollectionContainer")
          << "invalid handle for input collection: \"" << collContainer_i.inputTagLabel() << "\" (NTuple branches: \""
          << collContainer_i.name() << "_*\")";
    }
  }
}

void JMETriggerNTuple_MiniAOD_testPS::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  //  desc.add<std::string>("TTreeName", "TTreeName")->setComment("Name of TTree");
  //  desc.add<std::vector<std::string> >("TriggerResultsFilterOR")->setComment("List of HLT paths (without version) used in OR to select events in the output TTree");
  //  desc.add<std::vector<std::string> >("TriggerResultsFilterAND")->setComment("List of HLT paths (without version) used in AND to select events in the output TTree");
  //  desc.add<std::vector<std::string> >("outputBranchesToBeDropped")->setComment("Names of branches not to be included in the output TTree");
  //  desc.add<edm::InputTag>("TriggerResults", edm::InputTag("TriggerResults"))->setComment("edm::InputTag for edm::TriggerResults");
  //  desc.add<std::vector<std::string> >("TriggerResultsCollections")->setComment("List of HLT paths (without version) to be saved in the output TTree");

  //  edm::ParameterSetDescription recoCaloMETCollections;
  //  desc.add<edm::ParameterSetDescription>("recoCaloMETCollections", recoCaloMETCollections);
  descriptions.add("JMETriggerNTuple_MiniAOD_testPS", desc);
}

DEFINE_FWK_MODULE(JMETriggerNTuple_MiniAOD_testPS);
