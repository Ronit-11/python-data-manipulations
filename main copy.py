import json
import pandas as pd
import tarfile

def extractingFilesFrom_tar_gz(filename):
    tarData = tarfile.open(filename,'r:gz')
    return tarData

def en_US_DfGenerator():
    enByteData = extractedTarfiles.extractfile(enCheck).read()#format : b'{"id": "2941", "locale": "en-US", ...}\n{"id": "2942", "locale": "en-US", ...}\n'
    #print(enData)
    enStrData = enByteData.decode('utf-8')# type string with '\n' removed and data after it goes into next line
    #print(enStrData)
    enListData = []
    # Parse each JSON line and convert to a list format
    for line in enStrData.strip().split('\n'): # split data based on next line
        tempData = json.loads(line)
        enListData.append(tempData)
    # Step 3: Create a DataFrame from the list of dictionaries
    enDframeData = pd.DataFrame(enListData)
    #print(enDframeData)
    return enDframeData

def en_XX_fileGenerator():
    #global extractedTarfiles, enCheck, enDataDframe
    target_extension = '.jsonl'

    for member in extractedTarfiles.getmembers():
        if member.name.endswith(target_extension):
            if not member.isfile() or enCheck is member:
                continue

            tempDframe = tar_jsonlToDframe(member)
            combinedDframe = pd.concat([enDataDframe['id'],enDataDframe['utt'],tempDframe['utt'],enDataDframe['annot_utt'],tempDframe['annot_utt']], axis=1)
            print(combinedDframe)

            
            #cfile = extractedTarfiles.extractfile(member)
            #print(member)
            #cfile.close()
    extractedTarfiles.close()

def tar_jsonlToDframe(filename):
    ByteData = extractedTarfiles.extractfile(filename).read()#format : b'{"id": "2941", "locale": "en-US", ...}\n{"id": "2942", "locale": "en-US", ...}\n'
    #print(enData)
    StrData = ByteData.decode('utf-8')# type string with '\n' removed and data after it goes into next line
    #print(enStrData)
    ListData = []
    # Parse each JSON line and convert to a list format
    for line in StrData.strip().split('\n'): # split data based on next line
        tempData = json.loads(line)
        ListData.append(tempData)
    # Step 3: Create a DataFrame from the list of dictionaries
    DframeData = pd.DataFrame(ListData)
    #print(DframeData)
    return DframeData


rarFileToExtract = "amazon-massive-dataset-1.1_CAT1.tar.gz"
en_xx_fileName = '1.1/data/en-US.jsonl'
extractedTarfiles = extractingFilesFrom_tar_gz(rarFileToExtract) #global variable
enCheck = extractedTarfiles.getmember(en_xx_fileName)
enDataDframe = en_US_DfGenerator()
en_XX_fileGenerator()