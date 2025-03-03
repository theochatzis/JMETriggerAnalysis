#!/usr/bin/env python
import json

from JMETriggerAnalysis.Common.configs.HLT_dev_CMSSW_11_2_0_GRun_V19_Data_NoOutput_configDump import cms, process

outputFile = 'triggersForPureRate.json'

triggersForPureRate = []
for streamName in process.streams.parameterNames_():
  if streamName.startswith('Physics'):
    for dsetName in getattr(process.streams, streamName):
      for trigName in getattr(process.datasets, dsetName):
        if trigName.startswith('HLT_'):
          triggersForPureRate.append(trigName)
triggersForPureRate = list(set(triggersForPureRate))

json.dump(sorted(triggersForPureRate), open(outputFile, 'w'), sort_keys=True, indent=2)
