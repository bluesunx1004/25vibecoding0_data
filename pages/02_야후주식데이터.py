import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="주가 추세 및 수익률 분석", layout="wide")
st.title("📊 주가 추세 시각화 및 수익률 분석")

# 📌 종목 리스트 (확장 가능)
stock_list = {
    "삼성전자": "005930.KS",
    "Apple": "AAPL",
    "Google (Alphabet)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA"
}

# 사용자 입력
selected_stock = st.selectbox("종목 선택", options=list(stock_list.keys()))
interval = st.radio("보기 간격 선택", options=["일간", "주간", "월간"], horizontal=True)

# 간격별 Resample 코드 설정
resample_dict = {
    "일간": "D",
    "주간": "W",
    "월간": "M"
}
resample_rule = resample_dict[interval]

# 기간 설정
end = datetime.today()
start = end - timedelta(days=365)

# 📈 데이터 다운로드
ticker = stock_list[selected_stock]
df = yf.download(ticker, start=start, end=end)

if df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다.")
else:
    # 리샘플링 (종가 기준)
    df_resampled = df['Close'].resample(resample_rule).last().dropna().reset_index()

    # 수익률 계산 (%)
    df_resampled['수익률(%)'] = (df_resampled['Close'] / df_resampled['Close'].iloc[0] - 1) * 100

    # 📊 종가 선 그래프
    st.subheader("📈 종가 추세")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_resampled['Date'],
        y=df_resampled['Close'],
        mode='lines+markers',
        name='종가',
        line=dict(color='blue')
    ))
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="종가 (원 또는 USD)",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # 📈 수익률 그래프
    st.subheader("📈 누적 수익률 (%)")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df_resampled['Date'],
        y=df_resampled['수익률(%)'],
        mode='lines+markers',
        name='수익률',
        line=dict(color='green')
    ))
    fig2.update_layout(
        xaxis_title="날짜",
        yaxis_title="수익률 (%)",
        hovermode="x unified",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 📋 표 데이터 출력
    st.subheader("📋 데이터 테이블")
    df_table = df_resampled.copy()
    df_table['Date'] = df_table['Date'].dt.strftime('%Y-%m-%d')
    st.dataframe(df_table.rename(columns={'Date': '날짜', 'Close': '종가', '수익률(%)': '수익률 (%)'}), use_container_width=True)
