#ifndef NAK_NEUTRINORECO_H_
#define NAK_NEUTRINORECO_H_

#include <TLorentzVector.h>

namespace nak {

  class NeutrinoReco {
   public:
    virtual std::vector<TLorentzVector> operator()(const TLorentzVector&, const TLorentzVector&) const = 0;
  };

  class NeutrinoRecoSTD : public NeutrinoReco {
   public:
    virtual std::vector<TLorentzVector> operator()(const TLorentzVector&, const TLorentzVector&) const;
  };

  class NeutrinoRecoRE1 : public NeutrinoReco {
   public:
    virtual std::vector<TLorentzVector> operator()(const TLorentzVector&, const TLorentzVector&) const;
  };

  class NeutrinoRecoRWM : public NeutrinoReco {
   public:
    virtual std::vector<TLorentzVector> operator()(const TLorentzVector&, const TLorentzVector&) const;
  };

}

#endif
