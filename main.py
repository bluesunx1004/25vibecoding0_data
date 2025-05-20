import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 페이지 설정
st.set_page_config(page_title="나만의 여행지도", layout="centered")
st.title("🌍 나만의 여행지도 만들기")
st.write("방문했던 도시를 입력하면 지도에 마커로 표시됩니다!")

# 세션 상태 초기화 (최초 실행 시)
if "locations" not in st.session_state:
    st.session_state.locations = []

# 입력 폼
with st.form("location_form"):
    city = st.text_input("도시 이름 (예: Seoul, Tokyo, Paris 등)", "")
    note = st.text_input("메모 (선택 사항)", "")
    submitted = st.form_submit_button("지도에 추가하기")

# 도시가 입력되었을 경우 위치 좌표 찾기
if submitted and city:
    try:
        geolocator = Nominatim(user_agent="travel_map_app")
        location = geolocator.geocode(city)

        if location:
            st.session_state.locations.append({
                "city": city,
                "note": note,
                "lat": location.latitude,
                "lon": location.longitude
            })
            st.success(f"✅ '{city}' 위치를 지도에 표시했습니다!")
        else:
            st.error("❌ 도시를 찾을 수 없습니다. 다른 이름으로 다시 시도해보세요.")
    except Exception as e:
        st.error(f"🚨 오류 발생: {e}")

# 지도 초기화 (대한민국 중심)
m = folium.Map(location=[36.5, 127.5], zoom_start=4)

# 저장된 마커들 지도에 추가
for loc in st.session_state.locations:
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"<b>{loc['city']}</b><br>{loc['note']}",
        tooltip=loc["city"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 표시
st_folium(m, width=700, height=500)
