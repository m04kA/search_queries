from flask import Flask
from mongoLib import *
import pandas as pd
from fuzzywuzzy import process


# app = Flask(__name__)
# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)


def conecting_to_DB(name_DB, name_collection, port=27017):
    client = pymongo.MongoClient(port=port).DBNAME
    DB = client[name_DB]
    collection_name = DB[name_collection]
    return collection_name


def find_in_documents(words):
    collection_name = conecting_to_DB("Search_queries", "All_data")
    all_doks = pd.DataFrame(find_document(collection_name, all_documents=True))
    del all_doks['_id']
    help_find_df = all_doks[['text', 'id']]
    help_find_df.set_index('id', inplace=True)
    all_doks_result = process.extract(words, all_doks['text'], limit=18)
    mass_index = []
    for el in all_doks_result:
        mass_index.append(el[0])
    answer = all_doks.loc[all_doks['text'].isin(mass_index)]

    print(answer)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == '__main__':
    find_in_documents('е')
    # app.run()

    # ---- Update DB ----
    # df = pd.read_csv('posts.csv', sep=',')
    # df['created_date'] = pd.to_datetime(df['created_date'], yearfirst=True)
    # df = df.sort_values(by='created_date')
    # collection_name = conecting_to_DB("Search_queries", "All_data")
    # for ind, row in df.iterrows():
    #     data_row = {
    #         "id": ind,
    #         "rubrics": row["rubrics"],
    #         "text": row["text"],
    #         "created_date": row["created_date"]
    #     }
    #     result = find_document(collection_name, {"id": ind})
    #     if result:
    #         data_row = result | data_row
    #         update_document(collection_name, {'id': ind}, data_row)
    #     else:
    #         collection_name.create_index([("id", pymongo.ASCENDING)], unique=True)
    #         collection_name.create_index([("text", 'text')])
    #         insert_document(collection_name, data_row)
    # -----------------------
    # rez = collection_name.find({"$text": {"$search": tt}})
    # for el in rez:
    #     print(el)
