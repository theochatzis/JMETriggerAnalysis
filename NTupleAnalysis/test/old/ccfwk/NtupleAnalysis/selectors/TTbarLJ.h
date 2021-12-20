#ifndef NAK_TTbarLJ_H
#define NAK_TTbarLJ_H

#include "SelectorBASE.h"

class TTbarLJ : public SelectorBASE {
 public:
  explicit TTbarLJ(): SelectorBASE() {}
  virtual ~TTbarLJ() {}

  virtual void configure();
  virtual void configure_output(TFile&);

  virtual Bool_t Process(Long64_t entry);

  ClassDef(TTbarLJ, 0);
};

#endif
