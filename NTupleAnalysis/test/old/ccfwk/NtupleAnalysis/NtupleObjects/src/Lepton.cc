#include <inc/Lepton.h>

xtt::Lepton::Lepton() : xtt::Particle(){

  pdgID  = -999;
  charge = -999;
  vx     = -999.;
  vy     = -999.;
  vz     = -999.;
  dxyPV  = -999.;
  dzPV   = -999.;
  dB     = -999.;

  pfMINIIso_CH_stand = -999.;
  pfMINIIso_NH_stand = -999.;
  pfMINIIso_Ph_stand = -999.;
  pfMINIIso_PU_stand = -999.;
  pfMINIIso_NH_pfwgt = -999.;
  pfMINIIso_Ph_pfwgt = -999.;
}
