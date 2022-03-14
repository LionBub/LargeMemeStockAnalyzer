import redditPraw
import json


def printStockObjList():
    for stk in redditPraw.stockObjectsList:
        print(stk)


def printRedditData():
    numSubmissions = 0
    for submission in redditPraw.reddit.subreddit('wallstreetbets').hot(limit=400):
        print(submission.title)
        numSubmissions += 1

    print(f'\n{numSubmissions} posts searched')


def printStocksListJSON():
    print(json.load(open("StocksList.json", "r")))


def printOrderedStockObjList():
    for stk in redditPraw.InsertionSortStocksList(redditPraw.stockObjectsList):
        print(stk)


def updateMentionsOfStocks():
    redditPraw.findMentionsInSubmissions()


def updateStockJSON():
    redditPraw.updateStockJSON()


def clearStockJSON():
    redditPraw.clearStockJSON()


clearStockJSON()
#  updateMentionsOfStocks()
#  updateStockJSON()
#  printStocksListJSON()
#  printStockObjList()
printOrderedStockObjList()
#  printRedditData()
