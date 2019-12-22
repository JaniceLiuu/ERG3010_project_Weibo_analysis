import jieba
import pandas as pd

user = pd.read_csv('all_users_complete_3_ver2.csv')
contents = user['正文'].astype('str')

contents_list = list(contents)
tokenized_list = []
for text in contents_list:
    text_tokenize = list(jieba.cut(text))
    tokenized_list.append(text_tokenize)

tokenized_list_all = []
for i in range(len(tokenized_list)):
    for j in range(len(tokenized_list[i])):
        tokenized_list_all.append(tokenized_list[i][j])

with open('中文停用词整理(含标点符号和数字).txt', 'r', encoding='utf-8') as f:
    text = f.read()
    textlist = text.split(';\n')
    zn_STOPWORDS = set(textlist)

textlist = list(textlist)
# delete the stopwords
stopwords = {}.fromkeys(textlist)

tokenized_list_all
final_tokenize = []
for word in tokenized_list_all:
    if word not in stopwords:
            final_tokenize.append(word)
#print (final_tokenize)


final_tokenize
words={}
#统计词频
for word in final_tokenize:
    if(word in words):
        words[word]=words[word]+1
    else:
        words[word]=1

sortedWords = sorted(words.items(), key=lambda d: d[1], reverse=True)
wordsTop10=''
i=0

hotWords = []
rubbish = []
for i in range(1000):
    word = sortedWords[i][0]
    if word == ' ':
        rubbish.append(word)
    elif word == '\xa0':
        rubbish.append(word) 
    else:
        hotWords.append(word)


print(hotWords)

user = pd.read_csv('all_users_complete_3_ver2.csv')
contents = user['正文']
user['hotwords'] = ''


def judge_hotwords():
    global user
    for i in range(len(user)):
        comment = user['正文'][i]
        if comment != '' and type(comment) == str:
            text_tokenize = list(jieba.cut(comment))
            score = 0
            for every_token in text_tokenize:
                if every_token in hotWords:
                    score += 1
                    continue
                else:
                    continue
            user.loc[i,'hotwords'] = score
        else:
            pass


judge_hotwords()
user.to_csv('all_users_complete_4_ver2.csv')