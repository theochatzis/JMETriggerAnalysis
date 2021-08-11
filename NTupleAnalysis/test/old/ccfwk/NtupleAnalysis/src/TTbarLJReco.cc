#include <inc/TTbarLJReco.h>
#include <inc/utils.h>

#include <NtupleObjects/inc/Jet.h>
#include <NtupleObjects/inc/MergedJet.h>

#include <TLorentzVector.h>
#include <cmath>

const xtt::Particle* nak::TTbarLJReco::get_primary_lepton(const nak::Event& evt) const {

  const xtt::Particle* plep(0);

  double pt_max(-1.);
  for(int i=0; i<int(evt.MUO->size()); ++i){

    if(pt_max< evt.MUO->at(i).pt){
      pt_max = evt.MUO->at(i).pt;
      plep =  &evt.MUO->at(i);
    }
  }
  for(int i=0; i<int(evt.ELE->size()); ++i){

    if(pt_max< evt.ELE->at(i).pt){
      pt_max = evt.ELE->at(i).pt;
      plep =  &evt.ELE->at(i);
    }
  }

  if(!plep) util::KILL("TTbarLJReco::get_primary_lepton -- primary lepton not found");

  return plep;
}

const std::vector<nak::TTbarLJRecoHyp> nak::TTbarLJReco::get_hyps(const nak::Event& evt) const {

  std::vector<TTbarLJRecoHyp> reco_hyps;

  const xtt::Particle* lepton = get_primary_lepton(evt);

  //reconstruct neutrino
  std::vector<TLorentzVector> neutrinos = (*neutrino_reco_)(lepton->p4(), evt.MET->p4());

  const std::vector<xtt::Jet>& jets = *((std::vector<xtt::Jet>*) evt.get(jet_key_));

  const unsigned int jet_combs = pow(3, jets.size());

  for(unsigned int n=0; n<neutrinos.size(); ++n){
    const TLorentzVector& neutrino_p4 = neutrinos.at(n);

    for(unsigned int N=1; N<jet_combs; ++N){

      TTbarLJRecoHyp hyp;
      hyp.set_lepton(lepton);
      hyp.set_neutrino_p4(neutrino_p4);

      for(unsigned int j=0; j<jets.size(); ++j){

        // index for jet assignment to top leg (0=none, 1=leptonic-top, 2=hadronic-top)
        int jet_topidx = int(N/(pow(3,j))) % 3;

        const xtt::Jet* jet = &jets.at(j);

        if     (jet_topidx == 1) hyp.add_toplep_jet_ptr(jet);
        else if(jet_topidx == 2) hyp.add_tophad_jet_ptr(jet);
      }

//        // b-jet of leptonic top (pt-leading)
//        int blep_idx(-1);
//        float maxpt(-1.);
//        for(unsigned int i=0; i<hyp.toplep_jet_ptrs().size(); ++i){
//          if(maxpt< hyp.toplep_jet_ptrs().at(i).pt()){
//            maxpt = hyp.toplep_jet_ptrs().at(i).pt();
//            blep_idx = i;
//          }
//        }
//        if(blep_idx != -1) hyp.set_blep_v4(hyp.toplep_jet_ptrs().at(blep_idx).v4());

//!!      if(hyp.tophad_jet_ptrs().size() > 0 &&
//!!         hyp.toplep_jet_ptrs().size() > 0 ) reco_hyps.push_back(hyp);

      if(hyp.tophad_jet_ptrs().size() >  0 &&
         hyp.tophad_jet_ptrs().size() <= 3 &&
         hyp.toplep_jet_ptrs().size() == 1 ){ reco_hyps.push_back(hyp); }
    }
  }

  return reco_hyps;
}
///

