import csv
import sys
import getopt
import numpy as np
import pandas as pd 
import nltk
import datetime

def get_dataframe(filename):
    return pd.read_table(filename)

def get_reviews(product_title):
    table = get_dataframe("/source_file_path/Problem_C_Data/hairdryer.tsv")
    product_reviews = table[table['product_title']==product_title].values.tolist()
    return product_reviews

def trans(reviews):
    for r in reviews:
        r[-1] = datetime.datetime.strptime(r[-1], '%m/%d/%Y')
        # r[-1] = datetime.date(datetime.strptime(r[-1], '%m/%d/%Y'))
    return reviews

def get_section_reviews(d1, d2, all_reviews):
    reviews = trans(all_reviews)
    text = list()
    for rw in reviews:
        if rw[-1] >= d1 and rw[-1] <= d2:
            text.append(rw[-2])
    return text

def count_word(word, sentences):
    count = 0
    for s in sentences:
        try:
            tokens = nltk.word_tokenize(s)
            tk = list()
            for i in tokens:
                i = i.lower()
                tk.append(i)
        except TypeError as e:
            continue
        finally:
            if word in tk:
                count += 1
    return count



def persentage():
    raw = statistic()
    res = list()
    for item in raw:
        new_scores = list()
        scores = item[1]
        count = 0
        for sc in scores:
            count += sc[1]
        for sc in scores:
            new_scores.append((sc[0], (sc[1]+0.0)/count))
        res.append((item[0], new_scores))
    return res

def rate_of_5star(item):
    return item[1][4][1]
'''
res = persentage()
res.sort(key=rate_of_5star)
res.reverse()
for item in res:
    print(item[0]+": ")
    for sc in item[1]:
        print(str(sc[0])+": "+str(sc[1]))
'''

def main():
    rws = get_reviews("remington ac2015 t|studio salon collection pearl ceramic hair dryer, deep purple")
    d1 = datetime.datetime.strptime("2012-11-29", '%Y-%m-%d')
    d2 = datetime.datetime.strptime("2013-04-22", '%Y-%m-%d')
    rws = get_section_reviews(d1, d2, rws)
    word_set = ["excellent", "professional", "easy", 	"lightweighted", 	"quiet", 	"expensive", 	"compact", 	"light", 	"nice", 	"strong", 	"good", 	"better", 	"heavy", 	"loud", 	"cheap", 	"hard", 	"disappointed"]
    wordline = ""
    rateline = ""
    for w in word_set:
        wordline += w + ", "
        rateline += str((count_word(w, rws)+0.0)/len(rws)) + ", "
    print(wordline)
    print(rateline)


main()