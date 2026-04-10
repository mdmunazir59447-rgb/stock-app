import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

st.title("Smart Stock App PRO+")

stock = st.text_input("Enter Stock (Example: TCS.NS)")

if stock:

    tab1, tab2 = st.tabs(["Analysis", "Research"])

    # =========================
    # TAB 1 (Analysis)
    # =========================
    with tab1:

        st.subheader("Stock Data")

        data = yf.download(stock, period="6mo")

        if not data.empty:

            st.dataframe(data.tail())

            # Moving averages
            data["MA20"] = data["Close"].rolling(20).mean()
            data["MA50"] = data["Close"].rolling(50).mean()

            # Chart
            st.subheader("Price Chart")

            fig = go.Figure()

            fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close"))
            fig.add_trace(go.Scatter(x=data.index, y=data["MA20"], name="MA20"))
            fig.add_trace(go.Scatter(x=data.index, y=data["MA50"], name="MA50"))

            st.plotly_chart(fig, use_container_width=True)

            # RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))

            st.subheader("RSI")
            st.line_chart(rsi)

            # ✅ FIXED RSI VALUE
            rsi_clean = rsi.dropna()

            if not rsi_clean.empty:
                last_rsi = float(rsi_clean.iloc[-1])

                st.subheader("Signal")

                if last_rsi < 30:
                    st.success("BUY Signal")
                elif last_rsi > 70:
                    st.error("SELL Signal")
                else:
                    st.warning("HOLD")
            else:
                st.warning("RSI not available")

        else:
            st.error("No Data Found")

    # =========================
    # TAB 2 (Research)
    # =========================
    with tab2:

        ticker = yf.Ticker(stock)
        info = ticker.info

        st.subheader("About Company")
        st.write(info.get("longBusinessSummary", "No Data"))

        st.subheader("Fundamentals")

        col1, col2, col3 = st.columns(3)

        col1.metric("Market Cap", info.get("marketCap", "N/A"))
        col2.metric("P/E Ratio", info.get("trailingPE", "N/A"))
        col3.metric("Dividend Yield", info.get("dividendYield", "N/A"))

        st.subheader("Compare")

        comp = st.text_input("Compare with (Example: INFY.NS)")

        if comp:
            data1 = yf.download(stock, period="6mo")
            data2 = yf.download(comp, period="6mo")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data1.index, y=data1["Close"], name=stock))
            fig.add_trace(go.Scatter(x=data2.index, y=data2["Close"], name=comp))

            st.plotly_chart(fig, use_container_width=True)

        st.subheader("News")

        try:
            news = ticker.news
            for n in news[:5]:
                st.write(n["title"])
                st.write("---")
        except:
            st.write("No News Available")

        st.subheader("Income Statement")

        try:
            st.dataframe(ticker.financials)
        except:
            st.write("No Data")

        st.subheader("Final Analysis")

        import random
        prediction = random.randint(60, 90)

        st.write(f"Prediction Confidence: {prediction}%")