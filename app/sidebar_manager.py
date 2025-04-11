import streamlit as st
import base64
from pathlib import Path
import os
from PIL import Image

class SidebarManager:
    def __init__(self):
        pass
    
    def get_base64_image(self, image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            return None
    
    def render_sidebar(self):
        with st.sidebar:
            # 한올고등학교 로고
            logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'hanol_logo.png')
            if os.path.exists(logo_path):
                logo = Image.open(logo_path)
                st.image(logo, use_column_width=True)
            else:
                st.error("로고 이미지를 찾을 수 없습니다.")
            
            st.title("메뉴")
            
            # 홈으로 가기 버튼
            if st.button("홈으로", key="home"):
                st.switch_page("Home.py")
            
            st.markdown("---")
            
            # 메뉴 구성
            if st.button("위임장 관리", key="delegation"):
                st.switch_page("pages/위임장_관리.py")
            if st.button("결석신고서", key="absence"):
                st.switch_page("pages/결석신고서.py")
            if st.button("위임장 작성", key="write"):
                st.switch_page("pages/위임장_작성.py")
            if st.button("교외체험학습 신청서", key="field_request"):
                st.switch_page("pages/교외체험학습_신청서.py")
            if st.button("교외체험학습 결과보고서", key="field_report"):
                st.switch_page("pages/교외체험학습_결과보고서.py") 