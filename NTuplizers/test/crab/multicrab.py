#! /usr/bin/env python3

# Step1, create flat ntuple with crab
# Usage:   multicrab.py <pset> [options|
# Example: crab/multicrab.py jmeTriggerNTuple2023Data_miniAOD_cfg.py -i 2024F,2024G
# Example: crab/multicrab.py NanoAOD_JMETriggerSkim.py -i 2024 --list
# Datasamples defined in createCrabConfigFilesMiniAOD.py and createCrabConfigFilesNanoAOD.py

import os,sys,re
import datetime
from optparse import OptionParser
import importlib
import subprocess

from CRABAPI.RawCommand import crabCommand


def Execute(cmd):
    '''                                                                                                                                                  
    Executes a given command and return the output.                                                                                                      
    '''
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    stdin  = p.stdout
    stdout = p.stdout
    ret    = []
    for line in stdout:
        line = line.decode('utf-8')
        ret.append(line.replace("\n", ""))

    stdout.close()
    return ret

def GetDatasets(mdir):
    datasets = []
    cands = Execute("ls %s" %mdir)
    for cand in cands:
        datasetpath = os.path.join(mdir,cand)
        if os.path.exists(datasetpath) and os.path.isdir(datasetpath) and os.path.exists(os.path.join(datasetpath, "results")):
            datasets.append(datasetpath)
    return datasets

def GetRegularExpression(arg):
    if isinstance(arg, str):
        arg = [arg]
    return [re.compile(a) for a in arg]

def GetIncludeExcludeDatasets(datasets, opts):
    newDatasets  = {}

    # Exclude datasets                                                                                                                                   
    if opts.excludeTasks != None and opts.excludeTasks != 'None':
        exclude = GetRegularExpression(opts.excludeTasks)
        for samplename in datasets.keys():
            found = False
            for e_re in exclude:
                if e_re.search(samplename):
                    found = True
                    break
            if found:
                continue
            newDatasets[samplename] = datasets[samplename]
        return newDatasets

    # Include datasets                                                                                                                                   
    if opts.includeTasks != None and opts.includeTasks != 'None':
        include = GetRegularExpression(opts.includeTasks)
        for samplename in datasets.keys():
            found = False
            for i_re in include:
                if i_re.search(samplename):
                    found = True
                    break
            if found:
                newDatasets[samplename] = datasets[samplename]
        return newDatasets

    return datasets

def GetCMSSW():
    '''                                                                                                                                                  
    Get a command-line-friendly format of the CMSSW version currently use.                                                                               
    https://docs.python.org/2/howto/regex.html                                                                                                           
    '''

    # Get the current working directory                                                                                                                  
    pwd = os.getcwd()

    # Create a compiled regular expression object                                                                                                        
    cmssw_re = re.compile("/CMSSW_(?P<version>\S+?)/")

    # Scan through the string 'pwd' & look for any location where the compiled RE 'cmssw_re' matches                                                     
    match = cmssw_re.search(pwd)

    # Return the string matched by the RE. Convert to desirable format                                                                                   
    version = ""
    if match:
        version = match.group("version")
        version = version.replace("_","")
        version = version.replace("pre","p")
        version = version.replace("patch","p")
    return version

def isData(datasetname):
    data_re = re.compile("Run20\d\d\w")
    match = data_re.search(datasetname)
    if match:
        return True
    return False

def getsamples(args):
    returnsamples = {}
    if 'Nano' in args[0]:
        print("Samples in crab/createCrabConfigFilesNanoAOD.py")
        from createCrabConfigFilesNanoAOD import samples,samples_muons
    else:
        print("Samples in crab/createCrabConfigFilesMiniAOD.py")
        from createCrabConfigFilesMiniAOD import samples,samples_muons
    returnsamples.update(samples)
    returnsamples.update(samples_muons)    
    return returnsamples

def listdatasets(opts,args):
    samples = getsamples(args)
    samples = GetIncludeExcludeDatasets(samples, opts)
    for sample in samples.items():
        print(sample[0])

