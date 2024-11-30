import streamlit as st
from app.sidebar_manager import SidebarManager
from app.auth_manager import AuthManager

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

# 메인 페이지 내용
st.markdown("<h1 style='text-align: center;'>한올고등학교 스마트 문서 시스템</h1>", unsafe_allow_html=True)

# 로그인 상태에 따른 화면 표시
if not st.session_state.get("authenticated", False):
    # 로그인 폼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>교사 로그인</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>관리자 기능을 사용하려면 로그인하세요.</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("아이디")
            password = st.text_input("비밀번호", type="password")
            submit = st.form_submit_button("로그인")
            
            if submit:
                auth_manager = AuthManager()
                if auth_manager.authenticate(username, password):
                    st.success("로그인 성공!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
else:
    # 교사 대시보드 화면
    st.markdown("<h2 style='text-align: center;'>교사 대시보드</h2>", unsafe_allow_html=True)
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
            st.switch_page("pages/absence.py")
    
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
                st.switch_page("pages/field_trip_request.py")
        with col2:
            if st.button("결과보고서 →", key="goto_field_report"):
                st.switch_page("pages/field_trip_report.py")

# 일반 사용자를 위한 기능 소개 (항상 표시)
st.markdown("---")
st.markdown("### 📌 일반 기능")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### ✍️ 위임장 작성
    - 온라인 위임장 작성
    - 간편한 제출 방식
    """)

with col2:
    st.markdown("""
    #### 📝 교외체험학습 신청서
    - 신청서 양식 작성
    - 자동 문서 생성
    """)

with col3:
    st.markdown("""
    #### 📋 교외체험학습 결과보고서
    - 결과보고서 작성
    - 간편한 제출
    """)

st.markdown("---")
st.markdown("<div style='text-align: right;'>제작자: 박기윤</div>", unsafe_allow_html=True) 