const std::vector<nak::TTbarLJRecoHyp> nak::TTbarLJRecoVTAG::get_hyps(const nak::Event& evt) const {

  std::vector<TTbarLJRecoHyp> reco_hyps;

  const xtt::Particle* lepton = get_primary_lepton(evt);
  std::vector<TLorentzVector> neutrinos = (*neutrino_reco_)(lepton->p4(), evt.MET->p4());

  const std::vector<xtt::MergedJet>& VJETS = *((std::vector<xtt::MergedJet>*) evt.get(vjet_key_));
  const std::vector<xtt::Jet>& JETS = *((std::vector<xtt::Jet>*) evt.get(jet_key_));

  for(unsigned int vj=0; vj<VJETS.size(); ++vj){
    const xtt::MergedJet* vjet = &VJETS.at(vj);

    if(!(*vtagID_)(*vjet)) continue;

    // jet candidates for leptonic-top (not overlapping with v-tagged jet)
    std::vector<const xtt::Jet*> jets;
    jets.reserve(JETS.size());
    for(unsigned int j=0; j<JETS.size(); ++j){

      const xtt::Jet* jet = &JETS.at(j);
      if(vjet->p4().DeltaR(jet->p4()) > minDR_vjet_jet_) jets.push_back(jet);
    }

    const unsigned int jet_combs = pow(3, jets.size());

    for(int n=0; n<int(neutrinos.size()); ++n){
      const TLorentzVector& neutrino_p4 = neutrinos.at(n);

      for(unsigned int N=1; N<jet_combs; ++N){

        TTbarLJRecoHyp hyp;
        hyp.set_lepton(lepton);
        hyp.set_neutrino_p4(neutrino_p4);

        hyp.add_tophad_jet_ptr(vjet);

        for(int j=0; j<int(jets.size()); ++j){
          const xtt::Jet* jet = jets.at(j);

          // index for jet assignment to top leg (0=none, 1=leptonic-top, 2=hadronic-top)
          int jet_topidx = int(N/(pow(3,j))) % 3;

          if(jet_topidx == 1) hyp.add_toplep_jet_ptr(jet);
          if(jet_topidx == 2) hyp.add_tophad_jet_ptr(jet);
        }

//        // b-jet of leptonic top (pt-leading)
//        int blep_idx(-1);
//        float maxpt(-1.);
//        for(unsigned int i=0; i<hyp.toplep_jet_ptrs().size(); ++i){
//          if(maxpt< hyp.toplep_jet_ptrs().at(i).pt()){
//            maxpt = hyp.toplep_jet_ptrs().at(i).pt();
//            blep_idx = i;
//          }
//        }
//        if(blep_idx != -1) hyp.set_blep_v4(hyp.toplep_jet_ptrs().at(blep_idx).v4());

//!!        if(hyp.tophad_jet_ptrs().size() > 0 &&
//!!           hyp.toplep_jet_ptrs().size() > 0 ) reco_hyps.push_back(hyp);

        if(hyp.tophad_jet_ptrs().size() == 2 &&
           hyp.toplep_jet_ptrs().size() == 1 ){ reco_hyps.push_back(hyp); }
      }
    }
  }

  return reco_hyps;
}
///

