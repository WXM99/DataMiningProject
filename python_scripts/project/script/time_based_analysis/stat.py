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

def calc_star(today, star_and_count, reviews):
    today_rws = list()
    star = 0.0
    count = 0
    for i in reviews:
        if i[-1] == today:
            star += i[7]
            count += 1
    today_avg = 0
    if count != 0:
        today_avg = star / count
    today_star = ((star_and_count[0]*star_and_count[1]) + star) / (star_and_count[1] + count)
    return (today_star, star_and_count[1] + count, today_avg)


def count_stars(reviews):
    min_day = reviews[-1][-1]
    max_day = reviews[0][-1]
    tmp_day = min_day
    count = list()
    star_and_count = (0.0, 0.0, 0.0)
    while(tmp_day != max_day):
        star_and_count = calc_star(tmp_day, star_and_count, reviews)
        count.append((tmp_day, star_and_count[0], star_and_count[2]))
        delta = datetime.timedelta(days=1)
        tmp_day += delta
    return count

        

def main():
    rws = get_reviews("remington ac2015 t|studio salon collection pearl ceramic hair dryer, deep purple")
    rws = trans(rws)
    res = count_stars(rws)
    days = ""
    star = ""
    delta = ""
    for item in res:
        days += item[0].strftime('%Y-%m-%d')+", "
        star += str(item[1]) + ", "
        delta += str(item[2]) + ", "
    print(days)
    print(star)
    print(delta)


main()