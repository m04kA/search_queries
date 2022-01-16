import pandas as pd
from fuzzywuzzy import process
from flask import request


#
# df = pd.read_csv('posts.csv', sep=',')
#
# df['created_date'] = pd.to_datetime(df['created_date'], yearfirst=True)
# df = df.sort_values(by='created_date')
# print(df.dtypes)
# word = input()
# h = df['text']
a = process.extract(word, df['text'], limit=20)
for el in a:
    print(el)
print(h)

def make_ngrams(word, min_size=2):
    """
    basestring       word: word to split into ngrams
           int   min_size: minimum size of ngrams
    """
    length = len(word)
    size_range = range(min_size, max(length, min_size) + 1)
    return list(set(
        word[i:i + size]
        for size in size_range
        for i in range(0, max(0, length - size) + 1)
    ))


gg = make_ngrams('товт')
gg.sort(key=lambda x: len(x))
print(gg)
