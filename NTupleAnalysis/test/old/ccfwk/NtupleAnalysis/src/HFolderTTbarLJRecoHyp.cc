#include <inc/HFolderTTbarLJRecoHyp.h>

nak::HFolderTTbarLJRecoHyp::HFolderTTbarLJRecoHyp(TFile& file, const std::string& dname): HFolderBASE(file, dname) {

  book_TH1F("gen_ttbar__M" , 600, 0, 6000);
  book_TH1F("gen_ttbar__pt", 300, 0, 3000);

  book_TH1F("gen_thad__M" , 360, 0, 360);
  book_TH1F("gen_thad__pt", 180, 0, 1800);

  book_TH1F("gen_tlep__M" , 360, 0, 360);
  book_TH1F("gen_tlep__pt", 180, 0, 1800);
  book_TH1F("gen_tlep__px", 120, -1200, 1200);
  book_TH1F("gen_tlep__py", 120, -1200, 1200);
  book_TH1F("gen_tlep__pz", 120, -1200, 1200);

  book_TH1F("gen_tops__DR" , 60, 0, 6);
  book_TH1F("gen_tops__Dpt", 180, -450, 450);

  book_TH1F("gen_Wlep__M" , 120, 74, 86);
  book_TH1F("gen_Wlep__Mt", 180, 0, 180);
  book_TH1F("gen_Wlep__pt", 180, 0, 1800);
  book_TH1F("gen_Wlep__px", 120, -1200, 1200);
  book_TH1F("gen_Wlep__py", 120, -1200, 1200);
  book_TH1F("gen_Wlep__pz", 120, -1200, 1200);

  book_TH1F("gen_lep__pt"       , 120, 0, 1200);
  book_TH1F("gen_lep__eta"      , 60, -6, 6);
  book_TH1F("gen_lep__phi"      , 60, -3.15, 3.15);
  book_TH1F("gen_lep__cosThetaX", 40, -1, 1);

  book_TH1F("gen_neu__pt"       , 120, 0, 1200);
  book_TH1F("gen_neu__phi"      , 60, -3.15, 3.15);
  book_TH1F("gen_neu__px"       , 120, -600, 600);
  book_TH1F("gen_neu__py"       , 120, -600, 600);
  book_TH1F("gen_neu__pz"       , 120, -600, 600);
  book_TH1F("gen_neu__cosThetaX", 40, -1, 1);

  book_TH1F("gen_blep__pt"       , 120, 0, 1200);
  book_TH1F("gen_blep__eta"      , 60, -6, 6);
  book_TH1F("gen_blep__phi"      , 60, -3.15, 3.15);
  book_TH1F("gen_blep__px"       , 120, -1200, 1200);
  book_TH1F("gen_blep__py"       , 120, -1200, 1200);
  book_TH1F("gen_blep__pz"       , 120, -1200, 1200);
  book_TH1F("gen_blep__cosThetaX", 40, -1, 1);

  book_TH1F("rec_chi2", 300, 0, 600);
  book_TH2F("rec_chi2__VS__rec_ttbar__M", 300, 0, 600, 600, 0, 6000);

  book_TH1F("rec_ttbar__M"          , 600, 0, 6000);
  book_TH1F("rec_ttbar__pt"         , 300, 0, 3000);
  book_TH1F("rec_ttbar__gen_DM"     , 120, -600, 600);
  book_TH1F("rec_ttbar__gen_Dpt"    , 120, -600, 600);
  book_TH1F("rec_ttbar__gen_DM_pct" , 120, -1.2, 1.2);
  book_TH1F("rec_ttbar__gen_Dpt_pct", 120, -1.2, 1.2);

  book_TH1F("rec_thad__M"           , 360, 0, 360);
  book_TH1F("rec_thad__Msd"         , 360, 0, 360);
  book_TH1F("rec_thad__pt"          , 180, 0, 1800);
  book_TH1F("rec_thad__jetN"        , 7, 0, 7);
  book_TH1F("rec_thad__gen_DM"      , 240, -120, 120);
  book_TH1F("rec_thad__gen_DMsd"    , 240, -120, 120);
  book_TH1F("rec_thad__gen_Dpt"     , 120, -600, 600);
  book_TH1F("rec_thad__gen_Deta"    , 120, -1.2, 1.2);
  book_TH1F("rec_thad__gen_Dphi"    , 60, 0, 3.15);
  book_TH1F("rec_thad__gen_DR"      , 60, 0, 3);
  book_TH1F("rec_thad__gen_DM_pct"  , 120, -1.2, 1.2);
  book_TH1F("rec_thad__gen_DMsd_pct", 120, -1.2, 1.2);
  book_TH1F("rec_thad__gen_Dpt_pct" , 120, -1.2, 1.2);

  book_TH1F("rec_tlep__M"          , 360, 0, 360);
  book_TH1F("rec_tlep__pt"         , 180, 0, 1800);
  book_TH1F("rec_tlep__px"         , 120, -1200, 1200);
  book_TH1F("rec_tlep__py"         , 120, -1200, 1200);
  book_TH1F("rec_tlep__pz"         , 120, -1200, 1200);
  book_TH1F("rec_tlep__jetN"       , 4, 0, 4);
  book_TH1F("rec_tlep__gen_DM"     , 240, -120, 120);
  book_TH1F("rec_tlep__gen_Dpt"    , 120, -600, 600);
  book_TH1F("rec_tlep__gen_Dpx"    , 120, -600, 600);
  book_TH1F("rec_tlep__gen_Dpy"    , 120, -600, 600);
  book_TH1F("rec_tlep__gen_Dpz"    , 120, -600, 600);
  book_TH1F("rec_tlep__gen_Deta"   , 120, -1.2, 1.2);
  book_TH1F("rec_tlep__gen_Dphi"   , 60, 0, 3.15);
  book_TH1F("rec_tlep__gen_DR"     , 60, 0, 3);
  book_TH1F("rec_tlep__gen_DM_pct" , 120, -1.2, 1.2);
  book_TH1F("rec_tlep__gen_Dpt_pct", 120, -1.2, 1.2);
  book_TH1F("rec_tlep__gen_Dpx_pct", 120, -1.2, 1.2);
  book_TH1F("rec_tlep__gen_Dpy_pct", 120, -1.2, 1.2);
  book_TH1F("rec_tlep__gen_Dpz_pct", 120, -1.2, 1.2);

  book_TH1F("rec_tops__DR" , 60, 0, 6);
  book_TH1F("rec_tops__Dpt", 180, -450, 450);

  book_TH1F("rec_Wlep__M"          , 360, 0, 360);
  book_TH1F("rec_Wlep__Mt"         , 360, 0, 360);
  book_TH1F("rec_Wlep__pt"         , 180, 0, 1800);
  book_TH1F("rec_Wlep__px"         , 120, -1200, 1200);
  book_TH1F("rec_Wlep__py"         , 120, -1200, 1200);
  book_TH1F("rec_Wlep__pz"         , 120, -1200, 1200);
  book_TH1F("rec_Wlep__gen_DM"     , 240, -120, 120);
  book_TH1F("rec_Wlep__gen_DMt"    , 240, -120, 120);
  book_TH1F("rec_Wlep__gen_Dpt"    , 120, -600, 600);
  book_TH1F("rec_Wlep__gen_Dpx"    , 120, -600, 600);
  book_TH1F("rec_Wlep__gen_Dpy"    , 120, -600, 600);
  book_TH1F("rec_Wlep__gen_Dpz"    , 120, -600, 600);
  book_TH1F("rec_Wlep__gen_DM_pct" , 120, -1.2, 1.2);
  book_TH1F("rec_Wlep__gen_DMt_pct", 120, -1.2, 1.2);
  book_TH1F("rec_Wlep__gen_Dpt_pct", 120, -1.2, 1.2);
  book_TH1F("rec_Wlep__gen_Dpx_pct", 120, -1.2, 1.2);
  book_TH1F("rec_Wlep__gen_Dpy_pct", 120, -1.2, 1.2);
  book_TH1F("rec_Wlep__gen_Dpz_pct", 120, -1.2, 1.2);

  book_TH1F("rec_lep__pt"            , 120, 0, 1200);
  book_TH1F("rec_lep__eta"           , 60, -6, 6);
  book_TH1F("rec_lep__phi"           , 60, -3.15, 3.15);
  book_TH1F("rec_lep__cosThetaX"     , 40, -1, 1);
  book_TH1F("rec_lep__gen_DR"        , 60, 0, .06);
  book_TH1F("rec_lep__gen_Dpt"       , 60, -150, 150);
  book_TH1F("rec_lep__gen_Deta"      , 60, -.06, .06);
  book_TH1F("rec_lep__gen_Dphi"      , 60, 0., .06);
  book_TH1F("rec_lep__gen_DcosThetaX", 36, -1.8, 1.8);
  book_TH1F("rec_lep__gen_Dpt_pct"   , 60, -.6, .6);
  book_TH1F("rec_lep__gen_Deta_pct"  , 60, -.06, .06);

  book_TH1F("rec_neu__pt"            , 120, 0, 1200);
  book_TH1F("rec_neu__phi"           , 60, -3.15, 3.15);
  book_TH1F("rec_neu__px"            , 120, -600, 600);
  book_TH1F("rec_neu__py"            , 120, -600, 600);
  book_TH1F("rec_neu__pz"            , 120, -600, 600);
  book_TH1F("rec_neu__cosThetaX"     , 40, -1, 1);
  book_TH1F("rec_neu__gen_DR"        , 60, 0, 6);
  book_TH1F("rec_neu__gen_Dpt"       , 120, -600, 600);
  book_TH1F("rec_neu__gen_Dphi"      , 60, 0., 3.15);
  book_TH1F("rec_neu__gen_Dpx"       , 120, -600, 600);
  book_TH1F("rec_neu__gen_Dpy"       , 120, -600, 600);
  book_TH1F("rec_neu__gen_Dpz"       , 120, -600, 600);
  book_TH1F("rec_neu__gen_DcosThetaX", 36, -1.8, 1.8);
  book_TH1F("rec_neu__gen_Dpt_pct"   , 120, -1.2, 1.2);
  book_TH1F("rec_neu__gen_Dpx_pct"   , 120, -1.2, 1.2);
  book_TH1F("rec_neu__gen_Dpy_pct"   , 120, -1.2, 1.2);
  book_TH1F("rec_neu__gen_Dpz_pct"   , 120, -1.2, 1.2);

  book_TH1F("rec_blep__pt"            , 120, 0, 1200);
  book_TH1F("rec_blep__eta"           , 60, -6, 6);
  book_TH1F("rec_blep__phi"           , 60, -3.15, 3.15);
  book_TH1F("rec_blep__px"            , 120, -1200, 1200);
  book_TH1F("rec_blep__py"            , 120, -1200, 1200);
  book_TH1F("rec_blep__pz"            , 120, -1200, 1200);
  book_TH1F("rec_blep__cosThetaX"     , 40, -1, 1);
  book_TH1F("rec_blep__gen_DR"        , 60, 0, 3);
  book_TH1F("rec_blep__gen_Dpt"       , 60, -300, 300);
  book_TH1F("rec_blep__gen_Deta"      , 60, -.6, .6);
  book_TH1F("rec_blep__gen_Dphi"      , 60, 0., 3.15);
  book_TH1F("rec_blep__gen_Dpx"       , 60, -300, 300);
  book_TH1F("rec_blep__gen_Dpy"       , 60, -300, 300);
  book_TH1F("rec_blep__gen_Dpz"       , 60, -300, 300);
  book_TH1F("rec_blep__gen_DcosThetaX", 36, -1.8, 1.8);
  book_TH1F("rec_blep__gen_Dpt_pct"   , 60, -1.2, 1.2);
  book_TH1F("rec_blep__gen_Deta_pct"  , 60, -.3, .3);
  book_TH1F("rec_blep__gen_Dpx_pct"   , 60, -1.2, 1.2);
  book_TH1F("rec_blep__gen_Dpy_pct"   , 60, -1.2, 1.2);
  book_TH1F("rec_blep__gen_Dpz_pct"   , 60, -1.2, 1.2);

  book_TH1F("rec_lep__cosThetaX__X__rec_blep__cosThetaX", 40, -1, 1);
  book_TH1F("rec_lep__cosThetaX__X__rec_neu__cosThetaX" , 40, -1, 1);
  book_TH1F("rec_neu__cosThetaX__X__rec_blep__cosThetaX", 40, -1, 1);

  book_TH1F("rec_top__cosThetaCS", 40, -1, 1);

  book_TH1F("deltaR__gen_lep__gen_neu"   , 60, 0., 6.);
  book_TH1F("deltaPhi__gen_lep__gen_neu" , 60, 0., 3.15);
  book_TH1F("deltaR__gen_blep__gen_neu"  , 60, 0., 6.);
  book_TH1F("deltaPhi__gen_blep__gen_neu", 60, 0., 3.15);
  book_TH1F("deltaR__gen_lep__gen_blep"  , 60, 0., 6.);
  book_TH1F("deltaR__gen_lep__gen_thad"  , 60, 0., 6.);
  book_TH1F("deltaRsum__gen_thad_jets"   , 60, 0., 6.);

  book_TH1F("deltaR__rec_lep__rec_neu"   , 60, 0., 6.);
  book_TH1F("deltaPhi__rec_lep__rec_neu" , 60, 0., 3.15);
  book_TH1F("deltaR__rec_blep__rec_neu"  , 60, 0., 6.);
  book_TH1F("deltaPhi__rec_blep__rec_neu", 60, 0., 3.15);
  book_TH1F("deltaR__rec_lep__rec_blep"  , 60, 0., 6.);
  book_TH1F("deltaR__rec_lep__rec_thad"  , 60, 0., 6.);
  book_TH1F("deltaRsum__rec_thad_jets"   , 60, 0., 6.);

  return;
}

