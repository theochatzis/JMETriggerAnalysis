#include <inc/TTbarLJRecoTools.h>
#include <inc/utils.h>

#include <algorithm>

const nak::TTbarLJRecoHyp* nak::TTbarLJRecoRanker_chi2::best_hyp(const std::vector<nak::TTbarLJRecoHyp>& hyps) const {

  const nak::TTbarLJRecoHyp* p_hyp(0);

  float min_val(util::f_infty());
  for(int i=0; i<int(hyps.size()); ++i){
    const nak::TTbarLJRecoHyp& h = hyps.at(i);

    float v(hyp_value(h));
    if(min_val> v){
      min_val = v;
      p_hyp = &h;
    }
  }

  return p_hyp;
}

float nak::TTbarLJRecoRanker_chi2::hyp_value(const nak::TTbarLJRecoHyp& hyp) const {

  float chi2_tlep = pow((hyp.toplep_p4().M() - tlep_m_val_) / tlep_m_sig_, 2);
  float chi2_thad = pow((hyp.tophad_p4().M() - thad_m_val_) / thad_m_sig_, 2);

  return (chi2_tlep + chi2_thad);
}
////

float nak::TTbarLJRecoRanker_chi2_TTAG::hyp_value(const nak::TTbarLJRecoHyp& hyp) const {

  float chi2_tlep = pow((hyp.toplep_p4().M() - tlep_m_val_) / tlep_m_sig_, 2);

  if(hyp.tophad_jet_ptrs().size() != 1)
    util::KILL("TTbarLJRecoRanker_chi2_TTAG::hyp_value -- invalid number of hadronic-top jets ("+util::int_to_str(int(hyp.tophad_jet_ptrs().size()))+"!=1)");

  const xtt::MergedJet* tjet = dynamic_cast<const xtt::MergedJet*>(hyp.tophad_jet_ptrs().at(0));
  if(!tjet) util::KILL("TTbarLJRecoRanker_chi2_TTAG::hyp_value -- failed dynamic_cast of hadronic-top jet to MergedJet*");

  float chi2_thad = pow((tjet->Msoftdrop - thad_m_val_) / thad_m_sig_, 2);

  return (chi2_tlep + chi2_thad);
}
////

const nak::TTbarLJRecoHyp* nak::TTbarLJRecoRanker_genMatchDR::best_hyp(const std::vector<nak::TTbarLJRecoHyp>& hyps, const nak::TTbarGen& ttgen, int flag_ttagevt) const {

  const nak::TTbarLJRecoHyp* p_hyp(0);

  float min_val(util::f_infty());
  for(int i=0; i<int(hyps.size()); ++i){
    const nak::TTbarLJRecoHyp& h = hyps.at(i);

    float v(hyp_value(h, ttgen, flag_ttagevt));
    if(v == util::f_infty()) continue;

    if(min_val> v){
      min_val = v;
      p_hyp = &h;
    }
  }

  return p_hyp;
}

float nak::TTbarLJRecoRanker_genMatchDR::hyp_value(const nak::TTbarLJRecoHyp& hyp, const nak::TTbarGen& ttgen, int flag_toptagevent) const {

  if(!ttgen.is_emujets()) return util::f_infty();

  float dR_sum(0.);

  // lepton
  float dR_lep(ttgen.lepton()->p4().DeltaR(hyp.lepton()->p4()));
  if(dR_lep < minDR_lepton_) dR_sum += dR_lep;
  else return util::f_infty();

  // neutrino
  float dphi_neu(ttgen.neutrino()->p4().DeltaPhi(hyp.neutrino_p4()));
  float dR_neu(ttgen.neutrino()->p4().DeltaR(hyp.neutrino_p4()));
  if(fabs(dphi_neu) < minDphi_neutrino_) dR_sum += dR_neu;
  else return util::f_infty();

  // jets - leptonic-top
  if(hyp.toplep_jet_ptrs().size() != 1) return util::f_infty();

  float dR_jet_tlep(ttgen.b_lep()->p4().DeltaR(hyp.toplep_jet_ptrs().at(0)->p4()));
  if(dR_jet_tlep < minDR_jet_) dR_sum += dR_jet_tlep;
  else return util::f_infty();

  // jets - hadronic-top
  if(flag_toptagevent){

    if(hyp.tophad_jet_ptrs().size() != 1) return util::f_infty();

    float dR_tjet_thad(ttgen.t_had()->p4().DeltaR(hyp.tophad_jet_ptrs().at(0)->p4()));
    if(dR_tjet_thad < minDR_topjet_) dR_sum += dR_tjet_thad;
    else return util::f_infty();

    float dR_jet1_thad(ttgen.b_had()->p4().DeltaR(hyp.tophad_jet_ptrs().at(0)->p4()));
    if(dR_jet1_thad < minDR_topjet_) dR_sum += dR_jet1_thad;
    else return util::f_infty();

    float dR_jet2_thad(ttgen.W_had_fu()->p4().DeltaR(hyp.tophad_jet_ptrs().at(0)->p4()));
    if(dR_jet2_thad < minDR_topjet_) dR_sum += dR_jet2_thad;
    else return util::f_infty();

    float dR_jet3_thad(ttgen.W_had_fd()->p4().DeltaR(hyp.tophad_jet_ptrs().at(0)->p4()));
    if(dR_jet3_thad < minDR_topjet_) dR_sum += dR_jet3_thad;
    else return util::f_infty();
  }
  else {

    if(hyp.tophad_jet_ptrs().size() > 3) return util::f_infty();

    float dR_jet1_thad(dRmin(*ttgen.b_had(), to_vector_of_objs(hyp.tophad_jet_ptrs())));
    if(dR_jet1_thad < minDR_jet_) dR_sum += dR_jet1_thad;
    else return util::f_infty();

    float dR_jet2_thad(dRmin(*ttgen.W_had_fu(), to_vector_of_objs(hyp.tophad_jet_ptrs())));
    if(dR_jet2_thad < minDR_jet_) dR_sum += dR_jet2_thad;
    else return util::f_infty();

    float dR_jet3_thad(dRmin(*ttgen.W_had_fd(), to_vector_of_objs(hyp.tophad_jet_ptrs())));
    if(dR_jet3_thad < minDR_jet_) dR_sum += dR_jet3_thad;
    else return util::f_infty();

    // require each tophad_jet to have a match to GEN parton
    for(int j=0; j<int(hyp.tophad_jet_ptrs().size()); ++j){
      if     (hyp.tophad_jet_ptrs().at(j)->p4().DeltaR(ttgen.b_had()->p4())    < minDR_jet_) continue;
      else if(hyp.tophad_jet_ptrs().at(j)->p4().DeltaR(ttgen.W_had_fu()->p4()) < minDR_jet_) continue;
      else if(hyp.tophad_jet_ptrs().at(j)->p4().DeltaR(ttgen.W_had_fd()->p4()) < minDR_jet_) continue;
      else return util::f_infty();
    }
  }

  return dR_sum;
}
////
