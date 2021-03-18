#include "TTbarSR.h"

#include <inc/HFolderXObj.h>
#include <inc/HFolderLepton.h>
#include <inc/HFolderJet.h>
#include <inc/HFolderTopJet.h>
#include <inc/HFolderTTbarLJRecoHyp.h>

#include <inc/NeutrinoReco.h>
#include <inc/TTbarGen.h>
#include <inc/TopTagID.h>
#include <inc/utils.h>

#include <iostream>

nak::TTbarSR::TTbarSR(): SelectorBASE() {
}

void nak::TTbarSR::configure(){

  make_hfolders = (output_file_ != "");

  is_DATA = 0;//is_data_;

  std::string channel_("muon");
  if     (channel_ == "muon") channel = muon;
  else if(channel_ == "elec") channel = elec;
  else util::KILL("TTbarSR::TTbarSR -- invalid 'channel' argument ('muon' or 'elec'): "+channel_);

  HLT_conf = "none";

  // TTBAR RECO
  nu_reco.reset(new nak::NeutrinoRecoSTD());

  vtag_ID.reset(new nak::VTagger());
  const float minDR_vtag_j = 1.2;
  vtag_evt_sel.reset(new VTagEvent("JET_AK4", "JET_AK8", vtag_ID.get(), minDR_vtag_j));

  ttagH_ID.reset(new nak::HEPTopTagger());
  const float minDR_ttagH_j = 1.9;
  ttagH_evt_sel.reset(new TopTagEvent("JET_AK4", "JET_CA15", ttagH_ID.get(), minDR_ttagH_j));

  ttagC_ID.reset(new nak::CMSTopTagger_tau32());
  const float minDR_ttagC_j = 1.2;
  ttagC_evt_sel.reset(new TopTagEvent("JET_AK4", "JET_AK8", ttagC_ID.get(), minDR_ttagC_j));

  ttlj_reco_0tag .reset(new TTbarLJReco    (nu_reco.get(), "JET_AK4"));
  ttlj_reco_vtag .reset(new TTbarLJRecoVTAG(nu_reco.get(), "JET_AK4", "JET_AK8" , vtag_ID .get(), minDR_vtag_j));
  ttlj_reco_ttagH.reset(new TTbarLJRecoTTAG(nu_reco.get(), "JET_AK4", "JET_CA15", ttagH_ID.get(), minDR_ttagH_j));
  ttlj_reco_ttagC.reset(new TTbarLJRecoTTAG(nu_reco.get(), "JET_AK4", "JET_AK8" , ttagC_ID.get(), minDR_ttagC_j));

  ttlj_chi2_0tag .reset(new TTbarLJRecoRanker_chi2     (174., 18., 181., 15.));
  ttlj_chi2_vtag .reset(new TTbarLJRecoRanker_chi2     (174., 18., 181., 15.));
  ttlj_chi2_ttagH.reset(new TTbarLJRecoRanker_chi2     (174., 18., 181., 15.));
  ttlj_chi2_ttagC.reset(new TTbarLJRecoRanker_chi2     (174., 18., 181., 15.));

  // Data/MC SFs
  lepton_SF.reset(new leptonSF());
//  btag_SF.reset(new btagSF("CSVM", channel));

  return;
}

void nak::TTbarSR::configure_output(TFile& of){

  if(make_hfolders){

    book_HFolder_list(of, "lep1");
    book_HFolder_list(of, "HLT");
    book_HFolder_list(of, "jet2");
    book_HFolder_list(of, "jet1");
    book_HFolder_list(of, "met");
    book_HFolder_list(of, "htlep");
    book_HFolder_list(of, "twodcut");
    book_HFolder_list(of, "triangcut");
    book_HFolder_list(of, "toplep_pt");
    book_HFolder_list(of, "toplep_pt__0tag");
    book_HFolder_list(of, "toplep_pt__vtag");
    book_HFolder_list(of, "toplep_pt__ttagH");
    book_HFolder_list(of, "toplep_pt__ttagC");
    book_HFolder_list(of, "chi2");
    book_HFolder_list(of, "chi2__0tag");
    book_HFolder_list(of, "chi2__0tag__btag0");
    book_HFolder_list(of, "chi2__0tag__btag1");
    book_HFolder_list(of, "chi2__vtag");
    book_HFolder_list(of, "chi2__vtag__btag0");
    book_HFolder_list(of, "chi2__vtag__btag1");
    book_HFolder_list(of, "chi2__ttagH");
    book_HFolder_list(of, "chi2__ttagH__btag0");
    book_HFolder_list(of, "chi2__ttagH__btag1");
    book_HFolder_list(of, "chi2__ttagC");
    book_HFolder_list(of, "chi2__ttagC__btag0");
    book_HFolder_list(of, "chi2__ttagC__btag1");
  }

  return;
}

