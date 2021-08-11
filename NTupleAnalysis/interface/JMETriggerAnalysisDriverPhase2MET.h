#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2MET_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverPhase2MET_h

#include <map>

#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriver.h>

class JMETriggerAnalysisDriverPhase2MET : public JMETriggerAnalysisDriver {

 public:
  explicit JMETriggerAnalysisDriverPhase2MET(const std::string& outputFilePath="", const std::string& outputFileMode="recreate");
  explicit JMETriggerAnalysisDriverPhase2MET(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode="recreate");
  ~JMETriggerAnalysisDriverPhase2MET() {}

  void init() override;
  void analyze() override;

 protected:
  void bookHistograms(const std::string&);
  void fillHistograms(const std::string&, float const weight=1.f);

  bool l1tMETSeed(std::string const& key) const;

  float getMET(std::string const&) const;
  float getMHT(float const, float const) const;
};

#endif
