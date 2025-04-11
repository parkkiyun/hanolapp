import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from app.sidebar_manager import SidebarManager
import qrcode

# 페이지 설정
st.set_page_config(
    page_title="스마트 문서 시스템",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/parkkiyun/hanolapp',
        'Report a bug': "https://github.com/parkkiyun/hanolapp/issues",
        'About': "# 스마트 문서 시스템 v1.0"
    }
)

# 사이드바 설정
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 250px;
            max-width: 250px;
        }
    </style>
""", unsafe_allow_html=True)

# 사이드바 렌더링
sidebar = SidebarManager()
sidebar.render_sidebar()

# URL 파라미터 체크 및 리다이렉션
query_params = st.query_params
redirect_to = query_params.get("page", None)

if redirect_to:
    if redirect_to == "field_trip_request":
        st.switch_page("pages/field_trip_request.py")
    elif redirect_to == "field_trip_report":
        st.switch_page("pages/field_trip_report.py")

# 로고 이미지 로드 및 크기 조정
logo = Image.open("images/sidebar_logo.png")
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

# CSS로 로고만을 위한 간단한 레이아웃
st.markdown("""
    <style>
        .header-container {
            display: flex;
            justify-content: center;
            margin: 0 auto;
            max-width: 300px;
        }
    </style>
""", unsafe_allow_html=True)

# 로고만 표시
st.markdown(
    f"""
    <div class="header-container">
        <img src="data:image/png;base64,{image_to_base64(logo)}" 
             width="{logo_width}px" 
             height="{logo_height}px" 
             style="object-fit: contain;">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# 메인 대시보드 화면
st.markdown("<h2 style='text-align: center;'>스마트 문서 시스템</h2>", unsafe_allow_html=True)

# 탭 생성
tab1, tab2 = st.tabs(["대시보드", "직접 접속 링크"])

# 탭1: 대시보드
with tab1:
    st.markdown("### 환영합니다")
    st.write("스마트 문서 시스템을 통해 편리하게 문서를 관리하세요.")
    
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
            st.switch_page("pages/결석신고서.py")
    
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
    
    # 기본 URL 고정
    if 'base_url' not in st.session_state:
        st.session_state.base_url = "https://hanolapp-fngnwqhxmgvwcwj2dztiue.streamlit.app"
    
    # 링크 생성 및 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 교외체험학습 신청서")
        request_link = f"{st.session_state.base_url}?page=field_trip_request"
        st.text_input("링크를 선택하여 복사하세요:", value=request_link, key="request_link_input", label_visibility="collapsed")
        
    with col2:
        st.write("#### 교외체험학습 결과보고서")
        report_link = f"{st.session_state.base_url}?page=field_trip_report"
        st.text_input("링크를 선택하여 복사하세요:", value=report_link, key="report_link_input", label_visibility="collapsed")
    
    # QR 코드 생성 섹션
    if st.checkbox("QR 코드 생성"):
        try:
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

# 일반 사용자를 위한 기능 소개
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
