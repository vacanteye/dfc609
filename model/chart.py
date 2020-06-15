import sqlite3, datetime, json
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import os

#Select Stock
fp = open('./dat/stock_kospi200_en.json')
kospi200 = json.load(fp)
fp.close()
code = '005930'
name = kospi200[code]
qry = 'SELECT * FROM chart_min_' + code + ' ORDER BY date'

#Load Data
con = sqlite3.connect('./dat/chart.db')
df = pd.read_sql_query('SELECT * FROM chart_min_005930 ORDER BY date', con)
con.close()

#Refine Data for Plotting
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')
df = df.drop('amount',axis=1)   #Exclude data
df.set_index('date', inplace=True)
df.shape
df.head(3)
df.tail(3)


#Extract Unique Dates
unique_dates = df.index.strftime('%Y-%m-%d').unique()

#Chart Style
# up:lavenderblush down:lightcyan
up_style = mpf.make_mpf_style(base_mpl_style='default', facecolor='lavenderblush')
dn_style = mpf.make_mpf_style(base_mpl_style='default', facecolor='lightcyan')
uc_style = mpf.make_mpf_style(base_mpl_style='default')

for date in unique_dates:
    sub_df = df.loc[date:date]

    first_idx = sub_df.index[0]
    last_idx = sub_df.index[-1]

    open_price = sub_df['open'][first_idx]
    close_price = sub_df['close'][last_idx]

    style = up_style if close_price > open_price else dn_style if close_price < open_price else uc_style
    change = 'RISE' if close_price > open_price else 'FALL' if close_price < open_price else 'NO CHANGE'

    save_name = './png/' + code + '_min_' + date + '.png'
    title = '\n' + date + ' ' + change
    print(title)

    args = {
        'type': 'candle',
        'columns': ('open', 'high', 'low', 'close', 'volume'),
        'volume': True,
        'savefig': save_name,
        'title': title,
        'ylabel': '',
        'ylabel_lower': '',
        'figscale': 0.8,
        'style': style
        }
        
    rets = mpf.plot(sub_df, **args)
    print(save_name)
