import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import chardet

# 🔍 인코딩 자동 감지 함수
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        return chardet.detect(f.read(10000))['encoding']

# 🔢 문자열 숫자 → 정수 변환
def parse_number(val):
    try:
        return int(str(val).replace(",", ""))
    except:
        return 0

# 📦 데이터 로딩
def load_data():
    male_enc = detect_encoding("malefemale.csv")
    total_enc = detect_encoding("total.csv")
    male_female = pd.read_csv("malefemale.csv", encoding=male_enc)
    total = pd.read_csv("total.csv", encoding=total_enc)
    return male_female, total

# ✅ 데이터 불러오기
male_female_df, total_df = load_data()

# 🎛️ 동네 선택
st.title("📊 지역별 인구 시각화 대시보드")
districts = total_df["행정구역"].unique().tolist()
selected_district = st.selectbox("동네를 선택하세요:", districts)

# 🔍 total.csv에서 연령별 인구 추출
total_row = total_df[total_df["행정구역"] == selected_district].iloc[0]
age_cols = [col for col in total_df.columns if "계_" in col and "세" in col]
age_labels = [col.split("_")[-1] for col in age_cols]
age_values = [parse_number(total_row[col]) for col in age_cols]

# 📊 연령별 인구 막대그래프
st.subheader(f"📈 {selected_district} 연령별 총인구 (from total.csv)")
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(
    x=age_labels,
    y=age_values,
    name="총인구",
    marker_color="green"
))
bar_fig.update_layout(
    barmode='group',
    xaxis_title='연령',
    yaxis_title='인구 수',
    template='plotly_white'
)
st.plotly_chart(bar_fig)

# 🔍 malefemale.csv에서 성별 인구 추출
male_female_row = male_female_df[male_female_df["행정구역"] == selected_district].iloc[0]
male_cols = [col for col in male_female_df.columns if "남_" in col and "세" in col]
female_cols = [col for col in male_female_df.columns if "여_" in col and "세" in col]
mf_age_labels = [col.split("_")[-1] for col in male_cols]
male_values = [parse_number(male_female_row[col]) for col in male_cols]
female_values = [parse_number(male_female_row[col]) for col in female_cols]

# 🧍‍♂️🧍‍♀️ 성별 인구 피라미드
st.subheader(f"🔍 {selected_district} 성별 인구 피라미드 (from malefemale.csv)")
pyramid_fig = go.Figure()
pyramid_fig.add_trace(go.Bar(
    y=mf_age_labels,
    x=[-x for x in male_values],
    name='남성',
    orientation='h',
    marker_color='blue'
))
pyramid_fig.add_trace(go.Bar(
    y=mf_age_labels,
    x=female_values,
    name='여성',
    orientation='h',
    marker_color='pink'
))
pyramid_fig.update_layout(
    barmode='relative',
    xaxis=dict(title='인구 수'),
    yaxis_title='연령',
    legend=dict(x=0.85, y=0.05),
    template='plotly_white'
)
st.plotly_chart(pyramid_fig)
