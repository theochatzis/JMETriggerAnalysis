from JMETriggerAnalysis.NTuplizers.utils.common import *

# name of file
file_name = '/store/mc/Run3Summer22MiniAODv3/QCD_PT-15to7000_TuneCP5_13p6TeV_pythia8/MINIAODSIM/castor_124X_mcRun3_2022_realistic_v12-v2/50000/b72c6ff5-0480-46d7-be7c-f534057565a9.root'
# depth of level in parents 
parentLevel = 2

parentFiles= command_output_lines('dasgoclient --query "parent file='+file_name+'"')
parentFiles.remove('')

for iParent in range(parentLevel-1):
  newParentFiles = []
  for i_file in parentFiles:
    newParentFiles += command_output_lines('dasgoclient --query "parent file='+i_file+'"')
    newParentFiles.remove('')
  parentFiles = newParentFiles

# print results
[print(iFile) for iFile in parentFiles]
 
