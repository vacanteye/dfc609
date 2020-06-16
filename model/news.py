import sqlite3, datetime, json, glob, os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from konlpy.tag import Okt

def process_news(con, code, date, dic, verbose):

    #Create Directories
    paths = ['./img', './dat']
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)

    for path in Path('.').glob('./img/news*'):
        path.unlink()

    qry_date = date.replace('-', '')

    qry = "SELECT titl,dttm FROM news_table WHERE cod2='" + code + "' AND date='" + qry_date+"'"
    df = pd.read_sql_query(qry, con)

    okt = Okt()

    positive = 0.0
    negative = 0.0
    neutral = 0.0

    for index, row in df.iterrows():
        title = row['titl']
        words = okt.nouns(title)

        vector = 0
        log = ""
        for word in words:
            if word in dic:
                vector += dic[word]

        if vector > 0:
            positive += 1
        elif vector < 0:
            negative += 1
        else:
            neutral += 1

    total = positive + negative + neutral

    result = 'N/A'
        
    if total > 0:

        props = {
            'labels': ['Positive', 'Negative', 'Neutral'],
            'explode': (0, 0, 0),
            'colors': ['lightcoral', 'lightskyblue', 'lavender'],
            'startangle': 90,
            'autopct':'%1.2f%%'
        }

        result = 'POSITIVE' if positive > negative else 'NEGATIVE'
        title = date + ' ' + code + ' NEWS  ' + result

        if verbose: print(title)

        fname = './img/'+date + '_news.png'
        pie_values = [positive, negative, neutral]
        plt.rcParams['figure.figsize'] = [4,3]
        plt.pie(pie_values, **props)
        plt.title(title)
        plt.savefig(fname)
        plt.close()

    return result

