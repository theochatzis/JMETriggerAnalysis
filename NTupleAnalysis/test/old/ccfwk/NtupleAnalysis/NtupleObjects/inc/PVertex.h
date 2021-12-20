#ifndef UAM_PVERTEX_H_
#define UAM_PVERTEX_H_

namespace xtt {

  class PVertex {
   public:
    PVertex();
    virtual ~PVertex() {}

    bool isFake;
    float chi2;
    float nDOF;
    float vx;
    float vy;
    float vz;
  };

}

#endif
