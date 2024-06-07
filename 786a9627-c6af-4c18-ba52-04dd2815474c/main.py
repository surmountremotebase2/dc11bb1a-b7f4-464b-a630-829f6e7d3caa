from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # List of stock tickers to consider for the strategy
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]
        # Preparing data requirement: OHLCV data for each ticker
        self.data_list = [OHLCV(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        # Setting data interval to daily for analyzing the previous day's open-close performance
        return "1day"

    @property
    def assets(self):
        # Strategy will consider assets specified in