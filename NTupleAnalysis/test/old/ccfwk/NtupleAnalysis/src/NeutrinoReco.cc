#include <inc/NeutrinoReco.h>
#include <inc/utils.h>
#include <cmath>
#include <memory>

#include <TRandom3.h>

std::vector<TLorentzVector> nak::NeutrinoRecoSTD::operator()(const TLorentzVector& lepton, const TLorentzVector& MET) const {

  TVector3 lep_pT(lepton.X(), lepton.Y(), 0.);
  TVector3 neu_pT(MET.X(), MET.Y(), 0.);

  const float mass_w = 80.399;

  float mu = (mass_w * mass_w / 2.) + lep_pT*neu_pT;
  float A = -1. * (lep_pT * lep_pT);
  float B = mu * lepton.Pz();
  float C = mu * mu - (lepton.E() * lepton.E() * (neu_pT * neu_pT));
  float discr = B * B - A * C;

  std::vector<TLorentzVector> solutions;
  if(0 >= discr){

    TLorentzVector solution(MET.Px(), MET.Py(), -B/A, 0.);
    solution.SetE(solution.P());
    solutions.push_back(solution);
  }
  else {

    discr = sqrt(discr);
    TLorentzVector solution(MET.Px(), MET.Py(), (-B-discr)/A, 0.);
    solution.SetE(solution.P());
    solutions.push_back(solution);

    TLorentzVector solution2(MET.Px(), MET.Py(), (-B+discr)/A, 0.);
    solution2.SetE(solution2.P());
    solutions.push_back(solution2);
  }

  if(!solutions.size()) util::KILL("NeutrinoRecoSTD::operator() -- no solutions found");

  return solutions;
}
///

std::vector<TLorentzVector> nak::NeutrinoRecoRE1::operator()(const TLorentzVector& lepton, const TLorentzVector& MET) const {

  TVector3 lep_pT(lepton.X(), lepton.Y(), 0.);
  TVector3 neu_pT(MET.X(), MET.Y(), 0.);

  float mW = 2*((lepton.Pt()*MET.Pt()*lepton.E()/lepton.P()) - lep_pT*neu_pT);
  if(mW >= 0) mW = sqrt(mW);
  else if(fabs(mW/(lepton.Pt()*MET.Pt())) < 1e-5) mW = 0.;
  else util::KILL("NeutrinoRecoRE1::operator() -- negative value for W-boson mass");

  float mu = (mW * mW / 2.) + lep_pT*neu_pT;
  float A = -1 * lep_pT * lep_pT;
  float B = mu * lepton.Pz();

  std::vector<TLorentzVector> solutions;
  TLorentzVector solution(MET.Px(), MET.Py(), -B/A, 0.);
  solution.SetE(solution.P());
  solutions.push_back(solution);

  if(!solutions.size()) util::KILL("NeutrinoRecoRE1::operator() -- no solutions found");

  return solutions;
}
///

std::vector<TLorentzVector> nak::NeutrinoRecoRWM::operator()(const TLorentzVector& lepton, const TLorentzVector& MET) const {

  TVector3 lep_pT(lepton.X(), lepton.Y(), 0.);
  TVector3 neu_pT(MET.X(), MET.Y(), 0.);

  std::vector<TLorentzVector> solutions;

  std::auto_ptr<TRandom3> rand(new TRandom3());
  rand->SetSeed(0);

  int n_fail(0);
  bool sol_found(false);
  while(!sol_found){

    float mass_w(80.399);

    if(n_fail > 0) mass_w = rand->BreitWigner(79.82, 2.);
    if(76. > mass_w || mass_w > 84.) continue;

    float mu = (mass_w * mass_w / 2.) + lep_pT*neu_pT;
    float A = -1. * (lep_pT * lep_pT);
    float B = mu * lepton.Pz();
    float C = mu * mu - (lepton.E() * lepton.E() * (neu_pT * neu_pT));

    float discr = B * B - A * C;

    if(discr >= 0){

      sol_found = true;

      TLorentzVector solution(MET.Px(), MET.Py(), (-B-sqrt(discr))/A, 0.);
      solution.SetE(solution.P());
      solutions.push_back(solution);

      if(!discr){
        TLorentzVector solution2(MET.Px(), MET.Py(), (-B+sqrt(discr))/A, 0.);
        solution2.SetE(solution2.P());
        solutions.push_back(solution2);
      }

      if(!solutions.size()) util::KILL("NeutrinoRecoRWM::operator() -- no solutions found");
    }
    else if(n_fail > 10){

      sol_found = true;

      TLorentzVector solution(MET.Px(), MET.Py(), -B/A, 0.);
      solution.SetE(solution.P());
      solutions.push_back(solution);

      if(!solutions.size()) util::KILL("NeutrinoRecoRWM::operator() -- no solutions found");
    }
    else{ ++n_fail; continue; }
  }

  return solutions;
}
///
