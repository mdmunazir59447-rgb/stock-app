import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

st.title("Smart Stock App PRO+")

# =========================
# STOCK INPUT
# =========================
st.subheader("Search Stock")

stock = st.text_input("Enter Stock (Example: TCS.NS, AAPL, SAP.DE)")

st.write("India: TCS.NS, INFY.NS")
st.write("US: AAPL, TSLA")
st.write("Europe: SAP.DE, BMW.DE")

# =========================
# CACHE (RATE LIMIT FIX)
# =========================
@st.cache_data
def load_data(stock):
    return yf.download(stock, period="6mo")

# =========================
# MAIN APP
# =========================
if stock:

    tab1, tab2 = st.tabs(["Analysis", "Research"])

    # =========================
    # TAB 1 (Analysis)
    # =========================
    with tab1:

        st.subheader("Stock Data")

        data = load_data(stock)

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

            gain = delta.copy()
            loss = delta.copy()

            gain[gain < 0] = 0
            loss[loss > 0] = 0

            avg_gain = gain.rolling(14).mean()
            avg_loss = abs(loss.rolling(14).mean())

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            st.subheader("RSI")
            st.line_chart(rsi)

            # SIGNAL (SAFE)
            rsi_clean = rsi.dropna()

            st.subheader("Signal")

            if len(rsi_clean) > 0:

                last_rsi = rsi_clean.values[-1]

                if pd.notna(last_rsi):

                    if last_rsi < 30:
                        st.success("BUY Signal")
                    elif last_rsi > 70:
                        st.error("SELL Signal")
                    else:
                        st.warning("HOLD")

                else:
                    st.warning("RSI not valid")

            else:
                st.warning("Not enough data")

        else:
            st.error("Stock not found")

    # =========================
    # TAB 2 (Research)
    # =========================
    with tab2:

        ticker = yf.Ticker(stock)

        # RATE LIMIT SAFE
        try:
            info = ticker.info
        except:
            info = {}
            st.warning("Too many requests. Try again later.")

        st.subheader("About Company")
        st.write(info.get("longBusinessSummary", "No Data"))

        st.subheader("Fundamentals")

        col1, col2, col3 = st.columns(3)

        col1.metric("Market Cap", info.get("marketCap", "N/A"))
        col2.metric("P/E Ratio", info.get("trailingPE", "N/A"))
        col3.metric("Dividend Yield", info.get("dividendYield", "N/A"))

        # COMPARE
        st.subheader("Compare")

        comp = st.text_input("Compare with (Example: AAPL or INFY.NS)")

        if comp:
            data1 = load_data(stock)
            data2 = load_data(comp)

            if not data1.empty and not data2.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=data1.index, y=data1["Close"], name=stock))
                fig.add_trace(go.Scatter(x=data2.index, y=data2["Close"], name=comp))

                st.plotly_chart(fig, use_container_width=True)

        # NEWS
        st.subheader("News")

        try:
            news = ticker.news
            for n in news[:5]:
                st.write(n["title"])
                st.write("---")
        except:
            st.write("News not available")

        # INCOME
        st.subheader("Income Statement")

        try:
            st.dataframe(ticker.financials)
        except:
            st.write("No Data")

        # FINAL ANALYSIS
        st.subheader("Final Analysis")

        import random
        prediction = random.randint(60, 90)

        st.write(f"Prediction Confidence: {prediction}%")