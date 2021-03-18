#include <inc/Event.h>
#include <inc/utils.h>

nak::Event::Event(){

  INFO = 0;
  GENP = 0;
  HLT = 0;
  PVTX = 0;
  MUO = 0;
  ELE = 0;
  JET_AK4 = 0;
  JET_AK8 = 0;
  JET_CA15 = 0;
  MET = 0;
}

void* nak::Event::get(const std::string& key) const {

  void* coll(0);

  if     (key == "INFO")     coll = INFO;
  else if(key == "GENP")     coll = GENP;
  else if(key == "HLT")      coll = HLT;
  else if(key == "PVTX")     coll = PVTX;
  else if(key == "MUO")      coll = MUO;
  else if(key == "ELE")      coll = ELE;
  else if(key == "JET_AK4")  coll = JET_AK4;
  else if(key == "JET_AK8")  coll = JET_AK8;
  else if(key == "JET_CA15") coll = JET_CA15;
  else if(key == "MET")      coll = MET;

  else util::KILL("Event::get() -- invalid key: "+key);

  return coll;
}

void nak::Event::Delete(){

  if(INFO)     delete INFO;
  if(GENP)     delete GENP;
  if(HLT)      delete HLT;
  if(PVTX)     delete PVTX;
  if(MUO)      delete MUO;
  if(ELE)      delete ELE;
  if(JET_AK4)  delete JET_AK4;
  if(JET_AK8)  delete JET_AK8;
  if(JET_CA15) delete JET_CA15;
  if(MET)      delete MET;

  return;
}
