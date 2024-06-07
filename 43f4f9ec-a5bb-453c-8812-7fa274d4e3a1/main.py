from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker to trade
        self.ticker = "GME"

    @property
    def assets(self):
        # Return a list containing the asset we're trading
        return [self.ticker]

    @property
    def interval(self):
        # Set the interval for the data; "1day" for daily data
        return "1day"

    def run(self, data):
        # Check if there's enough historical data to analyze
        if len(data["ohlcv"]) < 2:
            # Not enough data to compare today's price with yesterday's
            log("Not enough data.")
            return TargetAllocation({})
        
        # Retrieve closing prices for the last two days
        yesterday_close = data["ohlcv"][-2][self.ticker]["close"]
        today_close = data["ohlcv"][-1][self.ticker]["close"]

        # Calculate the percentage change from yesterday to today
        percentage_change = (today_close - yesterday_close) / yesterday_close * 100

        # Determine action based on the percentage change
        if percentage_change >= 5:
            # If the stock rose 5% or more, allocate 100% of the portfolio to GME
            log("GME rose by 5% or more. Buying.")
            allocation_dict = {self.ticker: 1.0}
        elif percentage_change <= -5:
            # If the stock fell by 5% or more, sell all holdings in GME
            log("GME fell by 5% or more. Selling.")
            allocation_dict = {self.ticker: 0.0}
        else:
            # No action if the stock hasn't moved 5% in either direction
            log("No significant move. Holding position.")
            allocation_dict = {}

        return TargetAllocation(allocation_dict)