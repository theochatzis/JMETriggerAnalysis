#ifndef NAK_TTbarGen_h
#define NAK_TTbarGen_h

#include <NtupleObjects/inc/GenParticle.h>

#include <iostream>
#include <cstdlib>

namespace nak {

  class TTbarGen {

   public:
    explicit TTbarGen();
    explicit TTbarGen(const std::vector<xtt::GenParticle>&);
    ~TTbarGen() {}

    enum decay_t { null, jj, ej, muj, tauj, emu, etau, mutau, ee, mumu, tautau };

    void clear();
    void init(const std::vector<xtt::GenParticle>&);

    void init_decay_mode();
    void init_ljets();

    bool is_valid() const { return has_top_plus() && has_top_minus(); }
    bool has_top_plus() const { return p_t && p_b && p_W && p_W_fu && p_W_fd; }
    bool has_top_minus() const { return m_t && m_b && m_W && m_W_fu && m_W_fd; }

    decay_t decay_mode() const { return ttbar_decay; }
    bool is_ljets() const { return (decay_mode() == ej || decay_mode() == muj || decay_mode() == tauj); }
    bool is_emujets() const { return (decay_mode() == ej || decay_mode() == muj); }

    TLorentzVector ttbar() const { return (p_t->p4() + m_t->p4()); }
    float mttbar() const { return ttbar().M(); }

    void set_verbose(const bool v) { verbose = v; }

    void printout() const;
    void printout_genp(const std::string&, const xtt::GenParticle*) const;

    const xtt::GenParticle* t_lep() const { return lep_t; }
    const xtt::GenParticle* b_lep() const { return lep_b; }
    const xtt::GenParticle* W_lep() const { return lep_W; }
    const xtt::GenParticle* neutrino() const { return lep_W_fu; }
    const xtt::GenParticle* lepton() const { return lep_W_fd; }
    const xtt::GenParticle* t_had() const { return had_t; }
    const xtt::GenParticle* b_had() const { return had_b; }
    const xtt::GenParticle* W_had() const { return had_W; }
    const xtt::GenParticle* W_had_fu() const { return had_W_fu; }
    const xtt::GenParticle* W_had_fd() const { return had_W_fd; }

   protected:
    const xtt::GenParticle* p_t;
    const xtt::GenParticle* p_b;
    const xtt::GenParticle* p_W;
    const xtt::GenParticle* p_W_fu;
    const xtt::GenParticle* p_W_fd;
    const xtt::GenParticle* m_t;
    const xtt::GenParticle* m_b;
    const xtt::GenParticle* m_W;
    const xtt::GenParticle* m_W_fu;
    const xtt::GenParticle* m_W_fd;

    const xtt::GenParticle* lep_t;
    const xtt::GenParticle* lep_b;
    const xtt::GenParticle* lep_W;
    const xtt::GenParticle* lep_W_fu;
    const xtt::GenParticle* lep_W_fd;
    const xtt::GenParticle* had_t;
    const xtt::GenParticle* had_b;
    const xtt::GenParticle* had_W;
    const xtt::GenParticle* had_W_fu;
    const xtt::GenParticle* had_W_fd;

    decay_t ttbar_decay;
    bool verbose;
  };

}

#endif
