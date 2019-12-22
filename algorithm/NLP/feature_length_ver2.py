import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt


user = pd.read_csv('all_users_complete_1_ver2.csv')
contents = user['正文']
user['content_length'] = ''


def count_length():
    global user
    for i in range(len(user)):
        comment = user['正文'][i]
        if comment != '' and type(comment) == str:
            leng = len(comment)
            user.loc[i,'content_length'] = leng
        else:
            pass


count_length()
user.to_csv('all_users_complete_2_ver2.csv')
        