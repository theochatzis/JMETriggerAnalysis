#ifndef NAK_HFolderLepton_H
#define NAK_HFolderLepton_H

#include <inc/HFolderBASE.h>

namespace nak {

  class HFolderLepton : public HFolderBASE {

   public:
    explicit HFolderLepton(TFile&, const std::string& dir="");
    virtual ~HFolderLepton() {}

    void Fill(const nak::Event&, const float) {}

    void Fill(const xtt::Lepton&, const float);
  };

}

#endif
