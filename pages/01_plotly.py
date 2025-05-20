import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 파일 업로드
@st.cache_data
def load_data():
    male_female = pd.read_csv("malefemale.csv", encoding='cp949')
    total = pd.read_csv("total.csv", encoding='cp949')
    return male_female, total

male_female_df, total_df = load_data()

# 숫자형으로 변환하는 함수
def parse_number(val):
    try:
        return int(str(val).replace(',', ''))
    except:
        return 0

# 지역 선택
districts = male_female_df["행정구역"].unique().tolist()
selected_district = st.selectbox("동네를 선택하세요:", districts)

# 선택된 지역의 데이터 추출
row = male_female_df[male_female_df["행정구역"] == selected_district].iloc[0]

# 컬럼 필터링
male_cols = [col for col in male_female_df.columns if "남_" in col and "세" in col]
female_cols = [col for col in male_female_df.columns if "여_" in col and "세" in col]
age_labels = [col.split("_")[-1] for col in male_cols]

male_values = [parse_number(row[col]) for col in male_cols]
female_values = [parse_number(row[col]) for col in female_cols]

# 📊 1. 연령별 인구 막대그래프
st.subheader(f"{selected_district} 연령별 인구")
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(x=age_labels, y=male_values, name='남성', marker_color='blue'))
bar_fig.add_trace(go.Bar(x=age_labels, y=female_values, name='여성', marker_color='pink'))
bar_fig.update_layout(barmode='group', xaxis_title='연령', yaxis_title='인구수')
st.plotly_chart(bar_fig)

# 🧍‍♂️🧍‍♀️ 2. 항아리형 성별 인구그래프
st.subheader(f"{selected_district} 인구 피라미드")
pyramid_fig = go.Figure()
pyramid_fig.add_trace(go.Bar(y=age_labels, x=[-v for v in male_values], name='남성', orientation='h', marker_color='blue'))
pyramid_fig.add_trace(go.Bar(y=age_labels, x=female_values, name='여성', orientation='h', marker_color='pink'))
pyramid_fig.update_layout(
    barmode='relative',
    xaxis=dict(title='인구수', tickvals=[-500, 0, 500]),
    yaxis_title='연령'
)
st.plotly_chart(pyramid_fig)
