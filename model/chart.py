import sqlite3, datetime
import mplfinance as mpf
import pandas as pd

#Read Data
con = sqlite3.connect('chart.db')
df = pd.read_sql_query('SELECT * FROM chart_min_005930 ORDER BY date', con)
print(df)
con.close()

#Refine data for charting
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M%S')
df.rename(columns={"date":"Date", "open":"Open", "high":"High", "low":"Low", "close":"Close", "volume":"Volume"}, inplace=True)
df = df.drop('amount',axis=1)


#Prepare Chart
df.set_index('Date', inplace=True)
df.shape
df.head(3)
df.tail(3)

print(df)
print(df.dtypes)

df = df.loc['2020-06-04':]
mpf.plot(df, type='candle')


con.close()
