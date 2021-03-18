#ifndef NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverJES_h
#define NTupleAnalysis_JMETrigger_JMETriggerAnalysisDriverJES_h

#include <vector>

#include <JMETriggerAnalysis/NTupleAnalysis/interface/AnalysisDriverBase.h>

class JMETriggerAnalysisDriverJES : public AnalysisDriverBase {

 public:
  explicit JMETriggerAnalysisDriverJES(const std::string& outputFilePath="", const std::string& outputFileMode="recreate");
  explicit JMETriggerAnalysisDriverJES(const std::string& tfile, const std::string& ttree, const std::string& outputFilePath, const std::string& outputFileMode="recreate");
  virtual ~JMETriggerAnalysisDriverJES() {}

  void init() override;
  void analyze() override;

 protected:
  std::vector<std::string> jetCollectionsAK4_;
  std::vector<std::string> jetCollectionsAK8_;

  std::vector<float> jetEtaBinEdges_;

  std::string jetEtaString(float const jetEta) const;
  std::string jetEtaBinLabel(float const jetEta) const;

  class fillHistoDataJets {
   public:
    std::string jetCollection = "";
    float jetPtMin = -1.;

    struct Match {
      Match(const std::string& theLabel, const std::string& theJetCollection, const float theJetPtMin, const float theJetDeltaRMin)
        : label(theLabel), jetCollection(theJetCollection), jetPtMin(theJetPtMin), jetDeltaRMin(theJetDeltaRMin) {}
      std::string label;
      std::string jetCollection;
      float jetPtMin;
      float jetDeltaRMin;
    };
    std::vector<Match> matches;
  };

  void bookHistograms_Jets(const std::string& dir, const std::string& jetType, const std::vector<std::string>& matchLabels={});
  void fillHistograms_Jets(const std::string& dir, const fillHistoDataJets& fhDataJets);
};

#endif
