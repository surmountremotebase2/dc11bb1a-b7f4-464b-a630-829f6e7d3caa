from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a subset of S&P 500 tickers. In a real scenario, this list should be dynamically retrieved
        # to include the actual S&P 500 constituents.
        self.tickers = ["AAPL", "MSFT", "GOOGL", "FB", "AMZN", "NFLX", "NVDA", "TSLA", "BRK.B", "JPM", 
                        "V", "PG", "UNH", "HD", "MA", "DIS", "BAC", "XOM", "JNJ", "PFE"]
        self.rebalance_interval = 30  # days
        self.last_rebalance = None

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # The strategy uses daily data for calculating the EMA.
        return "1day"

    def run(self, data):
        current_date = data["ohlcv"][0][self.tickers[0]]["date"]  # Example to get current date from data
        if self.last_rebalance is None or (current_date - self.last_rebalance).days >= self.rebalance_interval:
            ema_values = {}
            for ticker in self.tickers:
                ema = EMA(ticker, data["ohlcv"], 30)  # Fetching 30-day EMA for each ticker
                if ema is not None and len(ema) > 0:
                    ema_values[ticker] = ema[-1]  # Get the most recent EMA value
            # Select top 10 tickers with highest EMA values
            selected_tickers = sorted(ema_values, key=ema_values.get, reverse=True)[:10]
            allocation = {ticker: 1.0/10 for ticker in selected_tickers}  # Equal allocation among selected tickers
            self.last_rebalance = current_date  # Update last rebalance date
            return TargetAllocation(allocation)
        else:
            return TargetAllocation({})  # No action if not a rebalance day