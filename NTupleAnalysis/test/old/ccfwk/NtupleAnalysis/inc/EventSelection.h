#ifndef NAK_EVENTSELECTION_H_
#define NAK_EVENTSELECTION_H_

#include <inc/Event.h>
#include <inc/TopTagID.h>

namespace nak {

  class EventSelection {
   public:
    virtual bool pass(const Event&) = 0;
  };

  class VTagEvent : public EventSelection {
   public:
    explicit VTagEvent(const std::string& jet_key, const std::string& vjet_key, const VTagger* vtagid, const float dr):
    jet_key_(jet_key), vjet_key_(vjet_key), vtagID_(vtagid), minDR_vtag_jet_(dr) {}

    virtual bool pass(const Event&);

   private:
    std::string jet_key_;
    std::string vjet_key_;
    const VTagger* vtagID_;
    float minDR_vtag_jet_;
  };

  class TopTagEvent : public EventSelection {
   public:
    explicit TopTagEvent(const std::string& jet_key, const std::string& topjet_key, const TopTagID* ttagid, const float dr):
      jet_key_(jet_key), topjet_key_(topjet_key), ttagID_(ttagid), minDR_ttag_jet_(dr) {}

    virtual bool pass(const Event&);

   private:
    std::string jet_key_;
    std::string topjet_key_;
    const TopTagID* ttagID_;
    float minDR_ttag_jet_;
  };

}

#endif
