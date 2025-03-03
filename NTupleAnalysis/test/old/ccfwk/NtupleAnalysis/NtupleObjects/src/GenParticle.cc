#include <inc/GenParticle.h>

xtt::GenParticle::GenParticle() : xtt::Particle() {

  pdgID      = -999;
  status     = -999;
  nMothers   = -999;
  nDaughters = -999;
  index      = -999;
  indexMo1   = -999;
  indexMo2   = -999;
  indexDa1   = -999;
  indexDa2   = -999;
}
