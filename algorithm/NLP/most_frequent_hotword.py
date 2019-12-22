import jieba
import pandas as pd
from collections import Counter

user_weibo = pd.read_csv('linshuhao.csv')
#user_weibo = user[2:]
user_weibo.columns = ['id','正文','日期','点赞数','评论数','转发数','话题']

contents = user_weibo['正文'].astype('str')

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
# 去除停用词
stopwords = {}.fromkeys(textlist)
#上面的停用词有待添加

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
print(sortedWords[:5])


wordsTop10=''
i=0

hotWords = []
rubbish = []
for i in range(len(sortedWords)):
    word = sortedWords[i][0]
    if word == ' ':
        rubbish.append(word)
    elif word == '\xa0':
        rubbish.append(word) 
    else:
        hotWords.append(word)

print(hotWords[1])
Freq_word = hotWords[1]


sentence_list = []
for c in contents:
    if c != ' ' and type(c) == str:
        if Freq_word in c:
            sentence_list.append(c)
        else:
            pass
    else:
        pass
                
print(sentence_list)

