import pandas as pd
from fuzzywuzzy import process

df = pd.read_csv('posts.csv', sep=',')

df['created_date'] = pd.to_datetime(df['created_date'], yearfirst=True)
df = df.sort_values(by='created_date')
# print(df.dtypes)
word = input()
# h = df['text']
a = process.extract(word, df['text'], limit=20)
for el in a:
    print(el)
exit(0)
# print(h)