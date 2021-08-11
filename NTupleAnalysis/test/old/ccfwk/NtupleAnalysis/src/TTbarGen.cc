#include <inc/TTbarGen.h>
#include <inc/utils.h>

#include <string>

nak::TTbarGen::TTbarGen(){

  clear();
}

nak::TTbarGen::TTbarGen(const std::vector<xtt::GenParticle>& genp) {

  clear();
  init(genp);
}

void nak::TTbarGen::clear(){

  ttbar_decay = null;

  verbose = false;

  p_t = NULL;
  p_b = NULL;
  p_W = NULL;
  p_W_fu = NULL;
  p_W_fd = NULL;

  m_t = NULL;
  m_b = NULL;
  m_W = NULL;
  m_W_fu = NULL;
  m_W_fd = NULL;

  return;
}

void nak::TTbarGen::init(const std::vector<xtt::GenParticle>& genp){

  std::vector<int> index_top;
  for(int i=0; i<int(genp.size()); ++i){

    if(!(21 <= genp.at(i).status && genp.at(i).status <= 29)) continue;
    if(std::abs(genp.at(i).pdgID) == 6) index_top.push_back(i);
  }

  if(verbose && index_top.size() != 2){
    util::WARNING("TTbarGen::init -- unexpected number (!=2) of top quarks in the hardest subprocess (21 <= status <= 29): "+util::int_to_str(int(index_top.size())));
    return;
  }

  for(int i=0; i<int(index_top.size()); ++i){

    const xtt::GenParticle *t(&genp.at(index_top.at(i)));
    const xtt::GenParticle *t_b(0), *t_W(0), *t_W_fu(0), *t_W_fd(0);

    const xtt::GenParticle *decayed_top(0), *tmp_top(0);
    while(!decayed_top){

      if(!tmp_top) tmp_top = t;

      if(tmp_top->nDaughters == 1){

        if(tmp_top->pdgID == genp.at(tmp_top->indexDa1).pdgID){
          tmp_top = &genp.at(tmp_top->indexDa1);
          continue;
        }
        else util::KILL("TTbarGen::init -- particle has unique daughter with different PDG code");
      }
      else if(!tmp_top->nDaughters || tmp_top->nDaughters > 2)
        util::KILL("TTbarGen::init -- top-quark with n="+util::int_to_str(tmp_top->nDaughters)+" daughters");

      int td1_id(genp.at(tmp_top->indexDa1).pdgID), td2_id(genp.at(tmp_top->indexDa2).pdgID);
      if((std::abs(td1_id) != 6 && std::abs(td2_id) != 6)) decayed_top = tmp_top;
      else tmp_top = (std::abs(td1_id) == 6) ? &genp.at(tmp_top->indexDa1) : &genp.at(tmp_top->indexDa2);
    }

    bool t_bW(false);
//    bool leptonic_decay(false);
    int td1_id(genp.at(decayed_top->indexDa1).pdgID), td2_id(genp.at(decayed_top->indexDa2).pdgID);
    if((std::abs(td1_id) == 24 && std::abs(td2_id) ==  5) ||
       (std::abs(td1_id) ==  5 && std::abs(td2_id) == 24) ){ t_bW = true; }

    if(t_bW){

      t_b = std::abs(td1_id) == 5 ? &genp.at(decayed_top->indexDa1) : &genp.at(decayed_top->indexDa2);
      t_W = std::abs(td1_id) == 5 ? &genp.at(decayed_top->indexDa2) : &genp.at(decayed_top->indexDa1);

      if(t->pdgID * t_b->pdgID < 0) util::KILL("TTbarGen::init -- logical error: inconsistent PDG codes for top-quark and b-quark");
      if(t->pdgID * t_W->pdgID < 0) util::KILL("TTbarGen::init -- logical error: inconsistent PDG codes for top-quark and W-boson");

      const xtt::GenParticle *decayed_W(0), *tmp_W(0);
      while(!decayed_W){

        if(!tmp_W) tmp_W = t_W;

        if(tmp_W->nDaughters == 1){
        
          if(tmp_W->pdgID == genp.at(tmp_W->indexDa1).pdgID){
            tmp_W = &genp.at(tmp_W->indexDa1);
            continue;
          }
          else util::KILL("TTbarGen::init -- particle has unique daughter with different PDG code");
        }
        else if(!tmp_W->nDaughters || tmp_W->nDaughters > 2)
          util::KILL("TTbarGen::init -- W-boson with n="+util::int_to_str(tmp_W->nDaughters)+" daughters");

        int wd1_id(genp.at(tmp_W->indexDa1).pdgID), wd2_id(genp.at(tmp_W->indexDa2).pdgID);
        if((std::abs(wd1_id) != 24 && std::abs(wd2_id) != 24)) decayed_W = tmp_W;
        else tmp_W = std::abs(wd1_id) == 24 ? &genp.at(tmp_W->indexDa1) : &genp.at(tmp_W->indexDa2);
      }

      int awd1_id(std::abs(genp.at(decayed_W->indexDa1).pdgID)), awd2_id(std::abs(genp.at(decayed_W->indexDa2).pdgID));
      if(!((awd1_id+awd2_id)%2)) util::KILL("TTbarGen::init -- logical error: inconsistent PDG codes for W-boson decay products");

//      if     ((11 <= awd1_id) && (awd1_id <= 16) && (11 <= awd2_id) && (awd2_id <= 16)) leptonic_decay = true;
//      else if(( 1 <= awd1_id) && (awd1_id <=  5) && ( 1 <= awd2_id) && (awd2_id <=  5)) leptonic_decay = false;
//      else util::KILL("TTbarGen::init -- logical error (PDG codes of W boson daughters: undefined decay mode)");

      t_W_fu = awd1_id%2 ? &genp.at(decayed_W->indexDa2) : &genp.at(decayed_W->indexDa1);
      t_W_fd = awd1_id%2 ? &genp.at(decayed_W->indexDa1) : &genp.at(decayed_W->indexDa2);
    }

    if(t && t_b && t_W && t_W_fu && t_W_fd){

      if(t->pdgID == 6){

        p_t = t;
        p_b = t_b;
        p_W = t_W;
        p_W_fu = t_W_fu;
        p_W_fd = t_W_fd;
      }

      if(t->pdgID == -6){

        m_t = t;
        m_b = t_b;
        m_W = t_W;
        m_W_fu = t_W_fu;
        m_W_fd = t_W_fd;
      }
    }
  }

  if(is_valid()) init_decay_mode();

  if(is_ljets()) init_ljets();

  return;
}

