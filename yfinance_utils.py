import yfinance as yf


class YFinanceUtils:
    def __init__(self, ticker_symbol: str):
        self.ticker_symbol = ticker_symbol
        self.ticker_data = yf.Ticker(ticker_symbol)
        self.ticker_info = self.ticker_data.info
        self.ticker_calender = self.ticker_data.calendar
        self.ticker_analyst_price_targets = self.ticker_data.analyst_price_targets
        self.ticker_quarterly_income_stmt = self.ticker_data.quarterly_income_stmt

    def get_ticker_data(self, start_date: str, end_date: str, period: str="1d"):
        return self.ticker_data.history(period='1d', start=f"{start_date}", end=f"{end_date}")

    def get_ticker_info(self):
        return self.ticker_info

    def get_ticker_calender(self):
        return self.ticker_calender

    def get_ticker_analyst_price_targets(self):
        return self.ticker_analyst_price_targets

    def get_ticker_quarterly_income_stmt(self):
        return self.ticker_quarterly_income_stmt