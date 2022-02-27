import praw
import stock

with open('pw.txt', 'r') as f:
    pw = f.read()
reddit = praw.Reddit(client_id='jwVLKWRrd3Rw9eCSojJz4w',
                     client_secret='8zkhCtiqMYfCeKpholGIaTq7MUYUKQ',
                     username='LionBub',
                     password=pw,
                     user_agent='prawstitute_v0.1')
subreddit = reddit.subreddit('wallstreetbets')

hot_python = subreddit.hot(limit=400)

knownErrors = {'A','ABOARD', 'BACK', 'BOYS', 'CALLS', 'CEO', 'CNBC', 'DIE', 'EU', 'G', 'GOING', 'HODL', 'HOW', 'I', 'J',
               'MARCH', 'MONEY', 'MOOOON', 'N', 'P', 'POV', 'REPOST', 'RIP', 'SEMI', 'STONKS', 'SWIFT', 'THIS', 'U',
               'US', 'WSB', 'WSJ', 'WWIII', 'YOLO', '$'}


# YOLO, A and I are companies but were marked as error due to overuse

def findStocks():
    capsList = []
    postIndex = -1
    for submission in hot_python:  # make array of all upper case sequences
        postIndex += 1
        # capsList = [char for char in submission.title if char.isupper()]
        charIndex = -1
        while charIndex < len(submission.title):
            charIndex += 1
            char = submission.title[charIndex: charIndex + 1]
            if char.isupper() or char == '$':
                lastChar = submission.title[charIndex - 1: charIndex]
                if lastChar.isupper() or lastChar == '$':
                    capsList[len(capsList) - 1] += char  # concats to exisitng item
                else:
                    nextChar = submission.title[charIndex + 1: charIndex + 2]
                    if not nextChar.islower():  # eliminates capitals at start of words
                        capsList.append(char)  # adds a new item
    print(f'{postIndex + 1} posts searched')

    suspectedStocksList = [s for s in capsList if len(s) <= 6]
    suspectedStocksSet = set(suspectedStocksList)
    suspectedStocksSet = suspectedStocksSet - knownErrors
    # counts and creates numMentions list
    numMentions = [0 for e in suspectedStocksSet]
    setIndex = -1
    for si in suspectedStocksSet:
        setIndex += 1
        for li in suspectedStocksList:
            if si == li:
                numMentions[setIndex] += 1

    # creates stock objects
    stockObjects = []
    setIndex = -1  # might be bad practice reusing this variable
    for name in suspectedStocksSet:
        setIndex += 1
        stockObjects.append(stock.Stock(name, numMentions[setIndex]))
    return stockObjects


for e in findStocks():
    if e.mentions > 1:
        print(str(e))
        # TO DO: order from greatest to least used
