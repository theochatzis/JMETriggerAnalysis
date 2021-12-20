#ifndef UAM_JET_H_
#define UAM_JET_H_

#include <inc/Particle.h>

namespace xtt {

  class Jet : public Particle {
   public:
    Jet();
    virtual ~Jet() {}

    bool isPFJet;
    int partonFlavor;    // partonFlavour()
    float jetCharge;
    float JEC;
    float JECUnc;
    float JER;
    float JERup;
    float JERdn;

    int nDaughters;      // numberOfDaughters()
    int chaMultiplicity; // chargedMultiplicity()
    float chaHadEneFrac; // chargedHadronEnergyFraction()
    float chaEmEneFrac;  // chargedEmEnergyFraction()
    float neuHadEneFrac; // neutralHadronEnergyFraction()
    float neuEmEneFrac;  // neutralEmEnergyFraction()

    float puBeta;
    float puIDmva;

    // b-tagging
    float btagJP;        // bDiscriminator("pfJetProbabilityBJetTags");
    float btagCSV;       // bDiscriminator("pfCombinedSecondaryVertexBJetTags");
    float btagCSVIVF;    // bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags");

    // N-subjettiness
    float Tau1;
    float Tau2;
    float Tau3;
  };

}

#endif
