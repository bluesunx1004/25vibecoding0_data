import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="주가 그래프", layout="wide")
st.title("📈 Apple (AAPL) 최근 1년간 주가 그래프")

# 기간 설정
end = datetime.today()
start = end - timedelta(days=365)

# 주식 데이터 불러오기
data = yf.download("AAPL", start=start, end=end)

# 데이터 확인
if data.empty:
    st.error("❌ 데이터를 가져오지 못했습니다.")
    st.write("Yahoo Finance 접근 실패 또는 인터넷 문제일 수 있어요.")
else:
    # Plotly 그래프 그리기
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], mode='lines', name='AAPL'))
    fig.update_layout(
        title="Apple (AAPL) 주가 (최근 1년)",
        xaxis_title="날짜",
        yaxis_title="종가 (USD)",
        template="plotly_white",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
