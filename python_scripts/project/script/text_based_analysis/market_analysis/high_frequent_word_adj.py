import csv
import sys
import getopt
import numpy as np
import pandas as pd 
import nltk

def get_dataframe(filename):
    return pd.read_table(filename)

def get_hfw():
    word_file = open('./picked/pacifier_a.txt', 'r')
    res = list()
    for word in word_file.readlines():
        word = word.split(" ")[0]
        res.append(word)
    return res

def statistic():
    table = get_dataframe("/source_file_path/Problem_C_Data/pacifier.tsv")
    hfw = get_hfw()
    res = list()
    for word in hfw:
        tmp_res = list()
        for i in range(1,6):
            count = 0
            all_reviews = table[table['star_rating']==i].review_body.tolist()
            for rw in all_reviews:
                try:
                    tokens = nltk.word_tokenize(rw)
                except TypeError as e:
                    continue
                finally:
                    if word in tokens:
                        last=""
                        for w in tokens:
                            if w == word and last != "not" and last != "barely" and last != "hardly":
                                count += 1
                                break
                            else:
                                continue
                            last = w
            pair = (i, count)
            tmp_res.append(pair)
        res.append((word, tmp_res))
    return res

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

res = persentage()
res.sort(key=rate_of_5star)
res.reverse()
for item in res:
    print(item[0]+": ")
    for sc in item[1]:
        print(str(sc[0])+": "+str(sc[1]))