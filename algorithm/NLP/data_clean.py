import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt

user = pd.read_csv('all_users.csv')
user_weibo = user
user_weibo.columns = ['id','正文','日期','点赞数','评论数','转发数','话题']
user_id = user_weibo['id']
contents = user_weibo['正文']

def data_clean():
    global user_id, user_weibo
    index_need = []
    for i in range(len(user_id)):
        #print(len(user_id[i]))
        if len(user_id[i]) == 16:
            index_need.append(i)
    #print(index_need)
    complete_user = user_weibo.loc[index_need]
    return complete_user


complete_user_weibo = data_clean()
complete_user_weibo.to_csv('all_users_complete.csv')