def create(opts,args):
    time = datetime.datetime.now().strftime("%Y%m%dT%H%M")
    version = GetCMSSW()

    isNano = False
    if 'Nano' in args[0]:
        isNano = True

    PSET = os.path.abspath(args[0])
    SKIMCONFIG = ""
    if isNano:
        PSET = 'PSet.py'
        SKIMCONFIG = os.path.abspath(args[0])

    #from createCrabConfigFilesMiniAOD import samples
    samples = getsamples(args)
    #print(samples)
    samples = GetIncludeExcludeDatasets(samples, opts)
    #print(samples)
    #sys.exit()
    run_re = re.compile("(?P<run>Run20\d\d)(?P<letter>\S)")
    runs = {}
    for sample, sample_attributes in samples.items():
        if not isData(sample):
            continue
        match = run_re.search(sample_attributes[0])
        if match:
            key = match.group("run")
            if not key in runs:
                runs[key] = []
            if match.group("letter") not in runs[key]:
                runs[key].append(match.group("letter"))

    s_runs = ''
    for i,run in enumerate(runs.keys()):
        s_runs += run
        for l in runs[run]:
            s_runs += l
        if i < len(runs)-1:
            s_runs += '_'

    STOREDIR = 'CoffTeaNTuples'+'_v'+version+'_'+s_runs+'_'+time
    if os.path.exists(opts.dirName):
        STOREDIR = opts.dirName
    else:
        if os.path.exists(STOREDIR):
            print("Storedir already exists, exiting..")
            sys.exit()
        else:
            os.mkdir(STOREDIR)
    
    for sample, sample_attributes in samples.items():
        name=sample

        isMuonData = "False"
        if "Muon" in name:
            isMuonData = "True"

        jecsName=sample_attributes[1]
        lumiJSON="/eos/user/c/cmsdqm/www/CAF/certification/" + sample_attributes[2]
        globalTag=sample_attributes[3]

        print("Creating file","crabConfig_"+name+".py")

        dIN = os.getcwd()
        while os.path.basename(dIN) != 'test':
            dIN = os.path.dirname(dIN)
        USER = os.environ["USER"]

        crab_cfg_file = os.path.join(STOREDIR,"crabConfig_"+name+".py")
        file = open(crab_cfg_file,"w")
        file.write("import sys\n")
        file.write("from CRABClient.UserUtilities import config\n")
        file.write("config = config()")
        file.write("\n")
        #  file.write("store_dir = \'%s\'\n"%(STOREDIR))
        #  file.write("sample_name = \'"+name+"\'\n")
        file.write("\n")
        file.write("input_file_dir = \'%s\'\n"%dIN)
        file.write("\n")
        file.write("config.section_(\'General\')\n")
        file.write("config.General.requestName = \'%s\'\n"%(name))
        file.write("config.General.workArea = \'%s\'\n"%(STOREDIR))
        file.write("config.General.transferOutputs = True\n")
        file.write("config.General.transferLogs = False\n")
        file.write("\n")
        file.write("config.section_(\'JobType\')\n")
        file.write("config.JobType.pluginName = \'Analysis\'\n")
        file.write("config.JobType.maxMemoryMB = 2500\n")
        file.write("config.JobType.psetName = \'%s\'\n"%(PSET))

        file.write("config.JobType.allowUndistributedCMSSW = True\n")
        if isNano:
                file.write("config.JobType.scriptExe = \'NanoAOD_crab_script.sh\'\n")
                file.write("config.JobType.inputFiles = [\'%s\', \'%s\']\n"%(SKIMCONFIG, os.path.join(dIN,PSET)))
        else:
            if (jecsName is not None) and (len(jecsName)>0):
                file.write("config.JobType.pyCfgParams = [\'offlineJecs="+jecsName+"\',\'globalTag="+globalTag+"\',\'isMuonData="+isMuonData+"\']\n")
                file.write("config.JobType.inputFiles = [\'%s\']\n"%(os.path.join(dIN,jecsName+".db")))
            else:
                file.write("config.JobType.pyCfgParams = [\'globalTag="+globalTag+"\',\'isMuonData="+isMuonData+"\']\n")

        #file.write("config.JobType.maxJobRuntimeMin = 2*1315\n")
        file.write("\n")
        file.write("config.section_(\'Data\')\n")
        file.write("config.Data.publication = False\n")
        file.write("config.Data.ignoreLocality = False\n")
        file.write("config.Data.inputDataset = \'%s\'\n"%(sample_attributes[0]))
        file.write("config.Data.splitting = \'Automatic\'\n")
        file.write("config.Data.unitsPerJob = 200\n")
        file.write("config.Data.totalUnits = -1\n")
        file.write("\n")
        file.write("config.Data.lumiMask = \'%s\'\n"%(os.path.join(dIN,lumiJSON)))
        file.write("config.Data.outLFNDirBase = \'/store/user/%s/%s/%s\'\n"%(USER,STOREDIR,name))
        file.write("\n")
        file.write("config.section_(\'Site\')\n")
        file.write("config.Site.storageSite = \'T3_CH_CERNBOX\'\n")
        file.close()

        cmd_submit = "crab submit " + crab_cfg_file
        os.system(cmd_submit)

        cmd_mv = "mv " + os.path.join(STOREDIR, "crab_" + name) + " " + os.path.join(STOREDIR, name)
        os.system(cmd_mv)


    print("Store dir",STOREDIR)

