#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriver_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriver_h

#include <vector>

#include <JMETriggerAnalysis/NTupleAnalysis/interface/AnalysisDriverBase.h>

class JMETriggerAnalysisDriver : public AnalysisDriverBase {
public:
  explicit JMETriggerAnalysisDriver(const std::string& outputFilePath = "",
                                    const std::string& outputFileMode = "recreate");
  explicit JMETriggerAnalysisDriver(const std::string& tfile,
                                    const std::string& ttree,
                                    const std::string& outputFilePath,
                                    const std::string& outputFileMode = "recreate");
  ~JMETriggerAnalysisDriver() override {}

  void init() override;
  void analyze() override;

protected:
  std::vector<std::string> jetCategoryLabels_;
  virtual bool jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta, const float jetPhi, const float jetEta) const;

  class fillHistoDataJets {
  public:
    std::string jetCollection = "";
    float jetPtMin = -1.;
    float jetAbsEtaMax = 9999.;

    struct Match {
      Match(const std::string& theLabel,
            const std::string& theJetCollection,
            const float theJetPtMin,
            const float theJetDeltaRMin)
          : label(theLabel), jetCollection(theJetCollection), jetPtMin(theJetPtMin), jetDeltaRMin(theJetDeltaRMin) {}
      std::string label;
      std::string jetCollection;
      float jetPtMin;
      float jetDeltaRMin;
    };
    std::vector<Match> matches;
  };

  class fillHistoDataMET {
  public:
    std::string metCollection = "";

    struct Match {
      Match(const std::string& theLabel, const std::string& theMETCollection)
          : label(theLabel), metCollection(theMETCollection) {}
      std::string label;
      std::string metCollection;
    };
    std::vector<Match> matches;
  };

  void bookHistograms_Jets(const std::string& dir,
                           const std::string& jetType,
                           const std::vector<std::string>& matchLabels = {},
                           bool const lightVersion = false);
  void bookHistograms_MET(const std::string& dir,
                          const std::string& metType,
                          const std::vector<std::string>& matchLabels = {},
                          bool const lightVersion = false);

  void fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhDataJets, float const weight = 1.f,bool const lightVersion = false);
  void fillHistograms_MET(const std::string& dir, const fillHistoDataMET& fhDataMET, float const weight = 1.f,bool const lightVersion = false);
};

#endif
