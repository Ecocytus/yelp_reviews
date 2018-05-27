import ast
import csv


def read_token_bayes():
    token_bayes = dict()
    with open('token_Bayes.csv', newline='') as tokens:
        curline = csv.reader(tokens)
        next(curline)
        for row in curline:
            row[0] = row[0].split("'")[1]
            a = row[0]
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

update_token_file()