from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('./dat/news_word_top.csv')
df.set_index('word', inplace=True)
freq_dict = df.to_dict()['count']

font_path='/home/vacanteye/dev/py/dfc609/model/font/NotoSansKR-Regular.otf'

wc = WordCloud(
    background_color='white', 
    max_words=1000, 
    font_path=font_path,
    width = 1920, 
    height = 1080
)
wc.generate_from_frequencies(freq_dict)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
