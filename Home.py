import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from app.sidebar_manager import SidebarManager
from app.auth_manager import AuthManager

# 페이지 설정
st.set_page_config(
    page_title="한올고 위임장 시스템",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL 파라미터 체크 및 리다이렉션
query_params = st.query_params
redirect_to = query_params.get("page", None)

if redirect_to:
    if redirect_to == "field_trip_request":
        st.switch_page("pages/field_trip_request.py")
    elif redirect_to == "field_trip_report":
        st.switch_page("pages/field_trip_report.py")

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# 사이드바 렌더링
sidebar = SidebarManager()
sidebar.render_sidebar()

# 로고 이미지 로드 및 크기 조정
logo = Image.open("images/logo.png")
logo_height = 40
aspect_ratio = logo.size[0] / logo.size[1]
logo_width = int(logo_height * aspect_ratio)
logo = logo.resize((logo_width, logo_height))

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 메인 타이틀과 헤더
st.markdown("<h1 style='text-align: center;'>스마트 문서 시스템</h1>", unsafe_allow_html=True)

# CSS로 반응형 레이아웃 구현
st.markdown("""
    <style>
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: nowrap;
            gap: 5px;
            margin: 0 auto;
            max-width: 300px;
        }
        .logo-container {
            flex: 0 0 auto;
            display: flex;
            align-items: center;
            margin-right: -5px;
        }
        .title-container {
            flex: 0 0 auto;
            text-align: left;
        }
        @media (max-width: 640px) {
            .header-container {
                gap: 0px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# 로고와 서브타이틀을 하나의 컨테이너에 배치
st.markdown(
    f"""
    <div class="header-container">
        <div class="logo-container">
            <img src="data:image/png;base64,{image_to_base64(logo)}" 
                 width="{logo_width}px" 
                 height="{logo_height}px" 
                 style="object-fit: contain;">
        </div>
        <div class="title-container">
            <h3 style="margin: 0; padding-left: 5px;">온양한올고등학교</h3>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

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
    st.markdown("---")
    # 교사 대시보드 화면
    st.markdown("<h2 style='text-align: center;'>교사 대시보드</h2>", unsafe_allow_html=True)
    
    # 탭 생성
    tab1, tab2 = st.tabs(["대시보드", "직접 접속 링크"])
    
    # 탭1: 대시보드 (기존 내용)
    with tab1:
        st.markdown("### 환영합니다")
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

    # 탭2: 직접 접속 링크
    with tab2:
        st.write("### 🔗 교외체험학습 직접 접속 링크")
        
        # 기본 URL 입력 (유지)
        if 'base_url' not in st.session_state:
            st.session_state.base_url = "https://hanolapp-fngnwqhxmgvwcwj2dztiue.streamlit.app"
        
        base_url = st.text_input(
            "기본 URL", 
            value=st.session_state.base_url,
            help="앱의 기본 URL을 입력하세요"
        )
        
        if base_url != st.session_state.base_url:
            st.session_state.base_url = base_url

        # 링크 생성 및 표시 (disabled 제거)
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("#### 교외체험학습 신청서")
            request_link = f"{base_url}?page=field_trip_request"
            st.text_input("링크를 선택하여 복사하세요:", value=request_link, key="request_link_input", label_visibility="collapsed")
            
        with col2:
            st.write("#### 교외체험학습 결과보고서")
            report_link = f"{base_url}?page=field_trip_report"
            st.text_input("링크를 선택하여 복사하세요:", value=report_link, key="report_link_input", label_visibility="collapsed")
        
        # QR 코드 생성 섹션 (기존 코드 유지)
        if st.checkbox("QR 코드 생성"):
            try:
                import qrcode
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("신청서 QR")
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(request_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    st.image(buffered)
                    
                with col2:
                    st.write("결과보고서 QR")
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(report_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    st.image(buffered)
            except ImportError:
                st.error("QR 코드 생성을 위해 'qrcode' 패키지를 설치해주세요.")

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