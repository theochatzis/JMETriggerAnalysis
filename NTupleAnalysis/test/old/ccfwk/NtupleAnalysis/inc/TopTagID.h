#ifndef NAK_TOPTAGID_H_
#define NAK_TOPTAGID_H_

#include <TLorentzVector.h>
#include <NtupleObjects/inc/MergedJet.h>

namespace nak {

  class TopTagID {
   public:
    virtual bool operator()(const xtt::MergedJet&) const = 0;
  };

  class VTagger {
   public:
    explicit VTagger(const float m_min=60., const float m_max=100., const float tau21_max=0.6):
      m_min_(m_min), m_max_(m_max), tau21_max_(tau21_max) {}

    virtual bool operator()(const xtt::MergedJet&) const;

   protected:
    float m_min_, m_max_;
    float tau21_max_;
  };

  class CMSTopTagger : public TopTagID {
   public:
    explicit CMSTopTagger(const int nsj_min=3, const float m_min=140., const float m_max=250., const float mmin_min=50.):
      nsubj_min_(nsj_min), m_min_(m_min), m_max_(m_max), mmin_min_(mmin_min) {}

    virtual bool operator()(const xtt::MergedJet&) const;

    int nsubj_min_;
    float m_min_, m_max_;
    float mmin_min_;
  };

  class CMSTopTagger_tau32 : public CMSTopTagger {
   public:
    explicit CMSTopTagger_tau32(const int nsj_min=3, const float m_min=140., const float m_max=250., const float mmin_min=50., const float tau32_max=0.7):
      CMSTopTagger(nsj_min, m_min, m_max, mmin_min), tau32_max_(tau32_max) {}

    virtual bool operator()(const xtt::MergedJet&) const;

    float tau32_max_;
  };

  class HEPTopTagger : public TopTagID {
   public:
    explicit HEPTopTagger() {}

    virtual bool operator()(const xtt::MergedJet&) const;
  };

}

#endif
