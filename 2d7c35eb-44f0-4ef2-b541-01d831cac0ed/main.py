from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
import numpy as np

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]  # Tickers of interest
        self.data_list = [OHLCV(i) for i in self.tickers]  # Getting historical data for each ticker

    @property
    def interval(self):
        return "1day"  # Daily data

    @property
    def assets(self):
        return self.tickers  # Assets we're trading

    @property
    def data(self):
        return self.data_list  # The data required for the strategy

    def run(self, data):
        worst_performance = None
        max_drop = 0

        # Calculate the drop percentage for each stock from open to close on the previous day
        for ticker in self.tickers:
            # Retrieve the two most recent trading days
            recent_data = data["ohlcv"][-2:][ticker]
            if len(recent_data) == 2:
                prev_day = recent_data[0]
                drop_pct = ((prev_day["close"] - prev_day["open"]) / prev_day["open"]) * 100
                
                # Identify the stock with the maximum drop
                if drop_pct < max_drop:
                    max_drop = drop_pct
                    worst_performance = ticker

        allocation_dict = {}
        # Allocate 100% to the worst-performing stock if identified, otherwise hold cash (0% allocation)
        if worst_performance is not None:
            allocation_dict[worst_performance] = 1.0  # Buy on the open
        else:
            # This means no trading signal was identified, or all stocks were positive/neutral from open to close
            for ticker in self.tickers:
                allocation_dict[ticker] = 0.0  # Hold position (in this case, it effectively means holding cash)
        
        return TargetAllocation(allocation_dict)