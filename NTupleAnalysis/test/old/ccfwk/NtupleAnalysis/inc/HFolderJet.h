#ifndef NAK_HFolderJet_H
#define NAK_HFolderJet_H

#include <inc/HFolderBASE.h>

namespace nak {

  class HFolderJet : public HFolderBASE {

   public: 
    explicit HFolderJet(TFile&, const std::string& dir="");

    void Fill(const nak::Event&, const float) {}

    void Fill(const std::vector<xtt::Jet>&, const float);

    float CSVIVFL_wp;
    float CSVIVFM_wp;
    float CSVIVFT_wp;
    float CSVL_wp;
    float CSVM_wp;
    float CSVT_wp;
    float JPL_wp;
    float JPM_wp;
    float JPT_wp;
  };

}

#endif
