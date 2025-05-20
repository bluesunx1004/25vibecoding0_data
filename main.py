import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# 제목
st.title("📌 나의 여행지도 메모 앱")

# 세션 상태 초기화
if "locations" not in st.session_state:
    st.session_state["locations"] = []

st.markdown("1. 지도를 클릭해 위치를 선택하세요.  
2. 여행 메모를 작성하고 저장하면 마커가 생깁니다.")

# 기본 지도 설정
m = folium.Map(location=[37.5665, 126.9780], zoom_start=6)  # 서울 중심

# 기존 마커 불러오기
for loc in st.session_state["locations"]:
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=loc["note"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 클릭 이벤트 수신
map_data = st_folium(m, width=700, height=500)

# 지도 클릭 시 위치 좌표 추출
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    
    st.success(f"선택한 위치: {lat:.4f}, {lon:.4f}")
    
    with st.form(key="note_form"):
        note = st.text_input("이 위치에 대한 여행 메모를 작성하세요:")
        submitted = st.form_submit_button("저장하기")
        if submitted and note:
            # 마커 데이터 저장
            st.session_state["locations"].append({
                "lat": lat,
                "lon": lon,
                "note": note
            })
            st.experimental_rerun()  # 마커 즉시 반영

# 저장된 메모 테이블 보기
if st.checkbox("📝 저장된 여행 메모 보기"):
    df = pd.DataFrame(st.session_state["locations"])
    st.dataframe(df)

