import re
import csv
import nltk
import ast
import math



def read_token_bayes():
    token_bayes = dict()
    with open('token_Bayes.csv', newline='') as tokens:
        curline = csv.reader(tokens)
        next(curline)
        for row in curline:
            token_bayes[row[0]]= ast.literal_eval(row[1])
    return token_bayes

def read_review(single_review) :
    predict = dict()
    for tokens in nltk.word_tokenize(single_review, language='english') :
        tokens = tokens.replace(".","")
        tokens = tokens.replace("-","")
        tokens = tokens.replace("'","")
        tokens = tokens.replace("\"","")
        tokens = tokens.replace("'","")
        tokens = tokens.replace(".","")
        tokens = tokens.lower()
        tokens = str(tokens.encode(encoding="utf-8", errors="ignore"))
        if tokens not in token_bayes:
            continue
        #if sum(token_bayes[tokens]) < 10:
        #    continue
        switch = 0
        for i in range(0,9,2):
            if token_bayes[tokens][i] == 0: switch = 1
        if switch == 1: continue
        if not tokens in predict:
            predict[tokens]= 0
        predict[tokens] += 1
    return predict

def get_review(token, index):
    return token_bayes[token][index]

def analyze_token():
    row_sum = dict()
    col_sum = [0,0,0,0,0,0,0,0,0]
    for i in range(0, 9):
        col_sum[i] = 0
    token_sum = 0
    for token in token_bayes.keys():
        row_sum[token] = sum(token_bayes[token])
        token_sum += row_sum[token]
        for i in range(0, 9):
            col_sum[i] += token_bayes[token][i]
    return [row_sum, col_sum, token_sum]


def review_evaluator(single_review):
    review_dict = read_review(single_review)
    [row_sum, col_sum, token_sum] = analyze_token()
    rating = 0
    S = 0
    for j in range(0,9,2):
        C = 1
        for token in review_dict:
            #print("{0}, {1}".format(j, get_review(token, j)))
            temp_c = C * (get_review(token, j) / col_sum[j])**(review_dict[token])
            if (temp_c == 0): 
                #print(token)
                #print(j)
                #temp_c = 0.1 * C
                continue
            C=temp_c
        D = col_sum[j]
        S += C*D

    for i in range(0,9,2):
        A = 1
        for token in review_dict:
            A *= (get_review(token, i) / col_sum[i])**(review_dict[token])
        B = col_sum[i]
        pi = A * B / S
        rating += pi * (i*0.5+1)
    
    print(rating)
    return rating

def review_evaluator_lines(str):
    los = str.split(".")
    r = 0
    leng = 0
    for lines in los:
        if len(lines) == 0: continue
        leng += 1
        cr = review_evaluator(lines)
        print("{0}*****:{1}".format(lines,cr))
        #print(cr)
        r += cr
    r = r / leng
    print("r={0}".format(r))
## token_bayes = dict() token_bayes = read_token_bayes()   print((analyze_token())[0]["b'this'"])

