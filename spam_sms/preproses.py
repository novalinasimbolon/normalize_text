import nltk
import string
import re
import requests
import json
import numpy


def bacafile(sms):
    url_remove = sms.str.replace(
        'bit.ly\S+|http\S+|https\S+|www.\S+|s.id\S+|S.id\S+|tiny.cc\S+', '')
    rupiah_replace = url_remove.str.replace(
        'Rp.\d+|jt|juta', '')
    persen_replace = rupiah_replace.str.replace('[0-9]%+', '')

    hashtag_replace = persen_replace.str.replace('#[A-Za-z0-9|A_Za_z0_9]+', '')

    regex = r'(?:\B\+ ?62|\b0)(?: *[(-]? *\d(?:[ \d]*\d)?)? *(?:[)-] *)?\d+ *(?:[/)-] *)?\d+ *(?:[/)-] *)?\d+(?: *- *\d+)?'
    phone_remove = hashtag_replace.str.replace(regex, '')
    # https://stackoverflow.com/questions/52093555/python-regular-expression-for-phone-numbers

    punc_no = '[^\w\s?@ | -]'
    punctuation_remove = phone_remove.str.replace(
        punc_no.format(string.punctuation), ' ')
    punctuation_remove2 = punctuation_remove.str.replace('-', '')
    punctuation_remove2 = punctuation_remove2.str.replace('?', ' ')

    lower_case = punctuation_remove2.str.lower()
    single_char = r'\b[a-zA-Z|0-9]\b'
    single_char_replace = lower_case.str.replace(single_char, ' ')
    return single_char_replace


def levenshteinDistanceDP(token1, token2):
    distances = numpy.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1-1] == token2[t2-1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    # printDistances(distances, len(token1), len(token2))
    return distances[len(token1)][len(token2)]


def calcDictDistance(word, numWords):
    file = open('../kateglo.json', 'r')
    lines = file.readlines()
    file.close()
    dictWordDist = []
    wordIdx = 0

    for line in lines:
        json_dict = json.loads(line)
        for post in json_dict:
            wordDistance = levenshteinDistanceDP(word, post['lema'].strip())
            if wordDistance >= 10:
                wordDistance = 9
            dictWordDist.append(str(int(wordDistance)) +
                                "-" + post['lema'].strip())
            wordIdx = wordIdx + 1

        # closestWords = []
        wordDetails = []
        currWordDist = 0
        dictWordDist.sort()
        # print(dictWordDist)
        for i in range(numWords):
            currWordDist = dictWordDist[i]
            wordDetails = currWordDist.split("-")
            # closestWords.append(wordDetails[1])
        return wordDetails[1]


def rule_based(text):

    nol_replace = text.str.replace('0', 'o')
    empat_replace = nol_replace.str.replace('4|@', 'a')
    enamsembilan_replace = empat_replace.str.replace('6|9', 'g')
    lima_replace = enamsembilan_replace.str.replace('5', 's')
    tujuh_replace = lima_replace.str.replace('7', 'j')
    tiga_replace = tujuh_replace.str.replace('3', 'e')
    satu_replace = tiga_replace.str.replace('1', 'i')
    as_replace = satu_replace.str.replace('ass', 'assalamualaikum')
    remove_number = as_replace.str.replace('\d+', ' ')

    single_char = r'\b[a-zA-Z]\b'
    single_char_replace = remove_number.str.replace(single_char, ' ')
    double_white_space = single_char_replace.str.replace('\s+', ' ')

    return double_white_space


def normalisasi(sms):
    token = nltk.word_tokenize(str(sms))
    normal_word = [calcDictDistance(item, 1) for item in token]

    return normal_word