void nak::HFolderTTbarLJRecoHyp::Fill(const nak::TTbarLJRecoHyp& hyp, const nak::TTbarGen& ttgen, const float hyp_val, const float w){

  float gen_ttbar_M(-1.), gen_ttbar_pt(-1.);
  if(ttgen.is_valid()){

    gen_ttbar_M  = ttgen.ttbar().M();
    gen_ttbar_pt = ttgen.ttbar().Pt();
    H1("gen_ttbar__M") ->Fill(gen_ttbar_M);
    H1("gen_ttbar__pt")->Fill(gen_ttbar_pt);
  }

  bool ttljets(ttgen.is_emujets());

  float gen_thad_M(-1.), gen_thad_pt(-1.);
  float gen_tlep_M(-1.), gen_tlep_pt(-1.), gen_tlep_px(-1.), gen_tlep_py(-1.), gen_tlep_pz(-1.);
  float gen_Wlep_M(-1.), gen_Wlep_pt(-1.), gen_Wlep_px(-1.), gen_Wlep_py(-1.), gen_Wlep_pz(-1.), gen_Wlep_Mt(-1.);
  float gen_lep_pt(-1.), gen_lep_eta(-1.), gen_lep_phi(-1.), gen_lep_cosThetaX(-10.);
  float gen_neu_pt(-1.), gen_neu_phi(-1.), gen_neu_px(-1.), gen_neu_py(-1.), gen_neu_pz(-1.), gen_neu_cosThetaX(-10.);
  float gen_blep_pt(-1.), gen_blep_eta(-1.), gen_blep_phi(-1.), gen_blep_px(-1.), gen_blep_py(-1.), gen_blep_pz(-1.), gen_blep_cosThetaX(-10.);
  if(ttljets){
    gen_thad_M  = ttgen.t_had()->p4().M();
    gen_thad_pt = ttgen.t_had()->p4().Pt();

    gen_tlep_M  = ttgen.t_lep()->p4().M();
    gen_tlep_pt = ttgen.t_lep()->p4().Pt();
    gen_tlep_px = ttgen.t_lep()->p4().Px();
    gen_tlep_py = ttgen.t_lep()->p4().Py();
    gen_tlep_pz = ttgen.t_lep()->p4().Pz();

    gen_Wlep_M  = ttgen.W_lep()->p4().M();
    gen_Wlep_Mt = sqrt(2*ttgen.lepton()->p4().Pt()*ttgen.neutrino()->p4().Pt()*(1.-cos(ttgen.lepton()->p4().DeltaPhi(ttgen.neutrino()->p4()))));
    gen_Wlep_pt = ttgen.W_lep()->p4().Pt();
    gen_Wlep_px = ttgen.W_lep()->p4().Px();
    gen_Wlep_py = ttgen.W_lep()->p4().Py();
    gen_Wlep_pz = ttgen.W_lep()->p4().Pz();

    gen_lep_pt        = ttgen.lepton()->p4().Pt();
    gen_lep_eta       = ttgen.lepton()->p4().Eta();
    gen_lep_phi       = ttgen.lepton()->p4().Phi();
    gen_lep_cosThetaX = util::cosThetaX(ttgen.lepton()->p4(), ttgen.t_lep()->p4(), ttgen.ttbar());

    gen_neu_pt        = ttgen.neutrino()->p4().Pt();
    gen_neu_phi       = ttgen.neutrino()->p4().Phi();
    gen_neu_px        = ttgen.neutrino()->p4().Px();
    gen_neu_py        = ttgen.neutrino()->p4().Py();
    gen_neu_pz        = ttgen.neutrino()->p4().Pz();
    gen_neu_cosThetaX = util::cosThetaX(ttgen.neutrino()->p4(), ttgen.t_lep()->p4(), ttgen.ttbar());

    gen_blep_pt        = ttgen.b_lep()->p4().Pt();
    gen_blep_eta       = ttgen.b_lep()->p4().Eta();
    gen_blep_phi       = ttgen.b_lep()->p4().Phi();
    gen_blep_px        = ttgen.b_lep()->p4().Px();
    gen_blep_py        = ttgen.b_lep()->p4().Py();
    gen_blep_pz        = ttgen.b_lep()->p4().Pz();
    gen_blep_cosThetaX = util::cosThetaX(ttgen.b_lep()->p4(), ttgen.t_lep()->p4(), ttgen.ttbar());
    ///

    H1("gen_thad__M") ->Fill(gen_thad_M, w);
    H1("gen_thad__pt")->Fill(gen_thad_pt, w);

    H1("gen_tlep__M") ->Fill(gen_tlep_M, w);
    H1("gen_tlep__pt")->Fill(gen_tlep_pt, w);
    H1("gen_tlep__px")->Fill(gen_tlep_px, w);
    H1("gen_tlep__py")->Fill(gen_tlep_py, w);
    H1("gen_tlep__pz")->Fill(gen_tlep_pz, w);

    H1("gen_tops__Dpt")->Fill(gen_tlep_pt-gen_thad_pt, w);
    H1("gen_tops__DR") ->Fill(ttgen.t_lep()->p4().DeltaR(ttgen.t_had()->p4()), w);

    H1("gen_Wlep__M") ->Fill(gen_Wlep_M , w);
    H1("gen_Wlep__Mt")->Fill(gen_Wlep_Mt, w);
    H1("gen_Wlep__pt")->Fill(gen_Wlep_pt, w);
    H1("gen_Wlep__px")->Fill(gen_Wlep_px, w);
    H1("gen_Wlep__py")->Fill(gen_Wlep_py, w);
    H1("gen_Wlep__pz")->Fill(gen_Wlep_pz, w);

    H1("gen_lep__pt")       ->Fill(gen_lep_pt       , w);
    H1("gen_lep__eta")      ->Fill(gen_lep_eta      , w);
    H1("gen_lep__phi")      ->Fill(gen_lep_phi      , w);
    H1("gen_lep__cosThetaX")->Fill(gen_lep_cosThetaX, w);

    H1("gen_neu__pt")       ->Fill(gen_neu_pt       , w);
    H1("gen_neu__phi")      ->Fill(gen_neu_phi      , w);
    H1("gen_neu__px")       ->Fill(gen_neu_px       , w);
    H1("gen_neu__py")       ->Fill(gen_neu_py       , w);
    H1("gen_neu__pz")       ->Fill(gen_neu_pz       , w);
    H1("gen_neu__cosThetaX")->Fill(gen_neu_cosThetaX, w);

    H1("gen_blep__pt")       ->Fill(gen_blep_pt       , w);
    H1("gen_blep__eta")      ->Fill(gen_blep_eta      , w);
    H1("gen_blep__phi")      ->Fill(gen_blep_phi      , w);
    H1("gen_blep__px")       ->Fill(gen_blep_px       , w);
    H1("gen_blep__py")       ->Fill(gen_blep_py       , w);
    H1("gen_blep__pz")       ->Fill(gen_blep_pz       , w);
    H1("gen_blep__cosThetaX")->Fill(gen_blep_cosThetaX, w);
  }

  float rec_ttbar_M (hyp.ttbar_p4().M() );
  float rec_ttbar_pt(hyp.ttbar_p4().Pt());

  H1("rec_chi2")->Fill(hyp_val, w);
  H2("rec_chi2__VS__rec_ttbar__M")->Fill(hyp_val, rec_ttbar_M, w);

  H1("rec_ttbar__M") ->Fill(rec_ttbar_M , w);
  H1("rec_ttbar__pt")->Fill(rec_ttbar_pt, w);
  if(ttgen.is_valid()){
    H1("rec_ttbar__gen_DM") ->Fill(rec_ttbar_M -gen_ttbar_M , w);
    H1("rec_ttbar__gen_Dpt")->Fill(rec_ttbar_pt-gen_ttbar_pt, w);
    if(gen_ttbar_M)  H1("rec_ttbar__gen_DM_pct") ->Fill((rec_ttbar_M -gen_ttbar_M) /fabs(gen_ttbar_M) , w);
    if(gen_ttbar_pt) H1("rec_ttbar__gen_Dpt_pct")->Fill((rec_ttbar_pt-gen_ttbar_pt)/fabs(gen_ttbar_pt), w);
  }

  float rec_thad_M (hyp.tophad_p4().M());
  float rec_thad_pt(hyp.tophad_p4().Pt());
  H1("rec_thad__M") ->Fill(rec_thad_M , w);
  H1("rec_thad__pt")->Fill(rec_thad_pt, w);
  H1("rec_thad__jetN")->Fill(hyp.tophad_jet_ptrs().size(), w);
  if(ttljets){
    H1("rec_thad__gen_DM")  ->Fill(rec_thad_M -gen_thad_M , w);
    H1("rec_thad__gen_Dpt") ->Fill(rec_thad_pt-gen_thad_pt, w);
    H1("rec_thad__gen_Deta")->Fill(     hyp.tophad_p4().Eta() -  ttgen.t_had()->p4().Eta(), w);
    H1("rec_thad__gen_Dphi")->Fill(fabs(hyp.tophad_p4().DeltaPhi(ttgen.t_had()->p4()))    , w);
    H1("rec_thad__gen_DR")  ->Fill(     hyp.tophad_p4().DeltaR  (ttgen.t_had()->p4())     , w);
    if(gen_thad_M)  H1("rec_thad__gen_DM_pct") ->Fill((rec_thad_M -gen_thad_M) /fabs(gen_thad_M) , w);
    if(gen_thad_pt) H1("rec_thad__gen_Dpt_pct")->Fill((rec_thad_pt-gen_thad_pt)/fabs(gen_thad_pt), w);
  }

  if(hyp.tophad_jet_ptrs().size() == 1){

    const xtt::MergedJet* tjet = dynamic_cast<const xtt::MergedJet*>(hyp.tophad_jet_ptrs().at(0));
    if(tjet){

      float rec_thad_Msd(tjet->Msoftdrop);

      H1("rec_thad__Msd")->Fill(rec_thad_Msd, w);
      if(ttljets){
        H1("rec_thad__gen_DMsd")->Fill(rec_thad_Msd-gen_thad_M, w);
        if(gen_thad_M) H1("rec_thad__gen_DMsd_pct")->Fill((rec_thad_Msd-gen_thad_M)/fabs(gen_thad_M), w);
      }
    }
  }

  float rec_tlep_M (hyp.toplep_p4().M());
  float rec_tlep_pt(hyp.toplep_p4().Pt());
  float rec_tlep_px(hyp.toplep_p4().Px());
  float rec_tlep_py(hyp.toplep_p4().Py());
  float rec_tlep_pz(hyp.toplep_p4().Pz());
  H1("rec_tlep__M") ->Fill(rec_tlep_M, w);
  H1("rec_tlep__pt")->Fill(rec_tlep_pt, w);
  H1("rec_tlep__px")->Fill(rec_tlep_px, w);
  H1("rec_tlep__py")->Fill(rec_tlep_py, w);
  H1("rec_tlep__pz")->Fill(rec_tlep_pz, w);
  H1("rec_tlep__jetN")->Fill(hyp.toplep_jet_ptrs().size(), w);
  if(ttljets){
    H1("rec_tlep__gen_DM") ->Fill(rec_tlep_M -gen_tlep_M, w);
    H1("rec_tlep__gen_Dpt")->Fill(rec_tlep_pt-gen_tlep_pt, w);
    H1("rec_tlep__gen_Dpx")->Fill(rec_tlep_px-gen_tlep_px, w);
    H1("rec_tlep__gen_Dpy")->Fill(rec_tlep_py-gen_tlep_py, w);
    H1("rec_tlep__gen_Dpz")->Fill(rec_tlep_pz-gen_tlep_pz, w);
    H1("rec_tlep__gen_Deta")->Fill(     hyp.toplep_p4().Eta() -  ttgen.t_lep()->p4().Eta(), w);
    H1("rec_tlep__gen_Dphi")->Fill(fabs(hyp.toplep_p4().DeltaPhi(ttgen.t_lep()->p4()))    , w);
    H1("rec_tlep__gen_DR")  ->Fill(     hyp.toplep_p4().DeltaR  (ttgen.t_lep()->p4())     , w);
    if(gen_tlep_M)  H1("rec_tlep__gen_DM_pct") ->Fill((rec_tlep_M -gen_tlep_M) /fabs(gen_tlep_M) , w);
    if(gen_tlep_pt) H1("rec_tlep__gen_Dpt_pct")->Fill((rec_tlep_pt-gen_tlep_pt)/fabs(gen_tlep_pt), w);
    if(gen_tlep_px) H1("rec_tlep__gen_Dpx_pct")->Fill((rec_tlep_px-gen_tlep_px)/fabs(gen_tlep_px), w);
    if(gen_tlep_py) H1("rec_tlep__gen_Dpy_pct")->Fill((rec_tlep_py-gen_tlep_py)/fabs(gen_tlep_py), w);
    if(gen_tlep_pz) H1("rec_tlep__gen_Dpz_pct")->Fill((rec_tlep_pz-gen_tlep_pz)/fabs(gen_tlep_pz), w);
  }

  H1("rec_tops__Dpt")->Fill(rec_tlep_pt-rec_thad_pt, w);
  H1("rec_tops__DR") ->Fill(hyp.toplep_p4().DeltaR(hyp.tophad_p4()), w);

  float rec_Wlep_M (hyp.Wlep_p4().M());
  float rec_Wlep_Mt(sqrt(2*hyp.lepton_p4().Pt()*hyp.neutrino_p4().Pt()*(1.-cos(hyp.lepton_p4().DeltaPhi(hyp.neutrino_p4())))));
  float rec_Wlep_pt(hyp.Wlep_p4().Pt());
  float rec_Wlep_px(hyp.Wlep_p4().Px());
  float rec_Wlep_py(hyp.Wlep_p4().Py());
  float rec_Wlep_pz(hyp.Wlep_p4().Pz());
  H1("rec_Wlep__M") ->Fill(rec_Wlep_M , w);
  H1("rec_Wlep__Mt")->Fill(rec_Wlep_Mt, w);
  H1("rec_Wlep__pt")->Fill(rec_Wlep_pt, w);
  H1("rec_Wlep__px")->Fill(rec_Wlep_px, w);
  H1("rec_Wlep__py")->Fill(rec_Wlep_py, w);
  H1("rec_Wlep__pz")->Fill(rec_Wlep_pz, w);
  if(ttljets){
    H1("rec_Wlep__gen_DM") ->Fill(rec_Wlep_M -gen_Wlep_M , w);
    H1("rec_Wlep__gen_DMt")->Fill(rec_Wlep_Mt-gen_Wlep_Mt, w);
    H1("rec_Wlep__gen_Dpt")->Fill(rec_Wlep_pt-gen_Wlep_pt, w);
    H1("rec_Wlep__gen_Dpx")->Fill(rec_Wlep_px-gen_Wlep_px, w);
    H1("rec_Wlep__gen_Dpy")->Fill(rec_Wlep_py-gen_Wlep_py, w);
    H1("rec_Wlep__gen_Dpz")->Fill(rec_Wlep_pz-gen_Wlep_pz, w);
    if(gen_Wlep_M)  H1("rec_Wlep__gen_DM_pct") ->Fill((rec_Wlep_M -gen_Wlep_M) /fabs(gen_Wlep_M) , w);
    if(gen_Wlep_Mt) H1("rec_Wlep__gen_DMt_pct")->Fill((rec_Wlep_Mt-gen_Wlep_Mt)/fabs(gen_Wlep_Mt), w);
    if(gen_Wlep_pt) H1("rec_Wlep__gen_Dpt_pct")->Fill((rec_Wlep_pt-gen_Wlep_pt)/fabs(gen_Wlep_pt), w);
    if(gen_Wlep_px) H1("rec_Wlep__gen_Dpx_pct")->Fill((rec_Wlep_px-gen_Wlep_px)/fabs(gen_Wlep_px), w);
    if(gen_Wlep_py) H1("rec_Wlep__gen_Dpy_pct")->Fill((rec_Wlep_py-gen_Wlep_py)/fabs(gen_Wlep_py), w);
    if(gen_Wlep_pz) H1("rec_Wlep__gen_Dpz_pct")->Fill((rec_Wlep_pz-gen_Wlep_pz)/fabs(gen_Wlep_pz), w);
  }

  // lepton
  const TLorentzVector& rec_lep = hyp.lepton_p4();

  float rec_lep_pt (hyp.lepton()->p4().Pt());
  float rec_lep_eta(hyp.lepton()->p4().Eta());
  float rec_lep_phi(hyp.lepton()->p4().Phi());
  float rec_lep_cosThetaX(util::cosThetaX(rec_lep, hyp.toplep_p4(), hyp.ttbar_p4()));
  H1("rec_lep__pt")       ->Fill(rec_lep_pt       , w);
  H1("rec_lep__eta")      ->Fill(rec_lep_eta      , w);
  H1("rec_lep__phi")      ->Fill(rec_lep_phi      , w);
  H1("rec_lep__cosThetaX")->Fill(rec_lep_cosThetaX, w);
  if(ttljets){
    H1("rec_lep__gen_DR")        ->Fill(hyp.lepton()->p4().DeltaR(ttgen.lepton()->p4()), w);
    H1("rec_lep__gen_Dpt")       ->Fill(rec_lep_pt -gen_lep_pt, w);
    H1("rec_lep__gen_Deta")      ->Fill(rec_lep_eta-gen_lep_eta, w);
    H1("rec_lep__gen_Dphi")      ->Fill(fabs(hyp.lepton()->p4().DeltaPhi(ttgen.lepton()->p4())), w);
    H1("rec_lep__gen_DcosThetaX")->Fill(rec_lep_cosThetaX-gen_lep_cosThetaX, w);
    if(gen_lep_pt)  H1("rec_lep__gen_Dpt_pct") ->Fill((rec_lep_pt -gen_lep_pt) /fabs(gen_lep_pt), w);
    if(gen_lep_eta) H1("rec_lep__gen_Deta_pct")->Fill((rec_lep_eta-gen_lep_eta)/fabs(gen_lep_eta), w);
  }

  // neutrino
  const TLorentzVector& rec_neu = hyp.neutrino_p4();

  float rec_neu_pt (rec_neu.Pt());
  float rec_neu_phi(rec_neu.Phi());
  float rec_neu_px (rec_neu.Px());
  float rec_neu_py (rec_neu.Py());
  float rec_neu_pz (rec_neu.Pz());
  float rec_neu_cosThetaX(util::cosThetaX(rec_neu, hyp.toplep_p4(), hyp.ttbar_p4()));
  H1("rec_neu__pt") ->Fill(rec_neu_pt, w);
  H1("rec_neu__phi")->Fill(rec_neu_phi, w);
  H1("rec_neu__px") ->Fill(rec_neu_px, w);
  H1("rec_neu__py") ->Fill(rec_neu_py, w);
  H1("rec_neu__pz") ->Fill(rec_neu_pz, w);
  H1("rec_neu__cosThetaX")->Fill(rec_neu_cosThetaX, w);
  if(ttljets){
    H1("rec_neu__gen_DR")        ->Fill(rec_neu.DeltaR(ttgen.neutrino()->p4()), w);
    H1("rec_neu__gen_Dpt")       ->Fill(rec_neu_pt -gen_neu_pt, w);
    H1("rec_neu__gen_Dphi")      ->Fill(fabs(rec_neu.DeltaPhi(ttgen.neutrino()->p4())), w);
    H1("rec_neu__gen_Dpx")       ->Fill(rec_neu_px -gen_neu_px, w);
    H1("rec_neu__gen_Dpy")       ->Fill(rec_neu_py -gen_neu_py, w);
    H1("rec_neu__gen_Dpz")       ->Fill(rec_neu_pz -gen_neu_pz, w);
    H1("rec_neu__gen_DcosThetaX")->Fill(rec_neu_cosThetaX-gen_neu_cosThetaX, w);
    if(gen_neu_pt) H1("rec_neu__gen_Dpt_pct")->Fill((rec_neu_pt-gen_neu_pt)/fabs(gen_neu_pt), w);
    if(gen_neu_px) H1("rec_neu__gen_Dpx_pct")->Fill((rec_neu_px-gen_neu_px)/fabs(gen_neu_px), w);
    if(gen_neu_py) H1("rec_neu__gen_Dpy_pct")->Fill((rec_neu_py-gen_neu_py)/fabs(gen_neu_py), w);
    if(gen_neu_pz) H1("rec_neu__gen_Dpz_pct")->Fill((rec_neu_pz-gen_neu_pz)/fabs(gen_neu_pz), w);
  }

  // b-lep
  const TLorentzVector& rec_blep = hyp.toplep_p4()-hyp.Wlep_p4();

  float rec_blep_pt (rec_blep.Pt());
  float rec_blep_eta(rec_blep.Eta());
  float rec_blep_phi(rec_blep.Phi());
  float rec_blep_px (rec_blep.Px());
  float rec_blep_py (rec_blep.Py());
  float rec_blep_pz (rec_blep.Pz());
  float rec_blep_cosThetaX(util::cosThetaX(rec_blep, hyp.toplep_p4(), hyp.ttbar_p4()));
  H1("rec_blep__pt") ->Fill(rec_blep_pt, w);
  H1("rec_blep__eta")->Fill(rec_blep_eta, w);
  H1("rec_blep__phi")->Fill(rec_blep_phi, w);
  H1("rec_blep__px") ->Fill(rec_blep_px, w);
  H1("rec_blep__py") ->Fill(rec_blep_py, w);
  H1("rec_blep__pz") ->Fill(rec_blep_pz, w);
  H1("rec_blep__cosThetaX")->Fill(rec_blep_cosThetaX, w);
  if(ttljets){
    H1("rec_blep__gen_DR")        ->Fill(rec_blep.DeltaR(ttgen.b_lep()->p4()), w);
    H1("rec_blep__gen_Dpt")       ->Fill(rec_blep_pt -gen_blep_pt, w);
    H1("rec_blep__gen_Deta")      ->Fill(rec_blep_eta-gen_blep_eta, w);
    H1("rec_blep__gen_Dphi")      ->Fill(fabs(rec_blep.DeltaPhi(ttgen.b_lep()->p4())), w);
    H1("rec_blep__gen_Dpx")       ->Fill(rec_blep_px -gen_blep_px, w);
    H1("rec_blep__gen_Dpy")       ->Fill(rec_blep_py -gen_blep_py, w);
    H1("rec_blep__gen_Dpz")       ->Fill(rec_blep_pz -gen_blep_pz, w);
    H1("rec_blep__gen_DcosThetaX")->Fill(rec_blep_cosThetaX-gen_blep_cosThetaX, w);
    if(gen_blep_pt)  H1("rec_blep__gen_Dpt_pct") ->Fill((rec_blep_pt -gen_blep_pt) /fabs(gen_blep_pt), w);
    if(gen_blep_eta) H1("rec_blep__gen_Deta_pct")->Fill((rec_blep_eta-gen_blep_eta)/fabs(gen_blep_eta), w);
    if(gen_blep_px)  H1("rec_blep__gen_Dpx_pct") ->Fill((rec_blep_px -gen_blep_px) /fabs(gen_blep_px), w);
    if(gen_blep_py)  H1("rec_blep__gen_Dpy_pct") ->Fill((rec_blep_py -gen_blep_py) /fabs(gen_blep_py), w);
    if(gen_blep_pz)  H1("rec_blep__gen_Dpz_pct") ->Fill((rec_blep_pz -gen_blep_pz) /fabs(gen_blep_pz), w);
  }

  // xobj -- deltaR
  float rec_top_cosThetaCS(util::cosThetaCS(hyp.top_p4(), hyp.ttbar_p4()));
  H1("rec_top__cosThetaCS")->Fill(rec_top_cosThetaCS, w);

  H1("rec_lep__cosThetaX__X__rec_blep__cosThetaX")->Fill(rec_lep_cosThetaX * rec_blep_cosThetaX, w);
  H1("rec_lep__cosThetaX__X__rec_neu__cosThetaX") ->Fill(rec_lep_cosThetaX * rec_neu_cosThetaX , w);
  H1("rec_neu__cosThetaX__X__rec_blep__cosThetaX")->Fill(rec_neu_cosThetaX * rec_blep_cosThetaX, w);

  if(ttljets){

    H1("deltaR__gen_lep__gen_neu") ->Fill(ttgen.lepton()->p4().DeltaR(ttgen.neutrino()->p4()), w);
    H1("deltaR__gen_lep__gen_blep")->Fill(ttgen.lepton()->p4().DeltaR(ttgen.b_lep()->p4())   , w);
    H1("deltaR__gen_lep__gen_thad")->Fill(ttgen.lepton()->p4().DeltaR(ttgen.t_had()->p4())   , w);
    H1("deltaR__gen_blep__gen_neu")->Fill(ttgen.b_lep() ->p4().DeltaR(ttgen.neutrino()->p4()), w);

    H1("deltaPhi__gen_lep__gen_neu") ->Fill(fabs(ttgen.lepton()->p4().DeltaPhi(ttgen.neutrino()->p4())), w);
    H1("deltaPhi__gen_blep__gen_neu")->Fill(fabs(ttgen.b_lep() ->p4().DeltaPhi(ttgen.neutrino()->p4())), w);
  }

  H1("deltaR__rec_lep__rec_neu") ->Fill(rec_lep .DeltaR(rec_neu)        , w);
  H1("deltaR__rec_lep__rec_blep")->Fill(rec_lep .DeltaR(rec_blep)       , w);
  H1("deltaR__rec_lep__rec_thad")->Fill(rec_lep .DeltaR(hyp.tophad_p4()), w);
  H1("deltaR__rec_blep__rec_neu")->Fill(rec_blep.DeltaR(rec_neu)        , w);

  H1("deltaPhi__rec_lep__rec_neu") ->Fill(fabs(rec_lep .DeltaPhi(rec_neu)), w);
  H1("deltaPhi__rec_blep__rec_neu")->Fill(fabs(rec_blep.DeltaPhi(rec_neu)), w);

  float deltaRsum__rec_thad_jets(0.);
  for  (unsigned int i=0  ; i<hyp.tophad_jet_ptrs().size(); ++i){
    for(unsigned int j=i+1; j<hyp.tophad_jet_ptrs().size(); ++j){

      deltaRsum__rec_thad_jets += hyp.tophad_jet_ptrs().at(i)->p4().DeltaR(hyp.tophad_jet_ptrs().at(j)->p4());
    }
  }
  if(!deltaRsum__rec_thad_jets) deltaRsum__rec_thad_jets = -1.;
  H1("deltaRsum__rec_thad_jets")->Fill(deltaRsum__rec_thad_jets, w);

  return;
}
