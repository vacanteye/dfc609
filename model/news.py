import sqlite3, datetime, json, glob, os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from konlpy.tag import Okt

def read_words(fn, value, dic):
    fp = open(fn, 'r')

    for line in fp.readlines():
        word = line.splitlines()[0]
        dic[word] = value
    fp.close()

def process_news(code, date):
    word_dic = {}

    read_words('news_word_negative.txt', -1, word_dic)
    read_words('news_word_positive.txt', 1, word_dic)

    #Create Directories
    paths = ['./img', './dat']
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

    for path in Path('.').glob('./img/news*'):
        path.unlink()

    qry_date = date.replace('-', '')

    qry = "SELECT titl,dttm FROM news_table WHERE cod2='" + code + "' AND date='" + qry_date+"'"
    print(qry)
    con = sqlite3.connect('./dat/news.db')
    df = pd.read_sql_query(qry, con)
    con.close()

    okt = Okt()

    positive = 0.0
    negaive = 0.0
    neutral = 0.0

    for index, row in df.iterrows():
        title = row['titl']
        words = okt.nouns(title)

        vector = 0
        log = ""
        for word in words:
            if word in word_dic:
                vector += word_dic[word]
                log = log + str(word_dic[word])
        if vector > 0:
            positive += 1
        elif vector < 0:
            negaive += 1
        else:
            neutral += 1

        #print(vector, log, title)

    total = positive + negaive + neutral

    #print (' + : ' + str(positive/total) + ' - : ' + str(negaive/total) + ' 0 : ' + str(neutral/total) )

    args = {
        'labels': ['Positive', 'Negative', 'Neutral'],
        'explode': (0, 0, 0),
        'colors': ['lightcoral', 'lightskyblue', 'lavender'],
        'startangle': 90,
        'autopct':'%1.2f%%'
    }

    fname = './img/'+date + '_news.png'
    pie_values = [positive, negaive, neutral]
    plt.rcParams['figure.figsize'] = [4,3]
    plt.pie(pie_values, **args)
    plt.title(date)
    plt.savefig(fname)
    plt.close()

