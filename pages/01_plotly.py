import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 제목
st.set_page_config(page_title="인구 피라미드", layout="centered")
st.title("👥 서울 종로구 인구 피라미드 (2025년 4월 기준)")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (남녀구분.csv)", type="csv")

if uploaded_file:
    try:
        # CP949 인코딩으로 읽기
        df = pd.read_csv(uploaded_file, encoding='cp949')

        # 종로구 데이터 추출
        row = df[df['행정구역'].str.contains("종로구 ")].iloc[0]

        # 연령별 남녀 컬럼
        male_columns = [col for col in df.columns if "남_" in col and "세" in col]
        female_columns = [col for col in df.columns if "여_" in col and "세" in col]

        # 연령 텍스트 추출
        ages = [col.split("_")[-1].replace("세", "") for col in male_columns]

        # 값 정수화
        male_pop = [-int(str(row[col]).replace(",", "")) for col in male_columns]
        female_pop = [int(str(row[col]).replace(",", "")) for col in female_columns]

        # Plotly 그래프 생성
        fig = go.Figure()
        fig.add_trace(go.Bar(y=ages, x=male_pop, name='남자', orientation='h', marker_color='blue'))
        fig.add_trace(go.Bar(y=ages, x=female_pop, name='여자', orientation='h', marker_color='pink'))

        fig.update_layout(
            title="서울 종로구 연령대별 남녀 인구 피라미드 (2025년 4월)",
            xaxis_title="인구 수",
            yaxis_title="연령",
            barmode='relative',
            height=800,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("왼쪽 사이드바에서 '남녀구분.csv' 파일을 업로드해주세요.")
