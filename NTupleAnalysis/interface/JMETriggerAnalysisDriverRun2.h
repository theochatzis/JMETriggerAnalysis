#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverRun2_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverRun2_h

#include <vector>

#include <JMETriggerAnalysis/NTupleAnalysis/interface/AnalysisDriverBase.h>

class JMETriggerAnalysisDriverRun2 : public AnalysisDriverBase {
public:
  explicit JMETriggerAnalysisDriverRun2(const std::string& outputFilePath = "",
                                        const std::string& outputFileMode = "recreate");
  explicit JMETriggerAnalysisDriverRun2(const std::string& tfile,
                                        const std::string& ttree,
                                        const std::string& outputFilePath,
                                        const std::string& outputFileMode = "recreate");
  ~JMETriggerAnalysisDriverRun2() override {}

  void init() override;
  void analyze() override;

protected:
  std::vector<std::string> jetCategoryLabels_;
  virtual bool jetBelongsToCategory(const std::string& categLabel, const float jetPt, const float jetAbsEta, const float jetPhi, const float jetEta) const;

  std::vector<std::string> hltPaths_PFMET_;

  class fillHistoDataJets {
  public:
    std::string jetCollection = "";
    float jetPtMin = -1.;

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
                           const std::vector<std::string>& matchLabels = {});
  void bookHistograms_MET(const std::string& dir,
                          const std::string& jetType,
                          const std::vector<std::string>& matchLabels = {});

  void fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhDataJets);
  void fillHistograms_MET(const std::string& dir, const fillHistoDataMET& fhDataMET);
};

#endif
