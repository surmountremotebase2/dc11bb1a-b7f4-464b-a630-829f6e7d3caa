from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, OHLCV
from datetime import datetime, timedelta

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the investment universe to S&P 500 stocks
        self.tickers = self.get_sp500_tickers()
        self.data_list = [OHLCV(ticker) for ticker in self.tickers]
        self.rebalance_period = 30  # days
        self.last_rebalance_date = None  # to track last rebalance date

    def get_sp500_tickers(self):
        # This method would fetch the current list of S&P 500 tickers
        # In a real scenario, this might be replaced with a call to an API or a static file providing this information
        return ["AAPL", "MSFT", "AMZN", "FB", "GOOGL", "..."]  # This should contain all SP500 tickers

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def should_rebalance(self, current_date):
        if self.last_rebalance_date is None or (current_date - self.last_rebalance_date).days >= self.rebalance_period:
            return True
        return False

    def run(self, data):
        current_date = datetime.now().date()
        if not self.should_rebalance(current_date):
            return TargetAllocation({})  # No rebalancing needed
        
        performance = {}
        for ticker in self.tickers:
            historical = data["ohlcv"].get(ticker, [])
            if len(historical) >= 30:
                price_30_days_ago = historical[-30]["close"]
                current_price = historical[-1]["close"]
                performance_percent = ((current_price - price_30_days_ago) / price_30_days_ago) * 100
                performance[ticker] = performance_percent
        
        # Sort tickers by worst performance
        sorted_performance = sorted(performance.items(), key=lambda x: x[1])

        # Select 10 worst performers
        worst_performers = sorted_performance[:10]
        
        # Calculate the target allocation
        allocation_dict = {ticker: 1.0/len(worst_performers) for ticker, _ in worst_performers}
        
        # Record the rebalance date
        self.last_rebalance_date = current_date
        
        return TargetAllocation(allocation_dict)