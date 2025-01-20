import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from yfinance_utils import YFinanceUtils  # Assuming this is a custom library for YFinance data retrieval
import datetime
from matplotlib import pyplot as plt


class TechnicalAnalyst:
    """
    This class performs technical analysis on OHLCV financial data.

    Attributes:
        data (pd.DataFrame): The OHLCV data for analysis.
        analysis_period (int): The number of periods to consider for analysis.
    """

    def __init__(self, data, analysis_period=20):
        """
        Initializes the TechnicalAnalyst class with OHLCV data and analysis period.

        Args:
            data (pd.DataFrame): DataFrame containing OHLCV data with columns:
                - 'Open'
                - 'High'
                - 'Low'
                - 'Close'
                - 'Volume'
                - 'Dividends' (optional)
                - 'Stock Splits' (optional)
            analysis_period (int): The number of periods to consider for analysis (default: 20).
        """

        self.data = data.copy()  # Avoid modifying the original data
        self.analysis_period = analysis_period

    def technical_analysis_commentary(self):
        """
        Generates a list of technical analysis commentaries based on the OHLCV data.

        Returns:
            list: List of commentary strings.
        """

        commentaries = []

        # Calculate indicators
        self.calculate_indicators()

        # Trend analysis
        if self.data['Close'][-1] > self.data['SMA_20'][-1] and self.data['Close'][-1] > self.data['EMA_50'][-1]:
            commentaries.append("Price is above both the 20-period and 50-period moving averages, suggesting an uptrend.")
        elif self.data['Close'][-1] < self.data['SMA_20'][-1] and self.data['Close'][-1] < self.data['EMA_50'][-1]:
            commentaries.append("Price is below both the 20-period and 50-period moving averages, suggesting a downtrend.")
        else:
            commentaries.append("Price is crossing or near the moving averages, indicating potential trend reversal.")

        # Momentum analysis
        if self.data['RSI'][-1] > 70:
            commentaries.append("RSI is above 70, indicating overbought conditions.")
        elif self.data['RSI'][-1] < 30:
            commentaries.append("RSI is below 30, indicating oversold conditions.")

        # MACD analysis
        if self.data['HIST'][-1] > 0:
            commentaries.append("MACD histogram is positive, suggesting bullish momentum.")
        elif self.data['HIST'][-1] < 0:
            commentaries.append("MACD histogram is negative, suggesting bearish momentum.")

        # Pattern recognition (basic)
        if self.data['Close'][-1] > self.data['Open'][-1]:
            commentaries.append("Price closed higher than the open, indicating bullish pressure.")
        elif self.data['Close'][-1] < self.data['Open'][-1]:
            commentaries.append("Price closed lower than the open, indicating bearish pressure.")

        return commentaries

    def calculate_indicators(self):
        """
        Calculates technical indicators (SMA, EMA, RSI, MACD) on the OHLCV data.
        """

        # Simple Moving Average (SMA)
        self.data['SMA_20'] = self.data['Close'].rolling(window=self.analysis_period).mean()

        # Exponential Moving Average (EMA)
        def ema(data, period):
            weights = np.exp(np.linspace(-1., 0., period))
            weights /= weights.sum()
            y = np.convolve(data, weights)[period - 1 :]
            y[:period] = y[period]
            return y

        self.data['EMA_50'] = ema(self.data['Close'], self.analysis_period) 

        # Relative Strength Index (RSI)
        def rsi(data, period):
            delta = data.diff()
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
            roll_up1 = up.rolling(period).mean()
            roll_down1 = down.abs().rolling(period).mean()
            RS = roll_up1 / roll_down1
            RSI = 100.0 - (100.0 / (1.0 + RS))
            return RSI

        self.data['RSI'] = rsi(self.data['Close'], self.analysis_period) 

        # Calculate MACD using Savgol filter for smoother signals
        # This is a simplified approximation, adjust parameters as needed
        self.data['MACD'] = self.data['Close'].ewm(span=12).mean() - self.data['Close'].ewm(span=26).mean()
        self.data['SIGNAL'] = savgol_filter(self.data['MACD'], window_length=9, polyorder=2)
        self.data['HIST'] = self.data['MACD'] - self.data['SIGNAL']

    def change_analysis_period(self, new_period):
        """
        Changes the analysis period for subsequent calculations.

        Args:
            new_period (int): The new number of periods to consider for analysis.
        """
        self.analysis_period = new_period
        self.calculate_indicators() 

if __name__ == "__main__":
    # Load your OHLCV data into a pandas DataFrame
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=180)
    ticker_data = YFinanceUtils("AAPL")
    data = ticker_data.get_ticker_data(start_date, end_date)

    ta = TechnicalAnalyst(data, 90)
       
    commentaries = ta.technical_analysis_commentary()
    for commentary in commentaries:
        print(commentary)