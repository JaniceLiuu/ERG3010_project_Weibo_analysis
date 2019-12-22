from flask import Flask, Response, request, jsonify, redirect, url_for, render_template
from os import path
import db_func 
import numpy as np
import web_instance_predict
import pandas as pd
import time
import calendar
import random
from sklearn import metrics
from sklearn.metrics import fbeta_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
from sklearn.externals import joblib

vv2 = 0

app = Flask(__name__,static_url_path = "", static_folder="static")
@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/')
def index():
    return app.send_static_file("index.html")



@app.route('/page3',methods=['GET','POST'])
def show1():
    global v
    global vv2
    
    conn, tunnel = db_func.create_db_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("USE %s;"%(db_func.config['db']))
        sql_id = "select id from user_group1 where screen_name = '%s';"%(request.json['name'])
        cur.execute(sql_id)
        v = cur.fetchall()
        id = v[0]

        sql = """select text, attitudes_count, comments_count, reposts_count from weibo_group1 
        where user_id = '%s' and date_sub(curdate(),interval 60 day) <= created_at"""%(id)
        cur.execute(sql)
        vv = cur.fetchall()

        list1 = [vv[0][0], vv[0][1], vv[0][2], vv[0][3], vv[1][0], vv[1][1], vv[1][2], vv[1][3], vv[2][0], vv[2][1], vv[2][2], vv[2][3]]

        sql2 = "select * from weibo_group1 where user_id = '%s'"%(id)
        cur.execute(sql2)
        vv2 = cur.fetchall()

        conn.commit()

        conn.close()
        tunnel.close()

        return jsonify(list1)

@app.route('/page3_2',methods=['GET','POST'])
def show2():
    conn, tunnel = db_func.create_db_conn()
    cur = conn.cursor()
    new_user_info = pd.DataFrame(list(vv2))
    print(new_user_info[1]) ##这里要把tuple变成data frame
    idd = new_user_info[1]
    index_need = []
    for i in range(len(idd)):
        if type(idd[i]) != float:
            if len(idd[i]) == 16:
                index_need.append(i)
    new_user_info.columns = ['user_id','weibo_id','正文','日期','转发数','评论数','点赞数','话题']
    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())[:10] 
    complete_new_user_info = new_user_info.loc[index_need]
    test_dict = {'0':['aaa'],'userid':[111],'id':[111],'日期':['2019-03-22'],'正文':['要注意身体啊 心里已经很变态了 身体一定要健康啊 ']}
    test_dict['日期'] = [time1]
    test_dict['正文'] = [request.json['name']]
    pred_sentence = pd.DataFrame(test_dict)
    pred_sentence = pred_sentence[['userid', 'id', '日期','正文']]
    pred_sentence = pred_sentence.set_index('id')
    
    dict = web_instance_predict.get_Dict(complete_new_user_info)
    predict_data = web_instance_predict.build_feature(pred_sentence,dict)

    train_df = pd.read_csv('train_dataset_updated_rf.csv')
    train_df = train_df.drop('Unnamed: 0',axis=1)
    predict_df = predict_data
 
    target = [ '转发数', '评论数', '点赞数']
    dropped_train_dataset=['id', 'userid', '日期','转发数', '评论数', '点赞数', '正文', 'Cache']
    dropped_predict_datastet=['id', 'userid', '日期', '正文','Cache']
 
    predictors = [x for x in train_df.columns if x not in target+dropped_train_dataset]
 
    for item in target:
        predict_df[item]=0

    for i in range(len(target)):
        rf = RandomForestRegressor()  # 这里使用了默认的参数设置
        rf.fit(train_df[predictors], train_df[target[i]])  # 进行模型的训练
        predict_df_predictions = rf.predict(predict_df[predictors])
        predict_df_predictions = [int(item) for item in  predict_df_predictions]
        predict_df[target[i]]=predict_df_predictions
        #print(predict_df[target[i]])
 
 
    result=predict_df.loc[:,['id', 'userid','转发数','评论数','点赞数']]
    result.columns=['uid','mid','forward_count','comment_count','like_count']
    result_list = result.values.tolist()[0][2:5]

    for i in result_list:
        i = int(i)
    return jsonify(result_list)


# fist page select and show the short/long recommendation
@app.route('/page1_sent1',methods=['GET','POST'])
def recommend1():
    pima = pd.read_csv('examples.csv',header = 0)
    a = list(range(25))
    index = random.sample(a,3)

    lst = []
    for i in index:
        lst.append(pima['negative'][i])
    return jsonify(lst)

@app.route('/page1_sent2',methods=['GET','POST'])
def recommend2():
    pima = pd.read_csv('examples.csv',header = 0)
    a = list(range(25))
    index = random.sample(a,3)

    lst = []
    for i in index:
        lst.append(pima['positive'][i])
    return jsonify(lst)

if __name__ == '__main__':
    db_func.load_config(False)

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(threaded = True, debug = True)