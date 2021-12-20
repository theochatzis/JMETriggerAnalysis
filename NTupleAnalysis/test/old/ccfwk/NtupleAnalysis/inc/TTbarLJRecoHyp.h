#ifndef NAK_TTBARLJRECOHYP_H_
#define NAK_TTBARLJRECOHYP_H_

#include <NtupleObjects/inc/Particle.h>
#include <NtupleObjects/inc/Lepton.h>
#include <NtupleObjects/inc/Jet.h>
#include <TLorentzVector.h>

#include <vector>
#include <map>

namespace nak {

  class TTbarLJRecoHyp {

   public:
    TTbarLJRecoHyp();
    ~TTbarLJRecoHyp() {}

    TLorentzVector ttbar_p4() const { return (toplep_p4()+tophad_p4()); }

    TLorentzVector tophad_p4() const;
    TLorentzVector toplep_p4() const;

    TLorentzVector     top_p4() const { return (((xtt::Lepton*) lepton())->charge > 0) ? toplep_p4() : tophad_p4(); }
    TLorentzVector antitop_p4() const { return (((xtt::Lepton*) lepton())->charge < 0) ? toplep_p4() : tophad_p4(); }

//    TLorentzVector Whad_p4() const;
    TLorentzVector Wlep_p4() const { return (lepton_p4()+neutrino_p4()); }
    TLorentzVector neutrino_p4() const;
    TLorentzVector lepton_p4() const { return lepton()->p4(); }
    const xtt::Particle* lepton() const;

    void set_lepton(const xtt::Particle* l){ lepton_ = l; }
    void set_neutrino_p4(const TLorentzVector& tl){ neutrino_p4_ = tl; }

    std::vector<const xtt::Jet*> toplep_jet_ptrs() const { return toplep_jet_ptrs_; }
    std::vector<const xtt::Jet*> tophad_jet_ptrs() const { return tophad_jet_ptrs_; }

    void add_toplep_jet_ptr(const xtt::Jet* j){ toplep_jet_ptrs_.push_back(j); }
    void add_tophad_jet_ptr(const xtt::Jet* j){ tophad_jet_ptrs_.push_back(j); }

    float discriminator(const std::string& disc_tag) const;
    void set_discriminator(const std::string& disc_tag, const float disc_val){ discriminator_map_[disc_tag] = disc_val; }

    void printout() const;
    void printout_p4(const std::string&, const TLorentzVector&) const;

   protected:
    const xtt::Particle* lepton_;
    TLorentzVector neutrino_p4_;

    std::vector<const xtt::Jet*> toplep_jet_ptrs_;
    std::vector<const xtt::Jet*> tophad_jet_ptrs_;

    std::map<std::string, float> discriminator_map_;
  };

}

#endif
