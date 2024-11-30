import streamlit as st
import json
import os
from app.auth_manager import AuthManager
from app.sidebar_manager import SidebarManager
from io import BytesIO

# 권한 체크
auth_manager = AuthManager()
auth_manager.check_page_access("delegation_login")

# 사이드바 렌더링
sidebar_manager = SidebarManager()
sidebar_manager.render_sidebar()

# 로그인 상태가 아니면 리다이렉트
if not st.session_state.get("authenticated", False):
    st.error("이 페이지는 교사 로그인이 필요합니다.")
    st.switch_page("Home.py")

def show_teacher_page():
    """선생님 페이지 메인"""
    st.markdown("<h1 style='text-align: center;'>위임장 관리</h1>", unsafe_allow_html=True)
    
    # 깔끔한 설명 박스
    st.markdown("""
        <div style="
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="color: #1f1f1f; font-size: 1.1em; margin-bottom: 8px;">
                🔗 위원회를 추가하고 학부모용 링크를 생성할 수 있습니다
            </div>
            <div style="color: #666; font-size: 0.9em;">
                생성된 링크를 학부모님께 공유하세요
            </div>
        </div>
    """, unsafe_allow_html=True)

    # JSON 파일 경로
    json_file = "form_config.json"

    # 위원회 목록 표시
    st.subheader("📋 위원회 목록")
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            form_configs = json.load(f)
            
        # 그리드 형식으로 위원회 표시
        cols = st.columns(3)  # 3열 그리드
        for idx, (committee_name, config) in enumerate(form_configs.items()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                        <div style="
                            padding: 20px;
                            border-radius: 10px;
                            border: 1px solid #ddd;
                            margin: 10px 0;
                            background-color: white;">
                            <h3 style="margin: 0 0 10px 0;">{committee_name}</h3>
                            <p style="color: #666; margin: 5px 0;">위임장 제목: {config['title']} 위임장</p>
                        </div>
                        """, unsafe_allow_html=True)
                    if st.button("삭제", key=f"delete_{committee_name}"):
                        del form_configs[committee_name]
                        with open(json_file, "w", encoding="utf-8") as f:
                            json.dump(form_configs, f, ensure_ascii=False, indent=4)
                        st.success(f"'{committee_name}' 위원회가 삭제되었습니다.")
                        st.rerun()
    else:
        st.error("위원회 설정 파일이 없습니다.")

    # 위원회 추가
    st.write("---")
    st.subheader("➕ 위원회 추가")
    with st.form("new_form"):
        committee_name = st.text_input("위원회 이름")
        submit_button = st.form_submit_button("위원회 추가")
        
        if submit_button:
            if committee_name:
                # 동적으로 타이틀과 텍스트 생성
                form_configs[committee_name] = {
                    "title": committee_name,
                    "image_texts": [
                        f"{committee_name} 결정 사항에 동의합니다"
                    ]
                }
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(form_configs, f, ensure_ascii=False, indent=4)
                st.success(f"'{committee_name}' 위원회가 추가되었습니다.")
                st.rerun()
            else:
                st.error("위원회 이름을 입력세요.")

    # 링크 생성
    st.write("---")
    st.subheader("🔗 위원회 링크 생성")
    if os.path.exists(json_file):
        # 세션 상태 초기화
        if "generated_link" not in st.session_state:
            st.session_state.generated_link = None
            
        # 드롭다운 메뉴 선택 변경 시 링크 초기화
        selected_form = st.selectbox(
            "위원회 선택", 
            list(form_configs.keys()), 
            key="selected_form"
        )
        
        # 기본 URL 고정
        base_url = "https://hanolapp-fngnwqhxmgvwcwj2dztiue.streamlit.app/write_delegation"
        
        # 드롭다운 메뉴 변경 시 링크 초기화
        if "last_selected_form" not in st.session_state:
            st.session_state.last_selected_form = selected_form
        
        if st.session_state.last_selected_form != selected_form:
            st.session_state.generated_link = None
            st.session_state.last_selected_form = selected_form
        
        # 링크 생성 버튼
        if st.button("링크 생성"):
            if selected_form:
                st.session_state.generated_link = f"{base_url}?form_type={selected_form}"
        
        # 링크 생성 버튼을 눌렀을 때만 링크 표시
        if st.session_state.generated_link is not None:
            st.write("생성된 링크:")
            st.text_input(
                "링크를 선택하여 복사하세요:", 
                value=st.session_state.generated_link,
                key="link_input",
                label_visibility="collapsed"
            )
            
            # QR 코드 생성 섹션
            if st.checkbox("QR 코드 생성"):
                try:
                    import qrcode
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(st.session_state.generated_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    
                    # QR 코드 이미지 표시
                    st.write(f"**{selected_form} QR 코드**")
                    st.image(buffered)
                    
                except ImportError:
                    st.error("QR 코드 생성을 위해 'qrcode' 패키지를 설치해주세요.")

# 메인 로직
if st.session_state.authenticated:
    show_teacher_page()
else:
    st.switch_page("Home.py")  # 로그인되지 않은 경우 홈페이지로 리다이렉트
