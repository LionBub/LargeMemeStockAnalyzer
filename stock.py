class Stock:
    def __init__(self, symbol, mentions) -> None:
        self.symbol = symbol
        self.mentions = mentions
        # we can get stock data from yfinance package
        # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

    def __str__(self) -> str:
        return f'{self.symbol} used {self.mentions} times'
