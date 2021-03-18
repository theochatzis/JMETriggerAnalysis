#ifndef NAK_leptonSF_H
#define NAK_leptonSF_H

#include <string>
#include <vector>

#include <inc/utils.h>

#include <TFile.h>
#include <TH2F.h>
#include <TF1.h>
#include <TGraphAsymmErrors.h>

namespace nak {

  class leptonSF {

   public:
    leptonSF();
    ~leptonSF();

    TH2F* th2_EleID;
    void open_EleID_file(const std::string&);
    double get_EleID_weight(const double&, const double&, const std::string& sys="none");

    TF1* tf1_EleHLT;
    void open_EleHLT_file(const std::string&);
    double get_EleHLT_weight(const double&, const std::string& sys="none");

    TFile* file_MuoID;
    void open_MuoID_file(const std::string&);
    double get_MuoID_weight(const double&, const double&, const std::string& sys="none");

    TFile* file_MuoHLT;
    void open_MuoHLT_file(const std::string&);
    double get_MuoHLT_weight(const double&, const double&, const std::string& sys="none");

    double get_weight_from_MuoPOG_graph(const TGraphAsymmErrors&, const double&, const std::string& sys="none", const double& sys_rerr=0.);
  };

}

#endif
