#include <JMETriggerAnalysis/NTupleAnalysis/interface/AnalysisDriverBase.h>
#include <JMETriggerAnalysis/NTupleAnalysis/interface/Utils.h>

#include <iostream>

AnalysisDriverBase::AnalysisDriverBase(const std::string& outputFilePath, const std::string& outputFileMode)
    : outputFilePath_(outputFilePath), outputFileMode_(outputFileMode) {}

AnalysisDriverBase::AnalysisDriverBase(const std::string& tfile,
                                       const std::string& ttree,
                                       const std::string& outputFilePath,
                                       const std::string& outputFileMode)
    : AnalysisDriverBase(outputFilePath, outputFileMode) {
  setInputTTree(tfile, ttree);
}

int AnalysisDriverBase::setInputTTree(const std::string& tfile, const std::string& ttree) {
  theFile_.reset(new TFile(tfile.c_str()));
  if ((theFile_.get() == nullptr) || theFile_->IsZombie()) {
    return 1;
  }

  theReader_.reset(new TTreeReader(ttree.c_str(), theFile_.get()));
  if ((theReader_.get() == nullptr) || theReader_->IsInvalid()) {
    throw std::runtime_error("AnalysisDriverBase::AnalysisDriverBase -- invalid TTreeReader");
  }

  map_TTreeReaderValues_.clear();

  auto iter = theReader_->GetTree()->GetIteratorOnAllLeaves();
  TLeaf* leaf(nullptr);
  while ((leaf = ((TLeaf*)iter->Next()))) {
    const std::string type(leaf->GetTypeName());
    if (type == "Bool_t") {
      map_TTreeReaderValues_.insert(
          std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<bool>>(*theReader_, leaf->GetName())));
    } else if (type == "UInt_t") {
      map_TTreeReaderValues_.insert(std::make_pair(
          leaf->GetName(), std::make_unique<TTreeReaderValue<unsigned int>>(*theReader_, leaf->GetName())));
    } else if (type == "Int_t") {
      map_TTreeReaderValues_.insert(
          std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<int>>(*theReader_, leaf->GetName())));
    } else if (type == "Long64_t") {
      map_TTreeReaderValues_.insert(
          std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<long long>>(*theReader_, leaf->GetName())));
    } else if (type == "ULong64_t") {
      map_TTreeReaderValues_.insert(std::make_pair(
          leaf->GetName(), std::make_unique<TTreeReaderValue<unsigned long long>>(*theReader_, leaf->GetName())));
    } else if (type == "Float_t") {
      map_TTreeReaderValues_.insert(
          std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<float>>(*theReader_, leaf->GetName())));
    } else if (type == "Double_t") {
      map_TTreeReaderValues_.insert(
          std::make_pair(leaf->GetName(), std::make_unique<TTreeReaderValue<double>>(*theReader_, leaf->GetName())));
    } else if (type == "vector<bool>") {
      map_TTreeReaderValues_.insert(std::make_pair(
          leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<bool>>>(*theReader_, leaf->GetName())));
    } else if (type == "vector<unsigned int>") {
      map_TTreeReaderValues_.insert(
          std::make_pair(leaf->GetName(),
                         std::make_unique<TTreeReaderValue<std::vector<unsigned int>>>(*theReader_, leaf->GetName())));
    } else if (type == "vector<int>") {
      map_TTreeReaderValues_.insert(std::make_pair(
          leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<int>>>(*theReader_, leaf->GetName())));
    } else if (type == "vector<float>") {
      map_TTreeReaderValues_.insert(std::make_pair(
          leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<float>>>(*theReader_, leaf->GetName())));
    } else if (type == "vector<double>") {
      map_TTreeReaderValues_.insert(std::make_pair(
          leaf->GetName(), std::make_unique<TTreeReaderValue<std::vector<double>>>(*theReader_, leaf->GetName())));
    } else {
      std::ostringstream ss_str;
      ss_str << "invalid type for input TLeaf \"" << leaf->GetName() << "\": " << type;
      throw std::runtime_error(ss_str.str());
    }
  }

  return 1;
}

void AnalysisDriverBase::process(const Long64_t firstEntry, const Long64_t maxEntries) {
  //  this->init();

  if ((theReader_.get() == nullptr) || theReader_->IsInvalid()) {
    throw std::runtime_error("AnalysisDriverBase::process -- invalid TTreeReader");
  } else {
    if (maxEntries != 0) {
      auto const totalEntries((maxEntries >= 0) ? maxEntries : theReader_->GetEntries());
      auto const lastEntry(firstEntry + totalEntries - 1);

      while (theReader_->Next()) {
        if (theReader_->GetCurrentEntry() < firstEntry) {
          continue;
        }

        if (theReader_->GetCurrentEntry() > lastEntry) {
          break;
        }

        this->analyze();
        ++eventsProcessed_;
      }
    }

    if (not outputFilePath_.empty()) {
      this->writeToFile(outputFilePath_, outputFileMode_);
    }
  }
}