const std::vector<nak::TTbarLJRecoHyp> nak::TTbarLJRecoTTAG::get_hyps(const nak::Event& evt) const {

  std::vector<TTbarLJRecoHyp> reco_hyps;

  const xtt::Particle* lepton = get_primary_lepton(evt);
  std::vector<TLorentzVector> neutrinos = (*neutrino_reco_)(lepton->p4(), evt.MET->p4());

  const std::vector<xtt::MergedJet>& TOPJETS = *((std::vector<xtt::MergedJet>*) evt.get(topjet_key_));
  const std::vector<xtt::Jet>& JETS = *((std::vector<xtt::Jet>*) evt.get(jet_key_));

  for(unsigned int tj=0; tj<TOPJETS.size(); ++tj){
    const xtt::MergedJet* tjet = &TOPJETS.at(tj);

    if(!(*toptagID_)(*tjet)) continue;

    // jet candidates for leptonic-top (not overlapping with top-tagged jet)
    std::vector<const xtt::Jet*> jets;
    jets.reserve(JETS.size());
    for(unsigned int j=0; j<JETS.size(); ++j){

      const xtt::Jet* jet = &JETS.at(j);
      if(tjet->p4().DeltaR(jet->p4()) > minDR_topjet_jet_) jets.push_back(jet);
    }

    const unsigned int jet_combs = pow(2, jets.size());

    for(int n=0; n<int(neutrinos.size()); ++n){
      const TLorentzVector& neutrino_p4 = neutrinos.at(n);

      for(unsigned int N=1; N<jet_combs; ++N){

        TTbarLJRecoHyp hyp;
        hyp.set_lepton(lepton);
        hyp.set_neutrino_p4(neutrino_p4);

        hyp.add_tophad_jet_ptr(tjet);

        for(int j=0; j<int(jets.size()); ++j){
          const xtt::Jet* jet = jets.at(j);

          // index for jet assignment to top leg (0=none, 1=leptonic-top)
          int jet_topidx = int(N/(pow(2,j))) % 2;

          if(jet_topidx == 1) hyp.add_toplep_jet_ptr(jet);
        }

//        // b-jet of leptonic top (pt-leading)
//        int blep_idx(-1);
//        float maxpt(-1.);
//        for(unsigned int i=0; i<hyp.toplep_jet_ptrs().size(); ++i){
//          if(maxpt< hyp.toplep_jet_ptrs().at(i).pt()){
//            maxpt = hyp.toplep_jet_ptrs().at(i).pt();
//            blep_idx = i;
//          }
//        }
//        if(blep_idx != -1) hyp.set_blep_v4(hyp.toplep_jet_ptrs().at(blep_idx).v4());

//!!        if(hyp.tophad_jet_ptrs().size() > 0 &&
//!!           hyp.toplep_jet_ptrs().size() > 0 ) reco_hyps.push_back(hyp);

        if(hyp.tophad_jet_ptrs().size() == 1 &&
           hyp.toplep_jet_ptrs().size() == 1 ){ reco_hyps.push_back(hyp); }
      }
    }
  }

  return reco_hyps;
}
///

const std::vector<nak::TTbarLJRecoHyp> nak::TTbarLJReco_LBJ::get_hyps(const nak::Event& evt) const {

  std::vector<TTbarLJRecoHyp> reco_hyps;

  const xtt::Particle* lepton = get_primary_lepton(evt);

  // neutrino reco
  std::vector<TLorentzVector> neutrinos = (*neutrino_reco_)(lepton->p4(), evt.MET->p4());

  std::vector<xtt::Jet*> jets;
  jets.reserve(evt.JET_AK4->size());
  for(unsigned int j=0; j<evt.JET_AK4->size(); ++j) jets.push_back(&evt.JET_AK4->at(j));

  const unsigned int jet_combs = pow(3, jets.size());

  for(unsigned int n=0; n<neutrinos.size(); ++n){
    const TLorentzVector& neutrino_p4 = neutrinos.at(n);

    for(unsigned int N=1; N<jet_combs; ++N){

      TTbarLJRecoHyp hyp;
      hyp.set_lepton(lepton);
      hyp.set_neutrino_p4(neutrino_p4);

      for(int j=0; j<int(jets.size()); ++j){
        const xtt::Jet* jet = jets.at(j);

        // index for jet assignment to top leg (0=none, 1=leptonic-top, 2=hadronic-top)
        int jet_topidx = int(N/(pow(3,j))) % 3;

        if     (jet_topidx == 1) hyp.add_toplep_jet_ptr(jet);
        else if(jet_topidx == 2) hyp.add_tophad_jet_ptr(jet);
      }

      bool btag_cond(false); {

        float min_CSVIVF(.5);

        int btagN(0);
        for(unsigned int j1=0; j1<jets.size(); ++j1)
          if(jets.at(j1)->btagCSVIVF > min_CSVIVF) ++btagN;

        if(!btagN) btag_cond = true;
        else {

          for(int j2=0; j2<int(hyp.toplep_jet_ptrs().size()); ++j2)
            if(hyp.toplep_jet_ptrs().at(j2)->btagCSVIVF > min_CSVIVF) btag_cond = true;

          for(int j2=0; j2<int(hyp.tophad_jet_ptrs().size()); ++j2)
            if(hyp.tophad_jet_ptrs().at(j2)->btagCSVIVF > min_CSVIVF) btag_cond = true;
        }
      }
      if(!btag_cond) continue;

//        // b-jet of leptonic top (pt-leading)
//        int blep_idx(-1);
//        float maxpt(-1.);
//        for(unsigned int i=0; i<hyp.toplep_jet_ptrs().size(); ++i){
//          if(maxpt< hyp.toplep_jet_ptrs().at(i).pt()){
//            maxpt = hyp.toplep_jet_ptrs().at(i).pt();
//            blep_idx = i;
//          }
//        }
//        if(blep_idx != -1) hyp.set_blep_v4(hyp.toplep_jet_ptrs().at(blep_idx).v4());

      if(hyp.tophad_jet_ptrs().size() >  0 &&
         hyp.tophad_jet_ptrs().size() <= 3 &&
         hyp.toplep_jet_ptrs().size() == 1 ) reco_hyps.push_back(hyp);
    }
  }

  return reco_hyps;
}
///

