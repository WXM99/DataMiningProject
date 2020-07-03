import csv
import sys
import getopt
import numpy as np
import pandas as pd 
import nltk

hair_vector = [15542.0, 2174.0, 1764.0, 1705.0, 1645.0, 1506.0, 1437.0, 1199.0, 1138.0, 1034.0, 946.0, 936.0, 900.0, 723.0, 664.0, 638.0, 577.0, 575.0, 569.0, 544.0, 512.0, 374.0]

def get_hfw():
    word_file = open('../market_analysis/statistic_result/hairdryer.txt', 'r')
    res = list()
    for word in word_file.readlines():
        word = word.split(" ")[0]
        res.append(word)
    return res

def get_hfw_weight():
    word_file = open('../market_analysis/statistic_result/hairdryer.txt', 'r')
    res = list()
    for word in word_file.readlines():
        for weigth in word.split(" "):
            try:
                res.append(float(weigth))
            except ValueError:
                pass
    return res

def get_adj():
    word_file = open('../market_analysis/statistic_result/hairdryer_a.txt', 'r')
    res_p = list()
    res_n = list()
    for word in word_file.readlines():
        is_positive = False
        if "1" in word.split(" ") or  "1\n"  in word.split(" "):
            is_positive = True
        word = word.split(" ")[0]
        if is_positive:
            res_p.append(word)
        else:
            res_n.append(word)
    return (res_p, res_n)

def get_sentence(paragraph):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return tokenizer.tokenize(paragraph)

def get_quantity_vector(review, review_title):
    hfw = get_hfw()
    hfw_weight = get_hfw_weight()
    adjs = get_adj()
    sentence_b = get_sentence(review)
    sentence_t = get_sentence(review_title)
    sentence_b.extend(sentence_t)
    vector = list()
    for hf_word in hfw:
        is_countain = False
        hfw_score = 0
        for sentence in sentence_b:
            tokens = nltk.word_tokenize(sentence)
            if hf_word in tokens:
                last_word = ""
                is_countain = True
                for word in tokens:
                    if word in adjs[0] and last_word != "not" and last_word != "barely" and last_word != "hardly" :
                        hfw_score = 1
                    elif word in adjs[1] and last_word != "not" and last_word != "barely" and last_word != "hardly":
                        hfw_score = -1
                    else:
                        pass
                    last_word = word
        vector.append((hf_word, hfw_score))
    res = list()
    for item in vector:
            res.append(item[1])
    return res


def compute_value(weights, vector):
    value = 0.0
    total = 0.0
    for w in weights:
        total += w
    st_weight = list()
    for w in weights:
        st_weight.append(w/total)
    # print("st_weight: ", st_weight)
    for i in range(len(vector)):
        value += vector[i] * st_weight[i]
    return value

# re_vector = get_quantity_vector("", "... blow dryer for about three years now and I love it. ")
re_vector = get_quantity_vector("I eagerly snapped up this ionic hair dryer about over a year ago because of it's retractable cord and folding capabilities. Even the price was attractive. It really did take up little room in my bathroom drawer and the retractable cord was a plus. I thought I had the perfect blow dryer because it did what it was supposed to do and quickly. Now for the bad news:  the retractable cord became chewed up and frayed after daily use and it became apparent that the cord was ultimately going to fray completely in due time. ", "Great concept but exceedingly short shelf life")


print(re_vector)
print(compute_value(hair_vector, re_vector))
                

