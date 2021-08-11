#include "EffyTTbarRECO.h"

#include <inc/HFolderTTbarLJRecoHyp.h>
#include <inc/HFolderTopJet.h>

#include <inc/NeutrinoReco.h>
#include <inc/TTbarGen.h>
#include <inc/TopTagID.h>
#include <inc/utils.h>

#include <iostream>

nak::EffyTTbarRECO::EffyTTbarRECO(): SelectorBASE() {

}

void nak::EffyTTbarRECO::configure(){

  channel = "muon";//channel_;

  nu_reco.reset(new nak::NeutrinoRecoSTD());
  ttagID.reset(new nak::CMSTopTagger_tau32());
  const float minDR_ttag_j = 1.2;

  ttagevt_sel.reset(new TopTagEvent("JET_AK4", "JET_AK8", ttagID.get(), minDR_ttag_j));

  ttlj_reco_ttag0.reset(new TTbarLJReco    (nu_reco.get(), "JET_AK4"));
  ttlj_reco_ttag1.reset(new TTbarLJRecoTTAG(nu_reco.get(), "JET_AK4", "JET_AK8", ttagID.get(), minDR_ttag_j));

  ttlj_chi2_STD .reset(new TTbarLJRecoRanker_chi2     (174., 18., 181., 15.));
  ttlj_chi2_TTAG.reset(new TTbarLJRecoRanker_chi2_TTAG(174., 18., 181., 15.));
  ttlj_genR.reset(new TTbarLJRecoRanker_genMatchDR(.1, .3, .4, .8));
}

void nak::EffyTTbarRECO::configure_output(TFile& of){

  // h-folder
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "input__chi2");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "input__chi2__ttag0");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "input__chi2__ttag1");

  book_HFolder<nak::HFolderTopJet>(of, "input__topjet__ttag1");

  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__chi2");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__chi2__ttag0");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__chi2__ttag1");

  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__genR");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__genR__ttag0");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__genR__ttag1");

  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__genR_eq_chi2");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__genR_eq_chi2__ttag0");
  book_HFolder<nak::HFolderTTbarLJRecoHyp>(of, "genlj__genR_eq_chi2__ttag1");

  return;
}

