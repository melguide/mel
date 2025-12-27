import streamlit as st
import pandas as pd
import urllib.parse
import base64
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="호주 멜번의 커피 문화와 맛집", page_icon="☕", layout="centered")

# 2. 고정 정보 설정
MY_MAP_ID = "1vX6A7OndXm8W2B3T_L472zT9E6f1yps"
FULL_MAP_URL = f"https://www.google.com/maps/d/viewer?mid={MY_MAP_ID}"
CURRENT_VERSION = "1.1.5" # 버전 업데이트
LAST_UPDATED = datetime.datetime.now().strftime("%Y-%m-%d")
MY_EMAIL = "all4kid@naver.com"

# 3. CSS 설정
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem !important; max-width: 500px; }
    header {visibility: hidden;}
    
    .stButton button { font-size: 14px !important; }
    .qr-link img { cursor: pointer; border-radius: 15px; width: 100%; border: 1px solid #ddd; }
    .footer { text-align: center; color: #888; font-size: 0.8rem; margin-top: 50px; line-height: 1.6; }
    
    /* 오디오 및 안내 문구 스타일 */
    .audio-caption { color: #5D4037; font-size: 15px; font-weight: bold; margin-bottom: 12px; text-align: center; }
    .qr-caption { color: #6D4C41; font-size: 13px; font-weight: 500; margin-bottom: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 4. 메인 제목 (국기 이모지를 삭제하고 텍스트만 남겼습니다)
st.markdown("### 호주 멜번의 커피 문화와 맛집")

# --- [ MP3 재생 섹션 ] ---
try:
    with open('mel_coffee.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()
    st.markdown('<p class="audio-caption">🎧 OK여행사와 함께하는 멜번 커피 이야기</p>', unsafe_allow_html=True)
    st.audio(audio_bytes, format='audio/mp3')
except FileNotFoundError:
    st.info("💡 오디오 파일을 준비 중입니다.")

# --- [ 맛집 리스트 출력 ] ---
file_name = 'Merged_Melbourne_Spots.csv'
try:
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
                place_query = f"{row['Name']}, {row['Address']}".strip()
                place_encoded = urllib.parse.quote(place_query)
                map_url = f"https://www.google.com/maps/search/?api=1&query={place_encoded}"
                st.link_button("📍 구글맵", map_url, use_container_width=True)
            with col2:
                site = str(row['Website']).strip()
                web_link = site if site.startswith('http') else f"https://www.google.com/search?q={urllib.parse.quote(row['Name'])}"
                st.link_button("🌐 웹사이트", web_link, use_container_width=True)

    # --- [ QR 코드 섹션 ] ---
    st.markdown("---")
    st.write("### 🗺️ 멜번 전체 지도")
    
    try:
        with open("qr1.png", "rb") as f:
            img_base64 = base64.b64encode(f.read()).decode()
        
        html_code = f'''
            <div style="text-align: center;">
                <p class="qr-caption">📸 아래 QR 이미지를 누르면 전체 지도로 연결됩니다</p>
                <a href="{FULL_MAP_URL}" target="_blank" class="qr-link">
                    <img src="data:image/png;base64,{img_base64}">
                </a>
            </div>
        '''
        st.markdown(html_code, unsafe_allow_html=True)
    except:
        st.link_button("🗺️ 전체 지도 열기", FULL_MAP_URL, use_container_width=True)

    # --- [ 푸터 ] ---
    st.markdown(f"""
        <div class="footer">
            <p>🛠️ <b>Developed by 김용 (Yong Kim)</b></p>
            <p>📧 <b>Contact:</b> <a href="mailto:{MY_EMAIL}" style="color: #888;">{MY_EMAIL}</a></p>
            <p>📅 <b>Last Updated:</b> {LAST_UPDATED} | 🚀 <b>Version:</b> {CURRENT_VERSION}</p>
            <p>© 2025 OK 여행사</p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"오류 발생: {e}")
