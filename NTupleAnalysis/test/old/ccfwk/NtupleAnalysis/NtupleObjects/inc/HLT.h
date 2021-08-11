#ifndef UAM_HLT_H_
#define UAM_HLT_H_

namespace xtt {

  class HLT {
   public:
    HLT();
    virtual ~HLT() {}

    int Mu45_eta2p1;
    int IsoMu24_eta2p1_IterTk02;
    int Mu40_eta2p1_PFJet200_PFJet50;

    int Ele95_CaloIdVT_GsfTrkIdT;
    int Ele32_eta2p1_WP75_Gsf;
    int Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50;

    int AK8PFJet360TrimMod_Mass30;
    int PFMET170_NoiseCleaned;
    int PFMET120_NoiseCleaned_BTagCSV07;
    int PFHT350_PFMET120_NoiseCleaned;
    int PFHT900;
  };

}

#endif
