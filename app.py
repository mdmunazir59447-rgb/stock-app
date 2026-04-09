import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

st.title("📈 Smart Stock App PRO")

stock = st.text_input("Enter Stock (Example: TATAMOTORS.NS)")

if stock:
    ticker = yf.Ticker(stock)
    info = ticker.info
    data = ticker.history(period="1y")

    if not data.empty:

        # =========================
        # 🔥 TOP SECTION (PRICE)
        # =========================
        price = info.get("currentPrice", 0)
        prev_close = info.get("previousClose", 0)

        change = price - prev_close
        percent = (change / prev_close) * 100 if prev_close != 0 else 0

        col1, col2 = st.columns([2,1])

        with col1:
            st.subheader(f"{stock}")
            st.markdown(f"### ₹ {price} ({round(change,2)} / {round(percent,2)}%)")

        with col2:
            st.write("🕒 Time:", datetime.now().strftime("%H:%M:%S"))
            st.write("🏢 Exchange:", info.get("exchange", "N/A"))

        st.divider()

        # =========================
        # 📊 CHART SECTION
        # =========================
        st.subheader("📊 Price Chart")
        st.line_chart(data["Close"])

        st.divider()

        # =========================
        # 📈 DETAILS SECTION
        # =========================
        col1, col2, col3 = st.columns(3)

        # Previous Close
        col1.metric("Previous Close", prev_close)

        # Day Range
        day_low = info.get("dayLow", 0)
        day_high = info.get("dayHigh", 0)
        col2.metric("Day Range", f"{day_low} - {day_high}")

        # Year Range
        year_low = info.get("fiftyTwoWeekLow", 0)
        year_high = info.get("fiftyTwoWeekHigh", 0)
        col3.metric("52 Week Range", f"{year_low} - {year_high}")

        st.divider()

        # =========================
        # 💼 EXTRA INFO
        # =========================
        col1, col2, col3 = st.columns(3)

        col1.metric("Market Cap", info.get("marketCap", "N/A"))
        col2.metric("Avg Volume", info.get("averageVolume", "N/A"))
        col3.metric("P/E Ratio", info.get("trailingPE", "N/A"))

        col1.metric("Dividend Yield", info.get("dividendYield", "N/A"))

    else:
        st.error("Invalid Stock or No Data Found")
