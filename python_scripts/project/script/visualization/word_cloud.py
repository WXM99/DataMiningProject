from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_hfw_weight():
    word_file = open('./somepath/hairdryer_a.txt', 'r')
    res = list()
    for word in word_file.readlines():
        for weigth in word.split(" "):
            try:
                res.append(float(weigth))
            except ValueError:
                pass
    return res

def create_word_cloud():
    frequencies = {}
    i = 0
    feq = get_hfw_weight()
    for line in open("./somepath/hairdryer_a.txt"):
        arr = line.split(" ")
        frequencies[arr[0]] = feq[i]
        i += 1
    print(frequencies)
    wc = WordCloud(
        max_words=100,
        width=2000,
        height=1200,
    )
    word_cloud = wc.generate_from_frequencies(frequencies)
    word_cloud.to_file("wordcloud2.jpg")

create_word_cloud()