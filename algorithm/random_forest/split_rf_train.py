import pandas as pd 
data = pd.read_csv('rf_train.csv')
idd = data['id']



index_need = []
for i in range(len(idd)):
    #print(len(user_id[i]))
    if type(idd[i]) != float:
        if len(idd[i]) == 16:
            index_need.append(i)
#print(index_need)
complete_user = data.loc[index_need]
data = complete_user



train_data = data.sample(frac=0.8, random_state = 0, axis=0)
test_data = data[~data.index.isin(train_data.index)]
train_data.to_csv("train_data_rf.csv",index=False)
test_data.to_csv("test_data_rf.csv",index=False)
