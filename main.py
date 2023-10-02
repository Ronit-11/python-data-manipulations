import json
import os
import jsonlines
import pandas as pd
import tarfile
import logging
from pprint import pprint


def extractingFilesFrom_tar_gz(filename):
    tarData = tarfile.open(filename,'r:gz')
    return tarData


def en_US_DfGenerator():
    enByteData = extractedTarfiles.extractfile(enCheck).read()#format : b'{"id": "2941", "locale": "en-US", ...}\n{"id": "2942", "locale": "en-US", ...}\n'
    enStrData = enByteData.decode('utf-8')# type string with '\n' removed and data after it goes into next line
    enListData = []
    # Parse each JSON line and convert to a list format
    for line in enStrData.strip().split('\n'): # split data based on next line
        tempData = json.loads(line)
        enListData.append(tempData)
    enDframeData = pd.DataFrame(enListData)
    return enDframeData


def en_XX_fileGenerator():
    target_extension = '.jsonl'
    directoryCreater(pathToStoreFiles)
    createLogs('Files storage directory created successfully.')
    filecount = 0

    for member in extractedTarfiles.getmembers():
        if member.name.endswith(target_extension):
            if not member.isfile() or enCheck is member:
                continue

            tempDframe = tar_jsonlToDframe(member)
            langInitial = tempDframe['locale'][0][0:2]

            combinedDframe = pd.concat([enDataDframe['id'],enDataDframe['utt'],tempDframe['utt'],enDataDframe['annot_utt'],tempDframe['annot_utt']], axis=1)
            xlxsheaders = ['id'] + ['en-utt'] + [langInitial + '-utt'] + ['en-annot_utt'] + [langInitial + '-annot_utt']
            
            combinedDframe.to_excel(pathToStoreFiles+'/en-'+langInitial+'.xlsx', 'en-'+langInitial, header = xlxsheaders, startrow=0, index = False)
            createLogs("en-" + langInitial + ".xlsx generated succesfully.")
            filecount += 1
    createLogs(str(filecount) + ' en-xx.xlsx Files generated succesfully.')


def tar_jsonlToDframe(filename):
    ByteData = extractedTarfiles.extractfile(filename).read()#format : b'{"id": "2941", "locale": "en-US", ...}\n{"id": "2942", "locale": "en-US", ...}\n'
    StrData = ByteData.decode('utf-8')# type string with '\n' removed and data after it goes into next line
    ListData = []
    # Parse each JSON line and convert to a list format
    for line in StrData.strip().split('\n'): # split data based on next line
        tempData = json.loads(line)
        ListData.append(tempData)
    DframeData = pd.DataFrame(ListData)
    return DframeData


def createLogs(message):
    logger.info(message)


def directoryCreater(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

def ttdJSONLGenerator(jsonlExtractedFile):
    tempDframe = tar_jsonlToDframe(jsonlExtractedFile)
    langInitial = tempDframe['locale'][0]
    colNameToSort = 'partition'
    sortingParam = ["test", "train", "dev"]

    directoryCreater(jsonlstoragepath)

    for param in sortingParam:
        sortedDframe = tempDframe.loc[tempDframe[colNameToSort] == param]
        sortedDframe.to_json(jsonlstoragepath+'/' + langInitial + '-' + param + '.jsonl', orient='records', lines=True, index=False, force_ascii = False)
        createLogs(langInitial+'-' + param + '.jsonl file generated successfully.')

def uttGenerator():
    target_extension = '.jsonl'
    langInitial = enDataDframe['locale'][0]
    colNameToSort = 'partition'
    sortingParam = "train"

    filteredDframe = enDataDframe.loc[enDataDframe[colNameToSort] == sortingParam]
    uttDframe = pd.concat([filteredDframe['id'],filteredDframe['utt']], axis = 1)
    uttDframe.rename(columns = {'utt': langInitial +'-utt'}, inplace = True)
    
    for member in extractedTarfiles.getmembers():
        if member.name.endswith(target_extension):
            if not member.isfile() or enCheck is member:
                continue
            tempDframe = tar_jsonlToDframe(member)
            langInitial = tempDframe['locale'][0]
            filteredDframe = tempDframe.loc[tempDframe[colNameToSort] == sortingParam]
            uttDframe = pd.concat([uttDframe, filteredDframe['utt']], axis = 1)
            uttDframe.rename(columns = {'utt': langInitial +'-utt'}, inplace = True)

    directoryCreater(jsonlstoragepath)

    uttDframe.to_json(jsonlstoragepath+'/en-xx-' + sortingParam + '-filtered.json', orient='records', index=False, force_ascii = False)
    createLogs('en-xx-' + sortingParam + '-filtered.json file generated successfully.')

def preetyprintJsonl():
    with jsonlines.open('jsonl_files/en-xx-train-filtered.json','r') as jsonl_en:
        lst = [obj for obj in jsonl_en]
    jsonl_en.close()
    pprint(lst)

rarFileToExtract = "amazon-massive-dataset-1.1_CAT1.tar.gz"
en_xx_fileName = '1.1/data/en-US.jsonl'
#pathToStoreFiles = r'C:/Users/ronit/Desktop/Python/CAT1_CompGraphics/Gen_xlsx_files'
#logDir = r'C:/Users/ronit/Desktop/Python/CAT1_CompGraphics/Logs'
pathToStoreFiles = 'Gen_xlsx_files'
jsonlstoragepath = 'jsonl_files'
logDir = 'Logs'
directoryCreater(logDir)

logging.basicConfig(filename = "Logs/log.txt", filemode='a', format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG) 
logger = logging.getLogger()

extractedTarfiles = extractingFilesFrom_tar_gz(rarFileToExtract) #global variable
createLogs('Data from zip file extracted successfully.')
enCheck = extractedTarfiles.getmember(en_xx_fileName)
enDataDframe = en_US_DfGenerator()
#en_XX_fileGenerator()

deFileName = '1.1/data/de-DE.jsonl'
swFileName = '1.1/data/sw-KE.jsonl'
swFile = extractedTarfiles.getmember(swFileName)
deFile = extractedTarfiles.getmember(deFileName)
ttdJSONLGenerator(enCheck)
ttdJSONLGenerator(swFile)
ttdJSONLGenerator(deFile)

uttGenerator()
    
preetyprintJsonl()