void nak::TTbarGen::init_decay_mode(){

  if(!is_valid()) util::KILL("TTbarGen::init_decay_mode -- uninitialized pointers (is_valid() = 0)");

  int pWfu_aID(std::abs(p_W_fu->pdgID)), mWfu_aID(std::abs(m_W_fu->pdgID));

  if(util::int_le_ge( 1, pWfu_aID, 5) && util::int_le_ge( 1, mWfu_aID, 5)) ttbar_decay = jj;

  else if((pWfu_aID == 12 && util::int_le_ge( 1, mWfu_aID, 5)) ||
          (mWfu_aID == 12 && util::int_le_ge( 1, pWfu_aID, 5)) ){ ttbar_decay = ej; }

  else if((pWfu_aID == 14 && util::int_le_ge( 1, mWfu_aID, 5)) ||
          (mWfu_aID == 14 && util::int_le_ge( 1, pWfu_aID, 5)) ){ ttbar_decay = muj; }

  else if((pWfu_aID == 16 && util::int_le_ge( 1, mWfu_aID, 5)) ||
          (mWfu_aID == 16 && util::int_le_ge( 1, pWfu_aID, 5)) ){ ttbar_decay = tauj; }

  else if((pWfu_aID == 12 && mWfu_aID == 14) ||
          (mWfu_aID == 12 && pWfu_aID == 14) ){ ttbar_decay = emu; }

  else if((pWfu_aID == 12 && mWfu_aID == 16) ||
          (mWfu_aID == 12 && pWfu_aID == 16) ){ ttbar_decay = etau; }

  else if((pWfu_aID == 14 && mWfu_aID == 16) ||
          (mWfu_aID == 14 && pWfu_aID == 16) ){ ttbar_decay = mutau; }

  else if(pWfu_aID == 12 && mWfu_aID == 12) ttbar_decay = ee;

  else if(pWfu_aID == 14 && mWfu_aID == 14) ttbar_decay = mumu;

  else if(pWfu_aID == 16 && mWfu_aID == 16) ttbar_decay = tautau;

  else util::KILL("TTbarGen::init_decay_mode -- undefined decay mode: (p_W_fu->pdgID="+util::int_to_str(pWfu_aID)+"; m_W_fu->pdgID="+util::int_to_str(mWfu_aID)+")");

  return;
}

