import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit 페이지 설정
st.set_page_config(page_title="삼성전자 주가 추세", layout="wide")
st.title("📈 삼성전자 (005930.KS) 최근 1년간 주가 추세")

# 날짜 범위 설정
end = datetime.today()
start = end - timedelta(days=365)

# 삼성전자 주식 데이터 불러오기
ticker = "005930.KS"
data = yf.download(ticker, start=start, end=end)

# 데이터 유효성 확인
if data.empty:
    st.error("❌ 데이터를 불러오지 못했습니다. 인터넷 연결 또는 Yahoo Finance 문제일 수 있습니다.")
else:
    # 선 그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines+markers',
        name="삼성전자 종가",
        line=dict(color='blue', width=2),
        marker=dict(size=3)
    ))

    fig.update_layout(
        title="삼성전자 주가 추세 (최근 1년)",
        xaxis_title="날짜",
        yaxis_title="종가 (KRW)",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