Bool_t nak::EffyTTbarRECO::Process(Long64_t entry){

  if(!SelectorBASE::Process(entry)) return kFALSE;

//  /* event weight */
//  double W = 1.;
//  if(!is_DATA) W *= EVT.INFO->MCWeight;

  // LEPTON
  xtt::Particle* lepton(0);
  bool doMuon(false), doElec(false);
  if(channel == "muon"){
    if(EVT.MUO->size() == 1 && EVT.ELE->size() == 0){

      lepton = &EVT.MUO->at(0);
      doMuon = true;
    }
    else return kFALSE;
  }
  else if(channel == "elec"){
    if(EVT.MUO->size() == 0 && EVT.ELE->size() == 1){

      lepton = &EVT.ELE->at(0);
      doElec = true;
    }
    else return kFALSE;
  }
  else util::KILL("TTbarRECOAnalyzer::AnalyzeEvent -- undefined value for 'channel' argument ('muon' or 'elec'): "+channel);

  if(!EVT.JET_AK4->size()) return kFALSE;

  // LEPTON 2D-cut boolean
  float minDR_jet25 = dRmin      (*lepton, *EVT.JET_AK4);
  float pTrel_jet25 = pTrel_dRmin(*lepton, *EVT.JET_AK4);
  bool lept_2Dcut = minDR_jet25 > 0.4 || pTrel_jet25 > 25.;

  //// JET
  EVT.clean_kin<xtt::Jet>      ("JET_AK4",  30., 2.4);
  EVT.clean_kin<xtt::MergedJet>("JET_AK8", 400., 2.4);

//  if(!is_DATA && doMuon) W *= lepton_SF->get_MuoID_weight(lepton->pt, lepton->eta);
//  if(!is_DATA && doElec) W *= lepton_SF->get_EleID_weight(lepton->pt, ((xtt::Electron*) lepton)->scEta);
//  fill_HFolderList("1_lepsel", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);
// 
//  // HIGH LEVEL TRIGGER
//  if(doMuon){
//    if(!EVT.HLT->Mu40_eta2p1) return kFALSE;
//    if(!is_DATA) W *= lepton_SF->get_MuoHLT_weight(lepton->pt, lepton->eta);
//  }
// 
//  if(doElec){
// 
//    bool HLT_bit(0);
//    if(HLT_conf == "EleHa_DATA") HLT_bit = EVT.HLT->Ele30_Jet100_Jet25;
//    else if(HLT_conf == "JetHT_DATA") HLT_bit = EVT.HLT->PFJet320 && !EVT.HLT->Ele30_Jet100_Jet25;
//    else HLT_bit = EVT.HLT->Ele30_Jet100_Jet25 || EVT.HLT->PFJet320;
// 
//    if(!HLT_bit) return kFALSE;
//    if(!is_DATA) W *= lepton_SF->get_EleHLT_weight(EVT.JET_AK4->at(0)->pt);
//  }
// 
//  fill_HFolderList("2_HLT", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);
//
  /* jet selection */
  int jetN_pt050(0), jetN_pt200(0);
  for(unsigned int i=0; i<EVT.JET_AK4->size(); ++i){
    if(EVT.JET_AK4->at(i).pt >  50.) ++jetN_pt050;
    if(EVT.JET_AK4->at(i).pt > 200.) ++jetN_pt200;
  }

  if(!(jetN_pt050 >= 2)) return kFALSE;
  if(!(jetN_pt200 >= 1)) return kFALSE;
//  fill_HFolderList("3_jetsel", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // MET selection
  float MET(EVT.MET->pt);
  if(!(MET > 50.)) return kFALSE;

  float HTlep(lepton->pt + EVT.MET->pt);
  if(!(HTlep > 150.)) return kFALSE;
//  fill_HFolderList("4_METsel", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // LEPTON 2D-cut selection
  if(!lept_2Dcut) return kFALSE;
//  fill_HFolderList("5_lep2Dcut", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

  // TRIANGULAR-CUTS (electron-only)
  if(doElec){

    bool triang_jet1   = triangular_cut(*EVT.MET, EVT.JET_AK4->at(0));
    bool triang_lepton = triangular_cut(*EVT.MET, *lepton);
    if(!triang_jet1 || !triang_lepton) return kFALSE;
  }
//  fill_HFolderList("5_triangc", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);

//  /* top-tag selection */
//  std::vector<xtt::MergedJet*> toptagjets = get_toptag_jets(EVT.JET_AK8);
//
//!//   bool lep_wo_overlap(false), jet_wo_overlap(false);
//!//   for(unsigned int i=0; i<toptagjets.size(); ++i){
//!// 
//!//     if(toptagjets.at(i).p4().DeltaR(lepton->p4()) > 0.8) lep_wo_overlap = true;
//!// 
//!//     for(unsigned int j=0; j<EVT.JET_AK4->size(); ++j)
//!//       if(toptagjets.at(i).p4().DeltaR(EVT.JET_AK4->at(j)->p4()) > 1.3) jet_wo_overlap = true;
//!//   }
//!// 
//!//   bool toptag_flag = toptagjets.size() && lep_wo_overlap && jet_wo_overlap;
//!// //  if(toptagjets.size() > 1) return kFALSE;
//!// 
//!//   /* ttbar kinematic reconstruction and final kinematic cuts */
//!//   nak::TTbar reco_ttbar;
//!//   if(!toptag_flag) nak::fill_ttbar(reco_ttbar, *lepton, *EVT.MET, *EVT.JET_AK4);
//!//   else nak::fill_ttbar_toptag(reco_ttbar, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8);
//!// 
//!//   if(doElec && !(reco_ttbar.toplep.Pt() > 140.)) return kFALSE;
//!// 
//!//   fill_HFolderList("6_kinsel", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);
//!//   if(toptag_flag) fill_HFolderList("6_kinsel_toptag", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);
//!// 
//!//   ((nak::HFolderTTbar*) folder["6_kinsel_ttbar"])->Fill(reco_ttbar, W);
//!//   if(toptag_flag) ((nak::HFolderTTbar*) folder["6_kinsel_toptag_ttbar"])->Fill(reco_ttbar, W);
//!// 
//!// //  if(!toptag_flag){
//!// //
//!// //    std::cout << "***" << EVT.INFO->Event << "***********\n";
//!// //    std::cout << " chi2    = " << nak::chi2(reco_ttbar.toplep, reco_ttbar.tophad) << std::endl;
//!// //    std::cout << " chi2lep = " << nak::chi2_toplep(reco_ttbar.toplep) << std::endl;
//!// //    std::cout << " chi2had = " << nak::chi2_tophad(reco_ttbar.tophad) << std::endl;
//!// //    std::cout << " nu pz   = " << reco_ttbar.neutrino_pz << std::endl;
//!// //    std::cout << " lep     = " << lepton->pt <<" "<< lepton->eta << std::endl;
//!// //    std::cout << " MET     = " << EVT.MET->pt <<" "<< EVT.MET->phi << std::endl;
//!// //  }
//!// 
//!//   /* cut on chi2 discriminator */
//!//   if(!(nak::chi2(reco_ttbar.toplep, reco_ttbar.tophad) < 50.)) return kFALSE;
//!// 
//!//   fill_HFolderList("7_chi2", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);
//!//   if(toptag_flag) fill_HFolderList("7_chi2_toptag", EVT.INFO->nPV, *lepton, *EVT.MET, *EVT.JET_AK4, *EVT.JET_AK8, minDR_jet25, pTrel_jet25, W);
//!// 
//!//   ((nak::HFolderTTbar*) folder["7_chi2_ttbar"])->Fill(reco_ttbar, W);
//!//   if(toptag_flag) ((nak::HFolderTTbar*) folder["7_chi2_toptag_ttbar"])->Fill(reco_ttbar, W);
//!// 
//!// //  /* b-tag selection */
//!// //
//!// //  if(!is_DATA) W *= 1.;//btag_SF->GetWeight(EVT.JET_AK4);
//!// 
//!//   if(is_DATA && W != 1.) util::KILL("TTbarRECOAnalyzer::AnalyzeEvent -- logical error: real DATA must not be reweighted");

  const float w = 1.;

  const TTbarGen ttgen(*EVT.GENP);

  const bool flag_ttagevt = ttagevt_sel->pass(EVT);

  const TTbarLJReco* ttlj_reco = flag_ttagevt ? ttlj_reco_ttag1.get() : ttlj_reco_ttag0.get();
  const std::vector<TTbarLJRecoHyp> tt_hyps(ttlj_reco->get_hyps(EVT));

  const TTbarLJRecoRanker_chi2* ttlj_chi2 = flag_ttagevt ? ttlj_chi2_TTAG.get() : ttlj_chi2_STD.get();

  const TTbarLJRecoHyp* bhyp_genR = ttlj_genR->best_hyp(tt_hyps, ttgen, flag_ttagevt);
  const TTbarLJRecoHyp* bhyp_chi2 = ttlj_chi2->best_hyp(tt_hyps);
  if(!bhyp_chi2) util::KILL("TTbarRECOAnalyzer::AnalyzeEvent -- best-chi2 ttbar hypothesis not found (hypotheses="+util::int_to_str(tt_hyps.size())+")");

  const float bhyp_chi2_val(ttlj_chi2->hyp_value(*bhyp_chi2));

  const std::string ttag_posx = flag_ttagevt ? "ttag1" : "ttag0";

  HFolder<nak::HFolderTTbarLJRecoHyp>("input__chi2")            ->Fill(*bhyp_chi2, ttgen, bhyp_chi2_val, w);
  HFolder<nak::HFolderTTbarLJRecoHyp>("input__chi2__"+ttag_posx)->Fill(*bhyp_chi2, ttgen, bhyp_chi2_val, w);

  if(flag_ttagevt) HFolder<nak::HFolderTopJet>("input__topjet__"+ttag_posx)->Fill(*EVT.JET_AK8, w);

  if(!ttgen.is_emujets()) return kFALSE;

  HFolder<nak::HFolderTTbarLJRecoHyp>("genlj__chi2")            ->Fill(*bhyp_chi2, ttgen, bhyp_chi2_val, w);
  HFolder<nak::HFolderTTbarLJRecoHyp>("genlj__chi2__"+ttag_posx)->Fill(*bhyp_chi2, ttgen, bhyp_chi2_val, w);

  if(bhyp_genR){
    const float bhyp_genR_val(ttlj_chi2->hyp_value(*bhyp_genR));

    HFolder<nak::HFolderTTbarLJRecoHyp>("genlj__genR")            ->Fill(*bhyp_genR, ttgen, bhyp_genR_val, w);
    HFolder<nak::HFolderTTbarLJRecoHyp>("genlj__genR__"+ttag_posx)->Fill(*bhyp_genR, ttgen, bhyp_genR_val, w);
  }

  if(bhyp_genR == bhyp_chi2){
    HFolder<nak::HFolderTTbarLJRecoHyp>("genlj__genR_eq_chi2")            ->Fill(*bhyp_chi2, ttgen, bhyp_chi2_val, w);
    HFolder<nak::HFolderTTbarLJRecoHyp>("genlj__genR_eq_chi2__"+ttag_posx)->Fill(*bhyp_chi2, ttgen, bhyp_chi2_val, w);
  }

//!//
//!//  std::cout << "--------------------\n";
//!//  std::cout << " event : " << EVT.INFO->Event << "; toptagged [y/n] = " << flag_ttagevt << std::endl;
//!//
//!//  for(int j=0; j<int(EVT.JET_AK4->size()); ++j)
//!//    std::cout << " rec        jet :" << " pt=" << EVT.JET_AK4->at(j).pt << " eta=" << EVT.JET_AK4->at(j).eta << " phi=" << EVT.JET_AK4->at(j).phi << std::endl;
//!//
//!//  std::cout << std::endl;
//!//  std::cout << "bhyp_genR::val = " << ttlj_genR->hyp_value(*bhyp_genR, ttgen, flag_ttagevt) << std::endl;
//!//  std::cout << "rec tophad M = " << bhyp_genR->tophad_p4().M() << std::endl;
//!//  std::cout << std::endl;
//!//
//!//  for(int j=0; j<int(bhyp_genR->tophad_jet_ptrs().size()); ++j)
//!//    std::cout << " rec tophad jet :" << " pt=" << bhyp_genR->tophad_jet_ptrs().at(j)->pt << " eta=" << bhyp_genR->tophad_jet_ptrs().at(j)->eta << " phi=" << bhyp_genR->tophad_jet_ptrs().at(j)->phi << std::endl;
//!//  for(int j=0; j<int(bhyp_genR->toplep_jet_ptrs().size()); ++j)
//!//    std::cout << " rec toplep jet :" << " pt=" << bhyp_genR->toplep_jet_ptrs().at(j)->pt << " eta=" << bhyp_genR->toplep_jet_ptrs().at(j)->eta << " phi=" << bhyp_genR->toplep_jet_ptrs().at(j)->phi << std::endl;
//!//
//!//  std::cout << "  ******\n";
//!//
//!//  std::cout << " gen b  lep     :" << " pt=" << ttgen.b_lep()   ->pt << " eta=" << ttgen.b_lep()   ->eta << " phi=" << ttgen.b_lep()   ->phi << std::endl;
//!//  std::cout << " gen b  had     :" << " pt=" << ttgen.b_had()   ->pt << " eta=" << ttgen.b_had()   ->eta << " phi=" << ttgen.b_had()   ->phi << std::endl;
//!//  std::cout << " gen Q1 had     :" << " pt=" << ttgen.W_had_fu()->pt << " eta=" << ttgen.W_had_fu()->eta << " phi=" << ttgen.W_had_fu()->phi << std::endl;
//!//  std::cout << " gen Q2 had     :" << " pt=" << ttgen.W_had_fd()->pt << " eta=" << ttgen.W_had_fd()->eta << " phi=" << ttgen.W_had_fd()->phi << std::endl;
//!//

//  std::cout << "\n";
//
//  std::cout << "*** JET_AK4\n";
//  for(int i=0; i<int(EVT.JET_AK4->size()); ++i)
//    std::cout << " " << i << " pt=" << EVT.JET_AK4->at(i).pt << " eta=" << EVT.JET_AK4->at(i).eta << " phi=" << EVT.JET_AK4->at(i).phi << std::endl;
//  std::cout << " lepton pt=" << lepton->pt << " eta=" << lepton->eta << " phi=" << lepton->phi << std::endl;
//  std::cout << " MET pt=" << EVT.MET->pt << " phi=" << EVT.MET->phi << std::endl;
//
//  std::cout << "*** GEN_ttbar\n";
//  std::cout << " b_lep    : pt=" << ttgen.b_lep()->pt << " eta=" << ttgen.b_lep()->eta << " phi=" << ttgen.b_lep()->phi << std::endl;
//  std::cout << " lepton   : pt=" << ttgen.lepton()->pt << " eta=" << ttgen.lepton()->eta << " phi=" << ttgen.lepton()->phi << std::endl;
//  std::cout << " neutrino : pt=" << ttgen.neutrino()->pt << " eta=" << ttgen.neutrino()->eta << " phi=" << ttgen.neutrino()->phi << std::endl;

  return kFALSE;
}
