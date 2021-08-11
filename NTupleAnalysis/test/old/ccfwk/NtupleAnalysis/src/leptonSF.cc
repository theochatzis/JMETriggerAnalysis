#include <inc/leptonSF.h>
#include <inc/utils.h>

nak::leptonSF::leptonSF(){

  th2_EleID = 0;
  tf1_EleHLT = 0;
  file_MuoID = 0;
  file_MuoHLT = 0;
}

nak::leptonSF::~leptonSF(){

  if(file_MuoID) file_MuoID->Close();
  if(file_MuoHLT) file_MuoHLT->Close();
}

void nak::leptonSF::open_EleID_file(const std::string& ifile_){

  TFile* file_EleID = TFile::Open(ifile_.c_str());
  if(!file_EleID->IsOpen()) util::KILL("leptonSF::open_EleID_file() -- failed to open input file: "+ifile_);

  th2_EleID = (TH2F*) file_EleID->Get("electronsDATAMCratio_FO_ID");
  if(!th2_EleID) util::KILL("leptonSF::open_EleID_file() -- TF1 object 'fit' not found in input file");

  th2_EleID->SetDirectory(0);
  file_EleID->Close();

  return;
}

void nak::leptonSF::open_EleHLT_file(const std::string& ifile_){

  TFile* file_EleHLT = TFile::Open(ifile_.c_str());
  if(!file_EleHLT->IsOpen()) util::KILL("leptonSF::open_EleHLT_file() -- failed to open input file: "+ifile_);

  tf1_EleHLT = (TF1*) file_EleHLT->Get("fit");
  if(!tf1_EleHLT) util::KILL("leptonSF::open_EleHLT_file() -- TF1 object 'fit' not found in input file");

  file_EleHLT->Close();

  return;
}

void nak::leptonSF::open_MuoID_file(const std::string& ifile_){

  file_MuoID = TFile::Open(ifile_.c_str());
  if(!file_MuoID->IsOpen()) util::KILL("leptonSF::open_MuoID_file() -- failed to open input file: "+ifile_);

  return;
}

void nak::leptonSF::open_MuoHLT_file(const std::string& ifile_){

  file_MuoHLT = TFile::Open(ifile_.c_str());
  if(!file_MuoHLT->IsOpen()) util::KILL("leptonSF::open_MuoHLT_file() -- failed to open input file: "+ifile_);

  return;
}

double nak::leptonSF::get_EleID_weight(const double& pt_, const double& etaSC_, const std::string& sys_){

  double weight(1.);

  double pt = pt_;
  if(pt >= th2_EleID->GetYaxis()->GetXmax()) pt = th2_EleID->GetYaxis()->GetXmax() * .999;

     if(sys_ == "none") weight = th2_EleID->GetBinContent(th2_EleID->FindBin(fabs(etaSC_), pt));
  else if(sys_ == "up") weight = th2_EleID->GetBinContent(th2_EleID->FindBin(fabs(etaSC_), pt)) + th2_EleID->GetBinError(th2_EleID->FindBin(fabs(etaSC_), pt));
  else if(sys_ == "dn") weight = th2_EleID->GetBinContent(th2_EleID->FindBin(fabs(etaSC_), pt)) - th2_EleID->GetBinError(th2_EleID->FindBin(fabs(etaSC_), pt));
  else util::KILL("leptonSF::get_EleID_weight() -- undefined 'sys' argument ('none', 'up' or 'dn'): "+sys_);

  if(weight < 0.) util::KILL("leptonSF::get_EleID_weight() -- logical error given by negative weight");

  return weight;
}

double nak::leptonSF::get_EleHLT_weight(const double& pt_, const std::string& sys_){

  double weight(1.);

  float arg = (float) pt_;
  if(arg < tf1_EleHLT->GetXmin()) arg = tf1_EleHLT->GetXmin();
  else if(arg > tf1_EleHLT->GetXmax()) arg = tf1_EleHLT->GetXmax();

     if(sys_ == "none") weight = tf1_EleHLT->Eval(arg);
  else if(sys_ == "up") weight = tf1_EleHLT->Eval(arg) * (1. + .01);
  else if(sys_ == "dn") weight = tf1_EleHLT->Eval(arg) * (1. - .01);
  else util::KILL("leptonSF::get_EleHLT_weight() -- undefined 'sys' argument ('none', 'up' or 'dn'): "+sys_);

  if(weight < 0.) util::KILL("leptonSF::get_EleHLT_weight() -- logical error given by negative weight");

  return weight;
}

