import nltk, string
import re, requests

def bacafile(sms):
    url_remove = sms.str.replace('bit.ly\S+|http\S+|https\S+|www.\S+', '')
    
    regex = r'(?:\B\+ ?62|\b0)(?: *[(-]? *\d(?:[ \d]*\d)?)? *(?:[)-] *)?\d+ *(?:[/)-] *)?\d+ *(?:[/)-] *)?\d+(?: *- *\d+)?'
    phone_remove = url_remove.str.replace(regex, '')
    # https://stackoverflow.com/questions/52093555/python-regular-expression-for-phone-numbers

    punc_no = '[^\w\s?@]'
    punctuation_remove = phone_remove.str.replace(punc_no.format(string.punctuation), ' ')
    punctuation_remove2 = punctuation_remove.str.replace('?', ' ')
    
    lower_case = punctuation_remove2.str.lower()    
    return lower_case