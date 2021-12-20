This directory contains tools and instructions
to derive the PF-Hadron calibrations (PFHCs)
used in the High-Level Trigger (HLT).

#### Introduction

 * General description of the calibration methods,
   incl. references to the relevant documentation
   (publications, analysis notes, presentations, webpages)

#### Setup

Instructions to set up the local CMSSW area:
```
scram project CMSSW_12_0_0_pre4
cd CMSSW_12_0_0_pre4/src
eval `scram runtime -sh`
git cms-merge-topic missirol:devel_hltRun3TRK_1200pre4

git clone https://github.com/missirol/JMETriggerAnalysis.git -o missirol -b run3
scram b -j 8
```

#### Production of NTuples for PFHCs

The first step to derive PFHCs is to create an NTuple with the relevant information for the calibration procedure.

PFHCs are derived using MC events simulating
the production of a single-pion without pileup (NoPU),
with the generated pion $p_{T}$ usually restricted to values below 200 GeV.

!! Add more details on how to find the relevant sample in DAS (e.g. look for `/*SinglePion*0*200*/*NoPU*/*RAW*`).

!! Add information on what to do if a sample is not available at a Tier-2 (transfer request, Rucio rule)

The first step in the calibration procedure is to create a flat ROOT NTuple
containing information on selected HLT PF-Candidates,
and the `PFSimParticle` candidates (truth-level information) associated to them.

!! Add more details on how HLT PF-Candidates are selected, and matched to `PFSimParticle` candidates.

To test the first step of the workflow, a small test NTuple can be produced locally as follows:
```
cmsRun ${CMSSW_BASE}/src/JMETriggerAnalysis/PFHadronCalibration/test/pfHadCalibNTuple_cfg.py maxEvents=1000
```

which contains information

!! Add information on how to run the NTuple step with crab, HTCondor and/or other batch systems

#### Derivation of PFHCs

 * Given a set of input PFHC NTuples, how to analyse them to derive the PFHC functions
 * How to produce final `.db` file containing the PFHCs

#### Validation of PFHCs

 * Given a set of PFHCs (i.e. a `.db` file containing the relevant records),
   how to validate this output, and verify that the corrections work as expected

#### Delivery of PFHCs

 * How to upload the relevant records to the appropriate database
 * How to integrate new PFHCs in a Global-Tag (GT)

#### Available sets of PFHCs

List of the available PFHCs for HLT,
with the necessary metadata to be able to reproduce them if needed.
This should include:
 * `git` tag corresponding to the version of `JMETriggerAnalysis` used for the calibrations
 * name of the CMSSW release used
 * names of the datasets in DAS used for the calibrations
 * link to the `cmsRun` configuration file used to create the PFHC-NTuples,
 * links to the PFHC-NTuples used for the calibrations (if still available)
 * link to the relevant analysis scripts to derive and validate the calibrations
 * any further instructions specific to a certain PFHC version (if necessary)
