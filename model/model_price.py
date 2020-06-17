import sqlite3, datetime, json, glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.dates import DateFormatter
from pathlib import Path

def plot_price(con, ax, code, date1, date2):

    #Load Data
    qry_date1 = date1.replace('-', '')
    qry_date2 = date2.replace('-', '')
    qry_stmt = ""
    title = ""

    if date1 == date2 :
        qry_stmt = """SELECT * FROM chart_min_{} 
                  WHERE date LIKE '{}%'
                  ORDER BY date""".format(code, qry_date1) 
        title = '{}'.format(date1)
    else:
        qry_stmt = """SELECT * FROM chart_min_{} 
                  WHERE date >= '{}' AND date <= '{}'
                  ORDER BY date""".format(code, qry_date1, qry_date2) 
        title = '{} ~ {}'.format(date1, date2)

    df = pd.read_sql_query(qry_stmt, con)
    if len(df) == 0:
        return None

    #Refine Dataframe for plotting
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')
    df = df.drop('amount',axis=1)   #Exclude account
    df.set_index('date', inplace=True)
    df.shape
    df.head(3)
    df.tail(3)
    #df.index = df.index.map(str)

    #Chart Style
    color = 'white'

    first_idx = df.index[0]
    last_idx = df.index[-1]

    open_p = df['open'][first_idx]
    close_p = df['close'][last_idx]

    truth  = True if close_p > open_p else False if close_p < open_p else None
    color = 'lavenderblush' if close_p > open_p else 'lightcyan' if close_p < open_p else 'white'

    ax.set_facecolor(color)

    line_axes = df['close'].plot(ax=ax)
    line_axes.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    line_axes.set_xlabel('')

    return truth 
