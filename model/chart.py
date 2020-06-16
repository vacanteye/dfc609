import sqlite3, datetime, json, glob
import mplfinance as mpf
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from pathlib import Path

def process_chart(con, code, date, verbose):

    #Load Data
    qry_date = date.replace('-', '')
    qry_stmt = "SELECT * FROM chart_min_"+code+" WHERE date LIKE '"+qry_date+"%' ORDER BY date"
    df = pd.read_sql_query(qry_stmt, con)
    if len(df) == 0:
        return 'N/A'

    #Refine Dataframe for plotting
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')
    df = df.drop('amount',axis=1)   #Exclude account
    df.set_index('date', inplace=True)
    df.shape
    df.head(3)
    df.tail(3)

    #Chart Style
    up_style = mpf.make_mpf_style(base_mpl_style='default', facecolor='lavenderblush')
    dn_style = mpf.make_mpf_style(base_mpl_style='default', facecolor='lightcyan')
    uc_style = mpf.make_mpf_style(base_mpl_style='default')

    first_idx = df.index[0]
    last_idx = df.index[-1]

    open_p = df['open'][first_idx]
    close_p = df['close'][last_idx]

    style = up_style if close_p > open_p else dn_style if close_p < open_p else uc_style
    truth  = 'TRUE' if close_p > open_p else 'FALSE' if close_p < open_p else 'N/A'

    if verbose: print(date + ' ' + code + ' CHART ' + truth)

    save_name = './img/' + date + '_chart.png'
    title = '\n' + date + ' CHART ' + truth

    props = {
        'type': 'candle',
        'columns': ('open', 'high', 'low', 'close', 'volume'),
        'volume': False,
        'savefig': save_name,
        'title': title,
        'ylabel': '',
        'ylabel_lower': '',
        'figscale': 0.5,
        'style': style
        }
        
    mpf.plot(df, **props)

    return truth 
