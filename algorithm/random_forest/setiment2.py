##Reference
##版权声明：本文为CSDN博主「猪蒙索洛夫」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
##原文链接：https://blog.csdn.net/weixin_40523230/article/details/80473084

import pandas as pd
import calendar
 
 
class feature_extraction(object):
    def read_train_Data(self,filepath):
        data=pd.read_csv(filepath)
        data['Cache']=0
        data.loc[:,['Cache']]=data['userid']
        data=data.set_index('id')
        return data
 
    def read_predict_data(self,filepath):
        data = pd.read_csv(filepath)
        data = data[['userid', 'id', '日期','正文']]
        data = data.set_index('id')
        return data
 
    def get_Dict(self,data):
        User_Id_Set=set(list(data['userid']))  
        Dict={}
        for item in list(User_Id_Set):
            Dict[item]=[0,0,0,0]   # 该用户的微博条数 总转发 总评论 总赞数
        for index,item in data.iterrows():
            if item['userid'] in User_Id_Set:
                user_list=Dict[item['userid']]
                user_list[0] = user_list[0]+1
                user_list[1] = user_list[1]+int(item['转发数'])
                user_list[2] = user_list[2]+int(item['评论数'])
                user_list[3] = user_list[3]+int(item['点赞数'])
        print("Dict:userID-该用户的微博条数——总转发——总评论——总赞数,准备完毕！")
        return Dict
 
    def build_feature(self,data,dict):
 
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
 
        # def whe_worktime(str):
        #     whe_work_time = 0
        #     time = int(str.strip().split()[1].split(':')[0])  # 10:22:56
        #     if (time >= 8 & time <= 12) or (time >= 14 & time <= 18): whe_work_time = 1
        #     return whe_work_time
 
        def get_average_ZPZ(dict, data):
            def fill_with_cache(dict,x):
                if  x in dict:
                    list=dict[x]
                    st=str(list[0])+" "+str(list[1])+" "+str(list[2])+" "+str(list[3])
                else:
                    st="0 0 0 0"
                return st
            def get_zhuanfa(x):
                if int(int(x.strip().split()[0]))!=0:
                    num   = int(x.strip().split()[0])
                    zhuanfa= int(x.strip().split()[1])
                    return zhuanfa/(num*1.0)
                else:
                    return 0
            def get_pinglun(x):
                if int(x.strip().split()[0])!=0:
                    num   = int(x.strip().split()[0])
                    pinglun= int(x.strip().split()[2])
                    return pinglun/( num*1.0)
                else:
                    return 0
            def get_zan(x):
                if int(x.strip().split()[0])!=0:
                    num = int(x.strip().split()[0])
                    zan = int(x.strip().split()[3])
                    return zan / (num * 1.0)
                else:
                    return 0
            def get_guanzhudu(x):
                if int(x.strip().split()[0])!=0:
                    guanzhudu=int(x.strip().split()[3])+int(x.strip().split()[2])+int(x.strip().split()[1])
                    return guanzhudu
                else:
                    return 0
            def get_huoyuedu(x):
                if int(x.strip().split()[0])!=0:
                    huoyuedu=int(x.strip().split()[0])
                else:
                    huoyuedu=0
                return huoyuedu
            new_feature_one = ['以往平均转发', '以往平均评论数', '以往平均赞数','关注度','活跃度']
            for item in new_feature_one:
                data[item] = 0
            data['Cache']=0
            data.loc[:,['Cache']]=data['userid'].map(lambda x:fill_with_cache(dict,x))
            data.loc[:,['以往平均转发']]=data['Cache'].map(lambda x:get_zhuanfa(x))
            data.loc[:, ['以往平均评论数']] = data['Cache'].map(lambda x: get_pinglun(x))
            data.loc[:, ['以往平均赞数']] = data['Cache'].map(lambda x: get_zan(x))
            data.loc[:, ['关注度']] = data['Cache'].map(lambda x: get_guanzhudu(x))
            data.loc[:, ['活跃度']] = data['Cache'].map(lambda x: get_huoyuedu(x))
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
        return data
 
 
if __name__=='__main__':
    fe=feature_extraction()
    train_data = fe.read_train_Data('train_data_rf.csv')
    predict_data = fe.read_train_Data('test_data_rf.csv')
    #train_data=fe.read_train_Data('weibo_train_data.txt')
    #predict_data=fe.read_predict_data('weibo_predict_data.txt')
    dict=fe.get_Dict(train_data)
    #print(dict)
    train_data_updated=fe.build_feature(train_data,dict)
    predict_data=fe.build_feature(predict_data,dict)
    # dict_dataframe=pd.DataFrame(dict).T
    # dict_dataframe.columns=['总数量','总转发','总评论','总赞']
    # dict_dataframe.to_csv('dict_pandas.csv')
 
    train_data.to_csv('train_dataset_updated_rf.csv')
    predict_data.to_csv('predict_dataset_updated_rf.csv')