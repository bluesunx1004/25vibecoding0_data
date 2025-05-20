import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="삼성전자 월별 주가 추세", layout="wide")
st.title("📈 삼성전자 (005930.KS) 최근 1년간 **월별 종가** 추세")

# 날짜 범위 설정
end = datetime.today()
start = end - timedelta(days=365)

# 삼성전자 주식 데이터 다운로드
ticker = "005930.KS"
df = yf.download(ticker, start=start, end=end)

if df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다.")
else:
    # 월별 종가만 추출 (reset_index 시 Date 열 자동 생성)
    df_monthly = df.resample('M').last().reset_index()[['Date', 'Close']]

    # Plotly 그래프 생성
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_monthly['Date'],
        y=df_monthly['Close'],
        mode='lines+markers',
        name='월별 종가',
        line=dict(color='green', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title="📅 최근 1년간 삼성전자 월별 종가 추세",
        xaxis_title="월",
        yaxis_title="종가 (KRW)",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # 월별 종가 표 표시
    st.subheader("📋 월별 종가 데이터")
    df_monthly['Date'] = df_monthly['Date'].dt.strftime('%Y-%m')
    st.dataframe(df_monthly.rename(columns={'Date': '월', 'Close': '종가(KRW)'}), use_container_width=True)
