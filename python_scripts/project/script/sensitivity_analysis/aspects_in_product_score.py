import csv
import sys
import getopt
import numpy as np
import pandas as pd 
import nltk

def get_dataframe(filename):
    return pd.read_table(filename)

def get_hfw():
    word_file = open('./../text_based_analysis/market_analysis/statistic_result/pacifier.txt', 'r')
    res = list()
    for word in word_file.readlines():
        word = word.split(" ")[0]
        res.append(word)
    return res

def get_brand():
    word_file = open('./../text_based_analysis/market_analysis/statistic_result/hd_brand.txt', 'r')
    res = list()
    for word in word_file.readlines():
        res.append(word.strip('\n'))
    return res

def get_hfw_weight():
    word_file = open('./../text_based_analysis/market_analysis/statistic_result/pacifier.txt', 'r')
    res = list()
    for word in word_file.readlines():
        for weigth in word.split(" "):
            try:
                res.append(float(weigth))
            except ValueError:
                pass
    return res

def get_adj():
    word_file = open('./../text_based_analysis/market_analysis/statistic_result/pacifier_a.txt', 'r')
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

def get_sentence(product_title):
    table = get_dataframe("/Users/Miao/Downloads/2020_Weekend2_Problems/Problem_C_Data/pacifier.tsv")
    product_reviews = table[table['product_title']==product_title].review_body.tolist()
    product_review_titles = table[table['product_title']==product_title].review_headline.tolist()
    '''
    product_reviews = table.review_body.tolist()
    product_review_titles = table.review_headline.tolist()
    '''
    product_reviews.extend(product_review_titles)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = list()
    for paragraph in product_reviews:
        try:
            sentences.extend(tokenizer.tokenize(paragraph))
        except:
            continue
        finally:
            pass
    return sentences

def get_pairs(product_title):
    # print("----------"+product_title+"----------")
    hfw = get_hfw()
    product_reviews = get_sentence(product_title)
    counts = {}
    for rw in product_reviews:
        tokens = nltk.word_tokenize(rw)
        for hf_word in hfw:
            if hf_word in tokens:
                pos_tags = nltk.pos_tag(tokens)
                last_token = ""
                for token, pos in pos_tags:
                    if pos == "JJ" or pos == "JJS" or pos == "JJR":
                        tmp_pair=(hf_word.lower(), token.lower())
                        if last_token != "not" and last_token != "barely" and last_token != "hardly":
                            counts[tmp_pair] = counts.get(tmp_pair, 0) + 1
                last_token = token
    return counts

def compute_vector(brandname):
    adjs = get_adj()
    positive_adj = adjs[0]
    negative_adj = adjs[1]
    dimension = get_hfw()
    pair_counts = get_pairs(brandname)
    items = list(pair_counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    vector = []
    # each dimension
    for d in dimension:
        val = 0
        adj_count = 0
        dimension_score = 0
        # iteration in pairs to 
        for pairs_ct in items:
            pairs, count = pairs_ct
            count = int(count)
            if pairs[0] == d:
                if pairs[1] in positive_adj:
                    val += 1 * count
                elif pairs[1] in negative_adj:
                    val -= 1 * count
                adj_count += count
        if adj_count != 0:
            dimension_score = val / adj_count
        dimension_res = (d, dimension_score)
        vector.append(dimension_res)
    # print("vector: ", vector)
    lines = ''
    for items in vector:
        lines += items[0] + ", "
    # print(lines)
    vals = ""
    for items in vector:
        vals += str(items[1]) + ", "
    # 
    # 
    # print(vals)

    return vector

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
        value += vector[i][1] * st_weight[i]
    return value




def main():
    items = get_brand()
    weights = get_hfw_weight()
    # print(weights)
    score_num = 36
    vector = compute_vector(items[3])
    title = ""
    for k in range(score_num+1):
        title += str(k)+ ", "
    print(title)
    for i in range(len(weights)):
        row = ""
        step = weights[i]/score_num
        for j in range(int(weights[i]/step) + 1):
            new_w = j*step
            old_w = weights[i]
            weights[i] = new_w
            row += str(compute_value(weights, vector)) + ", "
            weights[i] = old_w
        print(row)


# main()
# compute_vector()
# get_sentence("samsung smh1816s 1.8 cu. ft. stainless steel over-the-range pacifier")
main()