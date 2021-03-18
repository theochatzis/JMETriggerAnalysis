#ifndef UAM_EVENTINFO_H_
#define UAM_EVENTINFO_H_

namespace xtt {

  class EventInfo {
   public:
    EventInfo();
    virtual ~EventInfo() {}

    int Event;
    int LumiBlock;
    int Run;

    int nPV;
    float MCPileupBX0;

    float pdf_id1;
    float pdf_id2;
    float pdf_x1;
    float pdf_x2;
    float pdf_scalePDF;
    float pdf_xPDF1;
    float pdf_xPDF2;

    float MCWeight;
  };

}

#endif
