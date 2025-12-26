import streamlit as st
import pandas as pd
import urllib.parse
import base64

# 1. 페이지 설정
st.set_page_config(page_title="멜번 가이드", page_icon="☕", layout="centered")

# 2. CSS 설정 (상단 여백 제거 및 이미지 클릭 효과)
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem !important; max-width: 500px; }
    header {visibility: hidden;}
    [data-testid="column"] {
        width: calc(50% - 10px) !important;
        flex: 1 1 calc(50% - 10px) !important;
        min-width: calc(50% - 10px) !important;
    }
    .stButton button { font-size: 14px !important; }
    .qr-link img { 
        cursor: pointer; 
        transition: 0.3s; 
        border-radius: 15px; 
        width: 100%; 
        border: 1px solid #ddd;
    }
    .qr-link img:hover { opacity: 0.8; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("### 멜번 커피 & 라이프 가이드")

file_name = 'Merged_Melbourne_Spots.csv'

try:
    # 데이터 로드
    df = pd.read_csv(file_name, encoding='utf-8-sig')
    df = df.dropna(subset=['Name']).fillna("") 
    df = df[df['Name'].str.strip() != ""]
    df = df.sort_values(by='Category')
    last_category = None

    for index, row in df.iterrows():
        current_category = row['Category']
        if current_category != last_category:
            st.markdown("---")
            st.subheader(f"📍 {current_category}")
            last_category = current_category

        with st.expander(f"{row['Name']} (⭐ {row['Google Review']})", expanded=True):
            if str(row['Description']).strip(): st.write(f"{row['Description']}")
            if str(row['Address']).strip(): st.caption(f"🏠 {row['Address']}")

            col1, col2 = st.columns(2)
            with col1:
                # 개별 장소 핀
                place_query = f"{row['Name']}, {row['Address']}".strip()
                place_encoded = urllib.parse.quote(place_query)
                map_url = f"https://www.google.com/maps/search/?api=1&query={place_encoded}"
                st.link_button("📍 구글맵", map_url, use_container_width=True)
            with col2:
                site = str(row['Website']).strip()
                web_link = site if site.startswith('http') else f"https://www.google.com/search?q={urllib.parse.quote(row['Name'])}"
                st.link_button("🌐 웹사이트", web_link, use_container_width=True)

    # --- [QR 코드: 가이드님이 주신 공유 링크 적용] ---
    st.markdown("---")
    st.write("### 🗺️ 멜번 전체 지도 (My Maps)")
    
    # 404 방지를 위해 공유 주소를 직접 새 창으로 열도록 설정
    full_map_url = "https://www.google.com/maps/d/edit?mid=1n0IFCzWRilIcIk-DJBGkjE6aWepTK_M&usp=sharing"

    try:
        with open("qr1.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        
        # 텍스트와 이미지 전체를 클릭 가능한 링크로 변환 (타겟을 명확히 함)
        html_code = f'''
            <div style="text-align: center;">
                <p style="color: #FF4B4B; font-weight: bold; font-size: 15px; margin-bottom: 5px;">📍 아래 지도를 클릭하면 전체 위치가 열립니다</p>
                <a href="{full_map_url}" target="_blank" class="qr-link">
                    <img src="data:image/png;base64,{img_base64}">
                </a>
            </div>
        '''
        st.markdown(html_code, unsafe_allow_html=True)
    except:
        st.link_button("🗺️ 전체 지도 리스트 열기", full_map_url, use_container_width=True)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
