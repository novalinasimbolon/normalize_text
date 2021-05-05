from django.shortcuts import render
from spam_sms import preproses as preproses
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import json
import nltk
import string
import re
import requests

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer

# Create your views here.


def home(request):
    return render(request, "home.html")


def data(request):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='normalize_text')

    # create cursor
    cursor = connection.cursor()

    # Execute query
    sql = "SELECT * FROM `spam_sms_normalize`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()
    return render(request, "data.html", {'result': result})


def proses(request):
    engine = create_engine('mysql+pymysql://root:@localhost/normalize_text')
    df = pd.read_sql("select * from spam_sms_normalize", engine)
    spam_sms = df["sms_spam"]
    preproses_sms = preproses.bacafile(spam_sms)
    rulebased_sms = preproses.rule_based(preproses_sms)
    id_sms = df["id"]

    dict = {'id': id_sms, 'spam_sms': spam_sms,
            'preproses_sms': preproses_sms, 'rulebased_sms': rulebased_sms}
    df = pd.DataFrame(dict)

    df.to_sql('preproses', con=engine, if_exists='replace', index=False)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='normalize_text')

    # create cursor
    cursor = connection.cursor()

    # Execute query
    sql = "SELECT * FROM `preproses`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()
    return render(request, "proses.html", {'result': result})


def normalisasi(request):
    # m = []
    # n = []
    # x = []
    # y = []

    # connection = pymysql.connect(host='localhost',
    #                              user='root',
    #                              password='',
    #                              db='normal')

    # # create cursor
    # cursor = connection.cursor()

    # # Execute query
    # sql = "SELECT * FROM `preproses`"
    # cursor.execute(sql)

    # result = cursor.fetchall()
    # for row in result:
    #     m.append(row[0])
    #     n.append(row[1])
    #     x.append(row[2])
    #     y.append(row[3])

    # m = np.array(m)
    # n = np.array(n)
    # x = np.array(x)
    # y = np.array(y)

    # y_normalize = preproses.normalisasi(y)

    # df1 = pd.DataFrame()
    # df1['y_normalize'] = pd.Series(y_normalize)
    # df1.to_csv('normalize.csv')

    # df = pd.DataFrame()
    # # add the array to df as a column

    # df['y_normalize'] = y_normalize

    # dict = {'y_normalize': y_normalize}
    # df = pd.DataFrame(dict)
    # engine = create_engine('mysql+pymysql://root:@localhost/normalize_text')
    # df.to_sql('normalisasi', con=engine, if_exists='replace', index=False)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='normalize_text')

    # create cursor
    cursor = connection.cursor()

# udah bisa
    # Execute query
    sql = "SELECT * FROM `preproses`"
    cursor.execute(sql)

    result = cursor.fetchall()
    normalisasi_sms = []
    spam_sms = []

    for row in result:
        spam_sms.append(row[1])
        sms_tokens = nltk.word_tokenize(row[3])
        sms_tokens
        normal_text = []
        for word in sms_tokens:
            normal_text.append(preproses.calcDictDistance(word, 1))
            normal_text.append(" ")
            # result = "".join(normal_text)
        ntext = "".join(normal_text)
        normalisasi_sms.append(ntext)

    df = pd.DataFrame()
    df['spam_sms'] = spam_sms
    df['normalisasi_sms'] = normalisasi_sms

    dict = {'spam_sms': df['spam_sms'],
            'normalisasi_sms': df['normalisasi_sms']}
    df = pd.DataFrame(dict)
    engine = create_engine('mysql+pymysql://root:@localhost/normalize_text')
    df.to_sql('normalisasi', con=engine, if_exists='replace', index=False)

    # cursor = connection.cursor()
    # sql = "SELECT * FROM `normalisasi`"
    # cursor.execute(sql)

    # result = cursor.fetchall()

    return render(request, "normalisasi.html", {'result': result})


def upload(request):
    return render(request, "upload.html")


def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'
