import csv
import sys
import getopt
import numpy as np
import pandas as pd 
import nltk

def get_dataframe(filename):
    return pd.read_table(filename)

def get_hfw(filename):
    word_file = open(filename, 'r')
    res = list()
    for word in word_file.readlines():
        word = word.split(" ")[0]
        res.append(word)
    return res

def main(argv):
    counts = {}
    table = get_dataframe(sys.argv[1])
    # count for review body 
    all_reviews = table.review_body.tolist()
    '''
    for rw in all_reviews:
        try:
            tokens = nltk.word_tokenize(rw)
        except TypeError as e:
            continue
        finally:
            pos_tags = nltk.pos_tag(tokens)
            for word,pos in pos_tags:
                if pos == "JJ" or pos == "JJS" or pos == "JJR": # all kinds of adj
                    word = word.lower()
                    counts[word] = counts.get(word, 0) + 1
    # count for review title         
    all_titles = table.review_headline.tolist()
    for title in all_titles:
        try:
            tokens = nltk.word_tokenize(title)
        except TypeError as e:
            continue
        finally:
            pos_tags = nltk.pos_tag(tokens)
            for word,pos in pos_tags:
                if pos == "JJ" or pos == "JJS" or pos == "JJR": # all kinds of adj
                    word = word.lower()
                    counts[word] = counts.get(word, 0) + 1
    # sort noun by frequency and print 
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    for i in items:
        word, count = i
        print("{0:<10}{1:>5}".format(word, count))
    '''
    ## coverage check
    hf_words = get_hfw(argv[2])
    cover_count = 0
    for rw in all_reviews:
        try:
            tokens = nltk.word_tokenize(rw)
        except:
            pass
        finally:
            for hfw in hf_words:
                if hfw in tokens:
                    cover_count += 1
                    break
    print("total_num: ", len(all_reviews))
    print("cover count: ", cover_count)

main(sys.argv)