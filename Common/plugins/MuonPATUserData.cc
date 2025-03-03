#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/stream/EDProducer.h>
#include <FWCore/Framework/interface/Event.h>
#include <FWCore/Framework/interface/MakerMacros.h>
#include <FWCore/ParameterSet/interface/ParameterSet.h>
#include <CommonTools/Utils/interface/StringCutObjectSelector.h>
#include <CommonTools/Utils/interface/StringObjectFunction.h>
#include <DataFormats/Common/interface/ValueMap.h>
#include <DataFormats/PatCandidates/interface/Muon.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include <DataFormats/VertexReco/interface/VertexFwd.h>
#include <DataFormats/MuonReco/interface/MuonSelectors.h>

#include <string>
#include <vector>
#include <memory>
#include <utility>

class MuonPATUserData : public edm::stream::EDProducer<> {
public:
  explicit MuonPATUserData(const edm::ParameterSet&);

  static void fillDescriptions(edm::ConfigurationDescriptions&);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;

  edm::EDGetToken src_;

  std::vector<std::string> vmaps_bool_;
  std::vector<edm::EDGetToken> vmaps_bool_token_;

  std::vector<std::string> vmaps_float_;
  std::vector<edm::EDGetToken> vmaps_float_token_;

  std::vector<std::pair<std::string, std::string> > v_float_copycats_;

  std::vector<std::pair<std::string, StringCutObjectSelector<pat::Muon, true> > > userInt_stringSelects_;
  std::vector<std::pair<std::string, StringObjectFunction<pat::Muon, true> > > userFloat_stringFuncs_;

  edm::EDGetTokenT<edm::View<reco::Vertex> > primaryVertices_;

  // Muon IDs HZZ
  bool IDLooseHZZ(const reco::Muon&, const reco::Vertex&);
  bool IDTightHZZ(const reco::Muon&, const reco::Vertex&);
};

MuonPATUserData::MuonPATUserData(const edm::ParameterSet& iConfig) {
  src_ = consumes<edm::View<pat::Muon> >(iConfig.getParameter<edm::InputTag>("src"));

  // ValueMaps [bool]
  vmaps_bool_ = iConfig.exists("valueMaps_bool") ? iConfig.getParameter<std::vector<std::string> >("valueMaps_bool")
                                                 : std::vector<std::string>();

  for (const auto& vm_str : vmaps_bool_) {
    vmaps_bool_token_.emplace_back(consumes<edm::ValueMap<bool> >(edm::InputTag(vm_str)));
  }
  // -----------------

  // ValueMaps [float]
  vmaps_float_ = iConfig.exists("valueMaps_float") ? iConfig.getParameter<std::vector<std::string> >("valueMaps_float")
                                                   : std::vector<std::string>();

  for (const auto& vm_str : vmaps_float_) {
    vmaps_float_token_.emplace_back(consumes<edm::ValueMap<float> >(edm::InputTag(vm_str)));
  }
  // -----------------

  // PSet for userFloat copycat(s)
  const edm::ParameterSet pset_userFloat_copycat = iConfig.exists("userFloat_copycat")
                                                       ? iConfig.getParameter<edm::ParameterSet>("userFloat_copycat")
                                                       : edm::ParameterSet();
  for (unsigned int i = 0; i < pset_userFloat_copycat.getParameterNames().size(); ++i) {
    const std::string pset_arg = pset_userFloat_copycat.getParameterNames().at(i);
    const std::string pset_val = pset_userFloat_copycat.getParameter<std::string>(pset_arg);

    v_float_copycats_.emplace_back(std::make_pair(pset_arg, pset_val));
  }
  // -----------------

  // PSet for userInts from StringCutObjectSelector(s)
  const edm::ParameterSet& pset_userInt_stringSelects =
      iConfig.exists("userInt_stringSelectors") ? iConfig.getParameter<edm::ParameterSet>("userInt_stringSelectors")
                                                : edm::ParameterSet();
  for (const std::string& vname : pset_userInt_stringSelects.getParameterNamesForType<std::string>()) {
    userInt_stringSelects_.emplace_back(std::pair<std::string, StringCutObjectSelector<pat::Muon, true> >(
        vname, pset_userInt_stringSelects.getParameter<std::string>(vname)));
  }
  // -----------------

  // PSet for userFloats from StringObjectFunction(s)
  const edm::ParameterSet& pset_userFloat_stringFuncs =
      iConfig.exists("userFloat_stringFunctions") ? iConfig.getParameter<edm::ParameterSet>("userFloat_stringFunctions")
                                                  : edm::ParameterSet();
  for (const std::string& vname : pset_userFloat_stringFuncs.getParameterNamesForType<std::string>()) {
    userFloat_stringFuncs_.emplace_back(std::pair<std::string, StringObjectFunction<pat::Muon, true> >(
        vname, pset_userFloat_stringFuncs.getParameter<std::string>(vname)));
  }
  // -----------------

  primaryVertices_ = consumes<edm::View<reco::Vertex> >(iConfig.getParameter<edm::InputTag>("primaryVertices"));

  produces<pat::MuonCollection>();
}

void MuonPATUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<edm::View<pat::Muon> > patMuons;
  iEvent.getByToken(src_, patMuons);

  // ValueMaps [bool]
  std::vector<edm::Handle<edm::ValueMap<bool> > > v_vmap_bool;
  for (unsigned int i = 0; i < vmaps_bool_token_.size(); ++i) {
    edm::Handle<edm::ValueMap<bool> > vmap;
    iEvent.getByToken(vmaps_bool_token_.at(i), vmap);
    v_vmap_bool.emplace_back(vmap);
  }
  // -----------------

  // ValueMaps [float]
  std::vector<edm::Handle<edm::ValueMap<float> > > v_vmap_float;
  for (unsigned int i = 0; i < vmaps_float_token_.size(); ++i) {
    edm::Handle<edm::ValueMap<float> > vmap;
    iEvent.getByToken(vmaps_float_token_.at(i), vmap);
    v_vmap_float.emplace_back(vmap);
  }
  // -----------------

  // PV
  edm::Handle<edm::View<reco::Vertex> > recoVtxs;
  iEvent.getByToken(primaryVertices_, recoVtxs);

  const auto* PV = (!recoVtxs->empty()) ? &(recoVtxs->at(0)) : nullptr;

  if (PV == nullptr) {
    edm::LogWarning("Input") << "@@@ MuonPATUserData::produce -- empty collection of primary vertices";
  }
  // -----------------

  std::unique_ptr<pat::MuonCollection> newMuons(new pat::MuonCollection);
  newMuons->reserve(patMuons->size());

  for (unsigned int i_muo = 0; i_muo < patMuons->size(); ++i_muo) {
    newMuons->emplace_back(patMuons->at(i_muo));
    pat::Muon& muo = newMuons->back();

    // ValueMaps [bool]
    for (unsigned int i = 0; i < v_vmap_bool.size(); ++i) {
      if (muo.hasUserInt(vmaps_bool_.at(i))) {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- PAT user-int label already exists: " << vmaps_bool_.at(i);
      }

      if (v_vmap_bool.at(i)->contains(patMuons->refAt(i_muo).id())) {
        const bool val = (*(v_vmap_bool.at(i)))[patMuons->refAt(i_muo)];
        muo.addUserInt(vmaps_bool_.at(i), int(val));
      } else {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- object reference not found in ValueMap<bool> \"" << vmaps_bool_.at(i)
            << "\"";
      }
    }
    // -----------------

    // ValueMaps [float]
    for (unsigned int i = 0; i < v_vmap_float.size(); ++i) {
      if (muo.hasUserFloat(vmaps_float_.at(i))) {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- PAT user-float label already exists: " << vmaps_float_.at(i);
      }

      if (v_vmap_float.at(i)->contains(patMuons->refAt(i_muo).id())) {
        const float val = (*(v_vmap_float.at(i)))[patMuons->refAt(i_muo)];
        muo.addUserFloat(vmaps_float_.at(i), val);
      } else {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- object reference not found in ValueMap<float> \"" << vmaps_float_.at(i)
            << "\"";
      }
    }
    // -----------------

    // userFloat copycat(s)
    for (const auto& userfloat_copycat : v_float_copycats_) {
      const std::string& ref = userfloat_copycat.second;
      const std::string& out = userfloat_copycat.first;

      if (muo.hasUserFloat(ref) == false) {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- PAT user-float key \"" + ref + "\" not found";
      }

      if (muo.hasUserFloat(out) == true) {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- target PAT user-float key \"" + out + "\" already exists";
      }

      muo.addUserFloat(out, muo.userFloat(ref));
    }
    // -----------------

    // Impact Parameter(s)
    const float dxyPV = ((PV && muo.muonBestTrack().isNonnull()) ? muo.muonBestTrack()->dxy(PV->position()) : -9999.);
    const float dzPV = ((PV && muo.muonBestTrack().isNonnull()) ? muo.muonBestTrack()->dz(PV->position()) : -9999.);

    muo.addUserFloat("dxyPV", dxyPV);
    muo.addUserFloat("dzPV", dzPV);

    const float SIP3D =
        ((muo.edB(pat::Muon::PV3D) != 0.) ? (muo.dB(pat::Muon::PV3D) / muo.edB(pat::Muon::PV3D)) : +9999.);
    muo.addUserFloat("SIP3D", SIP3D);
    // -----------------

    // Muon-ID booleans

    // Run2016 HIP mitigation:
    //  https://github.com/cms-sw/cmssw/blob/b9e344f2d6420e4397c301b8fe75ca1e3c1c3f92/RecoMuon/MuonIdentification/plugins/MuonProducer.cc#L449
    const bool isRun2016BCDEF = ((272728 <= iEvent.run()) && (iEvent.run() <= 278808));

    muo.addUserInt("IDLoose", int(muo.isLooseMuon()));
    muo.addUserInt("IDMedium", int(muon::isMediumMuon(muo, isRun2016BCDEF)));
    muo.addUserInt("IDTight", int(PV ? muo.isTightMuon(*PV) : 0));
    muo.addUserInt("IDSoft", int(PV ? muon::isSoftMuon(muo, *PV, isRun2016BCDEF) : 0));
    muo.addUserInt("IDHighPt", int(PV ? muo.isHighPtMuon(*PV) : 0));
    muo.addUserInt("IDHighPtTRK", int(PV ? muon::isTrackerHighPtMuon(muo, *PV) : 0));
    muo.addUserInt("IDLooseHZZ", int(PV ? this->IDLooseHZZ(muo, *PV) : 0));
    muo.addUserInt("IDTightHZZ", int(PV ? this->IDTightHZZ(muo, *PV) : 0));
    // ------------------

    // PF-isolation R=0.3
    const reco::MuonPFIsolation& muoPFIsoR03 = muo.pfIsolationR03();

    const float pfIsoR03_CH(muoPFIsoR03.sumChargedHadronPt);
    const float pfIsoR03_NH(muoPFIsoR03.sumNeutralHadronEt);
    const float pfIsoR03_Ph(muoPFIsoR03.sumPhotonEt);
    const float pfIsoR03_PU(muoPFIsoR03.sumPUPt);

    const float pfIsoR03 =
        (muo.pt() != 0.) ? ((pfIsoR03_CH + std::max(0., pfIsoR03_NH + pfIsoR03_Ph - 0.5 * pfIsoR03_PU)) / muo.pt())
                         : -1.;

    muo.addUserFloat("pfIsoR03_CH", pfIsoR03_CH);
    muo.addUserFloat("pfIsoR03_NH", pfIsoR03_NH);
    muo.addUserFloat("pfIsoR03_Ph", pfIsoR03_Ph);
    muo.addUserFloat("pfIsoR03_PU", pfIsoR03_PU);
    muo.addUserFloat("pfIsoR03", pfIsoR03);
    // ------------------

    // PF-isolation R=0.4
    const reco::MuonPFIsolation& muoPFIsoR04 = muo.pfIsolationR04();

    const float pfIsoR04_CH(muoPFIsoR04.sumChargedHadronPt);
    const float pfIsoR04_NH(muoPFIsoR04.sumNeutralHadronEt);
    const float pfIsoR04_Ph(muoPFIsoR04.sumPhotonEt);
    const float pfIsoR04_PU(muoPFIsoR04.sumPUPt);

    const float pfIsoR04 =
        (muo.pt() != 0.) ? ((pfIsoR04_CH + std::max(0., pfIsoR04_NH + pfIsoR04_Ph - 0.5 * pfIsoR04_PU)) / muo.pt())
                         : -1.;

    muo.addUserFloat("pfIsoR04_CH", pfIsoR04_CH);
    muo.addUserFloat("pfIsoR04_NH", pfIsoR04_NH);
    muo.addUserFloat("pfIsoR04_Ph", pfIsoR04_Ph);
    muo.addUserFloat("pfIsoR04_PU", pfIsoR04_PU);
    muo.addUserFloat("pfIsoR04", pfIsoR04);
    // ------------------

    // Selectors [int]
    for (const auto& i_strNfunc : userInt_stringSelects_) {
      const auto& i_str = i_strNfunc.first;
      const auto& i_func = i_strNfunc.second;

      if (muo.hasUserInt(i_str)) {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- PAT user-int label already exists: " << i_str;
      }

      muo.addUserInt(i_str, int(i_func(muo)));
    }
    // -----------------

    // Functions [float]
    for (const auto& i_strNfunc : userFloat_stringFuncs_) {
      const auto& i_str = i_strNfunc.first;
      const auto& i_func = i_strNfunc.second;

      if (muo.hasUserFloat(i_str)) {
        throw cms::Exception("InputError")
            << "@@@ MuonPATUserData::produce -- PAT user-float label already exists: " << i_str;
      }

      muo.addUserFloat(i_str, float(i_func(muo)));
    }
    // -----------------
  }

  iEvent.put(std::move(newMuons));

  return;
}

