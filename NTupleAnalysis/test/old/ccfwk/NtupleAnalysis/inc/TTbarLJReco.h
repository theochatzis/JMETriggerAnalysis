#ifndef NAK_TTBARLJRECO_H_
#define NAK_TTBARLJRECO_H_

#include <inc/Event.h>
#include <NtupleObjects/inc/Particle.h>
#include <inc/NeutrinoReco.h>
#include <inc/TTbarLJRecoHyp.h>
#include <inc/TopTagID.h>

namespace nak {

  class TTbarLJReco {

   public:
    explicit TTbarLJReco(const NeutrinoReco* nu_rec, const std::string& jet_key):
      neutrino_reco_(nu_rec), jet_key_(jet_key) {}

    virtual const xtt::Particle* get_primary_lepton(const Event&) const;
    virtual const std::vector<TTbarLJRecoHyp> get_hyps(const Event&) const;

   protected:
    const NeutrinoReco* neutrino_reco_;
    std::string jet_key_;
  };

  class TTbarLJRecoVTAG : public TTbarLJReco {

   public:
    explicit TTbarLJRecoVTAG(const NeutrinoReco* nu_rec, const std::string& jet_key, const std::string& vjet_key, const VTagger* vtagID, const float dr):
      TTbarLJReco(nu_rec, jet_key), vjet_key_(vjet_key), vtagID_(vtagID), minDR_vjet_jet_(dr) {}

    virtual const std::vector<TTbarLJRecoHyp> get_hyps(const Event&) const;

   protected:
    std::string vjet_key_;
    const VTagger* vtagID_;
    float minDR_vjet_jet_;
  };
  ///

  class TTbarLJRecoTTAG : public TTbarLJReco {

   public:
    explicit TTbarLJRecoTTAG(const NeutrinoReco* nu_rec, const std::string& jet_key, const std::string& topjet_key, const TopTagID* ttagID, const float dr):
      TTbarLJReco(nu_rec, jet_key), topjet_key_(topjet_key), toptagID_(ttagID), minDR_topjet_jet_(dr) {}

    virtual const std::vector<TTbarLJRecoHyp> get_hyps(const Event&) const;

   protected:
    std::string topjet_key_;
    const TopTagID* toptagID_;
    float minDR_topjet_jet_;
  };
  ///

  class TTbarLJReco_LBJ : public TTbarLJReco {
   public:
    explicit TTbarLJReco_LBJ(const NeutrinoReco* nu_rec): TTbarLJReco(nu_rec, "JET_AK4") {}

    virtual const std::vector<TTbarLJRecoHyp> get_hyps(const Event&) const;
  };

  class TTbarLJRecoTTAG_LBJ : public TTbarLJRecoTTAG {
   public:
    explicit TTbarLJRecoTTAG_LBJ(const NeutrinoReco* nu_rec, const TopTagID* ttagID, float dr=1.2): TTbarLJRecoTTAG(nu_rec, "JET_AK4", "JET_AK8", ttagID, dr) {}

    virtual const std::vector<TTbarLJRecoHyp> get_hyps(const Event&) const;
  };
  ///

}

#endif
