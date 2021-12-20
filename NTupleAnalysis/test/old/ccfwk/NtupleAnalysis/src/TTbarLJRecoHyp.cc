#include <inc/TTbarLJRecoHyp.h>
#include <inc/utils.h>

#include <iostream>

nak::TTbarLJRecoHyp::TTbarLJRecoHyp(){

  lepton_ = 0;
  neutrino_p4_ = TLorentzVector(0., 0., 0., 0.);

  toplep_jet_ptrs_.clear();
  tophad_jet_ptrs_.clear();

  discriminator_map_.clear();
}

TLorentzVector nak::TTbarLJRecoHyp::tophad_p4() const {

  TLorentzVector thad(0., 0., 0., 0.);

  for(int i=0; i<int(tophad_jet_ptrs_.size()); ++i){

    if(!tophad_jet_ptrs_.at(i)) util::KILL("TTbarLJRecoHyp::tophad_p4 -- null pointer to associated jet");
    else thad += tophad_jet_ptrs_.at(i)->p4();
  }

  if(!thad.E()) util::KILL("TTbarLJRecoHyp::tophad_p4 -- null 4-momentum");

  return thad;
}

//TLorentzVector nak::TTbarLJRecoHyp::Whad_p4() const {
//
//  TLorentzVector Whad(0., 0., 0., 0.);
//
//  if(tophad_jet_ptrs_.size() == 1){
//
//    const xtt::MergedJet* tjet = static_cast<const xtt::MergedJet*>(tophad_jet_ptrs_.at(0));
//    if(tjet){
//      float mmin(-1.);
//
//      for(int a=0; a<int(tjet->subjets.size()); ++a){
//        for(int b=a+1; b<int(tjet->subjets.size()); ++b){
//
//          TLorentzVector w_had_p4 = tjet->subjets.at(a).p4() + tjet->subjets.at(b).p4();
//          if(w_had_p4.M() < mmin || !(a*(b-1))){ mmin = w_had_p4.M(); Whad = w_had_p4; }
//        }
//      }
//
//      if(!Whad.E()) util::KILL("TTbarLJRecoHyp::Whad_p4 -- null 4-momentum");
//
//      return Whad;
//    }
//  }
//
//  float mmin(-1.);
//  for(int i=0; i<int(tophad_jet_ptrs_.size()); ++i){
//
//    if(!tophad_jet_ptrs_.at(i)) util::KILL("TTbarLJRecoHyp::Whad_p4 -- null pointer to associated jet");
//
//    for(int j=i+1; j<int(tophad_jet_ptrs_.size()); ++j){
//      if(!tophad_jet_ptrs_.at(j)) util::KILL("TTbarLJRecoHyp::Whad_p4 -- null pointer to associated jet");
//
//      TLorentzVector w_had_p4 = tophad_jet_ptrs_.at(i)->p4() + tophad_jet_ptrs_.at(j)->p4();
//      if(w_had_p4.M() < mmin || !(i*(j-1))){ mmin = w_had_p4.M(); Whad = w_had_p4; }
//    }
//  }
//
//  if(!Whad.E()) util::KILL("TTbarLJRecoHyp::Whad_p4 -- null 4-momentum");
//
//  return Whad;
//}

TLorentzVector nak::TTbarLJRecoHyp::toplep_p4() const {

  TLorentzVector tlep = Wlep_p4();

  for(unsigned int i=0; i<toplep_jet_ptrs_.size(); ++i){

    if(!toplep_jet_ptrs_.at(i)) util::KILL("TTbarLJRecoHyp::toplep_p4 -- null pointer to associated jet");
    else tlep += toplep_jet_ptrs_.at(i)->p4();
  }

  if(!tlep.E()) util::KILL("TTbarLJRecoHyp::toplep_p4 -- null 4-momentum");

  return tlep;
}

const xtt::Particle* nak::TTbarLJRecoHyp::lepton() const {

  if(!lepton_) util::KILL("TTbarLJRecoHyp::lepton -- null pointer to lepton");

  return lepton_;
}

TLorentzVector nak::TTbarLJRecoHyp::neutrino_p4() const {

  if(!neutrino_p4_.E()) util::KILL("TTbarLJRecoHyp::neutrino_p4 -- null 4-momentum");

  return neutrino_p4_;
}

float nak::TTbarLJRecoHyp::discriminator(const std::string& key_) const {

  float val(-1.);

  if(discriminator_map_.find(key_) != discriminator_map_.end()) val = discriminator_map_.find(key_)->second;
  else util::KILL("TTbarLJRecoHyp::discriminator -- hypothesis discriminator not found: "+key_);

  return val;
}

void nak::TTbarLJRecoHyp::printout() const {

  if(!lepton()){

    util::WARNING("TTbarLJRecoHyp::printout() -- null pointer to lepton");
    return;
  }

  std::cout << "\n@@@ TTbarLJRecoHyp ---";

  std::cout << std::endl;

  printout_p4("  t_lep:      ", toplep_p4());
  printout_p4("  neutrino:   ", neutrino_p4());
  printout_p4("  lepton:     ", lepton_p4());
  for(unsigned int j=0; j<toplep_jet_ptrs().size(); ++j)
    printout_p4("  t_lep_jet "+util::int_to_str(j)+": ", toplep_jet_ptrs().at(j)->p4());

  printout_p4("  t_had:      ", tophad_p4());
  for(unsigned int j=0; j<tophad_jet_ptrs().size(); ++j)
    printout_p4("  t_had_jet "+util::int_to_str(j)+": ", tophad_jet_ptrs().at(j)->p4());

  for(std::map<std::string, float>::const_iterator it=discriminator_map_.begin(); it != discriminator_map_.end(); ++it)
    std::cout << "  discriminator[\"" << it->first << "\"]=" << it->second << std::endl;

  return;
}

void nak::TTbarLJRecoHyp::printout_p4(const std::string& log, const TLorentzVector& p4) const {

  std::cout << log;

  std::cout << "  pt="    << p4.Pt();
  std::cout << "  eta="   << p4.Eta();
  std::cout << "  phi="   << p4.Phi();
  std::cout << "  M="     << p4.M();

  std::cout << std::endl;

  return;
}
