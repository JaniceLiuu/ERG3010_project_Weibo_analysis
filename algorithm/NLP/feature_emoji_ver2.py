import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt


user = pd.read_csv('all_users_complete_2_ver2.csv')
contents = user['正文']
user['emoji'] = ''


def whe_emoji(strr):
    strr = str(strr)
    def isEmoji(content):
        if not content:
            return False
        if u"\U0001F600" <= content and content <= u"\U0001F64F":
            return True
        elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
            return True
        elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
            return True
        elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
            return True
        else:
            return False
    k=0
    for item in strr:
        if isEmoji(item):
            k=1
        if k==1:break
    return k


def count_length():
    global user
    for i in range(len(user)):
        comment = user['正文'][i]
        if comment != '' and type(comment) == str:
            judge_emoji = whe_emoji(comment)
            user.loc[i,'emoji'] = judge_emoji 
        else:
            pass


count_length()
user.to_csv('all_users_complete_3_ver2.csv')