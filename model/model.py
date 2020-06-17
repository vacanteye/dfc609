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

period = 1
while True:
    try:
        period = int(input("Select Period [1, 2, 4, 5] days: "))
        if period in (1, 2, 4, 5):
            break
        else:
            print('Invalid Period')
            continue
    except:
        print('')
        exit(1)

#Init & Setup
word_dic = {}
read_words('./dat/news_word_negative.txt', -1, word_dic)
read_words('./dat/news_word_positive.txt', 1, word_dic)

#Load KOSPI200 
fp = open('./dat/stock_kospi200_en.json', 'r')
kospi200_dic = json.load(fp)
fp.close()

#Directories
matplotlib.use('Agg')
paths = ['./img', './dat']
for path in paths:
    Path(path).mkdir(parents=True, exist_ok=True)

#for path in Path('.').glob('./img/*.png'):
#    path.unlink()

# DB Connection
conn_news  = sqlite3.connect('./dat/news.db')
conn_price = sqlite3.connect('./dat/price.db')

dateindex = pd.date_range('2020-05-02', '2020-05-31', freq='B')
dates = dateindex.strftime('%Y-%m-%d').tolist()

logfile = open('./dat/model_{}.csv'.format(period), 'w')
logfile.write('Code, Name, Precision, Recall, Accuracy\n')

# Popular Stocks in News
codes = ['005930','017670','035420','066570','006800']

for code in codes:
    name = kospi200_dic[code]
    
    fig, axes = plt.subplots(nrows=int(20/period), ncols=2)
    fig.set_size_inches(10,int(80/period))
    fig.tight_layout(pad=5.0)

    results = []

    index = 0

    for i in range(0, len(dates)-1, period):

        date1 = dates[i]
        date2 = dates[i+period-1]

        title = date1

        if date1 != date2:
            title = "{}~{}".format(date1, date2)

        row = int(index / 2)
        col = int(index % 2)
        axes[row, col].set_title("")
        news_predict = model_news.plot_news(conn_news, axes[row, col], code, date1, date2, word_dic)
        index = index + 1

        row = int(index / 2)
        col = int(index % 2)
        axes[row, col].set_title(title)
        chart_truth  = model_price.plot_price(conn_price, axes[row, col], code, date1, date2)
        index = index + 1

        results.append({'date': title, 'predict': news_predict, 'truth': chart_truth})

   #Performance Measure 
    tp = 0.0
    tn = 0.0
    fp = 0.0
    fn = 0.0

    for result in results:
        #print(result)

        if result['truth'] == True and result['predict'] == True:
            tp += 1
        elif result['truth'] == True and result['predict'] == False:
            tn += 1
        elif result['truth'] == False and result['predict'] == True:
            fp += 1
        elif result['truth'] == False and result['predict'] == False:
            fn += 1

    precision   = 0 if (tp+ fp) == 0 else tp/ (tp+ fp)
    recall      = 0 if (tp+ fn) == 0 else tp/ (tp+ fn)
    accuracy    = 0 if (tp+ fn + fp+ tn) == 0 else (tp+ tn) / (tp+ fn+ fp+ tn)

    log = '{},{},{:.2f},{:.2f},{:.2f}' .format(code, name, precision, recall, accuracy)
    print(log)

    logfile.write(log)
    logfile.write('\n')
    
    s = '{}({}) Precision:{:.2f} Recall:{:.2f} Accuracy:{:.2f}'
    title = s.format(name, code, precision, recall, accuracy)
    #fig.suptitle(title)
    plt.savefig('./img/{}_{}.png'.format(code,period), bbox_inches='tight')
    plt.close()

# DB Close
conn_news.close()
conn_price.close()

# File Close
logfile.close()

