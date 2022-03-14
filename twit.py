import tweepy
import pandas as pd
from stocksymbol import StockSymbol
from datetime import datetime, timedelta
import math

now = datetime.now()
thirty_minutes_before = now - timedelta(minutes = 30)

api_key = '623adca4-396e-4229-b867-f88fca59eba5'
ss = StockSymbol(api_key)

symbol_list_us = ss.get_symbol_list(market="US")

apikey ="K7U2lF2dwHZhjk8GoDygcPHWi"
apisecret ="h9yKjMY90x1qKLSdJf6XDghmj0dXYZKZztg172kcxU1EB0wk2w"
accesstoken ="1258080415300177922-mEHkrsqfYhXrBBlS130d6jjzus5ROb"
accesstokensecret="ndCcMrd4Y8Wx2gjGTkO0BO54uyUjTmvkHZkwXYyXi7zHf"

auth = tweepy.OAuthHandler(apikey, apisecret)
auth.set_access_token(accesstoken,accesstokensecret)
api = tweepy.API(auth)

ticklist = []
for index in range(len(symbol_list_us)):
    for key in symbol_list_us[index]:
        if index == "symbol":
            ticklist.append(symbol_list_us[index][key])
        else:
            pass

scoredict = {} # dictionary of the ticker symbols and their respective scores
for i in ticklist:
    scoredict[i] = None

likes = 0
num = 0
score = 0
def findtweets(query):
    for i in tweepy.Cursor(api.search_tweets, q=query, start_time= thirty_minutes_before).items(10):
        if len(i.full_text) > 0:
            num += 1
            likes = likes + i.favorite_count
            if likes == 0:
                score += 1
                scoredict[i] += score
            else:
                score = score + math.sqrt(likes) + 1
                scoredict[query] += score
        score = 0

for i in ticklist:
    findtweets(i)

