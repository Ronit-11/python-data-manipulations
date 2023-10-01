import json
import logging
from pprint import pprint
import jsonlines
import pandas as pd

#works for extracted files
#print(englishjsonl['utt'])
#print(afjsonl['utt'])

#print(combined)


with jsonlines.open('jsonl_files/en-xx-train-filtered.jsonl','r') as jsonl_en:
    lst = [obj for obj in jsonl_en]
    #englishjsonl = pd.DataFrame(lst)
jsonl_en.close()
print(type(lst))
pprint(lst)
#read tar with gzip compression