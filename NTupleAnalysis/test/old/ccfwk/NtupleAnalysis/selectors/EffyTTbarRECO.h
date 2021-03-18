#ifndef NAK_EffyTTbarRECO_H
#define NAK_EffyTTbarRECO_H

#include <string>
#include <memory>

#include "SelectorBASE.h"

#include <inc/EventSelection.h>
#include <inc/TTbarLJReco.h>
#include <inc/TTbarLJRecoTools.h>

namespace nak {

  class EffyTTbarRECO : public SelectorBASE {

   public:
    explicit EffyTTbarRECO();
    virtual ~EffyTTbarRECO() {}

    virtual void configure();
    virtual void configure_output(TFile&);

    virtual Bool_t Process(Long64_t entry);

   protected:
    std::string channel; //!

    std::auto_ptr<NeutrinoReco> nu_reco; //!
    std::auto_ptr<TopTagID> ttagID; //!

    std::auto_ptr<EventSelection> ttagevt_sel; //!

    std::auto_ptr<TTbarLJReco> ttlj_reco_ttag0; //!
    std::auto_ptr<TTbarLJReco> ttlj_reco_ttag1; //!

    std::auto_ptr<TTbarLJRecoRanker_chi2>       ttlj_chi2_STD; //!
    std::auto_ptr<TTbarLJRecoRanker_chi2>       ttlj_chi2_TTAG; //!
    std::auto_ptr<TTbarLJRecoRanker_genMatchDR> ttlj_genR; //!

    ClassDef(EffyTTbarRECO, 0);
  };

}

#endif
