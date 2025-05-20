import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Apple 주가 시계열", layout="wide")
st.title("📈 Apple (AAPL) 주가 시계열 변화 - 최근 1년")

# 기간 설정
end = datetime.today()
start = end - timedelta(days=365)

# 데이터 다운로드
data = yf.download("AAPL", start=start, end=end)

if data.empty:
    st.error("❌ 데이터를 불러올 수 없습니다. 인터넷 연결 또는 Yahoo Finance 문제일 수 있어요.")
else:
    # 선 + 마커 시계열 그래프
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode='lines+markers',
        name="AAPL 종가",
        line=dict(color='royalblue', width=2),
        marker=dict(size=4)
    ))

    fig.update_layout(
        title="Apple (AAPL) 최근 1년간 종가 추이",
        xaxis_title="날짜",
        yaxis_title="주가 (USD)",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
