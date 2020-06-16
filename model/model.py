import sqlite3, datetime, json, glob
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import news, chart
from matplotlib import rc
from pathlib import Path

# Read word from file
def read_words(fn, value, dic):
    fp = open(fn, 'r')
    for line in fp.readlines():
        word = line.splitlines()[0]
        dic[word] = value
    fp.close()

#Init & Setup
word_dic = {}
read_words('./dat/news_word_negative.txt', -1, word_dic)
read_words('./dat/news_word_positive.txt', 1, word_dic)

fp = open('./dat/stock_kospi200_ko.json', 'r')
kospi200_dic = json.load(fp)
fp.close()

matplotlib.use('Agg')
paths = ['./img', './dat']
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

for path in Path('.').glob('./img/*_chart.png'):
    path.unlink()

for path in Path('.').glob('./img/*_news.png'):
    path.unlink()

# DB Connection
conn_chart = sqlite3.connect('./dat/chart.db')
conn_news  = sqlite3.connect('./dat/news.db')

dateindex = pd.date_range('2020-05-01', '2020-05-31', freq='B')
dates = dateindex.strftime('%Y-%m-%d').tolist()

logfile = open('./dat/model.csv', 'w')
logfile.write('Code, Name, Precision, Recall, Accuracy\n')

for code in kospi200_dic:

    name = kospi200_dic[code]

    results = []

    verbose = False

    for date in dates:
        news_predict = news.process_news(conn_news, code, date, word_dic, verbose)
        chart_truth  = chart.process_chart(conn_chart, code, date, verbose)
        results.append({'date': date, 'predict': news_predict, 'truth': chart_truth})

   #Performance Measure 
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0

    for result in results:
        if result['truth'] == 'TRUE' and result['predict'] == 'POSITIVE':
            tp += 1
        elif result['truth'] == 'TRUE' and result['predict'] == 'NEGATIVE':
            tn += 1
        elif result['truth'] == 'FALSE' and result['predict'] == 'POSITIVE':
            fp += 1
        elif result['truth'] == 'FALSE' and result['predict'] == 'NEGATIVE':
            fn += 1

    precision   = 0 if (tp+ fp) == 0 else tp/ (tp+ fp)
    recall      = 0 if (tp+ fn) == 0 else tp/ (tp+ fn)
    accuracy    = 0 if (tp+ fn + fp+ tn) == 0 else (tp+ tn) / (tp+ fn+ fp+ tn)

    log = '{},{},{:.2f},{:.2f},{:.2f}' .format(code, name, precision, recall, accuracy)

    print(log)

    logfile.write(log)
    logfile.write('\n')


# DB Close
conn_chart.close()
conn_news.close()

# File Close
logfile.close()


