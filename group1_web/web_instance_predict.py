import pandas as pd
import calendar
from sklearn import metrics
import pandas as pd
from sklearn.metrics import fbeta_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
from sklearn.externals import joblib

 
def get_Dict(data): 
    dict = {}
    total_zpz = [0,0,0,0]    # 该用户的微博条数 总转发 总评论 总赞数
    for index,item in data.iterrows():
        total_zpz[0] = total_zpz[0] + 1
        total_zpz[1] = total_zpz[1] + int(item['转发数'])
        total_zpz[2] = total_zpz[2]+int(item['评论数'])
        total_zpz[3] = total_zpz[3]+int(item['点赞数'])
    print("Dict:userID-该用户的微博条数——总转发——总评论——总赞数,准备完毕！")
    print(total_zpz)
    dict[0] = total_zpz
    print(dict)
    return dict


#get_Dict(complete_new_user_info)


 
def build_feature(data,dict):

    def get_Length(strr):
        strr=str(strr)
        return len(strr)

    def getMonthdays(yeartemp):  #返回xxxx年的所有的工作日，不考虑节假日，只按照周末计算
        work_day_list = []
        c = calendar.TextCalendar()
        for ii in range(1, 13):
            message = ""
            message = message + str(ii) + "=["
            for week in c.monthdayscalendar(yeartemp, ii):
                for i in range(0, 5):
                    if week[i] != 0:
                        message = message + str(week[i])
                        date = ii * 100 + (week[i])
                        work_day_list.append(date)
        return (work_day_list)

    def whe_work_day(str, list_work_day):
        whe_work_day = 0
        set_work_day = set(list_work_day)
        date = str.strip().split()[0].split('-')  # 2016-12-21
        date = date[1] * 100 + date[2]
        if date in set_work_day: whe_work_day = 1
        return whe_work_day

    def get_average_ZPZ(dict, data):
        avg_zhuan = dict[0][1] / dict[0][0]
        avg_ping = dict[0][2] / dict[0][0]
        avg_zan = dict[0][3] / dict[0][0]
        cache = dict[0]
        guanzhudu = dict[0][1] + dict[0][2] + dict[0][3]
        huoyuedu = dict[0][0]


        new_feature_one = ['以往平均转发', '以往平均评论数', '以往平均赞数','关注度','活跃度']
        for item in new_feature_one:
            data[item] = 0
        data['Cache']= 0
        #data.loc[:,['Cache']]= cache 
        data.loc[:,['以往平均转发']]= avg_zhuan
        data.loc[:, ['以往平均评论数']] = avg_ping
        data.loc[:, ['以往平均赞数']] = avg_zan
        data.loc[:, ['关注度']] = guanzhudu
        data.loc[:, ['活跃度']] = huoyuedu
        return data

    def whe_link(strr):
        strr=str(strr)
        k=0
        if 'http:' in  strr:k=1
        return k

    def whe_title(strr):
        strr = str(strr)
        k=0
        for item in '[#【《](.*?)[#】》]':
            if item in strr:
                k=1
                break
        return k

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

    def whe_art(strr):
        strr = str(strr)
        k=0
        if '@'in strr: k=1
        return k

    print("开始建立特征！")
    data=get_average_ZPZ(dict,data)
    all_work_day_list=getMonthdays(2015)
    list_holiday = [101, 102, 103, 218, 219, 220, 221, 222, 223, 404, 405, 406, 501, 502, 503, 620, 621, 622, 926,
                    927, 928, 1001, 1002, 1003,1004, 1005, 1006, 1007]
    all_work_day_list = list(set(all_work_day_list) - set(list_holiday))
    #new_feature_two = ['是否工作日', '是否是工作点']
    data['是否工作日'] = 0
    #for item in new_feature_two:
    #    data[item] = 0
    data['是否工作日'] = data['日期'].map(lambda x: whe_work_day(x,all_work_day_list))
    #data['是否是工作点'] = data['发送时间'].map(lambda x: whe_worktime(x))
    new_feature_three=['是否有链接','是否有标题','是否有表情','是否有@','文本长度']
    for item in new_feature_three:
        data[item]=0
    data.loc[:,['是否有链接'] ] = data['正文'].map(lambda x:whe_link(x))
    data.loc[:,['是否有标题'] ] = data['正文'].map(lambda x: whe_title(x))
    data.loc[:,['是否有表情'] ] = data['正文'].map(lambda x: whe_emoji(x))
    data.loc[:,['是否有@'] ]   = data['正文'].map(lambda x: whe_art(x))
    data.loc[:,['文本长度'] ]   = data['正文'].map(lambda x :get_Length(x))
    print(data)
    return data


#dict = get_Dict(complete_new_user_info)

#predict_data = build_feature(pred_sentence,dict)





if  __name__ == '__main__':
    train_df = pd.read_csv('train_dataset_updated_rf.csv')
    train_df = train_df.drop('Unnamed: 0',axis=1)
    predict_df = predict_data
    #predict_df = predict_df.drop('Unnamed: 0',axis=1)
 
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
        print(predict_df[target[i]])
 
 
    result=predict_df.loc[:,['id', 'userid','转发数','评论数','点赞数']]
    result.columns=['uid','mid','forward_count','comment_count','like_count']
    print(predict_df)
    print(result)
