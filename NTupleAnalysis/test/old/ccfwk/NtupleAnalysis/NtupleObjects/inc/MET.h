#ifndef UAM_MET_H_
#define UAM_MET_H_

#include <TLorentzVector.h>

namespace xtt {

  class MET {
   public:
    MET();
    virtual ~MET() {}

    float pt;
    float phi;
    float sumEt;  // sumEt()
    float mEtSig; // mEtSig()
    float signif; // significance()

    TLorentzVector p4() const;

    float px() const { return p4().Px(); }
    float py() const { return p4().Py(); }
  };

}

#endif
