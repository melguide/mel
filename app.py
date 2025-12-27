import streamlit as st
import pandas as pd
import os
import datetime

# 1. 페이지 설정
st.set_page_config(page_title="멜번 커피 & 맛집 투어", page_icon="☕", layout="centered")

# 2. CSS 설정 (심플하고 깔끔한 모바일 최적화)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; max-width: 500px; }
    header {visibility: hidden;}
    .stAudio { margin-bottom: 20px; }
    .footer { text-align: center; color: #888; font-size: 0.8rem; margin-top: 30px; }
    iframe { border-radius: 15px; border: 1px solid #ddd; margin-top: 10px; }
    .category-header { background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-top: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. 메인 제목
st.markdown("### ☕ 멜번 커피 문화와 맛집")

# --- [ 4. 오디오 섹션 (순서 1) ] ---
mp3_file = 'mel_coffee.mp3'
if os.path.exists(mp3_file):
    try:
        with open(mp3_file, 'rb') as audio_file:
            audio_bytes = audio_file.read()
        st.write("🎧 **가이드와 함께하는 커피 이야기**")
        st.audio(audio_bytes, format='audio/mp3')
    except Exception as e:
        st.info("💡 오디오를 준비 중입니다.")

# --- [ 5. 맛집 리스트 섹션 (순서 2) ] ---
csv_file = 'Merged_Melbourne_Spots.csv'
if os.path.exists(csv_file):
    try:
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=['Name']).fillna("")
        
        st.markdown("#### 📍 추천 맛집 리스트")
        
        # 카테고리별로 정렬하여 표시
        for category in sorted(df['Category'].unique()):
            st.markdown(f"<div class='category-header'>{category}</div>", unsafe_allow_html=True)
            items = df[df['Category'] == category]
            for _, row in items.iterrows():
                with st.expander(f"{row['Name']} (⭐ {row['Google Review']})"):
                    if row['Description']: st.write(row['Description'])
                    st.caption(f"🏠 {row['Address']}")
                    # 웹사이트가 있으면 링크 제공
                    if row['Website'] and str(row['Website']).startswith('http'):
                        st.link_button("🌐 홈페이지 방문", row['Website'])
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다.")

# --- [ 6. 구글 지도 임베딩 섹션 (순서 3) ] ---
st.markdown("---")
st.markdown("#### 🗺️ 멜번 전체 지도")

# 가이드님이 주신 iframe 코드 (크기를 100%로 맞춰서 휴대폰에서 잘 보이게 했습니다)
map_html = """
<iframe src="https://www.google.com/maps/d/embed?mid=1n0IFCzWRilIcIk-DJBGkjE6aWepTK_M&hl=en&ehbc=2E312F" width="100%" height="480" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
"""
st.markdown(map_html, unsafe_allow_html=True)

# --- [ 7. 푸터 ] ---
last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
st.markdown(f"""
    <div class="footer">
        <p>🛠️ Developed by 김용 (Yong Kim)</p>
        <p>📅 Last Updated: {last_updated} | © 2025 OK 여행사</p>
    </div>
""", unsafe_allow_html=True)
