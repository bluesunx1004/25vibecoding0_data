import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시가총액 Top10", layout="wide")
st.title("📈 글로벌 시가총액 Top10 기업의 최근 1년 주가 변화")

# 기업명과 티커
top10 = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Tesla": "TSLA",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    # "Saudi Aramco": "2222.SR"  # 제거 또는 조건처리 필요
}

selected = st.multiselect("📌 비교할 기업을 선택하세요:", options=list(top10.keys()), default=list(top10.keys())[:5])

# 기간 설정
end = datetime.today()
start = end - timedelta(days=365)

if selected:
    fig = go.Figure()
    for company in selected:
        ticker = top10[company]
        try:
            df = yf.download(ticker, start=start, end=end)
            if not df.empty:
                fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name=company, mode='lines'))
            else:
                st.warning(f"⚠️ {company} ({ticker})의 데이터를 가져올 수 없습니다.")
        except Exception as e:
            st.error(f"{company} 데이터 오류: {e}")

    if fig.data:
        fig.update_layout(
            title="최근 1년간 주가 변화 (종가 기준)",
            xaxis_title="날짜",
            yaxis_title="주가 (USD)",
            template="plotly_white",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("유효한 데이터를 가진 기업이 없습니다.")
else:
    st.info("비교할 기업을 하나 이상 선택하세요.")