def prune(result):
    # From job id's like '3', '3-1', '3-2', '3-3', '3-4', if '3' exists, use it, if not, take only last entry
    pruned = {}
    jobs = sorted(result['jobs'].keys())
    cands = {}
    for job in jobs:
        if '-' in job:
            job0 = job[:job.find('-')]
            if job0 in jobs:
                continue

            if not job0 in cands.keys():
                cands[job0] = []
            cands[job0].append(job)
        else:
            pruned[job]=job
    #print("\ncheck prune",pruned)
    sortList = lambda x: (int(i[i.find('-')+1:]) for i in x)
    for key in cands.keys():
        jobs = cands[key]
        job1 = jobs[0]
        lastkey = job1[:job1.find('-')+1]+"%s"%(sorted(list(sortList(jobs)))[-1])
        #print("check lastkey",lastkey)
        pruned[job1[:job1.find('-')]] = lastkey
    #print("\ncheck prune2",pruned)

    ret_jobs = {}
    for key in pruned.keys():
        ret_jobs[key] = result['jobs'][pruned[key]]
    result['jobs'] = ret_jobs
    #print("\ncheck prune3",ret_jobs)
    return result

def status(opts,args):
    silent = False
    #if opts.resubmit:
    #    silent = True

    multicrabdir = os.getcwd()
    for arg in args:
        if os.path.exists(arg) and os.path.isdir(arg):
            multicrabdir = arg
            break
    taskdirs = GetDatasets(multicrabdir)
    reportDict = {}
    status_re = re.compile("\s+(?P<report>(?P<string>failed|finished|idle|transferring|running)\s+\S+\s+\(\s*(?P<value>\d+)/(?P<all>\d+)\s*\))")
    for taskdir in taskdirs:
        result = Execute("crab status %s"%taskdir)
        if not silent:
            for line in result:
                print(line)
        taskname = taskdir.split("/")[-1]
        if taskname not in reportDict.keys():
            reportDict[taskname] = {}
        b_failed = False
        for r in result:
            match = status_re.search(r)
            if match:
                if not "all" in reportDict[taskname].keys():
                    reportDict[taskname]["all"] = match.group("all")
                reportDict[taskname][match.group("string")] = match.group("value")
                if match.group("string") == "failed" and int(match.group("value"))>0:
                    b_failed = True

        if opts.resubmit and b_failed:
            resubmit(taskdir)

        if not silent:
            print("\033[1mDataset                  submitted     idle  running   failed transfr. finished\033[0m")
        for taskname in reportDict.keys():
            submitted     = '0'
            idle          = '0'
            running       = '0'
            failed        = '0'
            finished      = '0'
            transferring  = '0'
            if "all" in reportDict[taskname].keys():
                submitted = reportDict[taskname]["all"]
            if "idle" in reportDict[taskname].keys():
                idle = reportDict[taskname]["idle"]
            if "running" in reportDict[taskname].keys():
                running = reportDict[taskname]["running"]
            if "failed" in reportDict[taskname].keys():
                failed = reportDict[taskname]["failed"]
            if "finished" in reportDict[taskname].keys():
                finished = reportDict[taskname]["finished"]
            if "transferring" in reportDict[taskname].keys():
                transferring = reportDict[taskname]["transferring"]
            hspace = 8
            while len(taskname) < 25:
                taskname += ' '
            while len(submitted) < hspace:
                submitted = ' '+submitted
            while len(idle) < hspace:
                idle = ' '+idle
            while len(running) < hspace:
                running = ' '+running
            while len(failed) < hspace:
                failed =' '+failed
            while len(transferring) < hspace:
                transferring =' '+transferring
            while len(finished) < hspace:
                finished =' '+finished
            if int(failed) > 0:
                failed = "\033[91m%s\033[0m"%failed
            if int(finished) > 0 and int(finished) == int(submitted):
                finished = "\033[32m%s\033[0m"%finished

            if not silent:
                print(taskname,submitted,idle,running,failed,transferring,finished)

    return reportDict

