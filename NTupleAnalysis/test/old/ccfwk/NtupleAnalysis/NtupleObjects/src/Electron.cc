#include <inc/Electron.h>

xtt::Electron::Electron() : xtt::Lepton(){

  scEt          = -999.;
  scEta         = -999.;
  dEtaIn        = -999.;
  dPhiIn        = -999.;
  sigmaIEtaIEta = -999.;
  HoE           = -999.;
  ecalEnergy    = -999.;
  trackPAtVtx   = -999.;
  vtxFitConv    = false;
  convMissHits  = -999;
  mvaNoTrig     = -999.;
  mvaTrig       = -999.;
  IDcutBased    = -999;
  IDmvaNoTrig   = -999;
  IDmvaTrig     = -999;
}
