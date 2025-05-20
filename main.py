import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import geocoder
import pandas as pd

# 초기 세션 상태
if "locations" not in st.session_state:
    st.session_state["locations"] = []
if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None

# 현재 위치 기준 지도 중심
g = geocoder.ip('me')
current_location = g.latlng if g.latlng else [37.5665, 126.9780]

st.title("🗺️ 나의 여행지도 메모 앱")
st.markdown("도시 이름을 입력하고 메모를 저장하면 지도에 마커가 표시됩니다.")

# 도시 입력 폼
with st.form(key="location_form"):
    city = st.text_input("도시 이름 (예: 서울, 부산, Tokyo, Paris 등):")
    note = st.text_input("이 도시에서의 여행 메모:")
    submit = st.form_submit_button("저장")

    if submit and city and note:
        geolocator = Nominatim(user_agent="travel_app")
        location = geolocator.geocode(city)
        if location:
            st.session_state["locations"].append({
                "city": city,
                "lat": location.latitude,
                "lon": location.longitude,
                "note": note
            })
            st.success(f"'{city}'에 대한 메모가 저장되었습니다!")
            st.experimental_rerun()
        else:
            st.error("도시를 찾을 수 없습니다. 다시 입력해주세요.")

# 지도 생성
m = folium.Map(location=current_location, zoom_start=5)

# 마커 표시
for i, loc in enumerate(st.session_state["locations"]):
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=f"{loc['city']}<br>{loc['note']}",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=700, height=500)

# 메모 목록 + 수정/삭제
st.markdown("---")
st.subheader("📋 저장된 여행 메모")

if st.session_state["locations"]:
    for i, loc in enumerate(st.session_state["locations"]):
        cols = st.columns([4, 2, 1, 1])
        cols[0].markdown(f"**{loc['city']}** — {loc['note']}")
        if cols[1].button("수정", key=f"edit_{i}"):
            st.session_state["edit_index"] = i
        if cols[2].button("삭제", key=f"delete_{i}"):
            st.session_state["locations"].pop(i)
            st.experimental_rerun()

# 수정 폼
if st.session_state["edit_index"] is not None:
    i = st.session_state["edit_index"]
    st.markdown("### ✏️ 메모 수정")
    with st.form("edit_form"):
        new_note = st.text_input("새로운 메모:", value=st.session_state["locations"][i]["note"])
        save = st.form_submit_button("저장")
        if save:
            st.session_state["locations"][i]["note"] = new_note
            st.session_state["edit_index"] = None
            st.success("메모가 수정되었습니다.")
            st.experimental_rerun()
