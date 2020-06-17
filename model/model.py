import sqlite3, datetime, json, glob
from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
import model_news, model_price

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

#Load KOSPI200 
fp = open('./dat/stock_kospi200_ko.json', 'r')
kospi200_dic = json.load(fp)
fp.close()

matplotlib.use('Agg')
paths = ['./img', './dat']
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

for path in Path('.').glob('./img/*.png'):
    path.unlink()

# DB Connection
conn_price = sqlite3.connect('./dat/price.db')
conn_news  = sqlite3.connect('./dat/news.db')

dateindex = pd.date_range('2020-05-02', '2020-05-31', freq='B')
dates = dateindex.strftime('%Y-%m-%d').tolist()

logfile = open('./dat/model.csv', 'w')
logfile.write('Code, Name, Precision, Recall, Accuracy\n')

for code in kospi200_dic:
    
    fig, axes = plt.subplots(nrows=20, ncols=2)
    fig.set_size_inches(10,80)
    fig.tight_layout(pad=5.0)
    fig.suptitle(code, y=0.8)
   # code = '005930'

    name = kospi200_dic[code]

    results = []

    verbose = False

    index = 0

    for date in dates:

        row = int(index / 2)
        col = int(index % 2)
        axes[row, col].set_title(date)
        news_predict = model_news.process_news(conn_news, axes[row, col], code, date, word_dic, verbose)
        index = index + 1

        row = int(index / 2)
        col = int(index % 2)
        axes[row, col].set_title(date)
        chart_truth  = model_price.process_price(conn_price, axes[row, col], code, date, verbose)
        index = index + 1

        results.append({'date': date, 'predict': news_predict, 'truth': chart_truth})
        break;

    plt.savefig('./img/{}.png'.format(code), bbox_inches='tight')
    plt.close()
    break

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
conn_news.close()
conn_price.close()

# File Close
logfile.close()

