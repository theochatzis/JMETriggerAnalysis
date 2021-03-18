#ifndef UAM_ELECTRON_H_
#define UAM_ELECTRON_H_

#include <inc/Lepton.h>

namespace xtt {

  class Electron : public Lepton {
   public:
    Electron();
    virtual ~Electron() {}

    Float_t scEt;          // superCluster()->energy() * sin(superCluster()->position().theta())
    Float_t scEta;         // superCluster()->Eta()
    Float_t dEtaIn;        // deltaEtaSuperClusterTrackAtVtx()    
    Float_t dPhiIn;        // deltaPhiSuperClusterTrackAtVtx()    
    Float_t sigmaIEtaIEta; // sigmaIetaIeta()
    Float_t HoE;           // hadronicOverEm()
    Float_t ecalEnergy;    // ecalEnergy()
    Float_t trackPAtVtx;   // ecalEnergy() / eSuperClusterOverP()
    Bool_t vtxFitConv;     // passConversionVeto()
    Int_t convMissHits;    // gsfTrack()->trackerExpectedHitsInner().numberOfHits()
    Float_t mvaNoTrig;
    Float_t mvaTrig;
    Int_t IDcutBased;
    Int_t IDmvaNoTrig;
    Int_t IDmvaTrig;
  };

}

#endif
