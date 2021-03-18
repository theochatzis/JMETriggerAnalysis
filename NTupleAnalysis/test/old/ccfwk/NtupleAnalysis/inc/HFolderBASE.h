#ifndef NAK_HFolderBASE_H
#define NAK_HFolderBASE_H

#include <string>
#include <vector>
#include <map>

#include <TFile.h>
#include <TDirectory.h>
#include <TH1F.h>
#include <TH2F.h>

#include <inc/Event.h>

namespace nak {

  class HFolderBASE {

   protected:
    std::string name_;
    TDirectory* d0;

   public: 
    explicit HFolderBASE(TFile&, const std::string& dir="");
    virtual ~HFolderBASE();

    virtual void Fill(const nak::Event&, const float) = 0;

    std::string name() const { return name_; }

    void book_TH1F(const std::string&, const int, const float, const float);
    void book_TH2F(const std::string&, const int, const float, const float, const int, const float, const float);
    void Write();
    void Clear();

    TH1F* H1(const std::string&);
    TH2F* H2(const std::string&);

    std::string BinWidth(const TH1F&);

    std::vector<std::string> key_v;

    std::map<std::string, TH1F*> h1;
    std::map<std::string, TH2F*> h2;

    typedef std::map<std::string, TH1F*>::iterator h1_itr;
    typedef std::map<std::string, TH2F*>::iterator h2_itr;
  };

}

#endif
