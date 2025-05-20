import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="주가 분석 앱", layout="wide")
st.title("📊 글로벌 주요 기업 주가 및 수익률 분석")

# 종목 목록
stock_list = {
    "삼성전자": "005930.KS",
    "Apple": "AAPL",
    "Google (Alphabet)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA"
}

# 사용자 입력
selected_stock = st.selectbox("📌 종목 선택", options=list(stock_list.keys()))
interval = st.radio("간격 선택", options=["주간", "월간"], horizontal=True)

# 간격에 따른 리샘플링 규칙
resample_rule = {
    "주간": "W",
    "월간": "M"
}[interval]

# 기간 설정
end = datetime.today()
start = end - timedelta(days=365)

# 주식 데이터 불러오기
ticker = stock_list[selected_stock]
df = yf.download(ticker, start=start, end=end)

if df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다. 인터넷 연결이나 티커를 확인해주세요.")
else:
    # 'Close' 컬럼만 명시적으로 선택해 resample
    df_resampled = df[['Close']].resample(resample_
