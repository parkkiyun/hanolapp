import streamlit as st
from app.auth_manager import AuthManager
import base64
from pathlib import Path

class SidebarManager:
    def __init__(self):
        self.auth_manager = AuthManager()
    
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
            if st.button("🏠 홈으로", key="home"):
                st.switch_page("Home.py")
            
            st.markdown("---")
            
            # 로그인 상태에 따른 메뉴 구성
            if st.session_state.get("authenticated", False):
                st.markdown("### 교사 메뉴")
                if st.button("📝 위임장 관리", key="delegation"):
                    st.switch_page("pages/delegation_login.py")
                if st.button("📋 결석신고서", key="absence"):
                    st.switch_page("pages/absence.py")
                
                st.markdown("---")
                st.markdown("### 일반 메뉴")
            
            # 일반 메뉴 (항상 표시)
            if st.button("✍️ 위임장 작성", key="write"):
                st.switch_page("pages/write_delegation.py")
            if st.button("📝 교외체험학습 신청서", key="field_request"):
                st.switch_page("pages/field_trip_request.py")
            if st.button("📋 교외체험학습 결과보고서", key="field_report"):
                st.switch_page("pages/field_trip_report.py")
            
            # 로그인/로그아웃 버튼
            st.markdown("---")
            if st.session_state.get("authenticated", False):
                if st.button("로그아웃", key="logout"):
                    self.auth_manager.logout()
                    st.rerun()
    
    def logout(self):
        st.session_state.authenticated = False
        st.rerun() 