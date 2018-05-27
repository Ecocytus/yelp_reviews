from bs4 import BeautifulSoup
import urllib.request
import re
import csv
import nltk
import ast
from ultk.stem.lancaster import LancasterStemmer 


def read_toekn_bayes():
    token_bayes = dict()
    with open('token_Bayes.csv', newline='') as tokens:
        curline = csv.reader(tokens)
        next(curline)
        for row in curline:
            token_bayes[row[0]]= ast.literal_eval(row[1])
    return token_bayes

def stemming(dict):
    result = dict()
    s = LancasterStemmer()
    for words in dict:
        if s.stem(words) in result:
            for i in range(0,10):
                dict[s.stem(words)][i] += dict[words][i]
        else:
            result[words] = dict[words]
    return result

def update_dict(singe_review, rating) :
    s = LancasterStemmer()
    for tokens in nltk.word_tokenize(singe_review, language='english') :
        tokens = tokens.replace(".","")
        tokens = tokens.replace("-","")
        tokens = tokens.replace("'","")
        tokens = tokens.replace("\"","")
        tokens = tokens.replace("'","")
        tokens = tokens.replace(".","")
        tokens = tokens.lower()
        tokens = s.stem(tokens)
        tokens = str(tokens.encode(encoding="utf-8", errors="ignore"))
        if not tokens in dict_review_token:
            dict_review_token[tokens]= [0,0,0,0,0,0,0,0,0]
        (dict_review_token[tokens])[int(float(rating)/0.5-2)] += 1

def update_token_file() :
    with open('token_Bayes.csv', 'w', newline='') as f:
        fieldnames = ['token', 'list of numbers']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        data = [dict(zip(fieldnames, [key, value])) for key, value in dict_review_token.items()]
        writer.writerows(data)

def print_restaurant_info(url, startpag, startrev):
    headers ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    req = urllib.request.Request(url=url,headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    css_soup = BeautifulSoup(html, 'html.parser')
    loh = css_soup.find_all("div", class_="biz-page-header")
    hsoup = BeautifulSoup(str(loh[0]), 'html.parser')
    lov = hsoup.find_all("span", class_="review-count rating-qualifier")
    if (len(lov) != 0): 
        total_review = (((re.split("<.*span.*>", str(lov[0])))[1]).strip())[:-7]
    else:
        total_review = 0
        return 0
    for i in range(startpag, int((int(total_review))/20)+1):
        print('     current page is %d' %(i+1))
        url_review = url + "?start=" + str(20*i)
        req_review = urllib.request.Request(url=url_review,headers=headers)
        res_review = urllib.request.urlopen(req_review)
        html_review = res_review.read().decode('utf-8')
        css_soup_review = BeautifulSoup(html_review, 'html.parser')
        Total = css_soup_review.find_all("ul", class_="ylist ylist-bordered reviews")
        rsoup = BeautifulSoup(str(Total[0]), 'html.parser')
        loR = rsoup.find_all("div", class_="review review--with-sidebar")
        for j in range(startrev, len(loR)):
            review = loR[j]
            sreview = str(review)
            sreviewsoup = BeautifulSoup(sreview, 'html.parser')
            #rating
            lopicture = sreviewsoup.find_all("img", class_="offscreen")
            rating = str(lopicture[0])[10:13]
            #content
            locontent = sreviewsoup.find_all("p", lang="en")
            content = str(locontent[0])[13:-4]
            content = re.sub("<.*?br.*?>", " ", content)
            content = content.replace('\n', ' ')
            update_dict(content, rating)

restaurant_url = open("url.txt", "r")
lourl = restaurant_url.readlines() 
restaurant_url.close()
dict_review_token = dict()
i = 0
for url in lourl:
    url = url.strip()
    i = i + 1
    print("current url is: %s" %(url))
    per = i * 100 / 670
    print("we have done %f %%" %(per))
    dict_review_token = read_toekn_bayes() 
    print_restaurant_info(url,0,0)
    update_token_file()


#print_restaurant_info('http://www.yelp.ca/biz/red-house-waterloo', 0, 0)
