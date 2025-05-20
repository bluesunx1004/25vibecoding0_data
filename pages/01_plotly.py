import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="인구 피라미드", layout="centered")
st.title("👥 서울 종로구 인구 피라미드 (GitHub에서 불러오기)")

# GitHub raw CSV 링크 입력
csv_url = st.text_input("GitHub Raw CSV URL 입력", 
                        "https://raw.githubusercontent.com/yourusername/yourrepo/main/남녀구분.csv")

if csv_url:
    try:
        # GitHub에서 CSV 불러오기
        df = pd.read_csv(csv_url, encoding='cp949')

        # 종로구 데이터 추출
        row = df[df['행정구역'].str.contains("종로구 ")].iloc[0]

        # 연령별 남녀 컬럼
        male_columns = [col for col in df.columns if "남_" in col and "세" in col]
        female_columns = [col for col in df.columns if "여_" in col and "세" in col]
        ages = [col.split("_")[-1].replace("세", "") for col in male_columns]

        male_pop = [-int(str(row[col]).replace(",", "")) for col in male_columns]
        female_pop = [int(str(row[col]).replace(",", "")) for col in female_columns]

        # 그래프 생성
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
        st.error(f"🚨 CSV 파일을 불러오는 중 오류 발생: {e}")
else:
    st.info("GitHub Raw CSV 링크를 입력해주세요.")
