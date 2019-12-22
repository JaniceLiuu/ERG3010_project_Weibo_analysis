## to count the most frequent month a person use 

import pandas as pd
from snownlp import SnowNLP
from collections import Counter


def get_most_frequent_month(csv_file):
    user = pd.read_csv(csv_file)
    user_weibo = user[2:]
    user_weibo.columns = ['id','正文','日期','点赞数','评论数','转发数','话题']
    date = user_weibo['日期']
    month_list = []
    for d in date:
        month = d[5:7]
        month_list.append(month)
    count = Counter(month_list)
    most_common_month = count.most_common(1)
    return most_common_month



print(get_most_frequent_month('lironghao.csv'))