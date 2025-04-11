import streamlit as st
import base64
from pathlib import Path

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
            # 이미지 추가
            ROOT_DIR = Path(__file__).parent.parent.absolute()
            SIDEBAR_IMAGE_PATH = ROOT_DIR / "images" / "sidebar_logo.png"
            
            if SIDEBAR_IMAGE_PATH.exists():
                image_base64 = self.get_base64_image(SIDEBAR_IMAGE_PATH)
                if image_base64:
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="data:image/png;base64,{image_base64}" 
                                 style="width: 180px; margin: auto;">
                        </div>
                    """, unsafe_allow_html=True)
            
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