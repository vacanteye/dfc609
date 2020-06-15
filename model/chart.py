import sqlite3, datetime, json, glob, os
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from pathlib import Path

#Prepare Directories
paths = ['./img', './dat']
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

for path in Path('.').glob('./img/chart*'):
    path.unlink()

#Select Stock
code = '005930'
qry = "SELECT * FROM chart_min_" + code + " WHERE date LIKE '202005%' ORDER BY date"

#Load Data
con = sqlite3.connect('./dat/chart.db')
df = pd.read_sql_query(qry, con)
con.close()

#Refine Dataframe for plotting
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')
df = df.drop('amount',axis=1)   #Exclude data
df.set_index('date', inplace=True)
df.shape
df.head(3)
df.tail(3)

#Extract Unique Dates
unique_dates = df.index.strftime('%Y-%m-%d').unique()

#Chart Style
up_style = mpf.make_mpf_style(base_mpl_style='default', facecolor='lavenderblush')
dn_style = mpf.make_mpf_style(base_mpl_style='default', facecolor='lightcyan')
uc_style = mpf.make_mpf_style(base_mpl_style='default')

#Loop 
for date in unique_dates:
    sub_df = df.loc[date:date]

    first_idx = sub_df.index[0]
    last_idx = sub_df.index[-1]

    open_p = sub_df['open'][first_idx]
    close_p = sub_df['close'][last_idx]

    style = up_style if close_p > open_p else dn_style if close_p < open_p else uc_style
    change = 'RISE' if close_p > open_p else 'FALL' if close_p < open_p else 'NO CHANGE'

    save_name = './img/chart_' + date + '.png'
    title = '\n' + date + ' ' + change
    print(title)

    props = {
        'type': 'candle',
        'columns': ('open', 'high', 'low', 'close', 'volume'),
        'volume': False,
        'savefig': save_name,
        'title': title,
        'ylabel': '',
        'ylabel_lower': '',
        'figscale': 0.8,
        'style': style
        }
        
    rets = mpf.plot(sub_df, **props)
    print(save_name)