const std::vector<nak::TTbarLJRecoHyp> nak::TTbarLJRecoTTAG_LBJ::get_hyps(const nak::Event& evt) const {

  std::vector<TTbarLJRecoHyp> reco_hyps;

  const xtt::Particle* lepton = get_primary_lepton(evt);
  std::vector<TLorentzVector> neutrinos = (*neutrino_reco_)(lepton->p4(), evt.MET->p4());

  for(int tj=0; tj<int(evt.JET_AK8->size()); ++tj){
    const xtt::MergedJet* tjet = &evt.JET_AK8->at(tj);

    if(!(*toptagID_)(*tjet)) continue;

    // jet candidates for leptonic-top (not overlapping with top-tagged jet)
    std::vector<xtt::Jet*> jets;
    jets.reserve(evt.JET_AK4->size());
    for(int j=0; j<int(evt.JET_AK4->size()); ++j){
      xtt::Jet* jet = &evt.JET_AK4->at(j);
      if(tjet->p4().DeltaR(jet->p4()) > minDR_topjet_jet_) jets.push_back(jet);
    }

    const unsigned int jet_combs = pow(2, jets.size());

    for(int n=0; n<int(neutrinos.size()); ++n){
      const TLorentzVector& neutrino_p4 = neutrinos.at(n);

      for(unsigned int N=1; N<jet_combs; ++N){

        TTbarLJRecoHyp hyp;
        hyp.set_lepton(lepton);
        hyp.set_neutrino_p4(neutrino_p4);

        hyp.add_tophad_jet_ptr(tjet);

        for(int j=0; j<int(jets.size()); ++j){
          const xtt::Jet* jet = jets.at(j);

          // index for jet assignment to top leg (0=none, 1=leptonic-top)
          int jet_topidx = int(N/(pow(2,j))) % 2;

          if(jet_topidx == 1) hyp.add_toplep_jet_ptr(jet);
        }

        bool btag_cond(false); {

          float min_CSVIVF(.5);

          int btagN(0);
          for(int j1=0; j1<int(jets.size()); ++j1)
            if(jets.at(j1)->btagCSVIVF > min_CSVIVF) ++btagN;

          if(!btagN) btag_cond = true;
          else {

            for(int j2=0; j2<int(hyp.toplep_jet_ptrs().size()); ++j2)
              if(hyp.toplep_jet_ptrs().at(j2)->btagCSVIVF > min_CSVIVF) btag_cond = true;

            for(int j2=0; j2<int(hyp.tophad_jet_ptrs().size()); ++j2)
              if(hyp.tophad_jet_ptrs().at(j2)->btagCSVIVF > min_CSVIVF) btag_cond = true;
          }
        }
        if(!btag_cond) continue;

//        // b-jet of leptonic top (pt-leading)
//        int blep_idx(-1);
//        float maxpt(-1.);
//        for(unsigned int i=0; i<hyp.toplep_jet_ptrs().size(); ++i){
//          if(maxpt< hyp.toplep_jet_ptrs().at(i).pt()){
//            maxpt = hyp.toplep_jet_ptrs().at(i).pt();
//            blep_idx = i;
//          }
//        }
//        if(blep_idx != -1) hyp.set_blep_v4(hyp.toplep_jet_ptrs().at(blep_idx).v4());

      if(hyp.tophad_jet_ptrs().size() == 1 &&
         hyp.toplep_jet_ptrs().size() == 1 ) reco_hyps.push_back(hyp);
      }
    }
  }

  return reco_hyps;
}
///
