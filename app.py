from flask import Flask, render_template, request
from mongoLib import *
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__, template_folder='templates')

# Сброс ограничений на количество выводимых рядов (отладка)
pd.set_option('display.max_rows', None)

# Сброс ограничений на число столбцов (отладка)
pd.set_option('display.max_columns', None)

# Сброс ограничений на количество символов в записи (отладка)
pd.set_option('display.max_colwidth', None)

# Отключаем перенос строки для вывода (отладка)
pd.options.display.expand_frame_repr = False


def conecting_to_DB(name_DB, name_collection, port=27017):
    """
    Connect to DB
    :param name_DB:
    :param name_collection:
    :param port:
    :return:
    """
    client = pymongo.MongoClient(port=port).DBNAME
    DB = client[name_DB]
    collection_name = DB[name_collection]
    return collection_name


def find_in_documents(words, limits=20):
    """
    This funk take all documents and looking for matches. If there are no exact matches,
    then it looks for partial matches.
    :param words:
    :return:
    """
    collection_name = conecting_to_DB("Search_queries", "All_data")
    all_doks = pd.DataFrame(find_document(collection_name, all_documents=True))
    all_doks.set_index('id', inplace=True)
    del all_doks['_id']
    all_doks_result = process.extract(words, all_doks['text'], limit=limits)
    mass_index = []
    for el in all_doks_result:
        mass_index.append(el[2])

    answer = all_doks.loc[mass_index]
    return answer


@app.route('/', methods=['post', 'get'])
def search_queries():
    """
    This funk need for render template and get data from user.
    :return:
    """
    message = pd.DataFrame()
    if request.method == 'POST':
        user_text = request.form.get('users_text')
        message = find_in_documents(user_text)
    return render_template('find.html', tables=[message.to_html(classes='data', header="true")])


if __name__ == '__main__':
    # ---- Update DB ----
    df = pd.read_csv('posts.csv', sep=',')
    df['created_date'] = pd.to_datetime(df['created_date'], yearfirst=True)
    df = df.sort_values(by='created_date')
    collection_name = conecting_to_DB("Search_queries", "All_data")
    for ind, row in df.iterrows():
        data_row = {
            "id": ind,
            "rubrics": row["rubrics"],
            "text": row["text"],
            "created_date": row["created_date"]
        }
        result = find_document(collection_name, {"id": ind})
        if result:
            data_row = result | data_row
            update_document(collection_name, {'id': ind}, data_row)
        else:
            collection_name.create_index([("id", pymongo.ASCENDING)], unique=True)
            collection_name.create_index([("text", 'text')])
            insert_document(collection_name, data_row)
    # -----------------------

    # ---- Start ----
    app.run(debug=True)
    # ---------------
