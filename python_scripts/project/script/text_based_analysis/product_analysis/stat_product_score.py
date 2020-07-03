import csv
import sys
import getopt
import numpy as np
import pandas as pd 
import nltk

def get_dataframe(filename):
    return pd.read_table(filename)

def get_hfw():
    word_file = open('./picked/pacifier.txt', 'r')
    res = list()
    for word in word_file.readlines():
        word = word.split(" ")[0]
        res.append(word)
    return res

def get_hfw_weight():
    word_file = open('./picked/pacifier.txt', 'r')
    res = list()
    for word in word_file.readlines():
        for weigth in word.split(" "):
            try:
                res.append(float(weigth))
            except ValueError:
                pass
    return res

def get_adj():
    word_file = open('./picked/pacifier_a.txt', 'r')
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

def get_brands():
    table = get_dataframe("/source_file_path/Problem_C_Data/pacifier.tsv")
    product_titles = table[table['helpful_votes']!=0].product_title.tolist()
    count = {}
    for t in product_titles:
        count[t] = count.get(t, 0) + 1
    res = list()
    for title in count:
        if count[title] > 5:
            res.append(title)
    return res

def get_staratings(product_title):
    table = get_dataframe("/source_file_path/Problem_C_Data/pacifier.tsv")
    product_stars = table[table['product_title']==product_title].star_rating.tolist()
    product_votes = table[table['product_title']==product_title].helpful_votes.tolist()
    res = 0.0
    count = 0
    for i in range(len(product_stars)):
        res += product_stars[i] * product_votes[i]
        count += product_votes[i]
    return res/count

def get_sentence(product_title):
    table = get_dataframe("/source_file_path/Problem_C_Data/pacifier.tsv")
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

    return vector

def compute_value(brandname):
    vector = compute_vector(brandname)
    value = 0.0
    weights = get_hfw_weight()
    total = 0.0
    for w in weights:
        total += w
    st_weight = list()
    for w in weights:
        st_weight.append(w/total)
    for i in range(len(vector)):
        value += vector[i][1] * st_weight[i]
    return value



def main():
    items = get_brands()
    score_line = ""
    star_line = ""
    for i in items:
        score = compute_value(i)
        star = get_staratings(i)
        if True: #star < (20*score+2.5) and star > (1.25*16 / 3)*(score+0.125):
            score_line += str(score) + ", "
            star_line += str(star) + ", "
    print(score_line)
    print(star_line)

# main()
# compute_vector()
# get_sentence("samsung smh1816s 1.8 cu. ft. stainless steel over-the-range pacifier")
main()