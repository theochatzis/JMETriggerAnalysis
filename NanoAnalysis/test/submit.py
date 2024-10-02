import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", dest="dataset", action="store") 
parser.add_argument("-o", "--outputdir", dest="outputdir", action="store") 
args = parser.parse_args()

def Make_CondorScr(outname) :
    os.system("mkdir -p Scr/"+outname+"/log")
    condor_filename = "Scr/"+outname+"/condor.submit"
    lines =0
    with open("./input/"+outname+".out","r") as fp :
        lines = len(fp.readlines())
    f = open(condor_filename,"w")
    f.write('# Unix submit description file\n')
    f.write('Universe = vanilla\n')
    f.write('transfer_input_files = /afs/cern.ch/user/y/yeo/tmp/x509up\n') 
    f.write('Executable = ./Scr/'+outname+'/test.sh\n')
    f.write('request_memory = 1000\n') 
    f.write('should_transfer_files   = Yes\n')
    f.write('arguments = $(ProcId)\n')
    f.write('output = ./Scr/'+outname+'/log/$(ProcId).out\n')
    f.write('error = ./Scr/'+outname+'/log/$(ProcId).err\n')
    f.write('log = ./Scr/'+outname+'/log/$(ProcId).log\n')
    f.write('+MaxRuntime = 36000\n')
    f.write('Queue '+str(lines)+'\n')
    f.close()
    subchMod = "condor_submit ./Scr/"+outname+"/condor.submit"
    os.system("pwd")
    os.system(subchMod)
    return 0

def Make_Scr(outname) :
    os.system("mkdir -p Scr/"+outname)
    scr_filename = "Scr/"+outname+"/test.sh"
    f = open(scr_filename,"w")
    f.write('#!/bin/bash\n')
    f.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n') 
    f.write('source /cvmfs/sft.cern.ch/lcg/views/LCG_106/x86_64-el9-gcc13-opt/setup.sh\n')
    f.write('export X509_USER_PROXY=/afs/cern.ch/user/y/yeo/tmp/x509up\n')
    f.write('voms-proxy-info -all\n')
    f.write('voms-proxy-info -all --file $1\n')
    #f.write('cd /afs/cern.ch/user/y/yeo/rdf/24.09.25\n') 
    pwd = os.getcwd()
    f.write('cd '+ pwd +'\n') 
    f.write('mkdir -p ./output/'+outname+'\n') 
    f.write('python3 Rdataframe.py -f ./input/'+outname+' -i $1 -o output/'+outname)
    f.close()


    return 0

def Make_input(dataset,outname) :
    os.system("mkdir -p input")
    os.system("dasgoclient -query=\"file dataset=" + dataset +" system=rucio\" > ./input/"+outname+".out")
    os.system("echo "+dataset+" > ./input/"+outname+"_dataset.txt");
    return 0

if __name__ == '__main__':
    outname = args.outputdir
    dataset = args.dataset
    if (os.path.isfile('./input/'+outname+'.out')) :
    
        print('plz check output name')
    else :
        Make_input(dataset,outname)
        Make_Scr(outname)
        Make_CondorScr(outname)

    #Make_input("/JetMET0/Run2024C-PromptReco-v1/NANOAOD",outname)
    #Make_Scr(outname)
    #Make_CondorScr(outname)
