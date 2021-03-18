#ifndef NAK_TTBARLJRECOTOOLS_H_
#define NAK_TTBARLJRECOTOOLS_H_

#include <inc/TTbarLJRecoHyp.h>
#include <inc/TTbarGen.h>

#include <vector>

namespace nak {

  class TTbarLJRecoRanker_chi2 {
   public:
    explicit TTbarLJRecoRanker_chi2(float tl_m_v, float tl_m_s, float th_m_v, float th_m_s):
      tlep_m_val_(tl_m_v), tlep_m_sig_(tl_m_s), thad_m_val_(th_m_v), thad_m_sig_(th_m_s) {}

    virtual float hyp_value(const TTbarLJRecoHyp&) const;
    virtual const TTbarLJRecoHyp* best_hyp(const std::vector<TTbarLJRecoHyp>&) const;

   protected:
    float tlep_m_val_, tlep_m_sig_;
    float thad_m_val_, thad_m_sig_;
  };
  ///

  class TTbarLJRecoRanker_chi2_TTAG : public TTbarLJRecoRanker_chi2 {
   public:
    explicit TTbarLJRecoRanker_chi2_TTAG(float tl_m_v, float tl_m_s, float th_m_v, float th_m_s):
      TTbarLJRecoRanker_chi2(tl_m_v, tl_m_s, th_m_v, th_m_s) {}

    virtual float hyp_value(const TTbarLJRecoHyp&) const;
  };
  ///

  class TTbarLJRecoRanker_genMatchDR {
   public:
    explicit TTbarLJRecoRanker_genMatchDR(float minDR_l=.1, float minDphi_nu=.3, float minDR_j=.4, float minDR_tj=.8):
      minDR_lepton_(minDR_l), minDphi_neutrino_(minDphi_nu), minDR_jet_(minDR_j), minDR_topjet_(minDR_tj) {}

    float hyp_value(const TTbarLJRecoHyp&, const TTbarGen&, int) const;
    const TTbarLJRecoHyp* best_hyp(const std::vector<TTbarLJRecoHyp>&, const TTbarGen&, int) const;

   protected:
    float minDR_lepton_;
    float minDphi_neutrino_;
    float minDR_jet_;
    float minDR_topjet_;
  };

}

#endif
