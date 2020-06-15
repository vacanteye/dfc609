import sqlite3, datetime, json
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import os

#Select Stock
fp = open('kospi200_stock_en.json')
kospi200 = json.load(fp)
fp.close()
code = '005930'
name = kospi200[code]
qry = 'SELECT * FROM chart_min_' + code + ' ORDER BY date'

#Load Data
con = sqlite3.connect('chart.db')
df = pd.read_sql_query('SELECT * FROM chart_min_005930 ORDER BY date', con)
#print(df)
con.close()

#Refine data for charting
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')
df = df.drop('amount',axis=1)   #Exclude data
df.set_index('date', inplace=True)
df.shape
df.head(3)
df.tail(3)

#Extract Unique Dates
unique_dates = df.index.strftime('%Y-%m-%d').unique()

for date in unique_dates:
    sub_df = df.loc[date:date]
    save_name = './png/' + code + '_min_' + date + '.png'
    title = '\n' + name + '(' + code + ')'
    print(title)

    args = {
        'type': 'candle',
        'columns': ('open', 'high', 'low', 'close', 'volume'),
        'volume': True,
        'savefig': save_name,
        'title': title,
        'ylabel': '',
        'ylabel_lower': '',
        'figscale': 0.8
        }
        
    rets = mpf.plot(sub_df, **args)
    print(save_name)
    break
