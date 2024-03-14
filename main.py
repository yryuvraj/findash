import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np 
import plotly.express as px

st.title("FinDash")
ticker = st.sidebar.text_input("Enter Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

data = yf.download(ticker, start=start_date, end=end_date)

fig = px.line(data, x=data.index, y=data['Adj Close'], title="Time Series with Rangeslider")
st.plotly_chart(fig)

pricing_data, fundatmental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "News"])

with pricing_data:
    st.header("Price Movements")
    st.write("Highs and Lows, with proper rich data from Yahoo Finance API")
    data2 = data
    data2['%Change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    st.write(data2)
    
    annual_return = data2['%Change'].mean() * 252 * 100 
    # ignoring holidays-kyuki investor ko pagal banana hai (logic behind 252)
    st.write(f"Annual Return: ", annual_return, "%")
    
    stddev = np.std(data2['%Change'])*np.sqrt(252)*100
    st.write("Volatility or Standard Deviation is:", stddev, "%")
    st.write("Risk Adjusted Return: Sharpe Ratio : ", annual_return/stddev, "%")
    
with fundatmental_data:
    st.write("Fundamental Data")

from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment: {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment: {news_sentiment}')
        
    