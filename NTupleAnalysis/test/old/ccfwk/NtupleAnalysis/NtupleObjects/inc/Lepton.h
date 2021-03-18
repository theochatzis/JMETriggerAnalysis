#ifndef UAM_LEPTON_H_
#define UAM_LEPTON_H_

#include <inc/Particle.h>

namespace xtt {

  class Lepton : public Particle {
   public:
    Lepton();
    virtual ~Lepton() {}

    int pdgID;
    int charge;
    float vx;
    float vy;
    float vz;
    float dxyPV; // muonBestTrack()->dxy(VTX.position()) // gsfTrack()->dxy(VTX.position())
    float dzPV;  // muonBestTrack()->dz (VTX.position()) // gsfTrack()->dz (VTX.position())
    float dB;

    float pfMINIIso_CH_stand;
    float pfMINIIso_NH_stand;
    float pfMINIIso_Ph_stand;
    float pfMINIIso_PU_stand;
    float pfMINIIso_NH_pfwgt;
    float pfMINIIso_Ph_pfwgt;
  };

}

#endif
