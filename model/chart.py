import sqlite3, datetime
from matplotlib import dates, ticker
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec`
from matplotlib.finance import candlestick_ohlc

#Config Plot
fig = plt.figure(figsize = (8,5))
fig.set_facecolor('w')
gs = gridspec.GridSpec(2, 1, height_ratios=[3,1])


axes = []
axes.append(plt.subplot(gs[0])
axes.append(plt.subplot(gs[1], sharex=axes[0]))
axes[0].get_xaxis().set_visible(False)

dateformat = '%Y%m%d%H%M%s'
mpl.style.use('default')

conn = sqlite3.connect('chart.db')
cur = conn.cursor()
cur.execute('SELECT * FROM chart_min_005930')
rows = cur.fetchall()
for row in rows:
    x = datetime.datetime.strptime(row[0], dateformat)
    o = int(row[1])
    h = int(row[2])
    l = int(row[3])
    c = int(row[4])
    v = int(row[5])
    a = int(row[6])
    cdata = x, o, h, l, c, v
    ohlc_data.append(cdata)
conn.close()