Bool_t nak::TTbarSR::Process(Long64_t entry){

  if(!SelectorBASE::Process(entry)) return kFALSE;

  // event weight
  float W = 1.;
  if(!is_DATA) W *= EVT.INFO->MCWeight;
//  if(!is_DATA) W *= EVT.INFO->PUWeight;

  // LEPTON selection
  bool pass_lep1(false);
  xtt::Particle* lepton(0);
  if     (channel == muon      &&
          EVT.MUO->size() == 1 &&
          EVT.ELE->size() == 0 ){ lepton = &EVT.MUO->at(0); pass_lep1 = true; }
  else if(channel == elec      &&
          EVT.MUO->size() == 0 &&
          EVT.ELE->size() == 1 ){ lepton = &EVT.ELE->at(0); pass_lep1 = true; }

  if(!pass_lep1) return kFALSE;

  /* LEPTON 2D-cut boolean */
  if(!EVT.JET_AK4->size()) return kFALSE;
  float minDR_jet25 = dRmin      (*lepton, *EVT.JET_AK4);
  float pTrel_jet25 = pTrel_dRmin(*lepton, *EVT.JET_AK4);
  bool pass_twodcut = minDR_jet25 > 0.4 || pTrel_jet25 > 25.;

//  if(!is_DATA && muon) W *= lepton_SF->get_MuoID_weight(lepton->pt, lepton->eta);
//  if(!is_DATA && elec) W *= lepton_SF->get_EleID_weight(lepton->pt, ((xtt::Electron*) lepton)->scEta);
  if(make_hfolders) fill_HFolder_list("lep1", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // HLT selection
  bool pass_HLT(0);
  if     (channel == muon) pass_HLT = EVT.HLT->Mu40_eta2p1_PFJet200_PFJet50;
  else if(channel == elec) pass_HLT = EVT.HLT->Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50;

  if(!pass_HLT) return kFALSE;
  if(make_hfolders) fill_HFolder_list("HLT", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // JET selection
  /* skim jet collections */
  EVT.clean_kin<xtt::Jet>      ("JET_AK4" ,  30., 2.4);
  EVT.clean_kin<xtt::MergedJet>("JET_AK8" , 400., 2.4);
  EVT.clean_kin<xtt::MergedJet>("JET_CA15", 300., 2.4);

  int jetN_pt050(0), jetN_pt200(0);
  for(unsigned int i=0; i<EVT.JET_AK4->size(); ++i){

    if(EVT.JET_AK4->at(i).pt >  50.) ++jetN_pt050;
    if(EVT.JET_AK4->at(i).pt > 200.) ++jetN_pt200;
  }

  bool pass_jet2 = (jetN_pt050 >= 2) && (jetN_pt050 >= 2);
  if(!pass_jet2) return kFALSE;
  if(make_hfolders) fill_HFolder_list("jet2", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  bool pass_jet1 = (jetN_pt200 >= 1);
  if(!pass_jet1) return kFALSE;
  if(make_hfolders) fill_HFolder_list("jet1", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // MET selection
  bool pass_met = EVT.MET->pt > 50.;
  if(!pass_met) return kFALSE;
  if(make_hfolders) fill_HFolder_list("met", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  bool pass_htlep = (lepton->pt + EVT.MET->pt) > 150.;
  if(!pass_htlep) return kFALSE;
  if(make_hfolders) fill_HFolder_list("htlep", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // LEPTON 2D-cut selection
  if(!pass_twodcut) return kFALSE;
  if(make_hfolders) fill_HFolder_list("twodcut", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // TRIANGULAR-CUTS selection
  bool pass_triangcut(false);
  if     (channel == muon) pass_triangcut = true;
  else if(channel == elec){

    bool triangc_jet1 = triangular_cut(*EVT.MET, EVT.JET_AK4->at(0));
    bool triangc_lep1 = triangular_cut(*EVT.MET, *lepton);
    pass_triangcut = triangc_lep1 && triangc_jet1;
  }
  if(!pass_triangcut) return kFALSE;
  if(make_hfolders) fill_HFolder_list("triangcut", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // v/TOP-TAG EVENT boolean
  const bool flag_vtagevt  = vtag_evt_sel ->pass(EVT);
  const bool flag_ttagHevt = ttagH_evt_sel->pass(EVT);
  const bool flag_ttagCevt = ttagC_evt_sel->pass(EVT);

  // TTBAR RECO
  std::string xtag_p("");
  const TTbarLJReco* ttlj_reco(0);
  const TTbarLJRecoRanker_chi2* ttlj_chi2(0);

  if     (flag_ttagCevt) { xtag_p = "ttagC"; ttlj_reco = ttlj_reco_ttagC.get(); ttlj_chi2 = ttlj_chi2_ttagC.get(); }
  else if(flag_ttagHevt) { xtag_p = "ttagH"; ttlj_reco = ttlj_reco_ttagH.get(); ttlj_chi2 = ttlj_chi2_ttagH.get(); }
//  else if(flag_vtagevt)  { xtag_p = "vtag" ; ttlj_reco = ttlj_reco_vtag .get(); ttlj_chi2 = ttlj_chi2_vtag .get(); }
  else                   { xtag_p = "0tag" ; ttlj_reco = ttlj_reco_0tag .get(); ttlj_chi2 = ttlj_chi2_0tag .get(); }

  const std::vector<TTbarLJRecoHyp> tt_hyps(ttlj_reco->get_hyps(EVT));

  const TTbarLJRecoHyp* bhyp_chi2 = ttlj_chi2->best_hyp(tt_hyps);
  if(!bhyp_chi2) util::KILL("TTbarSR::AnalyzeEvent -- best-chi2 ttbar hypothesis not found");
  const float bhyp_chi2_val(ttlj_chi2->hyp_value(*bhyp_chi2));

  const TTbarGen ttgen(*EVT.GENP);


//  /*** ttbar reco debugging ***/
//  if(ttgen.is_ljets() && bhyp_chi2){
//
//    float rec_ttbar__gen_DM_pct((bhyp_chi2->ttbar_p4().M()-ttgen.mttbar())/ttgen.mttbar());
//
//    if(fabs(rec_ttbar__gen_DM_pct) > .5){
//
//      std::cout << "\n\n------- Event = " << EVT.INFO->Event << "--------------" << std::endl;
//      std::cout << " rec_ttbar__gen_DM_pct = " << rec_ttbar__gen_DM_pct << std::endl;
//      ttgen.printout();
//      bhyp_chi2->printout();
//
//      std::cout << "\n@@@ JET_AK4 ---\n";
//      for(unsigned int i=0; i<EVT.JET_AK4->size(); ++i){
//
//        std::cout << "  jet_AK4 " << i+1 << ":";
//
//        std::cout << "  pt="    << EVT.JET_AK4->at(i).p4().Pt();
//        std::cout << "  eta="   << EVT.JET_AK4->at(i).p4().Eta();
//        std::cout << "  phi="   << EVT.JET_AK4->at(i).p4().Phi();
//        std::cout << "  M="     << EVT.JET_AK4->at(i).p4().M();
//        std::cout << "  CSVv2IVF=" << EVT.JET_AK4->at(i).btagCSVIVF;
//
//        std::cout << std::endl;
//      }
//
//      std::cout << "\n@@@ JET_AK8 ---\n";
//      for(unsigned int i=0; i<EVT.JET_AK8->size(); ++i){
//
//        std::cout << "  jet_AK8 " << i+1 << ":";
//
//        std::cout << "  pt="    << EVT.JET_AK8->at(i).p4().Pt();
//        std::cout << "  eta="   << EVT.JET_AK8->at(i).p4().Eta();
//        std::cout << "  phi="   << EVT.JET_AK8->at(i).p4().Phi();
//        std::cout << "  M="     << EVT.JET_AK8->at(i).p4().M();
//        std::cout << "  Msd="   << EVT.JET_AK8->at(i).Msoftdrop;
//        std::cout << "  CSVv2IVF=" << EVT.JET_AK8->at(i).btagCSVIVF;
//
//        std::cout << std::endl;
//      }
//
//      std::cout << "\n@@@ JET_CA15 ---\n";
//      for(unsigned int i=0; i<EVT.JET_CA15->size(); ++i){
//
//        std::cout << "  jet_CA15 " << i+1 << ":";
//
//        std::cout << "  pt="    << EVT.JET_CA15->at(i).p4().Pt();
//        std::cout << "  eta="   << EVT.JET_CA15->at(i).p4().Eta();
//        std::cout << "  phi="   << EVT.JET_CA15->at(i).p4().Phi();
//        std::cout << "  M="     << EVT.JET_CA15->at(i).p4().M();
//        std::cout << "  Msd="   << EVT.JET_CA15->at(i).Msoftdrop;
//        std::cout << "  CSVv2IVF=" << EVT.JET_CA15->at(i).btagCSVIVF;
//
//        std::cout << std::endl;
//      }
//    }
//  }
//  /****************************/


  // LEPTONIC-TOP pt selection
  bool pass_topleppt(false);
  if     (channel == muon) pass_topleppt = true;
  else if(channel == elec) pass_topleppt = bhyp_chi2->toplep_p4().Pt() > 140.;
  if(!pass_topleppt) return kFALSE;

  if(make_hfolders){

    fill_HFolder_list("toplep_pt"         ,EVT.INFO->nPV,*lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, *bhyp_chi2, ttgen, bhyp_chi2_val, W);
    fill_HFolder_list("toplep_pt__"+xtag_p,EVT.INFO->nPV,*lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, *bhyp_chi2, ttgen, bhyp_chi2_val, W);
  }

  // CHI2 selection
  const bool pass_chi2 = bhyp_chi2_val < 50.;
  if(!pass_chi2) return kFALSE;

  int n_btagCSVM(0);
  for(int i=0; i<int(EVT.JET_AK4->size()); ++i){
    if(EVT.JET_AK4->at(i).btagCSV > 0.679) ++n_btagCSVM;
  }

  const std::string btag_p = n_btagCSVM > 0 ? "btag1" : "btag0";

  if(make_hfolders){

    fill_HFolder_list("chi2"                     , EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4,*EVT.JET_AK8,minDR_jet25,pTrel_jet25,*bhyp_chi2,ttgen,bhyp_chi2_val,W);
    fill_HFolder_list("chi2__"+xtag_p            , EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4,*EVT.JET_AK8,minDR_jet25,pTrel_jet25,*bhyp_chi2,ttgen,bhyp_chi2_val,W);
    fill_HFolder_list("chi2__"+xtag_p+"__"+btag_p, EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4,*EVT.JET_AK8,minDR_jet25,pTrel_jet25,*bhyp_chi2,ttgen,bhyp_chi2_val,W);
  }

  if(is_DATA && W != 1.) util::KILL("TTbarSR::AnalyzeEvent -- logical error: DATA must not be reweighted");

  return kTRUE;
}

void nak::TTbarSR::book_HFolder_list(TFile& of_, const std::string& name_){

  book_HFolder<nak::HFolderXObj>          (of_, name_+"__xobj");
  book_HFolder<nak::HFolderLepton>        (of_, name_+"__lepton");
  book_HFolder<nak::HFolderJet>           (of_, name_+"__ak4jet");
  book_HFolder<nak::HFolderTopJet>        (of_, name_+"__topjet");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of_, name_+"__ttbar");

  return;
}

void nak::TTbarSR::fill_HFolder_list(const std::string& name_, const int nPV_, const xtt::Particle& lepton_, const xtt::MET& MET_, const std::vector<xtt::Jet>& JET_, const std::vector<xtt::MergedJet>& TOPJET_, const float minDR_jet25_, const float pTrel_jet25_, const float W_){

  HFolder<nak::HFolderXObj>  (name_+"__xobj")  ->Fill(nPV_, lepton_, MET_, JET_, TOPJET_, minDR_jet25_, pTrel_jet25_, W_);
  HFolder<nak::HFolderLepton>(name_+"__lepton")->Fill(*((xtt::Lepton*) &lepton_), W_);
  HFolder<nak::HFolderJet>   (name_+"__ak4jet")->Fill(JET_, W_);
  HFolder<nak::HFolderTopJet>(name_+"__topjet")->Fill(TOPJET_, W_);

  return;
}

void nak::TTbarSR::fill_HFolder_list(const std::string& name_, const int nPV_, const xtt::Particle& lepton_, const xtt::MET& MET_, const std::vector<xtt::Jet>& JET_, const std::vector<xtt::MergedJet>& TOPJET_, const float minDR_jet25_, const float pTrel_jet25_, const nak::TTbarLJRecoHyp& hyp, const nak::TTbarGen& ttgen, const float hyp_val, const float W_){

  fill_HFolder_list(name_, nPV_, lepton_, MET_, JET_, TOPJET_, minDR_jet25_, pTrel_jet25_, W_);
  HFolder<nak::HFolderTTbarLJRecoHyp>(name_+"__ttbar")->Fill(hyp, ttgen, hyp_val, W_);

  return;
}
