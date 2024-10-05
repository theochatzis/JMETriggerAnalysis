#! /usr/bin/env python3

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

# This is the job name - change it to your liking.
job_name='compareCaloJets' 

# Make sure you use both MINIAOD and RAW in case you want to have the offline inputs as well.
primary_dataset='/Muon0/Run2024G-PromptReco-v1/MINIAOD'
secondary_dataset='/Muon0/Run2024G-v1/RAW'

# Options for reco argument
recoOptions=[
    'default',
    'caloTowers_thresholds'
]

# You can also add in case you want different db files for the JECs/PFHCs. If the key doesn't have a JEC defined here it will do nothing.
recoOptionsPFHCs={
    'caloTowers_thresholds':'PFCalibration.db'
}

recoOptionsJECs={
    'caloTowers_thresholds':'WCalo_Run3Winter24Digi.db'
}

# Note : check bellow outLFNDirBase such that you have a working directory 
# default is to output in personal EOS space /store/user/[your_lxplus_user_name]/2024_JRA_NTuples/

# common part in all submissions
input_file_dir = os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/NTuplizers/test/' 

config = config()

config.section_('General')
config.General.transferOutputs = True
config.General.transferLogs = False
config.General.workArea = job_name

config.section_('JobType')
config.JobType.pluginName  = 'Analysis'
config.JobType.psetName = input_file_dir+'jmeTriggerNTuple2023Data_cfg.py'

config.JobType.maxMemoryMB = 2500
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.splitting = 'FileBased' #'Automatic'
config.Data.unitsPerJob = 1 #200
config.Data.totalUnits = 1000

config.section_('Site')
config.Site.storageSite = 'T3_CH_CERNBOX'
config.section_('User')

from CRABAPI.RawCommand import crabCommand

from multiprocessing import Process

def submit(config):
    crabCommand('submit', config = config)

## loop over bpix cases and samples 
for reco in recoOptions:
    config.JobType.pyCfgParams = ['reco='+reco]
    
    output_requestName = job_name+'_'+getOutputName(input_dataset.split('/')[2])+reco
    config.General.requestName = output_requestName
    config.Data.outLFNDirBase = '/store/user/%s/%s/%s'%(getUsername(),job_name,output_requestName)
    config.Data.inputDataset = primary_dataset
    config.Data.secondaryInputDataset = secondary_dataset
    ## adding needed input files for calibrations and corresponding command arguments per job
    config.JobType.inputFiles = []
    if reco in recoOptionsPFHCs.keys():
        config.JobType.inputFiles.append(input_file_dir + recoOptionsPFHCs[reco])
        config.JobType.pyCfgParams.append('pfhcDBfile='+recoOptionsPFHCs[reco])
    if reco in recoOptionsJECs.keys() :
        config.JobType.inputFiles.append(input_file_dir + recoOptionsJECs[reco])
        config.JobType.pyCfgParams.append('jecDBfile='+recoOptionsJECs[reco])
    
    # needed to be able to use pyCfgParams 
    p = Process(target=submit, args=(config,))
    p.start()
    p.join()

