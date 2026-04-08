import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")

st.title("📈 Smart Stock App LIVE 🔴")

# ===== AUTO REFRESH =====
refresh_rate = st.sidebar.slider("Refresh Time (sec)", 2, 30, 5)

# ===== STOCK SELECT =====
stocks = {
    "TCS": "TCS.NS",
    "Reliance": "RELIANCE.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Apple": "AAPL",
    "Tesla": "TSLA"
}

stock_name = st.selectbox("Select Stock", list(stocks.keys()))
ticker = stocks[stock_name]

# ===== DATA =====
data = yf.download(ticker, period="1d", interval="1m")

if data.empty:
    st.error("No data found!")
    st.stop()

data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

# ===== LIVE PRICE =====
latest_price = data['Close'].iloc[-1]
st.metric("💰 Live Price", f"₹ {round(latest_price,2)}")

# ===== MOVING AVERAGES =====
ma20 = data['Close'].rolling(20).mean()
ma50 = data['Close'].rolling(50).mean()

# ===== CHART =====
st.subheader("📊 Live Chart")

fig = go.Figure()

# Candlestick
fig.add_trace(go.Candlestick(
    x=data.index,
    open=data['Open'],
    high=data['High'],
    low=data['Low'],
    close=data['Close'],
    name="Price"
))

# MA
fig.add_trace(go.Scatter(x=data.index, y=ma20, line=dict(width=2), name="MA20"))
fig.add_trace(go.Scatter(x=data.index, y=ma50, line=dict(width=2), name="MA50"))

# Volume
fig.add_trace(go.Bar(
    x=data.index,
    y=data['Volume'],
    name="Volume",
    yaxis="y2",
    opacity=0.3
))

fig.update_layout(
    template="plotly_dark",
    yaxis2=dict(overlaying='y', side='right')
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ===== RSI =====
st.subheader("📉 RSI")

delta = data['Close'].diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()
avg_loss[avg_loss == 0] = 0.0001

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

st.line_chart(rsi)

# ===== SIGNAL =====
st.subheader("🚀 Signal")

if rsi.iloc[-1] > 70:
    st.error("SELL 🔴")
elif rsi.iloc[-1] < 30:
    st.success("BUY 🟢")
else:
    st.warning("HOLD ⚖️")

# ===== AUTO REFRESH LOOP =====
time.sleep(refresh_rate)
st.rerun()