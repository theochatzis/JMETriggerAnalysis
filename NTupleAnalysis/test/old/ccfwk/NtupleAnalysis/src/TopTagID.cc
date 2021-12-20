#include <inc/TopTagID.h>
#include <inc/utils.h>
#include <iostream>

bool nak::VTagger::operator()(const xtt::MergedJet& tjet) const {

  if(!(tjet.Msoftdrop > m_min_)) return false;
  if(!(tjet.Msoftdrop < m_max_)) return false;

  if(!(tjet.Tau1 > 0.)) return false;
  if(!(tjet.Tau2 < tau21_max_ * tjet.Tau1)) return false;

  return true;
}

bool nak::CMSTopTagger::operator()(const xtt::MergedJet& tjet) const {

  if(!(int(tjet.subjets1.size()) >= nsubj_min_)) return false;

  if(!(tjet.Msoftdrop > m_min_)) return false;
  if(!(tjet.Msoftdrop < m_max_)) return false;

  if(!(topjet_mmin(tjet) > mmin_min_)) return false;

  return true;
}

bool nak::CMSTopTagger_tau32::operator()(const xtt::MergedJet& tjet) const {

  if(!(int(tjet.subjets1.size()) >= nsubj_min_)) return false;

  if(!(tjet.Msoftdrop > m_min_)) return false;
  if(!(tjet.Msoftdrop < m_max_)) return false;

  if(!(topjet_mmin(tjet) > mmin_min_)) return false;

  if(!(tjet.Tau2 > 0.)) return false;
  if(!(tjet.Tau3 < tau32_max_ * tjet.Tau2)) return false;

  return true;
}

bool nak::HEPTopTagger::operator()(const xtt::MergedJet& tjet) const {

  const float massratio_Wt(80.4 / 172.3);
  const float massfrac_min(1. - .15);
  const float massfrac_max(1. + .15);

  const float m23frac1_min(.35);
  const float m23frac2_min(.35);

  const float atan_m13m12_min(0.2);
  const float atan_m13m12_max(1.3);

  const float mjet_min(140.);
  const float mjet_max(250.);
  //

  const float mjet(tjet.Msoftdrop);
  const std::vector<xtt::Jet>& subjets(tjet.subjets1);

  float m12, m13, m23;

  if(subjets.size() == 3){

    std::vector<xtt::Jet> subj = subjets;
    sort_by_pt(subj);

    m12 = (subj.at(0).p4() + subj.at(1).p4()).M();
    m13 = (subj.at(0).p4() + subj.at(2).p4()).M();
    m23 = (subj.at(1).p4() + subj.at(2).p4()).M();
  }
  else return false;

  const float r_min(massfrac_min * massratio_Wt);
  const float r_max(massfrac_max * massratio_Wt);

  //1 condition
  const int cond1 = (atan(m13/m12) > atan_m13m12_min &&
                     atan(m13/m12) < atan_m13m12_max &&
                     r_min < (m23/mjet) && (m23/mjet) < r_max );

  //2 condition
  const float cond2C =  1. - pow(m23/mjet,2);
  const float cond2L = (1. + pow(m13/m12, 2)) * pow(r_min, 2);
  const float cond2R = (1. + pow(m13/m12, 2)) * pow(r_max, 2);

  const bool cond2 = (cond2L < cond2C && cond2C < cond2R && (m23/mjet) > m23frac1_min);

  //3 condition
  const float cond3C =  1. - pow(m23/mjet,2);
  const float cond3L = (1. + pow(m12/m13, 2)) * pow(r_min, 2);
  const float cond3R = (1. + pow(m12/m13, 2)) * pow(r_max, 2);

  const bool cond3 = (cond3L < cond3C && cond3C < cond3R && (m23/mjet) > m23frac2_min);

  const bool mass_jet = (mjet_min < mjet && mjet < mjet_max);

  return mass_jet && (cond1 || cond2 || cond3);
}
