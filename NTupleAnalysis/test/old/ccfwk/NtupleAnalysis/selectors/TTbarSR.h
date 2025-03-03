#ifndef NAK_TTbarSR_H
#define NAK_TTbarSR_H

#include <string>
#include <memory>

#include "SelectorBASE.h"

#include <inc/EventSelection.h>
#include <inc/TTbarLJReco.h>
#include <inc/TTbarLJRecoTools.h>
#include <inc/leptonSF.h>
#include <inc/btagSF.h>

namespace nak {

  class TTbarSR : public SelectorBASE {

   public:
    explicit TTbarSR();
    virtual ~TTbarSR() {}

    virtual void configure();
    virtual void configure_output(TFile&);

    virtual Bool_t Process(Long64_t entry);

   protected:
    void book_HFolder_list(TFile&, const std::string&);

    void fill_HFolder_list(const std::string&, const int, const xtt::Particle&, const xtt::MET&,
                           const std::vector<xtt::Jet>&, const std::vector<xtt::MergedJet>&, const float, const float,
                           const float);

    void fill_HFolder_list(const std::string&, const int, const xtt::Particle&, const xtt::MET&,
                           const std::vector<xtt::Jet>&, const std::vector<xtt::MergedJet>&, const float, const float,
                           const nak::TTbarLJRecoHyp&, const nak::TTbarGen&, const float,
                           const float);

    void set_HLT_conf(const bool& hlt_cfg_){ HLT_conf = hlt_cfg_; }

    //

    bool make_hfolders; //!

    enum lepton { muon, elec };
    lepton channel; //!

    bool is_DATA; //!
    std::string HLT_conf; //!

    std::auto_ptr<NeutrinoReco> nu_reco; //!

    std::auto_ptr<VTagger>        vtag_ID;      //!
    std::auto_ptr<EventSelection> vtag_evt_sel; //!

    std::auto_ptr<TopTagID>       ttagH_ID;      //!
    std::auto_ptr<EventSelection> ttagH_evt_sel; //!

    std::auto_ptr<TopTagID>       ttagC_ID;      //!
    std::auto_ptr<EventSelection> ttagC_evt_sel; //!

    std::auto_ptr<TTbarLJReco>     ttlj_reco_0tag;  //!
    std::auto_ptr<TTbarLJRecoVTAG> ttlj_reco_vtag; //!
    std::auto_ptr<TTbarLJRecoTTAG> ttlj_reco_ttagH; //!
    std::auto_ptr<TTbarLJRecoTTAG> ttlj_reco_ttagC; //!

    std::auto_ptr<TTbarLJRecoRanker_chi2> ttlj_chi2_0tag;  //!
    std::auto_ptr<TTbarLJRecoRanker_chi2> ttlj_chi2_vtag;  //!
    std::auto_ptr<TTbarLJRecoRanker_chi2> ttlj_chi2_ttagH; //!
    std::auto_ptr<TTbarLJRecoRanker_chi2> ttlj_chi2_ttagC; //!

    std::auto_ptr<leptonSF> lepton_SF; //!
    std::auto_ptr<btagSF> btag_SF; //!

    ClassDef(TTbarSR, 0);
  };

}

#endif
