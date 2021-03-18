#ifndef UAM_GENPARTICLE_H_
#define UAM_GENPARTICLE_H_

#include <inc/Particle.h>

namespace xtt {

  class GenParticle : public Particle {
   public:
    GenParticle();
    virtual ~GenParticle() {}

    int pdgID;
    int status;
    int nMothers;
    int nDaughters;
    int index;
    int indexMo1;
    int indexMo2;
    int indexDa1;
    int indexDa2;
  };

}

#endif
