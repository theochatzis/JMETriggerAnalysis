#ifndef NAK_HFolderTTbarLJRecoHyp_H
#define NAK_HFolderTTbarLJRecoHyp_H

#include <inc/HFolderBASE.h>
#include <inc/TTbarLJRecoHyp.h>
#include <inc/TTbarGen.h>

namespace nak {

  class HFolderTTbarLJRecoHyp : public HFolderBASE {

  public:
    explicit HFolderTTbarLJRecoHyp(TFile&, const std::string& dir="");
    virtual ~HFolderTTbarLJRecoHyp() {}

    void Fill(const nak::Event&, const float) {}
    void Fill(const nak::TTbarLJRecoHyp&, const TTbarGen&, const float, const float);
  };

}

#endif
