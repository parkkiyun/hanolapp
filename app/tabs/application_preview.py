import streamlit as st
from app.pdf_generator import generate_pdf
from app.helper_functions import validate_required_fields, render_signature_image
from app.resource_manager import ResourceManager
import json

def render():
    st.header("신청서 확인 및 PDF 생성")

    # ResourceManager 인스턴스를 세션 상태에 저장
    if 'resources' not in st.session_state:
        st.session_state['resources'] = ResourceManager()
    
    # form_configs가 세션 상태에 없으면 JSON 파일에서 로드
    if 'form_configs' not in st.session_state:
        try:
            with open("form_config.json", "r", encoding="utf-8") as f:
                st.session_state['form_configs'] = json.load(f)
        except Exception as e:
            st.error(f"설정 파일을 불러오는 중 오류 발생: {str(e)}")
            return
    
    # form_config 가져오기
    form_configs = st.session_state['form_configs']
    query_params = st.query_params
    form_type = query_params.get("form_type", "학업성적관리위원회 위임장")
    
    # form_config 설정
    if form_type in form_configs:
        form_config = form_configs[form_type]
    else:
        form_config = form_configs["학업성적관리위원회 위임장"]
    
    # 디이터 검증
    required_fields = ["name", "birth_date", "address", "contact", "delegation_date", "signature_img"]
    missing_fields = validate_required_fields(required_fields)
    
    if missing_fields:
        st.error(f"다음 내용을 입력하세요: {', '.join(missing_fields)}")
        return
    
    # 신청서 미리보기
    render_signature_image(preview_only=True, form_config=form_config, return_image=False)
    
    # PDF 생성 및 다운로드
    if st.button("신청서 PDF로 변환 및 다운로드"):
        with st.spinner("PDF 변환 중..."):
            pdf_generated = generate_pdf(form_config=form_config)
            if pdf_generated:
                st.success("PDF 파일 다운로드가 준비되었습니다!")
