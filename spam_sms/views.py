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
    id_sms = df["id"]

    dict = {'id': id_sms, 'spam_sms': spam_sms, 'preproses_sms': preproses_sms}
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
    engine = create_engine('mysql+pymysql://root:@localhost/normalize_text')
    df = pd.read_sql("select * from preproses", engine)
    preproses_sms = df["preproses_sms"]
    rulebased_sms = preproses.rule_based(preproses_sms)
    # disini tambahkan proses levenshtein
    spam_sms = df["spam_sms"]
    id_sms = df["id"]

    dict = {'id': id_sms, 'spam_sms': spam_sms,
            'preproses_sms': preproses_sms, 'rulebased': rulebased_sms}
    # dict = {'id': id_sms, 'sms_spam': sms}
    df = pd.DataFrame(dict)

    df.to_sql('normalisasi', con=engine, if_exists='replace', index=False)

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='normalize_text')

    # create cursor
    cursor = connection.cursor()

    # Execute query
    sql = "SELECT * FROM `normalisasi`"
    cursor.execute(sql)

    result = cursor.fetchall()
    return render(request, "normalisasi.html", {'result': result})
