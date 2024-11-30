import streamlit as st
from app.sidebar_manager import SidebarManager

# 페이지 설정
st.set_page_config(
    page_title="한올고 위임장 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 사이드바 렌더링
sidebar = SidebarManager()
sidebar.render_sidebar()

# 메인 페이지로 리다이렉트
st.switch_page("pages/dashboard.py") 