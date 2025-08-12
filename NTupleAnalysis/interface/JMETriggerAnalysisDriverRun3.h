#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverRun3_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverRun3_h

#include <map>

#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriver.h>

class JMETriggerAnalysisDriverRun3 : public JMETriggerAnalysisDriver {

 public:
  explicit JMETriggerAnalysisDriverRun3(const std::string& outputFilePath="", const std::string& outputFileMode="recreate");
  explicit JMETriggerAnalysisDriverRun3(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode="recreate");
  ~JMETriggerAnalysisDriverRun3() {}

  void init() override;
  void analyze() override;

  // adding setter methods for YAML-driven config (callable from Python for communication with the outside world)
  void setJetCategoryLabels(const std::vector<std::string>& labels);
  void setRunPeriods(const std::vector<std::string>& periods);
  void setLightVersion(bool val);
  void setUseOnlyTriggers(bool val);
  void setUseOnlyRunPeriods(bool val);
  void setJetTriggers(const std::vector<std::string>& triggers);
  void setHTTriggers(const std::vector<std::string>& triggers);
  void setMETTriggers(const std::vector<std::string>& triggers);

 protected:
  bool jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta, const float jetPhi, const float jetEta) const override;

  void bookHistograms_Jets_2DMaps(const std::string& dir, const std::string& jetType1, const std::string& jetType2);
  void bookHistograms_MET_2DMaps(const std::string& dir, const std::string& metType1, const std::string& metType2, bool const book1D=false);

  void fillHistograms_Jets_2DMaps(const std::string& dir, const fillHistoDataJets& fhDataJets1, const fillHistoDataJets& fhDataJets2, float const weight=1.f);
  void fillHistograms_MET_2DMaps(const std::string& dir, const fillHistoDataMET& fhDataMET1, const fillHistoDataMET& fhDataMET2, bool const fill1D=false, float const weight=1.f);
  
  void bookHistograms_METMHT(const std::string&);
  void fillHistograms_METMHT(const std::string&, float const weight=1.f);

  float getMET(std::string const&) const;
  float getPFMHT(float const, float const) const;
  float getPuppiMHT(float const, float const) const;
  
  // Helper variables
  std::map<std::string, std::map<std::string, std::string>> labelMap_jetAK4_;
  std::map<std::string, std::map<std::string, std::string>> labelMap_jetAK8_;
  std::map<std::string, std::map<std::string, std::string>> labelMap_MET_;

  std::vector<std::string> jettriggers;
  std::vector<std::string> httriggers;
  std::vector<std::string> mettriggers;
  std::vector<std::string> puintervals;
  std::vector<std::string> runPeriods;
  bool lightVersion;
  bool useOnlyTriggers;
  bool useOnlyRunPeriods;

  bool isOffline;

  bool hltJetTrigger(std::string const& key) const;
  bool hltHTTrigger(std::string const& key) const;
  bool hltMETTrigger(std::string const& key) const;
  bool pileupintervals(std::string const& key) const;
  bool runPeriod(std::string const& key) const;
  
};

#endif
