import csv
import random
import nltk

results = {}
with open('restaurants.csv', newline='') as restaurants:
    curline = csv.reader(restaurants)
    next(curline)
    reviews = dict(curline)

dict_review_token = dict()

def update_dict(dict) :
    for singe_review in reviews.keys() :
        for tokens in nltk.word_tokenize(singe_review, language='english') :
            dict.update({tokens:0})



def get_radom_restaurants(sum_rating) :
    (r_restaurants, r_rate) = random.choice(list(reviews.items()))
    while (abs(sum_rating + float(r_rate) - 2.75) > 10) :
        (r_restaurants, r_rate) = random.choice(list(reviews.items()))
    return (r_restaurants,r_rate)

def update_token_file() :
    with open('token.csv', 'w', newline='') as f:
        fieldnames = ['token', 'value']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = [dict(zip(fieldnames, [key, value])) for key, value in dict_review_token.items()]
        writer.writerows(data)


def read_token_file() :
    new_token = dict()
    with open('token_naive.csv', newline='') as tokens:
        curline = csv.reader(tokens)
        next(curline)
        new_token = dict(curline)
    return new_token


def adjust_token(k) :
    ratingsum = 0
    for i in range (0, k+1) :
        num = 0
        sum = 0
        cur_tokendict = dict()
        (curreview, scurrating) = get_radom_restaurants(ratingsum)
        currating = float(scurrating)
        tokens_curreview = nltk.word_tokenize(curreview, language='english')
        for token in tokens_curreview :
            num = num + 1
            if token in cur_tokendict :
                cur_tokendict[token] += 1
            else :
                cur_tokendict.update({token:1}) 
            sum = sum + dict_review_token[token]
        gradient = (currating - sum) / num
        ratingsum += currating - 2.75 
        for token in cur_tokendict.keys() :
            dict_review_token[token] += gradient * cur_tokendict[token]
        if (int(i/10) == i/10) :
            update_token_file()
    
def rating_guess(str):
    guessd_rate = 0
    strtoken = nltk.word_tokenize(str, language='english')
    n = len(strtoken)
    m = n
    for token in strtoken:
        if (token in dict_review_token) :
            guessd_rate += dict_review_token[token]
        else :
            m = m - 1
    return guessd_rate * n / m

dict_review_token = read_token_file()

update_dict(dict_review_token)
update_token_file()
adjust_token(1000)


print (rating_guess("I would give a doing five if I could."))


## 