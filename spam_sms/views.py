from django.shortcuts import render
from spam_sms import preproses as preproses
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Create your views here.
def home(request):
    return render(request, "home.html")

def data(request):
    connection = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='normalize_text')    

    # create cursor
    cursor=connection.cursor()   

    # Execute query
    sql = "SELECT * FROM `spam_sms_normalize`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()
    return render(request, "data.html", {'result':result})

def proses(request):
    engine = create_engine('mysql+pymysql://root:@localhost/normalize_text')
    df = pd.read_sql("select * from spam_sms_normalize", engine)
    sms = df["sms_spam"]
    lower = preproses.bacafile(sms)
    id_sms = df["id"]


    dict = {'id': id_sms, 'sms_spam': sms, 'lower':lower}  
    df = pd.DataFrame(dict) 

    df.to_sql('preproses', con = engine, if_exists = 'replace',index = False)

    connection = pymysql.connect(host='localhost',
                         user='root',
                         password='',
                         db='normalize_text')    

    # create cursor
    cursor=connection.cursor()   

    # Execute query
    sql = "SELECT * FROM `preproses`"
    cursor.execute(sql)

    # Fetch all the records
    result = cursor.fetchall()
    return render(request, "proses.html", {'result':result})
