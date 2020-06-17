import sqlite3, datetime, json, glob, os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from konlpy.tag import Okt

def process_news(con, ax, code, date, dic, verbose):

    qry_date = date.replace('-', '')
    qry_stmt = "SELECT titl FROM news_table WHERE cod2='{}' AND date='{}'".format(code, qry_date)
    df = pd.read_sql_query(qry_stmt, con)

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
        labels = []
        values = []
        colors = []

        if positive > 0:
            labels.append('Positive')
            values.append(positive)
            colors.append('lightcoral')

        if negative > 0:
            labels.append('Negative')
            values.append(negative)
            colors.append('lightskyblue')

        if negative > 0:
            labels.append('Neutral')
            values.append(neutral)
            colors.append('lavender')

        props = {
            'labels': labels ,
            'colors': colors,
            'startangle': 90,
            'autopct':'%1.2f%%'
        }

        result = 'POSITIVE' if positive > negative else 'NEGATIVE'
        #title = '{} {} NEWS {}'.format(date, code, result)
        title = '{}'.format(date)

        if verbose: print(title)

        fname = './img/{}+{}_news.png'.format(code, date)

        ax.pie(values, **props)

    return result

