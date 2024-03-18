from CRABClient.UserUtilities import config, getUsername
import os
import re

def getOutputName(input_dataset):
    # regular expression to get the wanted pattern
    
    # Regular expression pattern to match the desired substring
    pattern = r'-([A-Za-z0-9]+)_'

    # Search for the pattern in the input string
    match = re.search(pattern, input_dataset)

    # Extract the matched substring
    if match:
        extracted_string = match.group(1)
        print('dataset output name = %s'%(extracted_string))
        return extracted_string
    else:
        print("Substring not found in the input string.")

dataset_flatPU='/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter24Digi-FlatPU0to80_133X_mcRun3_2024_realistic_v9_ext1-v2/GEN-SIM-RAW'
dataset_noPU='/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/Run3Winter24Digi-NoPU_133X_mcRun3_2024_realistic_v9_ext1-v2/GEN-SIM-RAW'

# Note : check bellow outLFNDirBase such that you have a working directory 
# default is to output in personal EOS space /store/user/[your_lxplus_user_name]/2024_JRA_NTuples/

# common part in all submissions
input_file_dir = os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/JESCorrections/test/' 

config = config()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = False
config.General.workArea = 'bpix_crab_dir'

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = input_file_dir+'jescJRA_cfg.py'

config.JobType.inputFiles = [input_file_dir + 'PFCalibration.db']
config.JobType.maxMemoryMB = 2500
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'FileBased' #'Automatic'
config.Data.unitsPerJob = 1 #200
config.Data.totalUnits = -1

config.section_('Site')
config.Site.storageSite = 'T3_CH_CERNBOX'
config.section_('User')

from CRABAPI.RawCommand import crabCommand

from multiprocessing import Process

def submit(config):
    crabCommand('submit', config = config)

## loop over bpix cases and samples 
for bpixMode in ['noBPix','BPix','BPixPlus', 'BPixMinus']:
    config.JobType.pyCfgParams = ['bpixMode='+bpixMode]
    for input_dataset in [dataset_flatPU, dataset_noPU]:
        output_requestName = 'JRA_'+getOutputName(input_dataset.split('/')[2])+bpixMode
        config.General.requestName = output_requestName
        config.Data.outLFNDirBase = '/store/user/%s/JRA_NTuples_Winter24/%s'%(getUsername(),output_requestName)
        config.Data.inputDataset = input_dataset
        
        # needed to be able to use pyCfgParams 
        p = Process(target=submit, args=(config,))
        p.start()
        p.join()

