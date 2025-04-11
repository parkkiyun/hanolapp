import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from app.sidebar_manager import SidebarManager

# 페이지 설정
st.set_page_config(
    page_title="위임장 목록",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 렌더링
sidebar = SidebarManager()
sidebar.render_sidebar()

# 로고 이미지 로드 및 크기 조정
try:
    logo = Image.open("images/logo.png")
    logo_height = 40
    aspect_ratio = logo.size[0] / logo.size[1]
    logo_width = int(logo_height * aspect_ratio)
    logo = logo.resize((logo_width, logo_height))
except FileNotFoundError:
    logo = None

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 메인 타이틀
st.markdown("<h1 style='text-align: center;'>위임장 목록</h1>", unsafe_allow_html=True)

# 로고 표시
if logo:
    st.markdown(
        f"""
        <div style="text-align: center; margin: 20px auto;">
            <img src="data:image/png;base64,{image_to_base64(logo)}" 
                 width="{logo_width}px" 
                 height="{logo_height}px" 
                 style="object-fit: contain;">
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("---")

# 위임장 목록 표시
st.markdown("### 위임장 목록")
st.write("생성된 위임장 목록이 여기에 표시됩니다.")

# 푸터
st.markdown("---")
st.markdown("<div style='text-align: right;'>제작자: 박기윤</div>", unsafe_allow_html=True) 