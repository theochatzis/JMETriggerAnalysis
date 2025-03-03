#ifndef JMETriggerAnalysis_TriggerResultsContainer_h
#define JMETriggerAnalysis_TriggerResultsContainer_h

#include <FWCore/Utilities/interface/EDGetToken.h>
#include <FWCore/Framework/interface/Event.h>
#include <DataFormats/Common/interface/TriggerResults.h>

#include <string>
#include <vector>

class TriggerResultsContainer {
public:
  explicit TriggerResultsContainer(const std::vector<std::string>&, const std::string&, const edm::EDGetToken&);
  virtual ~TriggerResultsContainer() {}

  void clear();
  void fill(const edm::TriggerResults&, const edm::Event&);

  const std::string& inputTagLabel() const { return inputTagLabel_; }
  const edm::EDGetToken& token() const { return token_; }

  class Entry {
  public:
    explicit Entry(const std::string& name, const bool res) : name(name), accept(res), wasrun(res) {}
    virtual ~Entry() {}

    const std::string name;
    bool accept; // shows if trigger trigger accepts the event
    bool wasrun; // shows if trigger is available to "decide" due to prescales (unprescaled triggers are always ON)
  };

  const std::vector<Entry>& entries() { return entries_; }

protected:
  std::vector<Entry> entries_;
  const std::string inputTagLabel_;
  const edm::EDGetToken token_;
};

#endif