def resubmit(taskdir):
    print("RESUBMITTING",taskdir.split("/")[-1])
    crabCommand('resubmit', dir=taskdir)
    print("RESUBMITTED")
    """
    try:
        crabCommand('resubmit', dir=taskdir)
        print("RESUBMITTED")
    except:
        pass
    """

def proxy():
    result = Execute("voms-proxy-info")
    #print(result[0])
    #print(type(result))
    proxy_re = re.compile("Proxy not found")
    match = proxy_re.search(result[0])
    if match:
        print("Proxy not found, exiting..")
        sys.exit()

def main(opts,args):

    proxy()

    if opts.list:
        listdatasets(opts,args)
        sys.exit()

    if opts.status or opts.resubmit:
        status(opts,args)
    else:
        create(opts,args)

if __name__=="__main__":

    parser = OptionParser(usage="Step1: make flat ntuples with crab\n      %prog <pset> [-options]\n      %prog --status [<dir>]\n      %prog --resubmit [<dir>]")
    #parser.add_option("--create", dest="create", default=False, action="store_true",
    #                  help="Flag to create a CRAB job")
    parser.add_option("--status", dest="status", default=False, action="store_true",
                      help="Flag to check the status of CRAB jobs")
    parser.add_option("--resubmit", dest="resubmit", default=False, action="store_true",
                      help="Flag to resubmit CRAB jobs")
    parser.add_option("-i", "--include", dest="includeTasks", default="None", type="string",
                      help="Only perform action for this dataset(s) [default: \"\"]")
    parser.add_option("-e", "--exclude", dest="excludeTasks", default="None", type="string",
                      help="Exclude this dataset(s) from action [default: \"\"]")
    parser.add_option("-d", "--dir", dest="dirName", default="", type="string",
                      help="Use existing multicrab [default: \"\"]")
    parser.add_option("-l", "--list", dest="list", default=False, action="store_true",
                      help="List datasets and exit")

    (opts, args) = parser.parse_args()

    opts.includeTasks = opts.includeTasks.split(',')
    opts.excludeTasks = opts.excludeTasks.split(',')
    if 'None' in opts.includeTasks:
        opts.includeTasks = opts.includeTasks.remove('None')
    if 'None' in opts.excludeTasks:
        opts.excludeTasks = opts.excludeTasks.remove('None')

    #if len(args) == 0:
    #    parser.error("pset missing.")

    #if not opts.create and not opts.status and not opts.resubmit and not opts.list:
    #    parser.print_help()
    #    sys.exit()

    opts.silent = False

    main(opts,args)
