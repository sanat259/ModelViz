import yfinance as yf
import streamlit as st
import pandas as pd
import datetime 
st.title("Stock Market Analysis")

#st.sidebar.title("Stock Market Analysis")

# Later create yfinance utils
ticker_symbol = st.text_input("Enter ticker symbol", "AAPL")

col1, col2 = st.columns(2)
start_date = None
end_date = None
with col1:
    st.write("Enter start date")
    start_date = st.date_input("Start date", datetime.date(2023, 1, 1))

with col2:
    st.write("Enter End date")
    end_date = st.date_input("End date", datetime.date.today())

ticker_data = yf.Ticker(ticker_symbol)
ticker_info= ticker_data.info
ticker_calender = ticker_data.calendar
ticker_analyst_price_targets = ticker_data.analyst_price_targets
ticker_quarterly_income_stmt = ticker_data.quarterly_income_stmt
ticker_hist_df = ticker_data.history(period='1d', start=f"{start_date}", end=f"{end_date}") 
#ticker_data.option_chain(ticker_data.options[0]).calls

st.write(f"Showing ticker info for: {ticker_symbol}")

st.dataframe(ticker_hist_df)

col1, col2 = st.columns(2)
with col1:
    st.header("Volume")
    st.line_chart(ticker_hist_df["Volume"])

with col2:
    st.header("Close Price")
    st.line_chart(ticker_hist_df["Close"])