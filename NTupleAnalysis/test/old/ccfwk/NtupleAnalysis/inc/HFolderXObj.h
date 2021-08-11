#ifndef NAK_HFolderXObj_H
#define NAK_HFolderXObj_H

#include <inc/HFolderBASE.h>

namespace nak {

  class HFolderXObj : public HFolderBASE {

   public: 
    explicit HFolderXObj(TFile&, const std::string& dir="");
    virtual ~HFolderXObj() {}

    void Fill(const nak::Event&, const float) {}

    void Fill(const int, const xtt::Particle&, const xtt::MET&,
              const std::vector<xtt::Jet>&, const std::vector<xtt::MergedJet>&, const float);

    void Fill(const int, const xtt::Particle&, const xtt::MET&,
              const std::vector<xtt::Jet>&, const std::vector<xtt::MergedJet>&, const float, const float, const float);
  };

}

#endif
