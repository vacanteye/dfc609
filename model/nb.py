#-*- coding: utf-8 -*-
from konlpy.tag import *
from konlpy.utils import pprint
 
#make lists
def getting_list(filename, listname):
    while 1:
        line = filename.readline()
        str = unicode(line, 'utf-8')
        line_parse = kkma.pos(str)
        for i in line_parse:
            if i[1] == 'SW':
                if i[0] in ['♡', '♥']:
                    listname.append(i[0])
            if i[1] in list_tag:
                listname.append(i[0])
        if not line:
            break
    return listname
 
#naive bayes classifier + smoothing
def naive_bayes_classifier(test, train, all_count):
    counter = 0
    list_count = []
    for i in test:
        for j in range(len(train)):
            if i == train[j]:
                counter = counter + 1
        list_count.append(counter)
        counter = 0
    list_naive = []
    for i in range(len(list_count)):
        list_naive.append((list_count[i]+1)/float(len(train)+all_count))
    result = 1
    for i in range(len(list_naive)):
        result *= float(round(list_naive[i], 6))
    return float(result)*float(1.0/3.0)
 
# get the data
kkma = Kkma()
f_pos = open('./dat/word_pos.txt', 'r')
f_neg = open('./dat/word_neg.txt', 'r')
f_neu = open('./dat/word_neu.txt', 'r')
f_test = open('test.txt', 'r')
 
# tag list (보통명사, 동사, 형용사, 보조동사, 명사추정범주) 
# 참고 : https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit#gid=0
list_tag = [u'NNG', u'VV', u'VA', u'VXV', u'UN']
list_positive=[]
list_negative=[]
list_neutral=[]
 
# extract test sentence
test_line = f_test.readline()
test_s = unicode(test_line, 'utf-8')
test_list=kkma.pos(test_s)
test_output=[]
for i in test_list:
    if i[1] == 'SW':
        if i[0] in ['♡', '♥']:
            test_output.append(i[0])
    if i[1] in list_tag:
        test_output.append(i[0])
 
# getting_list함수를 통해 필요한 tag를 추출하여 list 생성
list_positive = getting_list(f_pos, list_positive)
list_negative = getting_list(f_neg, list_negative)
list_neutral = getting_list(f_neu, list_neutral)
 
ALL = len(set(list_positive))+len(set(list_negative))+len(set(list_neutral)) #전체 카운트, 함수에 들어가야한다. (all_count)
 
# naive bayes 값 계산
result_pos = naive_bayes_classifier(test_output, list_positive, ALL)
result_neg = naive_bayes_classifier(test_output, list_negative, ALL)
result_neu = naive_bayes_classifier(test_output, list_neutral, ALL)
 
if (result_pos > result_neg and result_pos > result_neu):
    print('긍정')
elif (result_neg > result_pos and result_neg > result_neu):
    print('부정')
else:
    print('중립')
 
f_pos.close()
f_neg.close()
f_neu.close()
f_test.close()
