import tarfile


rarFileToExtract = "amazon-massive-dataset-1.1_CAT1.tar.gz"
tar = tarfile.open(rarFileToExtract,'r:gz')

en_xx_fileName = '1.1/data/en-US.jsonl'
enCheck = tar.getmember(en_xx_fileName)


target_extension = '.jsonl'
for member in tar.getmembers():
    if member.name.endswith(target_extension):
        if not member.isfile() or enCheck is member:
            continue
        cfile = tar.extractfile(member)
        print(member)
        cfile.close()
tar.close()
