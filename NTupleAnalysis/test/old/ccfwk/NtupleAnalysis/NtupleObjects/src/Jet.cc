#include <inc/Jet.h>

xtt::Jet::Jet() : xtt::Particle(){

  isPFJet         = false;
  partonFlavor    = -999;
  jetCharge       = -999.;
  JEC             = -999.;
  JECUnc          = -999.;
  JER             = -999.;
  JERup           = -999.;
  JERdn           = -999.;

  nDaughters      = -999;
  chaMultiplicity = -999;
  chaHadEneFrac   = -999.;
  chaEmEneFrac    = -999.;
  neuHadEneFrac   = -999.;
  neuEmEneFrac    = -999.;

  puBeta          = -999.;
  puIDmva         = -999.;

  btagJP          = -999.;    
  btagCSV         = -999.;   
  btagCSVIVF      = -999.;

  Tau1            = -999.;
  Tau2            = -999.;
  Tau3            = -999.;
}
