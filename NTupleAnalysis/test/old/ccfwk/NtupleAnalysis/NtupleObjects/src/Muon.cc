#include <inc/Muon.h>

xtt::Muon::Muon() : xtt::Lepton(){

  isGlobalMuon       = false;
  isPFMuon           = false;
  normChi2           = -999.;
  nValidMuonHits     = -999;
  nMatchedStations   = -999;
  nTrkLayersWithMsrt = -999;
  nValidPixelHits    = -999;
  IDLoose            = -999;
  IDMedium           = -999;
  IDTight            = -999;
  IDSoft             = -999;
  IDHighPt           = -999;
}
