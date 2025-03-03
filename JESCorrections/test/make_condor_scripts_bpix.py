import os
############# USER DEFINED ##################################################
# Directory with input files
input_directory = "/eos/user/t/tchatzis/JRA_NTuples_Winter24"

bpix_categories = ['noBPix','BPix','BPixPlus','BPixMinus']
flatPU_label = 'FlatPU0to80'
noPU_label = 'NoPU'

#############################################################################

# Loop over each input file
with open("sub_jecs_total_forBPix.htc", "w") as job_script:
    # Common parts in all jobs
    job_script.write("executable            = fitJESCs\n")
    job_script.write("getenv                = True\n")
    job_script.write("should_transfer_files = YES\n")
    job_script.write("when_to_transfer_output = ON_EXIT_OR_EVICT\n")
    job_script.write("output_destination =  %s\n"%(os.environ['CMSSW_BASE']+'/src/JMETriggerAnalysis/JESCorrections/test'))
    job_script.write("MY.XRDCP_CREATE_DIR = True\n")
    job_script.write("MY.WantOS = \"el8\"\n")
    

    for bpix_cat in bpix_categories:
        job_script.write("\n"*5)
        job_script.write(f"transfer_output_files = JESCs_2024_{bpix_cat}\n")
        jet_categories = ['ak4pfHLT','ak8pfHLT']
        if bpix_cat == 'noBPix':
            jet_categories = ['ak4pfHLT','ak8pfHLT','ak4caloHLT','ak8caloHLT']
        for jet_cat in jet_categories:
            job_script.write("\n"*5)
            job_script.write(f"arguments             =  -i_nopu {input_directory}/JRA_{noPU_label}{bpix_cat}.root -i_flatpu {input_directory}/JRA_{flatPU_label}{bpix_cat}.root -o JESCs_2024_{bpix_cat} -b -j {jet_cat} -n 1000000\n")
            job_script.write(f"output = htc_out_2024/{jet_cat}.out\n")
            job_script.write(f"error = htc_out_2024/{jet_cat}.err\n")
            job_script.write(f"log = htc_out_2024/{jet_cat}.log\n")
            job_script.write("+JobFlavour           = \"workday\"\n")
            job_script.write("queue\n")


