from sklearn import metrics
import pandas as pd
from sklearn.metrics import fbeta_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
import os
from sklearn.externals import joblib
import matplotlib.pyplot as plt
 
 
 
if  __name__ == '__main__':
    train_df = pd.read_csv('train_dataset_updated_rf.csv')
    train_df = train_df.drop('Unnamed: 0',axis=1)
    predict_df = pd.read_csv('predict_dataset_updated_rf.csv')
    predict_df = predict_df.drop('Unnamed: 0',axis=1)
 
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
    #result.columns=['uid','mid','forward_count','comment_count','like_count']
    #result.to_csv('result_rf.csv')

    # # 创建文件目录
    # dirs = 'testModel'
    # if not os.path.exists(dirs):
    #     os.makedirs(dirs)
        
    # # 保存模型


feature_list = ['avg_repost','avg_comment','avg_like','attention','activeness','workday','link','title','emoji','@','content_length']
importances = list(rf.feature_importances_) 

# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
 
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
 
# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]


x_values = list(range(len(importances)))
 
# Make a bar chart
plt.bar(x_values, importances, orientation = 'vertical')
 
# Tick labels for x axis
plt.xticks(x_values, feature_list, rotation='vertical')
 
# Axis labels and title
plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances')


#plt.savefig("emotions_pie_chart.jpg",dpi = 360)
#plt.show()
