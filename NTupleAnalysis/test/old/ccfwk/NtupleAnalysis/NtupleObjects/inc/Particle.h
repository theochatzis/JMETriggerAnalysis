#ifndef UAM_PARTICLE_H_
#define UAM_PARTICLE_H_

#include <TLorentzVector.h>

namespace xtt {

  class Particle {
   public:
    Particle();
    virtual ~Particle() {}

    float pt;
    float eta;
    float phi;
    float M;

    TLorentzVector p4() const;

    float px() const { return p4().Px(); }
    float py() const { return p4().Py(); }
    float pz() const { return p4().Pz(); }
    float E()  const { return p4().M();  }
  };

}

#endif
