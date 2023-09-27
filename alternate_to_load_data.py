import logging
import jsonlines
import pandas as pd

#works for extracted files
with jsonlines.open('1.1\data\en-US.jsonl','r') as jsonl_en:
    lst = [obj for obj in jsonl_en]
    englishjsonl = pd.DataFrame(lst)
jsonl_en.close()

with jsonlines.open('1.1\data\/am-ET.jsonl','r') as jsonl_af:
    lst2 = [obj for obj in jsonl_af]
    afjsonl = pd.DataFrame(lst2)

combined = pd.concat([englishjsonl['id'],englishjsonl['utt'],afjsonl['utt'],englishjsonl['annot_utt'],afjsonl['annot_utt']], axis=1)
#print(englishjsonl['utt'])
#print(afjsonl['utt'])

print(combined)


#read tar with gzip compression