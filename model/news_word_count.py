import sqlite3, datetime, json, glob, os
import pandas as pd
from pathlib import Path
from konlpy.tag import Okt

#Open Korean Text
okt = Okt()

#Create Directories
paths = ['./img', './dat']
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

#qry = "SELECT titl,date FROM news_table WHERE date >= '20200501' AND date <= '20200505'"
qry = "SELECT titl,date FROM news_table WHERE date LIKE '202005%'"
print(qry)
con = sqlite3.connect('./dat/news.db')
df = pd.read_sql_query(qry, con)
con.close()

word_count = {}

for index, row in df.iterrows():
    title = row['titl']
    #tokens = okt.pos(title)
    words = okt.nouns(title)
    print(words)
    for word in words:
        if len(word) < 2: # more than 2 letters
            continue
            
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

results = sorted(word_count.items(), key=(lambda x:x[1]), reverse=True)

fp = open('news_word_top.csv', 'w')
fp.write('word, count\n')
for result in results:
    word = result[0]
    occur = result[1]
    if occur < 100:         # at least 100 occurences
        break
    fp.write(word  + ',' + str(occur) + '\n')

fp.close()

for i in range(10):
    print(results[i])

print('count=',df.count())
print('word=', len(results))


