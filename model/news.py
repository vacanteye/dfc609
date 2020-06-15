import sqlite3, datetime, json, glob, os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

#Create Directories
paths = ['./img', './dat']
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

for path in Path('.').glob('./img/news*'):
    path.unlink()

#Select Code
code = '005930'
date = '20200504'

qry = "SELECT titl,dttm FROM news_table WHERE cod2='"+code+"' AND date='"+date+"'"
print(qry)
con = sqlite3.connect('./dat/news.db')
df = pd.read_sql_query(qry, con)
con.close()

for index, row in df.iterrows():
    print(row['dttm'], row['titl'])

