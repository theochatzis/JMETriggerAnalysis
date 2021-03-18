#ifndef NAK_HFolderTopJet_H
#define NAK_HFolderTopJet_H

#include <inc/HFolderBASE.h>

namespace nak {

  class HFolderTopJet : public HFolderBASE {

   public: 
    explicit HFolderTopJet(TFile&, const std::string& dir="");
    virtual ~HFolderTopJet() {}

    void Fill(const nak::Event&, const float) {}

    void Fill(const std::vector<xtt::MergedJet>&, const float);

    float CSVL_wp;
    float CSVM_wp;
    float CSVT_wp;
    float JPL_wp;
    float JPM_wp;
    float JPT_wp;
  };

}

#endif
