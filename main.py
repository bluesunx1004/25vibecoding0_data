import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import chardet

# 📌 인코딩 자동 감지 함수
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding']

# 📦 데이터 불러오기 (Streamlit 캐시 사용)
@st.cache_data
def load_data():
    male_encoding = 'cp949'  # 확인된 인코딩
    total_encoding = detect_encoding('total.csv')  # 자동 감지
    male_female = pd.read_csv('malefemale.csv', encoding=male_encoding)
    total = pd.read_csv('total.csv', encoding=total_encoding)
    return male_female, total

male_female_df, total_df = load_data()

# 숫자 파싱 유틸리티
def parse_number(val):
    try:
        return int(str(val).replace(',', ''))
    except:
        return 0

# 🎛️ 동네 선택
st.title("📊 지역별 인구 시각화")
districts = male_female_df["행정구역"].unique().tolist()
selected_district = st.selectbox("동네를 선택하세요:", districts)

# 🧮 데이터 추출
row = male_female_df[male_female_df["행정구역"] == selected_district].iloc[0]
male_cols = [col for col in male_female_df.columns if "남_" in col and "세" in col]
female_cols = [col for col in male_female_df.columns if "여_" in col and "세" in col]
age_labels = [col.split("_")[-1] for col in male_cols]

male_values = [parse_number(row[col]) for col in male_cols]
female_values = [parse_number(row[col]) for col in female_cols]

# 📊 연령별 인구 막대그래프
st.subheader(f"📈 {selected_district} 연령별 인구")
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(x=age_labels, y=male_values, name='남성', marker_color='blue'))
bar_fig.add_trace(go.Bar(x=age_labels, y=female_values, name='여성', marker_color='pink'))
bar_fig.update_layout(barmode='group', xaxis_title='연령', yaxis_title='인구수')
st.plotly_chart(bar_fig)

# 🧍‍♂️🧍‍♀️ 성별 인구 피라미드
st.subheader(f"🔍 {selected_district} 성별 인구 피라미드")
pyramid_fig = go.Figure()
pyramid_fig.add_trace(go.Bar(y=age_labels, x=[-x for x in male_values], name='남성', orientation='h', marker_color='blue'))
pyramid_fig.add_trace(go
