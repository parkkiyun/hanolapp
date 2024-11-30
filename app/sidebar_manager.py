import streamlit as st
from app.auth_manager import AuthManager

class SidebarManager:
    def __init__(self):
        self.auth_manager = AuthManager()
    
    def render_sidebar(self):
        # 스타일 추가
        st.markdown("""
            <style>
                [data-testid="stSidebar"][aria-expanded="true"] {
                    min-width: 250px;
                    max-width: 250px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # 사이드바 내용
        with st.sidebar:
            st.title("메뉴")
            
            # 로그인 상태에 따른 메뉴 구성
            if st.session_state.get("authenticated", False):
                st.markdown("### 메인")
                if st.button("🏠 대시보드", key="dashboard"):
                    st.switch_page("pages/dashboard.py")
                
                st.markdown("### 교사 메뉴")
                if st.button("📝 위임장 관리", key="delegation"):
                    st.switch_page("pages/delegation_login.py")
                if st.button("📋 결석신고서", key="absence"):
                    st.switch_page("pages/03_Absence.py")
                st.markdown("---")
                
                st.markdown("### 일반 메뉴")
                if st.button("✍️ 위임장 작성", key="write"):
                    st.switch_page("pages/write_delegation.py")
                if st.button("📝 교외체험학습 신청서", key="field_request"):
                    st.switch_page("pages/04_Field_Trip_Request.py")
                if st.button("📋 교외체험학습 결과보고서", key="field_report"):
                    st.switch_page("pages/05_Field_Trip_Report.py")
            else:
                st.markdown("### 일반 메뉴")
                if st.button("✍️ 위임장 작성", key="write_guest"):
                    st.switch_page("pages/write_delegation.py")
                if st.button("📝 교외체험학습 신청서", key="field_request_guest"):
                    st.switch_page("pages/04_Field_Trip_Request.py")
                if st.button("📋 교외체험학습 결과보고서", key="field_report_guest"):
                    st.switch_page("pages/05_Field_Trip_Report.py")
            
            # 구분선과 교사 로그인 메뉴 추가 (항상 표시)
            st.markdown("---")
            st.markdown("### 교사 로그인")
            if st.button("👩‍🏫 교사 로그인", key="teacher_login"):
                st.switch_page("pages/dashboard.py")
    
    def logout(self):
        st.session_state.authenticated = False
        st.rerun() 