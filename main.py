import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    male_female = pd.read_csv("malefemale.csv", encoding='cp949')  # 남녀 데이터
    total = pd.read_csv("total.csv", encoding='euc-kr')            # 전체 인구 데이터
    return male_female, total

male_female_df, total_df = load_data()

# 🚫 캐시 제거한 상태로 로딩
male_female_df, total_df = load_data()


# 🧹 숫자 변환 유틸
def parse_number(val):
    try:
        return int(str(val).replace(",", ""))
    except:
        return 0

# 🏙️ 동네 선택
st.title("📊 지역별 인구 시각화 대시보드")
districts = male_female_df["행정구역"].unique().tolist()
selected_district = st.selectbox("동네를 선택하세요:", districts)

# 🔎 해당 지역 데이터 필터링
row = male_female_df[male_female_df["행정구역"] == selected_district].iloc[0]
male_cols = [col for col in male_female_df.columns if "남_" in col and "세" in col]
female_cols = [col for col in male_female_df.columns if "여_" in col and "세" in col]
age_labels = [col.split("_")[-1] for col in male_cols]

male_values = [parse_number(row[col]) for col in male_cols]
female_values = [parse_number(row[col]) for col in female_cols]

# 📊 연령별 인구 막대그래프
st.subheader(f"📈 {selected_district} 연령별 인구 분포")
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(x=age_labels, y=male_values, name='남성', marker_color='blue'))
bar_fig.add_trace(go.Bar(x=age_labels, y=female_values, name='여성', marker_color='pink'))
bar_fig.update_layout(barmode='group', xaxis_title='연령', yaxis_title='인구 수')
st.plotly_chart(bar_fig)

# 🧍 성별 인구 피라미드
st.subheader(f"🔍 {selected_district} 성별 인구 피라미드")
pyramid_fig = go.Figure()
pyramid_fig.add_trace(go.Bar(
    y=age_labels,
    x=[-x for x in male_values],
    name='남성',
    orientation='h',
    marker_color='blue'
))
pyramid_fig.add_trace(go.Bar(
    y=age_labels,
    x=female_values,
    name='여성',
    orientation='h',
    marker_color='pink'
))
pyramid_fig.update_layout(
    barmode='relative',
    xaxis=dict(title='인구 수'),
    yaxis_title='연령',
    legend=dict(x=0.85, y=0.05)
)
st.plotly_chart(pyramid_fig)
