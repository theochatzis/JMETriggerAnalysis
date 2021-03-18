#include <inc/MET.h>

xtt::MET::MET(){

  pt     = -999.;
  phi    = -999.;
  sumEt  = -999.;
  mEtSig = -999.;
  signif = -999.;
}

TLorentzVector xtt::MET::p4() const {

  TLorentzVector v;
  v.SetPtEtaPhiM(pt, 0., phi, 0.);

  return v;
}
