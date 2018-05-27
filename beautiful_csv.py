import ast
import csv
from nltk.stem.lancaster import LancasterStemmer 

def stemming(dic):
    result = dict()
    s = LancasterStemmer()
    for words in dic:
        if s.stem(words) in result:
            for i in range(0,9):
                result[s.stem(words)][i] += dic[words][i]
        else:
            result[s.stem(words)] = dic[words]
    return result

def read_token_bayes():
    token_bayes = dict()
    with open('beautiful_csv.csv', newline='') as tokens:
        curline = csv.reader(tokens)
        next(curline)
        for row in curline:
            #row[0] = row[0].split("'")[1]
            token_bayes[row[0]]= ast.literal_eval(row[1])
    return token_bayes

def update_token_file() :
    with open('beautiful_csv.csv', 'w', newline='') as f:
        fieldnames = ['token', 'list of numbers']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = [dict(zip(fieldnames, [key, value])) for key, value in dict_review_token.items()]
        writer.writerows(data)

dict_review_token = dict()

dict_review_token = read_token_bayes()

dict_review_token = stemming(dict_review_token)


update_token_file()