bool MuonPATUserData::IDLooseHZZ(const reco::Muon& muon, const reco::Vertex& vtx) {
  const bool kin = ((muon.pt() > 5.) && (fabs(muon.eta()) < 2.4));
  if (not kin) {
    return false;
  }

  const bool ip = (muon.muonBestTrack().isNonnull() && fabs(muon.muonBestTrack()->dxy(vtx.position())) < 0.5 &&
                   fabs(muon.muonBestTrack()->dz(vtx.position())) < 1.0);
  if (!ip) {
    return false;
  }

  const bool id = (muon.isGlobalMuon() || muon.isTrackerMuon());
  if (!id) {
    return false;
  }

  const bool trk_type = (muon.muonBestTrackType() != 2);
  if (!trk_type) {
    return false;
  }

  return true;
}

bool MuonPATUserData::IDTightHZZ(const reco::Muon& muon, const reco::Vertex& vtx) {
  const bool looseHZZ = IDLooseHZZ(muon, vtx);
  if (not looseHZZ) {
    return false;
  }

  bool pass = muon.isPFMuon();

  if (muon.pt() > 200.) {
    pass |= muon::isTrackerHighPtMuon(muon, vtx);
  }

  return pass;
}

void MuonPATUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.setUnknown();

  descriptions.add("MuonPATUserData", desc);
}

DEFINE_FWK_MODULE(MuonPATUserData);