token_bayes = dict()
token_bayes = read_token_bayes()
##review_evaluator("For people who are new to poke bowls, think about a burrito and burrito bowl, its literally a deconstructed sushi roll. I had the umami bowl here expecting it to hit me with umami, however i felt a little let down with how bland everything was. The salmon and tuna didnt have much taste and the texture was a bit off. In addition, each bowl is quite expensive averaging around $12 before tax. I felt like maybe i had an off day and went back to try their umami bowl again and it was pretty much the same, i do enjoy poke bowls usually but i feel like this place is missing something. On the plus side its a quaint store and the bowl looks really nice and you dont feel too guilty eating it if youre trying to eat a little healthier")
##review_evaluator("Went here for a girl's brunch. Service was great, and I like that she kept our coffees topped up regularly. My girlfriend ordered a mimosa at like 10:49 and the waitress brought it right at 11, the legally allowed time. Cinderella's mimosa.The prosciutto and goat cheese perogies were unpleasantly sour, although the Caesar salad was rich and rustic. Good hearty dressing and lots of anchovies, nice little crostinis instead of crummy cubed bread. Yeah, I really liked that salad. In a devastating twist, the Caesar cocktail I ordered was really bad and unfinishable. They'd put the devil's powder, aka that mass market crap known as 'Montreal steak spice, all around the rim. Blech. The drink itself was not very good; sort of tasted like the juice was a little old. I think they use Walters, which is yummy but has a short shelf life - maybe that was the cause? Anyway, if I don't finish a drink, it's not a good drink. This was not a good drink.")
##review_evaluator("Came here for an early dinner on a weekday; be warned, it gets really packed because the food is DANGEROUSLY GOOD! The best authentic Thai food that I've had in Toronto!I would actually give Pai a 4.5/5, only due to the slow service. The restaurant itself seats lots of people and does not have too many servers, so the service is actually quite slow (but still everyone was extremely nice and friendly). We got seated right away and did not need to wait the line since we were okay with a communal table, which was actually enjoyable since they separate your party and the party next to you by leaving an empty seat. We ordered the Chef Nuit Pad Thai with Chicken! It was so packed with flavour and the portion size was really good. It was a nice blend of both sweet and savoury, with the perfect amount of peanuts and coriander. I'm excited to come back soon to try more food from their menu!")
##review_evaluator_lines("The food is really good, especially the curries. The green curry is a must try (Penang curry), the cocktails are very good but the best thing about this place is the decor and ambiance and atmosphere. The reason why I am giving it one star, when it should really get a 5 star is the personal experience I had. I told our server 2,3 times that I am extremely allergic to shrimp, that it'll kill me if there is shrimp in my food, and asked her to note it down. When she brought my checked curry it was filled with actual shrimp. But since the coconut shell was filled with the coconut milk and the broth, I couldn't see the shrimps and it was possible that I eat the broth and be dead by now!!! Luckily, before I start my food, I asked my friend to try some of my curry and then he realized there is shrimp in my food, just when I was about to eat it!!!! Now I would have been dead because the server made a mistake but the worst part was the restaurant management! Not only it took them 30 min to bring me another chicken curry , but also they even charged me for it!!! Everyone on our table finished their food and were waiting for me meal to arrive! I think I made a mistake by not making it a big deal... I felt bad for the server so I kept saying, it's ok, it's ok don't worry, thank God I'm still alive and .... but the least management should have done is to serve that food complementary, like any other food establishment would have done this .... the min they should have done.Pai was my fav place and I used to go there at least 2,3 times a month but after this behavior not only I am not going , but my friends also decided not to go there again. I think it was so inconsiderate of the management (who came to my table to ask about my allergy after the incident), but ultimately went and charged me for the whole thing... the super late food, the drink and ....So disappointing .... some practices are just industry's norms.... maybe an experienced manager would have know that they should have not charged me or had to offer something as an apology....")
##review_evaluator("typical core downtown restaurant where prices and quality don't usually match. pad thai was very plain. when i looked at the dish, there was about 95% noodles, 3% bean sprouts and remainder was meat. tomyum soup tasted only tomatoes, lots of tomatoes. the high chairs were not comfortable at all. I didnt find the quality of the food justified the money I pay for.")
##review_evaluator("I'm not sure how much worse food + customer service can get in this Waterloo Plaza until I tried this restaurant...Food was EXTREMELY salty. I really cant comment on the flavour of the food because all I could taste was salt. I had no idea what was going on with my food because I was too busy chugging water.After we were done, I paid for the food, sat back to my table to drink more water. When we were leaving, the girl/lady who took my $$ yelled at my REALLY LOUDLY, accusing me of not paying in an EXTREMELY rude manner. I told her I paid and reached into my pocket for the receipt. She let me go after I presented her with the receipt I had. I don't know what would've happened if I didnt' take my receipt..... Ironically, the restaurant wasn't even full.I laughed at this incident with couple of my friends, and apparently it has happened to more than one of them.")
##review_evaluator("This is my 6th year dining out at the campus plaza and this restaurant is really the new low of how bad the customer service can be. I was surprised the waitress rolled her eyes at me for asking for a menu and a glass of water. I had to seat myself after coming into the restaurant and was ignored by the staffs for 10+ minutes. The response to my request was I did not see you sitting there" and "I asked you if you want water you did not answer me. Glad I made the choice to walk out of the restaurant before ordering anything because I learned from the rest of the reviews that the rude waitress is probably the owners daughter that likes to insult everyone and will demand a 15% tip or tell you to GTFU. ")
##review_evaluator_lines("Went to Seoul Soul with a friend today. Food was ok. First of all, the waiter forgot to gave us water for like a full 10 min until i asked for it. The place wasn't even busy. The wait just stood at the cash registry. Then we headed up to pay for food, my friend forgot to tip so the lady at the cash registry (who clearly looks like the owner) told him the money he paid does not include tip (basically hint hint you didn't give us tip!!), so my friend threw his change in the tipping jar. Despite the fact that the service was only ok and tbh the place wasn't anything fancy, i still gave a small tip. What happened next was kind of  bizarre. The lady pointed to the receipt and said you are suppose to give a 10% tip in an unpleasant and incredibly self righteous tone, which i thought was just incredibly rude. The point of a tip is that it's optional and entirely up to the customer. If your place wasn't even that great why should i pay a bigger amount than what i think the place deserve? If you think that your place deserve a mandatory 10% tip you might as well just put up a sign on the door that says we don't serve people who doesn't give 10% tip or add that tip amount to the cost of the food. You are already making tons of money off of the food.")
##review_evaluator_lines("I really enjoyed my experience at this place! I was a little skeptical wen I first arrived as the lights were way too bright and the decor was a little cheesy. But our waitress was an absolute doll! Her name was Molly and she was so attentive and helpful. They were out of the wine we wanted but she suggested an alternative that went really well with our chicken and waffles. The food was good, but the service was why I'll be back to this spot.")
##review_evaluator_lines("Pai was my fav place and I used to go there at least 2,3 times a month but after this behavior not only I am not going , but my friends also decided not to go there again.")
##review_evaluator("I love this restaurant so much!!!!I love this restaurant so much!!!!I love this restaurant so much!!!!I love this restaurant so much!!!!I love this restaurant so much!!!!I love this restaurant so much!!!!I love this restaurant so much!!!!")
#review_evaluator_lines("During a visit from out of town, we went to GTS twice in one week to try out their interesting cocktails and get a taste of their twist on southern food. Both times we had great experiences both with our service and our tastebuds! They have a wide variety of craft cocktails, presented on the menu into taste categories. While I didn't enjoy the two I tried (Hurricane and Friendly Traveller) as much as I expected, my partner loved the two (Toadvine and the Humidor) he tried, so depending on your taste you may or may not find a new favourite. The food was delicious, but a little on the pricey side (ex. $19 for Chicken & Waffles). We absolutely loved the alligator nuggets, the scotch egg, the gumbo, and the house Caesar salad! Great atmosphere, great service, and a cocktail menu which is sure to keep you on your toes - we'll be back!")
review_evaluator_lines("Never order the duck. Seriously lacking in flavour. Duck is supposed to be crispy and gooey and fatty and just a little pink.What I got was bland and dry and grey. Seriously underwhelming. There was a hint of sauce that could have redeemed this lack of taste, but sadly they used only a small amount which left me with roughly 3 flavourful bites.The next thing that bugged me is they closed an hour early. The website says 10. The door says 10. The girl says at 8:40 Take-out only, we close at 9. I'm sure she meant Due to an emergency we're closing an hour early. Hope everything works out.Just kidding, I know they just wanted to leave.It's a real shame, too. This is just the type of place I'm always trying to fall in love with. Modern takes on traditional ethnic foods. My kinda hipster fun. I might try them again. Maybe the pork belly is better. I will post an updated review if I ever convince myself to go again.Maybe I will tell them to go bonkers with the sauces and spices. Maybe they profiled me based on my race and assumed I wanted Kraft Dinner and Hot Dogs. I drove 20 minutes to try that sandwich.I want gas money.")
##review_evaluator_lines("Other than the smell that is constantly staining my clothes, this place is an hidden gem in the tiny city of Waterloo. I love how they incorporate foods from different cultures into the filling of their bao.My faves are the dynasty duck and the 5 spice belly. The pork belly is cooked to perfection by being seasoned and juicy. The dynasty duck is also delicious and well seasoned. Come check this place out, it's entrance is facing the inside plaza of condos.")

