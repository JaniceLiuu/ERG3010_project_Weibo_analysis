import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt


#user = pd.read_csv('all_users_complete.csv')
user = pd.read_csv('linshuhao.csv')
contents = user['正文']
user['sentiment_score'] = ''


user['sentiment_score'][0]

def seti_col():
    global user
    for i in range(len(user)):
        comment = user['正文'][i]
        if comment != '' and type(comment) == str:
            s = SnowNLP(comment)
            rates = s.sentiments
            user.loc[i,'sentiment_score'] = rates 
        else:
            pass
 
seti_col()
print(user['sentiment_score'])

#user.to_csv('all_users_complete_1_ver2.csv')