import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import producers_by_type

def customise_SiPixelClusterProducerForRun2(process):
    for producer in producers_by_type(process, 'SiPixelClusterProducer'):
        producer.VCaltoElectronGain = 47
        producer.VCaltoElectronGain_L1 = 50
        producer.VCaltoElectronOffset = -60
        producer.VCaltoElectronOffset_L1 = -670

    return process
