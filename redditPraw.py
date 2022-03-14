import praw
import json
import stock
from stocksymbol import StockSymbol

with open('pw.txt', 'r') as f:
    pw = f.read()
reddit = praw.Reddit(client_id='jwVLKWRrd3Rw9eCSojJz4w',
                     client_secret='8zkhCtiqMYfCeKpholGIaTq7MUYUKQ',
                     username='LionBub',
                     password=pw,
                     user_agent='prawstitute_v0.1')
subreddit = reddit.subreddit('wallstreetbets')
hot_python = subreddit.hot(limit=200)

stocksDict = json.load(open("StocksList.json", "r"))
stockObjectsList = []
for e in stocksDict:
    stockObjectsList.append(stock.Stock(symbol=e["symbol"],
                                        shortName=e["shortName"],
                                        longName=e["longName"],
                                        exchange=e["exchange"],
                                        market=e["market"],
                                        mentions=e["mentions"]
                                        ))


def clearStockJSON():
    ss_api_key = '623adca4-396e-4229-b867-f88fca59eba5'
    ss = StockSymbol(ss_api_key)
    symbol_list_us = ss.get_symbol_list(market="US")

    newStocksDict = symbol_list_us.copy()  # unnecessary
    for stk in newStocksDict:
        stk["mentions"] = 0
    json.dump(newStocksDict, open("StocksList.json", "w"))
    return newStocksDict  # Dict is the python interpretation of the JSON. The mailman


def updateStockJSON():
    newStocksDict = []
    for obj in stockObjectsList:
        newStocksDict.append(obj.__dict__)
    json.dump(newStocksDict, open("StocksList.json", "w"))


def findMentionsInSubmissions():
    capsList = []
    postIndex = -1
    for submission in hot_python:  # make array of all upper case sequences
        postIndex += 1
        # capsList = [char for char in submission.title if char.isupper()]
        charIndex = -1
        while charIndex < len(submission.title):
            charIndex += 1
            char = submission.title[charIndex: charIndex + 1]
            if char.isupper():
                lastChar = submission.title[charIndex - 1: charIndex]
                if lastChar.isupper():
                    capsList[len(capsList) - 1] += char  # concats to exisitng item
                else:
                    nextChar = submission.title[charIndex + 1: charIndex + 2]
                    if not nextChar.islower():  # eliminates capitals at start of words
                        capsList.append(char)  # adds a new item

    suspectedStocksList = [s for s in capsList if len(s) <= 5]
    stocksSet = set(suspectedStocksList)  # converts list to set, eliminating duplicates
    stocksSet = stocksSet.intersection()
    # counts and creates numMentions list
    numMentions = [0 for e in stocksSet]
    setIndex = -1
    for si in stocksSet:
        setIndex += 1
        for li in suspectedStocksList:
            if si == li:
                numMentions[setIndex] += 1

    # creates stock objects
    stockObjects = []
    setIndex = -1  # might be bad practice reusing this variable
    for name in stocksSet:
        setIndex += 1
        for stockFromObjList in stockObjectsList:
            if name == stockFromObjList.symbol:
                stockFromObjList.addMention(numMentions[setIndex])

    return stockObjectsList


def InsertionSortStocksList(refList):
    objlist = refList.copy()
    for i in range(1, len(objlist)):

        key = objlist[i]
        # Move elements of arr[0..i-1], that are greater than key, to one position ahead of their current position
        j = i - 1
        while j >= 0 and key.mentions < objlist[j].mentions:
            objlist[j + 1] = objlist[j]
            j -= 1
        objlist[j + 1] = key
    return objlist
