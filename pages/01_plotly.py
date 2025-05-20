import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import chardet

# 인코딩 자동 감지 함수
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        return chardet.detect(f.read(10000))['encoding']

# 숫자 변환 유틸리티
def parse_number(val):
    try:
        return int(str(val).replace(",", ""))
    except:
        return 0

# 데이터 로딩
def load_total_data():
    encoding = detect_encoding("total.csv")
    return pd.read_csv("total.csv", encoding=encoding)

total_df = load_total_data()

# Streamlit UI
st.title("📊 연령별 총인구 분포 (from total.csv)")
districts = total_df["행정구역"].unique().tolist()
selected_district = st.selectbox("동네를 선택하세요:", districts)

# 선택된 행정구역의 데이터 추출
row = total_df[total_df["행정구역"] == selected_district].iloc[0]

# 연령별 총인구 컬럼 필터링
age_columns = [col for col in total_df.columns if "계_" in col and "세" in col]
age_labels = [col.split("_")[-1] for col in age_columns]
age_values = [parse_number(row[col]) for col in age_columns]

# 그래프 그리기
st.subheader(f"🧓 {selected_district} 연령별 총인구 분포")
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(
    x=age_labels,
    y=age_values,
    name='총인구',
    marker_color='green'
))
bar_fig.update_layout(
    xaxis_title='연령',
    yaxis_title='인구 수',
    template='plotly_white'
)
st.plotly_chart(bar_fig)
