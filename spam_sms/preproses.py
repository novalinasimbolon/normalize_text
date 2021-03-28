import nltk, string

def bacafile(sms):
    url_remove = sms.str.replace('bit.ly\S+|http\S+|https\S+|www.\S+', '')
    lower_case = url_remove.str.lower()
    return lower_case