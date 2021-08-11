#ifndef UAM_MERGEDJET_H_
#define UAM_MERGEDJET_H_

#include <inc/Jet.h>
#include <vector>

namespace xtt {

  class MergedJet : public Jet {
   public:
    MergedJet();
    virtual ~MergedJet() {}

    float Msoftdrop;
    float Mfiltered;
    float Mpruned;
    float Mtrimmed;

    std::vector<Jet> subjets0;
    std::vector<Jet> subjets1;
  };

}

#endif
