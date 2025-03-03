#ifndef NAK_btagSF_H
#define NAK_btagSF_H

#include <string>
#include <vector>

#include <inc/utils.h>

#include <NtupleObjects/inc/Jet.h>

namespace nak {

  class btagSF {

   public:
    btagSF(const std::string&, const std::string&);//, const systematic&);

    float GetWeight(const std::vector<xtt::Jet*>&);
    float GetWeight(const std::vector<xtt::Jet*>&, const std::vector<xtt::Jet*>&);

   protected:
    std::string channel_;
//    systematic sys;
  };

}

#endif
