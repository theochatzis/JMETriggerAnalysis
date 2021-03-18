#include <inc/Particle.h>

xtt::Particle::Particle(){

  pt  = -999.;
  eta = -999.;
  phi = -999.;
  M   = -999.;
}

TLorentzVector xtt::Particle::p4() const {

  TLorentzVector v;
  v.SetPtEtaPhiM(pt, eta, phi, M);

  return v;
}
