import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="글로벌 시가총액 Top10 주가 추이", layout="wide")
st.title("📈 글로벌 시가총액 Top10 기업의 최근 1년 주가 변화")

# 시가총액 Top10 기업 티커
top10 = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 시장
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Tesla": "TSLA",
    "Meta (Facebook)": "META",
    "TSMC": "TSM"
}

# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# 사용자 티커 선택 (멀티)
selected = st.multiselect("📌 비교할 기업을 선택하세요:", options=list(top10.keys()), default=list(top10.keys())[:5])

if selected:
    fig = go.Figure()
    
    for name in selected:
        symbol = top10[name]
        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=name))
        except Exception as e:
            st.error(f"{name} ({symbol}) 데이터를 불러오는데 문제가 발생했습니다: {e}")

    fig.update_layout(
        title="최근 1년간 주가 변화 (종가 기준)",
        xaxis_title="날짜",
        yaxis_title="주가 (USD / SAR)",
        template="plotly_white",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("하나 이상의 기업을 선택해주세요.")
