import streamlit as st
from app.auth_manager import AuthManager
from app.sidebar_manager import SidebarManager

# 페이지 설정
st.set_page_config(
    page_title="대시보드",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화 (처음 한 번만)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 권한 체크
auth_manager = AuthManager()
auth_manager.check_page_access("dashboard")  # 영문으로 변경

# 사이드바 렌더링
sidebar = SidebarManager()
sidebar.render_sidebar()

def show_login():
    """로그인 화면"""
    if "login_submitted" not in st.session_state:
        st.session_state.login_submitted = False
        
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>교사 로그인</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>관리자 기능을 사용하려면 로그인하세요.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            password = st.text_input("비밀번호", type="password")
            submit = st.form_submit_button("로그인")
            
            if submit and not st.session_state.login_submitted:
                if password == "teacher123":
                    st.session_state.authenticated = True
                    st.session_state.login_submitted = True
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("비밀번호가 올바르지 않습니다.")

def show_dashboard():
    """대시보드 메인 화면"""
    st.markdown("<h1 style='text-align: center;'>교사 대시보드</h1>", unsafe_allow_html=True)
    
    # 로그아웃 버튼
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("로그아웃"):
            st.session_state.authenticated = False
            st.rerun()
    
    # 대시보드 내용
    st.markdown("###  환영합니다")
    st.write("교사용 관리 기능을 사용할 수 있습니다.")
    
    # 바로가기 카드들
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin: 10px 0;'>
            <h3>📝 위임장 관리</h3>
            <p>위원회 생성 및 위임장 링크 관리</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("바로가기 →", key="goto_delegation"):
            st.switch_page("pages/delegation_login.py")
    
    with col2:
        st.markdown("""
        <div style='padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin: 10px 0;'>
            <h3>📋 결석신고서</h3>
            <p>결석신고서 관리 및 처리</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("바로가기 →", key="goto_absence"):
            st.switch_page("pages/03_Absence.py")
    
    with col3:
        st.markdown("""
        <div style='padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin: 10px 0;'>
            <h3>📝 교외체험학습</h3>
            <p>신청서 및 결과보고서 작성</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("신청서 →", key="goto_field_request"):
                st.switch_page("pages/04_Field_Trip_Request.py")
        with col2:
            if st.button("결과보고서 →", key="goto_field_report"):
                st.switch_page("pages/05_Field_Trip_Report.py")

# 메인 로직
if st.session_state.authenticated:
    show_dashboard()
else:
    show_login() 