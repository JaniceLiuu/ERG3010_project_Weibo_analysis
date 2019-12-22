import pandas as pd
from snownlp import SnowNLP
import jieba
import jieba.posseg as pseg
import csv

#len(d.index)
d = pd.read_csv("all_users_complete.csv",usecols = ['text'])
per = []
for i in range(len(d.index)):
    count = 0
    output = list(pseg.cut(str(d.loc[i])))
    length = 0
    for word, label in output:
        if label not in ['eng','x']:
            length = length + 1
        if label in ['a','ad']:
            count = count + 1
    score = round((count/length),4)   
    per.append(score)
    print(score)

test = pd.DataFrame(columns = ['per'], data=per)
test.to_csv('percentage.csv')


