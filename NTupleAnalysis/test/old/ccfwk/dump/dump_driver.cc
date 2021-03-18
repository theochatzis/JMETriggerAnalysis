#include <iostream>

#include <TProof.h>
#include <TChain.h>
#include <TEnv.h>
#include <TDSet.h>

#include <NtupleAnalysis/inc/utils.h>

int main(int argc, char** argv){

  const std::string input(argv[1]);
  const std::string selec(argv[2]);
  const std::string opts (argv[3]);

  const std::string wrks_str(util::get_option_from_string(opts, "w"));
  const int PROOF_wrkN(wrks_str != "" ? atoi(wrks_str.c_str()) : 0);

  // cfg chain
  TChain c("Events");
  c.Add(input.c_str());

  // execution
  if(PROOF_wrkN > 0){

    gEnv->SetValue("ProofLite.Sandbox", "$PROOF_SANDBOX");

    TProof* p = TProof::Open("lite://", ("workers="+util::int_to_str(PROOF_wrkN)).c_str());
    p->Exec("gSystem->Load(\"libNtupleAnalysis.so\")");
//    p->UploadPackage("$TTBSM_ENV/NtupleAnalysis/lib/NtupleAnalysisPAR.par");
//    p->EnablePackage("NtupleAnalysisPAR");
//    p->ShowPackages();
//    p->ShowEnabledPackages();
//    p->Exec("gSystem->ListLibraries()");

    if(p->GetQueryResults()){

      p->GetQueryResults()->SetOwner(kTRUE);
      p->GetQueryResults()->Clear();
      p->GetQueryResults()->SetOwner(kFALSE);
    }

    p->ClearInput();

    const Long64_t eventsPerNode(c.GetEntries() / p->GetParallel());
    p->SetParameter("PROOF_MemLogFreq", (Long64_t) (eventsPerNode > 10000 ? (eventsPerNode/10) : 1000));
    p->SetParameter("PROOF_LookupOpt", "none");

//    p->AddEnvVar("PROOF_MASTER_WRAPPERCMD", "valgrind_opts:--leak-check=full --track-origins=yes --num-callers=32");
//    p->AddEnvVar("PROOF_SLAVE_WRAPPERCMD" , "valgrind_opts:--leak-check=full --track-origins=yes --num-callers=32");
    p->AddEnvVar("PROOF_RESMEMMAX" , "10000");
    p->AddEnvVar("PROOF_VIRTMEMMAX", "10000");

    TDSet iset(c);
    p->Process(&iset, selec.c_str(), opts.c_str());

    p->Close();
  }
  else {

    clock_t begin(clock());

    c.Process(selec.c_str(), opts.c_str());

    clock_t end(clock());
    float exe_time(float((end-begin)/CLOCKS_PER_SEC));
    std::cout << "@@@ execution time : " << exe_time << " sec\n";
  }

  return 0;
}
