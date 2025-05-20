import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 타이틀
st.title("🌍 나만의 여행지도 만들기")
st.write("방문했던 도시를 입력하면 지도에 표시해드려요!")

# 입력 폼
with st.form("location_form"):
    city = st.text_input("도시 이름 (예: Seoul, Tokyo, Paris 등)")
    note = st.text_input("메모 (선택 사항)")
    submitted = st.form_submit_button("지도에 추가하기")

# 초기 위치 (대한민국 중심 좌표)
m = folium.Map(location=[36.5,]()

