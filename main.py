import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import pandas as pd
import base64

# ---------- 초기 세션 상태 ----------
if "locations" not in st.session_state:
    st.session_state["locations"] = []
if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None

# ---------- 기본 지도 중심 (대한민국) ----------
current_location = [36.5, 127.8]

st.title("🗺️ 나의 여행지도 메모 앱")
st.markdown("도시 이름과 여행 메모, 사진을 입력하면 지도에 마커가 생성됩니다.")

# ---------- 입력 폼 ----------
with st.form(key="location_form"):
    city = st.text_input("도시 이름 (예: 서울, 부산, Tokyo 등):").strip()
    note = st.text_input("이 도시에서의 여행 메모:").strip()
    uploaded_file = st.file_uploader("📸 여행 사진 업로드 (선택)", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("저장")

    if submit and city and note:
        geolocator = Nominatim(user_agent="travel_app")
        try:
            location = geolocator.geocode(city)
            if location:
                photo_bytes = uploaded_file.read() if uploaded_file else None
                st.session_state["locations"].append({
                    "city": city,
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "note": note,
                    "photo": photo_bytes
                })
                st.success(f"'{city}'에 대한 메모가 저장되었습니다!")
                st.rerun()
            else:
                st.error("도시를 찾을 수 없습니다. 정확한 이름을 입력해주세요.")
        except Exception as e:
            st.error(f"위치 검색 중 오류 발생: {e}")

# ---------- 지도 생성 ----------
m = folium.Map(location=current_location, zoom_start=7)

# ---------- 마커 표시 ----------
for loc in st.session_state["locations"]:
    # 사진이 있는 경우 base64 인코딩해서 HTML 이미지 삽입
    if loc["photo"]:
        encoded = base64.b64encode(loc["photo"]).decode()
        img_html = f'<br><img src="data:image/png;base64,{encoded}" width="150"/>'
    else:
        img_html = ""
    
    popup_content = f"<b>{loc['city']}</b><br>{loc['note']}{img_html}"
    
    folium.Marker(
        location=[loc["lat"], loc["lon"]],
        popup=folium.Popup(popup_content, max_width=300),
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# ---------- 지도 렌더링 ----------
st_data = st_folium(m, width=700, height=500)

# ---------- 저장된 메모 목록 ----------
st.markdown("---")
st.subheader("📋 저장된 여행 메모")

if st.session_state["locations"]:
    for i, loc in enumerate(st.session_state["locations"]):
        cols = st.columns([4, 1, 1, 1])
        with cols[0]:
            st.markdown(f"**{loc['city']}** — {loc['note']}")
            if loc["photo"]:
                st.image(loc["photo"], width=150)
        if cols[1].button("수정", key=f"edit_{i}"):
            st.session_state["edit_index"] = i
        if cols[2].button("삭제", key=f"delete_{i}"):
            st.session_state["locations"].pop(i)
            st.rerun()

# ---------- 수정 폼 ----------
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
            st.rerun()
