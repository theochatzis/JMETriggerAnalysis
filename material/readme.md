### HLT Upgrade workshop
Link for 5th HLT Upgrade Workshop [here](https://indico.cern.ch/event/1087907/)

### UPSG Future LLP and Timing: First Workshop
Link for [here](https://indico.cern.ch/event/1068193/)

### EGamma group
Samples produced are located in `/eos/cms/store/group/phys_egamma/sobhatta/egamma_timing_studies/samples/`.
They include MINIAOD + [MTD-track info](https://cmssdt.cern.ch/lxr/source/RecoMTD/Configuration/python/RecoMTD_EventContent_cff.py#0012)
Computing electron track iso with [plugin](https://github.com/SohamBhattacharya/cmssw/blob/egamma_timing_studies_12_2_0/RecoEgamma/EgammaIsolationAlgos/plugins/EgammaElectronTkIsolationProducerNew.cc) and [config](https://github.com/SohamBhattacharya/cmssw/blob/egamma_timing_studies_12_2_0/EgammaTimingTools/MyTools/python/testElectronMVA_cfg_mod1.py#L182-L200), using the [ElectronTkIsolation.cc](https://github.com/SohamBhattacharya/cmssw/blob/egamma_timing_studies_12_2_0/RecoEgamma/EgammaIsolationAlgos/src/ElectronTkIsolation.cc#L46)

Samples:

Reco run with `CMSSW_12_2_0`:

`DYToLL_M-50_TuneCP5_14TeV-pythia8_Phase2HLTTDRWinter20DIGI-PU200_pilot2_110X_mcRun4_realistic_v3-v2_GEN-SIM-DIGI-RAW_2022-02-02_12-47-21`
`TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8_Phase2HLTTDRWinter20DIGI-PU200_110X_mcRun4_realistic_v3-v2_GEN-SIM-DIGI-RAW_2022-02-02_13-08-05`

Reco run with `CMSSW_12_2_0_pre1`:

`DYToLL_M-50_TuneCP5_14TeV-pythia8_Phase2HLTTDRWinter20DIGI-PU200_pilot2_110X_mcRun4_realistic_v3-v2_GEN-SIM-DIGI-RAW_2021-12-06_23-02-44`
`QCD_Pt-15to3000_TuneCP5_Flat_14TeV-pythia8_Phase2HLTTDRWinter20DIGI-PU200_castor_110X_mcRun4_realistic_v3-v2_GEN-SIM-DIGI-RAW_2021-12-06_23-04-36`



