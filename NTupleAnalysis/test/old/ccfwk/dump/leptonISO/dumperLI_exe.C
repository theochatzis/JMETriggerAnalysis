void dumperLI_exe(const std::string& lepton, const std::string& iprex, const std::string& oprex){

  gROOT->ProcessLine(".L dumperLI.C+");

  std::cout << "\n";
  std::cout << ">> input  prefix: " << iprex << "\n";
  std::cout << ">> output prefix: " << oprex << "\n";
  std::cout << "\n";

  std::vector<std::string> samples;
  samples.push_back(".MC.Zp_M1000w01p__phys14_pu20bx25.root");
  samples.push_back(".MC.Zp_M2000w01p__phys14_pu20bx25.root");
  samples.push_back(".MC.Zp_M3000w01p__phys14_pu20bx25.root");

  if(lepton == "muon"){
    samples.push_back(".MC.QCD_MuPt15_py8__phys14_pu20bx25.root");
  }
  else if(lepton == "elec"){
    samples.push_back(".MC.QCD_Pt030to080_bcE_py8__phys14_pu20bx25.root");
    samples.push_back(".MC.QCD_Pt080to170_bcE_py8__phys14_pu20bx25.root");
    samples.push_back(".MC.QCD_Pt170toINF_bcE_py8__phys14_pu20bx25.root");
  }

//  TProof::Open("");

  for(unsigned int i=0; i<samples.size(); ++i){

    TChain c;
    c.Add((iprex+samples.at(i)+"/Events").c_str());

    dumperLI dumperLI;
    dumperLI.set_channel(lepton);
    dumperLI.set_output(oprex+samples.at(i));
    c.Process(&dumperLI);
  }
}
