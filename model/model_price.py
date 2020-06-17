import sqlite3, datetime, json, glob
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.dates import DateFormatter
from pathlib import Path

def process_price(con, ax, code, date, verbose):

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
    color = 'white'

    first_idx = df.index[0]
    last_idx = df.index[-1]

    open_p = df['open'][first_idx]
    close_p = df['close'][last_idx]

    style = up_style if close_p > open_p else dn_style if close_p < open_p else uc_style
    truth  = 'TRUE' if close_p > open_p else 'FALSE' if close_p < open_p else 'N/A'
    color = 'lavenderblush' if close_p > open_p else 'lightcyan' if close_p < open_p else 'white'

    save_name = './img/{}_{}_chart.png'.format(code, date)
    title = '{}'.format(date)

    if verbose: print(title)

    ax.set_facecolor(color)

    line_axes = df['close'].plot(ax=ax)
    line_axes.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    line_axes.set_xlabel('')

    return truth 