void AnalysisDriverBase::writeToFile(const std::string& output_file, const std::string& output_mode) {
  TFile outFile(output_file.c_str(), output_mode.c_str());
  if (not outFile.IsZombie()) {
    outFile.cd();
    this->write(outFile);
    outFile.Close();
  } else {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::writeToFile(\"" << output_file << "\", \"" << output_mode << "\") -- "
        << "failed to open output TFile";
    throw std::runtime_error(oss.str());
  }
}

void AnalysisDriverBase::addOption(const std::string& key, const std::string& opt) {
  if (hasOption(key)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addOption(\"" << key << "\", \"" << opt << "\") -- option with key \"" << key
        << "\" already exists:"
        << " (key = \"" << key << "\", value = \"" << map_options_.at(key) << "\")";
    throw std::runtime_error(oss.str());
  } else {
    if (verbosity_ >= 0) {
      std::cout << ">> added option (key = \"" << key << "\", value = \"" << opt << "\")" << std::endl;
    }
    map_options_.insert(std::make_pair(key, opt));
  }
}

std::string const& AnalysisDriverBase::getOption(const std::string& key) const {
  if (not hasOption(key)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::getOption(\"" << key << "\") -- "
        << "option with key \"" << key << "\" does not exist";
    throw std::runtime_error(oss.str());
  }

  return map_options_.at(key);
}

void AnalysisDriverBase::write(TFile& outFile) {
  for (auto const& key : outputKeys_) {
    auto keyTokens(utils::stringTokens(key, "/"));
    if (keyTokens.empty()) {
      continue;
    }

    TDirectory* targetDir(&outFile);
    while (keyTokens.size() != 1) {
      TDirectory* key = dynamic_cast<TDirectory*>(targetDir->Get(keyTokens.begin()->c_str()));
      targetDir = key ? key : targetDir->mkdir(keyTokens.begin()->c_str());
      keyTokens.erase(keyTokens.begin());
    }

    targetDir->cd();

    if (hasTH1D(key)) {
      mapTH1D_.at(key)->SetName(keyTokens.begin()->c_str());
      mapTH1D_.at(key)->SetTitle(keyTokens.begin()->c_str());
      if (mapTH1D_.at(key)->GetEntries() > 0){ // only write outputs in case the histogram has entries
        mapTH1D_.at(key)->Write();
      }
    } else if (hasTH2D(key)) {
      mapTH2D_.at(key)->SetName(keyTokens.begin()->c_str());
      mapTH2D_.at(key)->SetTitle(keyTokens.begin()->c_str());
      if (mapTH2D_.at(key)->GetEntries() > 0){ // only write outputs in case the histogram has entries
        mapTH2D_.at(key)->Write();
      }
    } else if (hasTH3D(key)) {
      mapTH3D_.at(key)->SetName(keyTokens.begin()->c_str());
      mapTH3D_.at(key)->SetTitle(keyTokens.begin()->c_str());
      if (mapTH3D_.at(key)->GetEntries() > 0){ // only write outputs in case the histogram has entries
        mapTH3D_.at(key)->Write();
      }
    }
  }
}

void AnalysisDriverBase::addTH1D(const std::string& name, int const nxbins, float const xmin, float const xmax) {
  if (hasTH1D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH1D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH2D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH2D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH3D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH3D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (xmin >= xmax) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "x-min value is not smaller than x-max value (" << xmin << " >= " << xmax << ")";
    throw std::runtime_error(oss.str());
  } else if (nxbins <= 0) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "number of x-axis bins is not positive (" << nxbins << " <= 0)";
    throw std::runtime_error(oss.str());
  }

  mapTH1D_.insert(
      std::make_pair(name, std::unique_ptr<TH1D>(new TH1D(name.c_str(), name.c_str(), nxbins, xmin, xmax))));
  mapTH1D_.at(name)->SetDirectory(nullptr);
  mapTH1D_.at(name)->Sumw2();

  outputKeys_.emplace_back(name);
}

void AnalysisDriverBase::addTH1D(const std::string& name, const std::vector<float>& binEdges) {
  if (hasTH1D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH1D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH2D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH2D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH3D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "TH3D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (binEdges.size() < 2) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH1D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of bin-edges has invalid size (" << binEdges.size() << " < 2)";
    throw std::runtime_error(oss.str());
  }

  mapTH1D_.insert(std::make_pair(
      name, std::unique_ptr<TH1D>(new TH1D(name.c_str(), name.c_str(), binEdges.size() - 1, &binEdges[0]))));
  mapTH1D_.at(name)->SetDirectory(nullptr);
  mapTH1D_.at(name)->Sumw2();

  outputKeys_.emplace_back(name);
}

void AnalysisDriverBase::addTH2D(const std::string& name,
                                 const std::vector<float>& binEdgesX,
                                 const std::vector<float>& binEdgesY) {
  if (hasTH1D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH2D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH1D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH2D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH2D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH2D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH3D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH2D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH3D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (binEdgesX.size() < 2) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH2D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of X-axis bin-edges has invalid size (" << binEdgesX.size() << " < 2)";
    throw std::runtime_error(oss.str());
  } else if (binEdgesY.size() < 2) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH2D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of Y-axis bin-edges has invalid size (" << binEdgesY.size() << " < 2)";
    throw std::runtime_error(oss.str());
  }

  mapTH2D_.insert(std::make_pair(
      name,
      std::unique_ptr<TH2D>(new TH2D(
          name.c_str(), name.c_str(), binEdgesX.size() - 1, &binEdgesX[0], binEdgesY.size() - 1, &binEdgesY[0]))));
  mapTH2D_.at(name)->SetDirectory(nullptr);
  mapTH2D_.at(name)->Sumw2();

  outputKeys_.emplace_back(name);
}

void AnalysisDriverBase::addTH3D(const std::string& name,
                                 const std::vector<float>& binEdgesX,
                                 const std::vector<float>& binEdgesY,
                                 const std::vector<float>& binEdgesZ) {
  if (hasTH1D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH3D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH1D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH2D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH3D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH2D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (hasTH3D(name)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH3D(\"" << name << "\", const std::vector<float>&, const std::vector<float>&) -- "
        << "TH3D object associated to key \"" << name << "\" already exists";
    throw std::runtime_error(oss.str());
  } else if (binEdgesX.size() < 2) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH3D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of X-axis bin-edges has invalid size (" << binEdgesX.size() << " < 2)";
    throw std::runtime_error(oss.str());
  } else if (binEdgesY.size() < 2) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH3D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of Y-axis bin-edges has invalid size (" << binEdgesY.size() << " < 2)";
    throw std::runtime_error(oss.str());
  } else if (binEdgesZ.size() < 2) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::addTH3D(\"" << name << "\", const std::vector<float>&) -- "
        << "std::vector of Z-axis bin-edges has invalid size (" << binEdgesY.size() << " < 2)";
    throw std::runtime_error(oss.str());
  }

  mapTH3D_.insert(std::make_pair(name,
                                 std::unique_ptr<TH3D>(new TH3D(name.c_str(),
                                                                name.c_str(),
                                                                binEdgesX.size() - 1,
                                                                &binEdgesX[0],
                                                                binEdgesY.size() - 1,
                                                                &binEdgesY[0],
                                                                binEdgesZ.size() - 1,
                                                                &binEdgesZ[0]))));
  mapTH3D_.at(name)->SetDirectory(nullptr);
  mapTH3D_.at(name)->Sumw2();

  outputKeys_.emplace_back(name);
}

TH1D* AnalysisDriverBase::H1(const std::string& key) {
  if (not hasTH1D(key)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::H1(\"" << key << "\") -- no TH1D associated to key \"" << key << "\"";
    throw std::runtime_error(oss.str());
  } else if (not mapTH1D_.at(key).get()) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::H1(\"" << key << "\") -- null pointer to TH1D associated to key \"" << key << "\"";
    throw std::runtime_error(oss.str());
  }

  return mapTH1D_.at(key).get();
}

TH2D* AnalysisDriverBase::H2(const std::string& key) {
  if (not hasTH2D(key)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::H2(\"" << key << "\") -- no TH2D associated to key \"" << key << "\"";
    throw std::runtime_error(oss.str());
  } else if (not mapTH2D_.at(key).get()) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::H2(\"" << key << "\") -- null pointer to TH2D associated to key \"" << key << "\"";
    throw std::runtime_error(oss.str());
  }

  return mapTH2D_.at(key).get();
}

TH3D* AnalysisDriverBase::H3(const std::string& key) {
  if (not hasTH3D(key)) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::H3(\"" << key << "\") -- no TH3D associated to key \"" << key << "\"";
    throw std::runtime_error(oss.str());
  } else if (not mapTH3D_.at(key).get()) {
    std::ostringstream oss;
    oss << "AnalysisDriverBase::H3(\"" << key << "\") -- null pointer to TH3D associated to key \"" << key << "\"";
    throw std::runtime_error(oss.str());
  }

  return mapTH3D_.at(key).get();
}
