import pandas as pd
import numpy as np

predict_result = pd.read_csv('result_rf.csv')
ground_truth = pd.read_csv('predict_dataset_updated_rf.csv')
predict_zpz = predict_result[['转发数','评论数','点赞数']]
truth_zpz = ground_truth[['转发数','评论数','点赞数']]

pred = np.array(predict_zpz)
trut = np.array(truth_zpz)
error_rate = (trut - pred)/(trut+0.0001) ## MAPE
error_rate_for_one = np.mean(error_rate, axis=1) ##expected MAPE
acc = sum(error_rate_for_one<0.15) / len(error_rate_for_one)
print('The accuracy is:',acc)



