#include <inc/MergedJet.h>

xtt::MergedJet::MergedJet() : xtt::Jet(){

  Msoftdrop = -999.;
  Mfiltered = -999.;
  Mpruned   = -999.;
  Mtrimmed  = -999.;

  subjets0.clear();
  subjets1.clear();
}
