class Stock:
    def __init__(self, symbol, shortName, longName, exchange, market, mentions) -> None:
        self.symbol = symbol
        self.shortName = shortName
        self.longName = longName
        self.exchange = exchange
        self.market = market
        self.mentions = mentions
        self.data = None

        # we can get stock data from yfinance package
        # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

    def setStockData(self, data):
        self.data = data

    def addMention(self, n):
        self.mentions += n

    def __str__(self) -> str:
        return f'{self.symbol} used {self.mentions} times.'