double nak::leptonSF::get_MuoID_weight(const double& pt_, const double& eta_, const std::string& sys_){

  double abseta = fabs(eta_);
  TGraphAsymmErrors* gSF(0);
       if(0.0 <= abseta && abseta < 0.9) gSF = (TGraphAsymmErrors*) file_MuoID->Get("DATA_over_MC_Tight_pt_abseta<0.9");
  else if(0.9 <= abseta && abseta < 1.2) gSF = (TGraphAsymmErrors*) file_MuoID->Get("DATA_over_MC_Tight_pt_abseta0.9-1.2");
  else if(1.2 <= abseta && abseta < 2.1) gSF = (TGraphAsymmErrors*) file_MuoID->Get("DATA_over_MC_Tight_pt_abseta1.2-2.1");
  else if(2.1 <= abseta && abseta < 2.4) gSF = (TGraphAsymmErrors*) file_MuoID->Get("DATA_over_MC_Tight_pt_abseta2.1-2.4");

  if(!gSF) util::KILL("leptonSF::get_MuoID_weight() -- failed to open TGraph object containing the scale factors");

  double weight = get_weight_from_MuoPOG_graph(*gSF, pt_, sys_, .005);
  return weight;
}

double nak::leptonSF::get_MuoHLT_weight(const double& pt_, const double& eta_, const std::string& sys_){

  double abseta = fabs(eta_);
  TGraphAsymmErrors* gSF(0);
       if(0.0 <= abseta && abseta < 0.9) gSF = (TGraphAsymmErrors*) file_MuoHLT->Get("Mu40_eta2p1_DATA_over_MC_TightID_PT_ABSETA_Barrel_0to0p9_pt45-500_2012ABCD");
  else if(0.9 <= abseta && abseta < 1.2) gSF = (TGraphAsymmErrors*) file_MuoHLT->Get("Mu40_eta2p1_DATA_over_MC_TightID_PT_ABSETA_Transition_0p9to1p2_pt45-500_2012ABCD");
  else if(1.2 <= abseta && abseta < 2.1) gSF = (TGraphAsymmErrors*) file_MuoHLT->Get("Mu40_eta2p1_DATA_over_MC_TightID_PT_ABSETA_Endcaps_1p2to2p1_pt45-500_2012ABCD");

  if(!gSF) util::KILL("leptonSF::get_MuoHLT_weight() -- failed to open TGraph object containing the scale factors");

  double weight = get_weight_from_MuoPOG_graph(*gSF, pt_, sys_, .002);
  return weight;
}

double nak::leptonSF::get_weight_from_MuoPOG_graph(const TGraphAsymmErrors& gSF_, const double& arg_, const std::string& sys_, const double& sys_rerr_){

  int idx(-1);
  bool not_above(false), not_below(false);
  for(int i=0; i<gSF_.GetN(); ++i){

    double x(0.), y(0.);
    gSF_.GetPoint(i, x, y);

    double xup = x + gSF_.GetErrorXhigh(i);
    double xdn = x - gSF_.GetErrorXlow(i);
    if(xdn <= arg_ && arg_ < xup){ idx = i; break; }

    if(arg_ < xup) not_above = true;
    if(arg_ > xdn) not_below = true;
  }

  if(idx < 0){

    if(not_above && !not_below){

      double xmin(3000.);
      for(int i=0; i<gSF_.GetN(); ++i){

        double x(0.), y(0.);
        gSF_.GetPoint(i, x, y);
        double xdn = x - gSF_.GetErrorXlow(i);
        if(xdn < xmin){ xmin = xdn; idx = i; }
      }
    }

    if(!not_above && not_below){

      double xmax(-100.);
      for(int i=0; i<gSF_.GetN(); ++i){

        double x(0.), y(0.);
        gSF_.GetPoint(i, x, y);
        double xup = x + gSF_.GetErrorXhigh(i);
        if(xup > xmax){ xmax = xup; idx = i; }
      }
    }
  }

  if(idx < 0) util::KILL("leptonSF::get_weight_from_MuoPOG_graph() -- logical error given by negative index for SF bin");

  double weight(1.);
  double x(0.), SF(0.);
  gSF_.GetPoint(idx, x, SF);

  if(sys_ == "none") weight = SF;
  else if(sys_ == "up"){
    double estat = gSF_.GetErrorYhigh(idx);
    double esyst = SF * sys_rerr_;
    weight = SF + sqrt(esyst*esyst + estat*estat);
  }
  else if(sys_ == "dn"){
    double estat = gSF_.GetErrorYlow(idx);
    double esyst = SF * sys_rerr_;
    weight = SF - sqrt(esyst*esyst + estat*estat);
  }
  else util::KILL("leptonSF::get_MuoHLT_weight() -- undefined 'sys' argument ('none', 'up' or 'dn'): "+sys_);

  if(weight < 0.) util::KILL("leptonSF::get_weight_from_MuoPOG_graph() -- logical error given by negative weight");

  return weight;
}