void nak::TTbarGen::init_ljets(){

  if(!is_valid()) util::KILL("TTbarGen::init_ljets -- uninitialized pointers (is_valid() = 0)");

  if(!is_ljets()) return;

  int pWfu_aID(std::abs(p_W_fu->pdgID)), mWfu_aID(std::abs(m_W_fu->pdgID));
  int pWfd_aID(std::abs(p_W_fd->pdgID)), mWfd_aID(std::abs(m_W_fd->pdgID));

  if(util::int_le_ge(11, pWfu_aID, 16) &&
     util::int_le_ge(11, pWfd_aID, 16) &&
     util::int_le_ge( 1, mWfu_aID,  5) &&
     util::int_le_ge( 1, mWfd_aID,  5) ){

    lep_t    = p_t;
    lep_b    = p_b;
    lep_W    = p_W;
    lep_W_fu = p_W_fu;
    lep_W_fd = p_W_fd;

    had_t    = m_t;
    had_b    = m_b;
    had_W    = m_W;
    had_W_fu = m_W_fu;
    had_W_fd = m_W_fd;
  }
  else if(util::int_le_ge( 1, pWfu_aID,  5) &&
          util::int_le_ge( 1, pWfd_aID,  5) &&
          util::int_le_ge(11, mWfu_aID, 16) &&
          util::int_le_ge(11, mWfd_aID, 16) ){

    lep_t    = m_t;
    lep_b    = m_b;
    lep_W    = m_W;
    lep_W_fu = m_W_fu;
    lep_W_fd = m_W_fd;

    had_t    = p_t;
    had_b    = p_b;
    had_W    = p_W;
    had_W_fu = p_W_fu;
    had_W_fd = p_W_fd;
  }
  else util::KILL("TTbarGen::init_ljets -- logical error (input inconsistent with a semileptonic decay)");

  return;
}

void nak::TTbarGen::printout() const {

  if(!is_valid()){

    util::WARNING("TTbarGen::printout() -- ttbar decay not found (is_valid == 0)");
    return;
  }

  std::cout << "\n@@@ TTbarGen ---";

  std::cout << " decay_mode=" << decay_mode();
  std::cout << " is_ljets="   << int(is_ljets());
  std::cout << " is_emujets=" << int(is_emujets());

  std::cout << std::endl;

//  printout_genp("  t_lep:    ", t_lep() );
//  printout_genp("  b_lep:    ", b_lep() );
//  printout_genp("  W_lep:    ", W_lep() );
//  printout_genp("  neutrino: ", neutrino() );
//  printout_genp("  lepton:   ", lepton() );
//  printout_genp("  t_had:    ", t_had() );
//  printout_genp("  b_had:    ", b_had() );
//  printout_genp("  W_had:    ", W_had() );
//  printout_genp("  W_had_fu: ", W_had_fu() );
//  printout_genp("  W_had_fd: ", W_had_fd() );

  printout_genp("  p_t:    ", p_t);
  printout_genp("  p_b:    ", p_b);
  printout_genp("  p_W:    ", p_W);
  printout_genp("  p_W_fu: ", p_W_fu);
  printout_genp("  p_W_fd: ", p_W_fd);
  printout_genp("  m_t:    ", m_t);
  printout_genp("  m_b:    ", m_b);
  printout_genp("  m_W:    ", m_W);
  printout_genp("  m_W_fu: ", m_W_fu);
  printout_genp("  m_W_fd: ", m_W_fd);

  return;
}

void nak::TTbarGen::printout_genp(const std::string& log, const xtt::GenParticle* p) const {

  std::cout << log;

  std::cout << "  pdgID=" << p->pdgID;
  std::cout << "  pt="    << p->pt;
  std::cout << "  eta="   << p->eta;
  std::cout << "  phi="   << p->phi;
  std::cout << "  M="     << p->M;

  std::cout << std::endl;

  return;
}
