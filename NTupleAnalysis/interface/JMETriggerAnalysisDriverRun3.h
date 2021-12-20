#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverRun3_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverRun3_h

#include <map>

#include <JMETriggerAnalysis/NTupleAnalysis/interface/JMETriggerAnalysisDriver.h>

class JMETriggerAnalysisDriverRun3 : public JMETriggerAnalysisDriver {
public:
  explicit JMETriggerAnalysisDriverRun3(const std::string& outputFilePath = "",
                                        const std::string& outputFileMode = "recreate");
  explicit JMETriggerAnalysisDriverRun3(const std::string& tfile,
                                        const std::string& ttree,
                                        const std::string& outputFilePath,
                                        const std::string& outputFileMode = "recreate");
  ~JMETriggerAnalysisDriverRun3() override {}

  void init() override;
  void analyze() override;

protected:
  bool jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta) const override;

  void bookHistograms_Jets_2DMaps(const std::string& dir, const std::string& jetType1, const std::string& jetType2);
  void bookHistograms_MET_2DMaps(const std::string& dir,
                                 const std::string& metType1,
                                 const std::string& metType2,
                                 bool const book1D = false);

  void fillHistograms_Jets_2DMaps(const std::string& dir,
                                  const fillHistoDataJets& fhDataJets1,
                                  const fillHistoDataJets& fhDataJets2,
                                  float const weight = 1.f);
  void fillHistograms_MET_2DMaps(const std::string& dir,
                                 const fillHistoDataMET& fhDataMET1,
                                 const fillHistoDataMET& fhDataMET2,
                                 bool const fill1D = false,
                                 float const weight = 1.f);

  std::map<std::string, std::map<std::string, std::string>> labelMap_jetAK4_;
  std::map<std::string, std::map<std::string, std::string>> labelMap_jetAK8_;
  std::map<std::string, std::map<std::string, std::string>> labelMap_MET_;

  std::vector<std::string> l1tSeeds_1Jet_;
  std::vector<std::string> l1tSeeds_HT_;
  std::vector<std::string> l1tSeeds_MET_;
};

#endif
