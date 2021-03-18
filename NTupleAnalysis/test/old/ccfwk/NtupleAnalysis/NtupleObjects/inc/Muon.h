#ifndef UAM_MUON_H_
#define UAM_MUON_H_

#include <inc/Lepton.h>

namespace xtt {

  class Muon : public Lepton {
   public:
    Muon();
    virtual ~Muon() {}

    bool isGlobalMuon;      // isGlobalMuon();
    bool isPFMuon;          // isPFMuon();
    float normChi2;         // globalTrack()->normalizedChi2()
    int nValidMuonHits;     // globalTrack()->hitPattern().numberOfValidMuonHits()
    int nMatchedStations;   // numberOfMatchedStations()
    int nTrkLayersWithMsrt; // innerTrack()->hitPattern().trackerLayersWithMeasurement()
    int nValidPixelHits;    // innerTrack()->hitPattern().numberOfValidPixelHits()
    int IDLoose;
    int IDMedium;
    int IDTight;
    int IDSoft;
    int IDHighPt;
  };

}

#endif
