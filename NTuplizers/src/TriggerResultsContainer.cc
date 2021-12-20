#include <JMETriggerAnalysis/NTuplizers/interface/TriggerResultsContainer.h>
#include <FWCore/MessageLogger/interface/MessageLogger.h>
#include <FWCore/Common/interface/TriggerNames.h>

TriggerResultsContainer::TriggerResultsContainer(const std::vector<std::string>& names,
                                                 const std::string& inputTagLabel,
                                                 const edm::EDGetToken& token)
    : inputTagLabel_(inputTagLabel), token_(token) {
  entries_.clear();
  entries_.reserve(names.size());

  for (const auto& name_i : names) {
    bool skip_entry(false);

    for (const auto& entry_i : entries_) {
      if (entry_i.name == name_i) {
        skip_entry = true;
        break;
      }
    }

    if (skip_entry) {
      break;
    }

    entries_.emplace_back(TriggerResultsContainer::Entry(name_i, false));
  }
}

void TriggerResultsContainer::clear() {
  for (auto& entry_i : entries_) {
    entry_i.accept = false;
  }
}

void TriggerResultsContainer::fill(const edm::TriggerResults& triggerResults, const edm::Event& iEvent) {
  // reset values to false
  this->clear();

  const auto& triggerNames = iEvent.triggerNames(triggerResults).triggerNames();

  if (triggerResults.size() != triggerNames.size()) {
    edm::LogWarning("TriggerResultsContainer::fill")
        << "input error: size of TriggerResults (" << triggerResults.size() << ") and TriggerNames ("
        << triggerNames.size() << ") differ, exiting function";

    return;
  }

  for (unsigned int idx = 0; idx < triggerResults.size(); ++idx) {
    // since default value of Entry::accept is false,
    // value needs to be changed only for accepted triggers
    if (triggerResults.at(idx).accept()) {
      const auto& triggerName = triggerNames.at(idx);
      const auto triggerName_unv = triggerName.substr(0, triggerName.rfind("_v"));

      LogDebug("Value") << "path = " << triggerName << ", path (un-versioned) = " << triggerName_unv
                        << ", accept = " << triggerResults.at(idx).accept();

      for (auto& entry_i : entries_) {
        // require Entry::name to match either full name (e.g. "HLT_IsoMu24_v10")
        // or name without version (e.g. "HLT_IsoMu24")
        if ((entry_i.name == triggerName_unv) || (entry_i.name == triggerName)) {
          entry_i.accept = triggerResults.at(idx).accept();

          LogDebug("Value") << "path = " << triggerName << ", path (un-versioned) = " << triggerName_unv
                            << ", accept = " << triggerResults.at(idx).accept()
                            << ", matched to entry with name = " << entry_i.name << " (accept = " << entry_i.accept
                            << ")";
        }
      }
    }
  }
}
