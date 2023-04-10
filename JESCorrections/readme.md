This directory contains tools and instructions
to derive Jet Energy Scale Corrections
for the jets used in the High-Level Trigger (HLT).

#### Setup

Instructions to set up the CMSSW area to produce JRA NTuples, and derive JESCs:
```
scram project CMSSW_13_0_0
cd CMSSW_13_0_0/src
eval `scram runtime -sh`
git cms-merge-topic  silviodonato:customizeHLTfor2023

git clone https://github.com/cghuh/JetMETAnalysis.git -b hlt_run3
git clone https://github.com/cghuh/JMETriggerAnalysis.git -b run3_13_0_X
scram b -j 8
```

#### Produce JRA NTuples with HLT Jets

 * How to run the JRA step locally and with crab
 * Which samples to use, how to find them in DAS
 * What to do if a sample is not available at a Tier-2 (transfer request, Rucio rule)

#### Derive Jet Energy Scale Corrections from JRA NTuples

Once JRA NTuples have been produced,
JESCs can be derived from them by running
the executables of the `JetMETAnalysis` package.

An example of how to do this is given below:
```
cd ${CMSSW_BASE}/src/JMETriggerAnalysis/JESCorrections/test/
./fitJESCs -o output_tmp1 -n -1
```
The `fitJESCs` script is an example of
a wrapper executing the various steps of the JESCs derivation
(caveat: the script presently includes several hard-coded parameters).

List of Run-3 HLT JESCs:

  * `Run3Winter20_V2_MC`:

    - Description: preliminary HLT JESCs for Run-3 studies

    - Tag of `JMETriggerAnalysis`: `hltJESCs_Run3Winter20_V2_MC`

    - Tag of `missirol/JetMETAnalysis`: `Run3Winter20_V2_MC`

    - JRA NTuples:
      ```
      root://cms-xrd-global.cern.ch//eos/cms/store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/npv_fix_noPU/npvFix_noPU.root
      root://cms-xrd-global.cern.ch//eos/cms/store/group/phys_jetmet/saparede/runIII_hlt_jec/jra_ntuples/npv_fix_flatPU/npvFix_flatPU.root
      ```

    - executable for JESCs fits (contains settings of all JESCs fits):
      [`JESCorrections/test/fitJESCs`](https://github.com/missirol/JMETriggerAnalysis/blob/hltJESCs_Run3Winter20_V2_MC/JESCorrections/test/fitJESCs)

    - Notes:

      - JRA NTuples affected by a bug in the `rho` value saved for Calo and PFCluster (AK4 and AK8) HLT jets:
        the `rho` based on PF-candidates was erronously used,
        instead of the `rho` values calculated from calo-towers and PFClusters, respectively.
